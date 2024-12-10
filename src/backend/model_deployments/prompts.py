from typing import List

from backend.schemas.citation import CitationList


def get_system_promp(agent_id: str) -> str:
    match agent_id:
        case "basic":
            return "Du hilfst Nutzern bei der Beantwortung von Fragen und Aufgaben. Halte dich dabei genau an die Anweisungen."
        case "kerlin":
            pass
        case "zitatki":
            pass
        case "researchki":
            pass

    return ""


def get_search_prompt(query: str, prev_queries: List[str], interview_text: str) -> str:
    prev_queries_concat = "\n".join(prev_queries)
    prompt = f"""Im Folgenden erhaeltst du ein Einzelinterview Transcript (INTERVIEW_TRANSKRIPT) einer
 tiefenpsychologischen Markforschungsstudie. Anschliessend folgt eine Frage oder Aufgabe (FRAGE) zu dem Interview.
 In manachen Fällen baut die Frage auf vorherigen Fragen (FRAGEN_VORHER) auf. Beantworte die FRAGE in dem du
 passende Zitate aus dem INTERVIEW_TRANSKRIPT verwendest. Dabei soll deine Antwort folgendes JSON Format haben:
 {CitationList.model_json_schema()}
Du kannst bis zu 10 Zitate zurückgeben.

INTERVIEW_TRANSKRIPT:
{interview_text}

FRAGEN_VORHER:
{prev_queries_concat}

FRAGE: {query}
"""
    return prompt
