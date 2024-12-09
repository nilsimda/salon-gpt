from typing import Any, AsyncGenerator, Generator, List

from huggingface_hub import InferenceClient

from backend.schemas.chat import BaseChatRequest, SearchChatRequest, StreamEvent
from backend.schemas.context import Context


class TGIDeployment:
    def __init__(self, base_url="http://tgi:80/v1"):
        self.client = InferenceClient(base_url)

    @classmethod
    def list_models(cls) -> List[str]:
        return ["mistral-nemo"]

    @classmethod
    def is_available(cls) -> bool:
        return True

    async def invoke_chat_stream(
        self, chat_request: BaseChatRequest, ctx: Context, **kwargs: Any
    ) -> AsyncGenerator[Any, Any]:
        yield {
            "event_type": StreamEvent.STREAM_START,
            "generation_id": "",
        }

        messages = [
            {
                "role": "system",
                "content": chat_request.system,
            },
        ]

        if chat_request.chat_history is not None:
            for message in chat_request.chat_history:
                messages.append(message.to_dict())

        messages.append({"role": "user", "content": chat_request.message})
        print(messages)

        output = self.client.chat.completions.create(
            model="tgi",
            messages=messages,
            stream=True,
        )

        for chunk in output:
            yield {
                "event_type": StreamEvent.TEXT_GENERATION,
                "text": chunk.choices[0].delta.content,
            }

        yield {"event_type": StreamEvent.STREAM_END, "finish_reason": "COMPLETE"}

    def invoke_search_stream(
        self, search_request: SearchChatRequest, ctx: Context, **kwargs: Any
    ) -> Generator[Any, Any, Any]:
        yield {
            "event_type": StreamEvent.STREAM_START,
            "generation_id": "",
        }

        for interview in search_request.interviews:
            output = self.client.text_generation(
                prompt=json_search_template(search_request.query, [], interview.text),
                seed=42,
                grammar="json"
            )
            yield {
                "event_type": StreamEvent.TEXT_GENERATION,
                "text": output.choices[0].delta.content,
            }

        yield {"event_type": StreamEvent.STREAM_END, "finish_reason": "COMPLETE"}


def json_search_template(
    self, query: str, prev_queries: List[str], interview_text: str
) -> str:
    prev_queries_concat = "\n".join(prev_queries)
    prompt = f"""Im Folgenden erhaeltst du ein Einzelinterview Transcript (INTERVIEW_TRANSKRIPT) einer 
tiefenpsychologischen Markforschungsstudie. Anschliessend folgt eine Frage oder Aufgabe (FRAGE) zu dem Interview.
In manachen Fällen baut die Frage auf vorherigen Fragen (FRAGEN_VORHER) auf. Beantworte die FRAGE in dem du 
passende Zitate aus dem INTERVIEW_TRANSKRIPT verwendest. Dabei soll deine Antwort folgendes JSON Format haben:
{{ "zitate": [
    {{
        "text": <1. Zitat aus dem Interview>,
        "confidence_score": <Wie sicher bist du dir mit deiner Antwort auf einer Skala von 0.0-1.0>
    }},
    {{
        "text": <2. Zitat aus dem Interview>,
        "confidence_score": <Wie sicher bist du dir mit deiner Antwort auf einer Skala von 0.0-1.0>
    }},
    ...
    ]
}}
Du kannst bis zu 10 Zitate zurückgeben.

INTERVIEW_TRANSKRIPT:
{interview_text}

FRAGEN_VORHER:
{prev_queries_concat}

FRAGE: {query}
"""
    return prompt
