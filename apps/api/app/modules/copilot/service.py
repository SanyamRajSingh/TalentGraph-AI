from app.domain.copilot import CopilotDraftResponse
from app.domain.evaluation import EvaluationBundle


class CopilotService:
    """Generates personalized recruiter outreach emails deterministically based on evaluation bundles."""

    def draft_email(self, candidate_name: str, role_title: str, bundle: EvaluationBundle) -> CopilotDraftResponse:
        subject = f"TalentGraph: Exploring the {role_title} role"
        
        all_strengths = []
        if bundle.technical and bundle.technical.strengths:
            all_strengths.extend(bundle.technical.strengths)
        if bundle.domain and bundle.domain.strengths:
            all_strengths.extend(bundle.domain.strengths)
        if bundle.growth and bundle.growth.strengths:
            all_strengths.extend(bundle.growth.strengths)
        
        strength = "your impressive background"
        if all_strengths:
            # Clean up the strength text for better email flow
            first_strength = all_strengths[0].replace("Matches required skills: ", "").replace("Matches preferred skills: ", "").rstrip(".")
            strength = f"your strong experience with {first_strength}"
            
        body = f"Hi {candidate_name},\n\n"
        body += f"I was reviewing your profile and was really impressed by {strength}. "
        body += f"We have an opening for a {role_title} that seems like a great match for your skills.\n\n"
        body += "I'd love to chat and share more details about the team and what we are building.\n\n"
        body += "Are you open to a quick call sometime next week?\n\n"
        body += "Best,\nTalentGraph Recruiter"
        
        return CopilotDraftResponse(subject=subject, body=body)
