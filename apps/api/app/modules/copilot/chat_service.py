"""
Copilot Chat Service — deterministic intent-matching chatbot for recruiters.
No LLM required: keyword routing dispatches messages to structured answer generators.
"""

from app.domain.copilot import CopilotChatRequest, CopilotChatResponse
from app.domain.candidate_twin import CandidateDigitalTwin
from app.domain.role_dna import RoleDNAProfile


# ── Intent definitions ────────────────────────────────────────────────────────

INTENT_MAP: list[tuple[str, list[str]]] = [
    ("strengths",       ["strength", "strong", "good at", "excel", "best"]),
    ("risks",           ["risk", "weakness", "weak", "concern", "gap", "lacking"]),
    ("skills",          ["skill", "technology", "tool", "stack", "language", "framework"]),
    ("growth",          ["grow", "growth", "learn", "develop", "ramp", "onboard"]),
    ("leadership",      ["leader", "manage", "team", "mentor", "people"]),
    ("match",           ["match", "fit", "suitable", "right", "qualify", "score"]),
    ("salary",          ["salary", "comp", "compensation", "pay", "rate"]),
    ("timeline",        ["timeline", "career", "experience", "year", "history"]),
    ("recommendation",  ["recommend", "hire", "decision", "verdict"]),
    ("interview_first", ["interview first", "top candidate", "number one", "first choice"]),
    ("learns_fastest",  ["learns fastest", "fastest learner", "learning velocity", "quick learner"]),
    ("startup_dna",     ["startup dna", "startup experience", "founder", "hustle", "scrappy"]),
    ("similar",         ["similar", "like", "compare", "looks like"]),
    ("why_a_over_b",    ["why", "over", "better than", "compare to"]),
    ("transition_ml",   ["transition into ml", "move to ml", "learn ml", "switch to ml"]),
    ("draft_email",     ["draft outreach email", "draft email", "write email", "outreach"]),
    ("help",            ["help", "what can you do", "how do you work", "commands"]),
]


def _classify_intent(message: str) -> str:
    text = message.casefold()
    for intent, keywords in INTENT_MAP:
        if any(kw in text for kw in keywords):
            return intent
    return "general"


# ── Answer generators (one per intent) ───────────────────────────────────────

def _answer_strengths(candidate: CandidateDigitalTwin | None, role: RoleDNAProfile | None) -> tuple[str, list[str]]:
    if candidate is None:
        return ("Please provide a candidate to analyse their strengths.", ["Which candidate would you like to assess?"])
    top = sorted(
        [("technical_depth", candidate.technical_depth),
         ("learning_velocity", candidate.learning_velocity),
         ("ownership", candidate.ownership),
         ("communication", candidate.communication)],
        key=lambda x: x[1], reverse=True
    )[:3]
    bullets = ", ".join(f"{k.replace('_', ' ')} ({v}/100)" for k, v in top)
    answer = f"{candidate.name}'s top scoring dimensions are: {bullets}."
    if candidate.skills:
        answer += f" Key skills include: {', '.join(candidate.skills[:5])}."
    return answer, ["What are their biggest risks?", "How do they compare to the role requirements?"]


def _answer_risks(candidate: CandidateDigitalTwin | None, role: RoleDNAProfile | None) -> tuple[str, list[str]]:
    if candidate is None:
        return ("Provide a candidate to analyse risks.", ["Which candidate would you like to assess?"])
    low = sorted(
        [("technical_depth", candidate.technical_depth),
         ("communication", candidate.communication),
         ("leadership", candidate.leadership),
         ("project_complexity", candidate.project_complexity)],
        key=lambda x: x[1]
    )[:2]
    bullets = " and ".join(f"{k.replace('_', ' ')} ({v}/100)" for k, v in low)
    answer = f"The lowest scoring dimensions for {candidate.name} are {bullets}."
    if role and candidate.communication < role.communication:
        answer += " Communication is below role expectations."
    return answer, ["What can they do to improve their profile?", "Are there any strengths to balance these risks?"]


def _answer_skills(candidate: CandidateDigitalTwin | None, role: RoleDNAProfile | None) -> tuple[str, list[str]]:
    if candidate is None:
        return ("No candidate loaded. Provide a candidate to see their skill profile.", [])
    ans = f"{candidate.name} has {len(candidate.skills)} extracted skill(s): {', '.join(candidate.skills)}."
    if role:
        matched = [s for s in role.required_skills if s.lower() in {x.lower() for x in candidate.skills}]
        missing = [s for s in role.required_skills if s.lower() not in {x.lower() for x in candidate.skills}]
        ans += f" {len(matched)}/{len(role.required_skills)} required role skills are present."
        if missing:
            ans += f" Missing: {', '.join(missing[:4])}."
    return ans, ["What is their technical depth score?", "Are there preferred skills they meet?"]


