from typing import Any, AsyncGenerator

import bm25s
from huggingface_hub import InferenceClient

from backend.model_deployments.prompts import get_search_prompt, get_system_prompt
from backend.schemas.chat import (
    SalonChatRequest,
    StreamEvent,
)
from backend.schemas.citation import Citation, CitationList


class TGIDeployment:
    def __init__(self, base_url="http://tgi:80"):
        self.client = InferenceClient(base_url)

    async def invoke_chat_stream(
        self, chat_request: SalonChatRequest
    ) -> AsyncGenerator[Any, Any]:
        yield {
            "event_type": StreamEvent.STREAM_START,
            "generation_id": "",
        }
        handlers = {
            "zitatki": self.handle_search,
            "kerlin": self.handle_chat,
            "basic": self.handle_chat,
        }
        async for item in handlers[chat_request.agent_id](chat_request):
            yield item

        yield {"event_type": StreamEvent.STREAM_END, "finish_reason": "COMPLETE"}

    async def handle_chat(
        self, chat_request: SalonChatRequest
    ) -> AsyncGenerator[Any, Any]:
        description = (
            chat_request.description if chat_request.agent_id == "kerlin" else ""
        )

        messages = [
            {
                "role": "system",
                "content": get_system_prompt(
                    agent_id=chat_request.agent_id, description=description
                ),
            }
        ]

        if chat_request.chat_history is not None:
            for message in chat_request.chat_history:
                messages.append(
                    {"role": message.role.value, "content": message.message}
                )

        messages.append({"role": "user", "content": chat_request.message})

        output = self.client.chat_completion(
            messages=messages,
            seed=42,
            stream=True,
        )

        for chunk in output:
            yield {
                "event_type": StreamEvent.TEXT_GENERATION,
                "text": chunk.choices[0].delta.content,
            }

    async def handle_search(
        self, search_request: SalonChatRequest
    ) -> AsyncGenerator[Any, Any]:
        assert search_request.interviews is not None, (
            "Interviews must be provided for search task."
        )

        for interview in search_request.interviews:
            prompt: str = get_search_prompt(search_request.message, [], interview.text)
            bm25s.tokenize(prompt)

            # output = self.client.text_generation(
            # prompt=prompt,
            # seed=42,
            # grammar={"type": "json", "value": CitationList.model_json_schema()},  # type: ignore
            # )
            output = CitationList(
                zitate=[Citation(erklaerung="test", text="test", bewertung=0.5)]
            )

            yield {
                "event_type": StreamEvent.SEARCH_RESULTS,
                "search_results": output,  # CitationList.model_validate_json(output),
                "interview_id": interview.id,
            }
