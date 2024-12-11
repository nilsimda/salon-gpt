from typing import List

from backend.schemas.citation import CitationList

BASIC_SYSTEM_PROMPT = "Du hilfst Nutzern bei der Beantwortung von Fragen und Aufgaben. Halte dich dabei genau an die Anweisungen."

SYSTEM_PROMPT_MAP = {
    "basic": BASIC_SYSTEM_PROMPT,
}


def get_system_prompt(agent_id: str, description="") -> str:
    if agent_id == "kerlin":
        return get_kerlin_system_prompt(description)
    return SYSTEM_PROMPT_MAP.get(agent_id, BASIC_SYSTEM_PROMPT)


def get_kerlin_system_prompt(description: str) -> str:
    return f"""Du simulierst einen synthetischen Nutzer der an einem Marktforschungsinterview teilnimmt. Deine Aufgabe ist es, auf die Fragen des Interviewers zu antworten und
 dabei so zu tun, als wärst du ein echter Mensch. Hier ist die Beschreibung des Nutzers (also von dir):

 BECHREIBUNG DES NUTZERS:
{description}
"""


def get_search_prompt(query: str, prev_queries: List[str], interview_text: str) -> str:
    prev_queries_concat = "\n".join(prev_queries)
    prompt = f"""Deine Aufgabe ist es, direkte Zitate aus einem langen Markforschungs-Interview zu finden und in folgendem JSON-Format zurückzugeben:
 {CitationList.model_json_schema()}. Im folgenden erhältst du vom Nutzer ein Interview-Transkript (INTERVIEW_TRANSKRIPT) und eine Frage oder Aufgabe (FRAGE), zu der du passende Zitate finden sollst.
 Du kannst bis zu 10 Zitate zurückgeben. Jeglicher Text innerhalb der JSON-Struktur sollte Deutsch sein.

INTERVIEW_TRANSKRIPT:
{interview_text}

FRAGEN_VORHER:
{prev_queries_concat}

FRAGE: {query}
"""
    return prompt