def _answer_growth(candidate: CandidateDigitalTwin | None, role: RoleDNAProfile | None) -> tuple[str, list[str]]:
    if candidate is None:
        return ("Provide a candidate to discuss growth potential.", [])
    lv = candidate.learning_velocity
    stage = candidate.growth_stage
    ans = f"{candidate.name} is at the '{stage}' growth stage with a learning velocity of {lv}/100."
    if lv >= 75:
        ans += " They are expected to ramp quickly — within 1–2 months."
    elif lv >= 50:
        ans += " Estimated 2–4 month onboarding window."
    else:
        ans += " Longer onboarding may be required."
    return ans, ["What leadership potential do they show?", "How does their growth compare to role expectations?"]


def _answer_leadership(candidate: CandidateDigitalTwin | None, role: RoleDNAProfile | None) -> tuple[str, list[str]]:
    if candidate is None:
        return ("Provide a candidate to assess leadership.", [])
    lr = getattr(candidate, 'leadership_readiness', candidate.leadership)
    ans = f"{candidate.name} has a leadership score of {candidate.leadership}/100 and leadership readiness of {lr}/100."
    if lr >= 70:
        ans += " Strong signals of readiness for team-lead or mentoring roles."
    elif lr >= 50:
        ans += " Shows potential but may need structured growth opportunities."
    else:
        ans += " Leadership signals are limited at this stage."
    return ans, ["What is their communication score?", "Would they suit a senior individual contributor role instead?"]


def _answer_match(candidate: CandidateDigitalTwin | None, role: RoleDNAProfile | None) -> tuple[str, list[str]]:
    if candidate is None or role is None:
        return ("Load both a candidate and a role to assess fit.", ["Which candidate and role would you like me to compare?"])
    td_diff = candidate.technical_depth - role.technical_depth
    ow_diff = candidate.ownership - role.ownership
    comm_diff = candidate.communication - role.communication
    gaps = [f for f, d in [("technical depth", td_diff), ("ownership", ow_diff), ("communication", comm_diff)] if d < -10]
    ans = f"Comparing {candidate.name} to the '{role.role_title}' role."
    if not gaps:
        ans += " Candidate meets or exceeds key dimension benchmarks."
    else:
        ans += f" Notable gaps in: {', '.join(gaps)}."
    return ans, ["Run a formal evaluation to get an exact match score.", "Generate an explanation for full detail."]


def _answer_timeline(candidate: CandidateDigitalTwin | None, role: RoleDNAProfile | None) -> tuple[str, list[str]]:
    if candidate is None:
        return ("Provide a candidate to review their career timeline.", [])
    if not candidate.timeline:
        return (f"No career timeline events were extracted for {candidate.name}.", ["Try re-parsing the resume with more detail."])
    events = sorted(candidate.timeline, key=lambda e: e.year)
    summary = "; ".join(f"{e.year}: {e.event}" for e in events[:5])
    ans = f"{candidate.name}'s career timeline ({len(candidate.timeline)} events): {summary}."
    return ans, ["What was their most recent role?", "How long have they been working?"]


def _answer_recommendation(candidate: CandidateDigitalTwin | None, role: RoleDNAProfile | None) -> tuple[str, list[str]]:
    if candidate is None:
        return ("Provide a candidate to get a hiring recommendation.", [])
    confidence = candidate.confidence
    if confidence >= 75:
        verdict = "STRONG HIRE — high confidence profile with strong signals."
    elif confidence >= 55:
        verdict = "HIRE — solid profile with minor gaps."
    elif confidence >= 40:
        verdict = "GROWTH HIRE — promising but needs development."
    else:
        verdict = "BORDERLINE — limited evidence; recommend additional interview."
    return (f"Copilot recommendation for {candidate.name}: {verdict} (confidence: {confidence}/100).",
            ["Generate a formal explanation for audit trail.", "What can they do to improve their standing?"])


def _answer_salary(candidate: CandidateDigitalTwin | None, role: RoleDNAProfile | None) -> tuple[str, list[str]]:
    ans = "TalentGraph does not make salary recommendations — this is outside its scope."
    return ans, ["Focus on skill match and evaluation score instead.", "Use an external compensation benchmarking tool."]


def _answer_help(candidate: CandidateDigitalTwin | None, role: RoleDNAProfile | None) -> tuple[str, list[str]]:
    return (
        "I am the TalentGraph Recruiter Copilot. You can ask me about: "
        "candidate strengths, risks, skills, growth potential, leadership, "
        "career timeline, hiring recommendation, or role fit.",
        ["What are this candidate's strengths?",
         "What are the risks of hiring them?",
         "How do they match the role?"]
    )


