import re
import sys

def apply_dark_mode(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replacements
    replacements = {
        r'\bbg-white\b(?! dark:bg-)': 'bg-white dark:bg-slate-900',
        r'\bborder-gray-200\b(?! dark:border-)': 'border-gray-200 dark:border-slate-800',
        r'\btext-ink\b(?! dark:text-)': 'text-ink dark:text-slate-50',
        r'\btext-graphite\b(?! dark:text-)': 'text-graphite dark:text-slate-400',
        r'\bbg-gray-50\b(?! dark:bg-)': 'bg-gray-50 dark:bg-slate-800/50',
        r'\bborder-gray-300\b(?! dark:border-)': 'border-gray-300 dark:border-slate-700',
        r'\btext-gray-900\b(?! dark:text-)': 'text-gray-900 dark:text-slate-100',
        r'\btext-gray-500\b(?! dark:text-)': 'text-gray-500 dark:text-slate-400',
        r'\btext-gray-700\b(?! dark:text-)': 'text-gray-700 dark:text-slate-300',
        r'\bbg-gray-100\b(?! dark:bg-)': 'bg-gray-100 dark:bg-slate-800',
        r'\bbg-[#f7f8fb]\b(?! dark:bg-)': 'bg-[#f7f8fb] dark:bg-slate-950',
        r'\btext-gray-600\b(?! dark:text-)': 'text-gray-600 dark:text-slate-400',
        r'\btext-gray-800\b(?! dark:text-)': 'text-gray-800 dark:text-slate-200',
    }

    for pattern, repl in replacements.items():
        content = re.sub(pattern, repl, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

apply_dark_mode('apps/web/app/page.tsx')
apply_dark_mode('apps/web/components/CandidateLibrary.tsx')
apply_dark_mode('apps/web/components/CopilotChatPanel.tsx')
