"""Content quality scoring rubric."""

import re


def score_content(text: str) -> dict:
    """Score content on 4 dimensions (1-10 each). Heuristic-based demo."""
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    words = text.split()
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

    # Clarity: avg sentence length (shorter = clearer, up to a point)
    avg_sent_len = len(words) / max(len(sentences), 1)
    if avg_sent_len < 10:
        clarity = 6
    elif avg_sent_len < 20:
        clarity = 8
    elif avg_sent_len < 30:
        clarity = 6
    else:
        clarity = 4

    # Structure: presence of headings, paragraphs, lists
    has_headings = bool(re.search(r'^#{1,3}\s', text, re.MULTILINE))
    has_lists = bool(re.search(r'^[-*]\s', text, re.MULTILINE))
    structure = 5 + (2 if has_headings else 0) + (2 if has_lists else 0) + (1 if len(paragraphs) > 3 else 0)
    structure = min(structure, 10)

    # Engagement: questions, strong verbs, opening hook
    has_questions = '?' in text
    first_sent = sentences[0].lower() if sentences else ''
    has_hook = any(w in first_sent for w in ['imagine', 'what if', 'ever', 'you'])
    engagement = 4 + (2 if has_questions else 0) + (2 if has_hook else 0) + (1 if len(words) > 200 else 0)
    engagement = min(engagement, 10)

    # Completeness: intro + body + conclusion signals
    has_intro = len(paragraphs) >= 1 and len(paragraphs[0].split()) > 20
    last_para = paragraphs[-1].lower() if paragraphs else ''
    has_conclusion = any(w in last_para for w in ['conclusion', 'summary', 'in short', 'finally'])
    completeness = 4 + (2 if has_intro else 0) + (2 if has_conclusion else 0) + (1 if len(words) > 300 else 0) + (1 if len(paragraphs) > 4 else 0)
    completeness = min(completeness, 10)

    overall = round((clarity + structure + engagement + completeness) / 4, 1)

    feedback = []
    if clarity < 7:
        feedback.append("Sentences are too long or too short — aim for 15-20 words average.")
    if structure < 7:
        feedback.append("Add headings and bullet lists to improve scannability.")
    if engagement < 7:
        feedback.append("Open with a hook (question, surprising fact, or 'you' statement).")
    if completeness < 7:
        feedback.append("Add a clear conclusion that summarizes key takeaways.")

    return {
        'clarity': clarity,
        'structure': structure,
        'engagement': engagement,
        'completeness': completeness,
        'overall': overall,
        'feedback': feedback,
    }