def _answer_general(candidate: CandidateDigitalTwin | None, role: RoleDNAProfile | None) -> tuple[str, list[str]]:
    name = candidate.name if candidate else "the candidate"
    return (
        f"I didn't quite catch that. I can help with analysis of {name}'s strengths, risks, skills, growth, "
        "leadership, timeline, and hiring recommendation.",
        ["What are their strengths?", "What are the key risks?", "How do they match the role?"]
    )


def _answer_interview_first(candidate: CandidateDigitalTwin | None, role: RoleDNAProfile | None) -> tuple[str, list[str]]:
    return ("Based on overall match and confidence, I recommend interviewing candidates with a High risk_profile and top technical scores first.", ["Who learns fastest?"])

def _answer_learns_fastest(candidate: CandidateDigitalTwin | None, role: RoleDNAProfile | None) -> tuple[str, list[str]]:
    if candidate:
        return (f"{candidate.name} has a learning velocity of {candidate.learning_velocity}/100.", ["Who has startup DNA?"])
    return ("Look for candidates with a learning velocity score above 85/100.", ["Who has startup DNA?"])

def _answer_startup_dna(candidate: CandidateDigitalTwin | None, role: RoleDNAProfile | None) -> tuple[str, list[str]]:
    return ("Candidates with high ambiguity tolerance and ownership typically have strong startup DNA.", ["Which candidates are similar?"])

def _answer_similar(candidate: CandidateDigitalTwin | None, role: RoleDNAProfile | None) -> tuple[str, list[str]]:
    return ("To find similar candidates, check the 'Similar Profiles' section in the Comparison Workspace which uses vector similarity.", ["Why Candidate A over Candidate B?"])

def _answer_why_a_over_b(candidate: CandidateDigitalTwin | None, role: RoleDNAProfile | None) -> tuple[str, list[str]]:
    return ("Candidate A might be preferred over Candidate B if they have stronger role alignment, higher ownership, and better learning velocity. Check the detailed evaluation for specific gaps.", ["Who can transition into ML?"])

def _answer_transition_ml(candidate: CandidateDigitalTwin | None, role: RoleDNAProfile | None) -> tuple[str, list[str]]:
    return ("Strong backend engineers with high learning velocity and problem-solving scores can often transition into ML smoothly.", ["Draft outreach email."])

def _answer_draft_email(candidate: CandidateDigitalTwin | None, role: RoleDNAProfile | None) -> tuple[str, list[str]]:
    name = candidate.name if candidate else "[Candidate]"
    return (f"Subject: Exploring opportunities at our company\n\nHi {name},\n\nI was impressed by your background and would love to chat about a potential fit for our open role. Let me know when you're free for a quick call.\n\nBest,\nRecruiting Team", ["What are their strengths?"])


# ── Intent router ─────────────────────────────────────────────────────────────

_HANDLERS = {
    "strengths":      _answer_strengths,
    "risks":          _answer_risks,
    "skills":         _answer_skills,
    "growth":         _answer_growth,
    "leadership":     _answer_leadership,
    "match":          _answer_match,
    "timeline":       _answer_timeline,
    "recommendation": _answer_recommendation,
    "salary":         _answer_salary,
    "interview_first": _answer_interview_first,
    "learns_fastest": _answer_learns_fastest,
    "startup_dna":    _answer_startup_dna,
    "similar":        _answer_similar,
    "why_a_over_b":   _answer_why_a_over_b,
    "transition_ml":  _answer_transition_ml,
    "draft_email":    _answer_draft_email,
    "help":           _answer_help,
    "general":        _answer_general,
}


class CopilotChatService:
    """Deterministic recruiter chat service — intent routing without LLMs."""

    def __init__(
        self,
        candidate_repository=None,
        role_repository=None,
    ) -> None:
        self.candidate_repository = candidate_repository
        self.role_repository = role_repository

    def chat(self, request: CopilotChatRequest) -> CopilotChatResponse:
        candidate: CandidateDigitalTwin | None = None
        role: RoleDNAProfile | None = None

        if request.candidate_id and self.candidate_repository:
            candidate = self.candidate_repository.get_by_candidate_id(request.candidate_id)

        if request.role_id and self.role_repository:
            role = self.role_repository.get_by_role_id(request.role_id)

        intent = _classify_intent(request.message)
        handler = _HANDLERS.get(intent, _answer_general)
        answer, follow_ups = handler(candidate, role)

        return CopilotChatResponse(
            intent=intent,
            answer=answer,
            follow_up_questions=follow_ups,
        )
