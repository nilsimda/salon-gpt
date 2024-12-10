from typing import Any, AsyncGenerator

from huggingface_hub import InferenceClient

import backend.model_deployments.prompts as prompts
from backend.schemas.chat import BaseChatRequest, SearchChatRequest, StreamEvent
from backend.schemas.citation import CitationList


class TGIDeployment:
    def __init__(self, base_url="http://tgi:80/v1"):
        self.client = InferenceClient(base_url)

    async def invoke_chat_stream(
        self, chat_request: BaseChatRequest
    ) -> AsyncGenerator[Any, Any]:
        yield {
            "event_type": StreamEvent.STREAM_START,
            "generation_id": "",
        }

        messages = [
            {
                "role": "system",
                "content": prompts.get_system_promp(chat_request.agent_id),
            }
        ]

        if chat_request.chat_history is not None:
            for message in chat_request.chat_history:
                messages.append(message.to_dict())

        messages.append({"role": "user", "content": chat_request.message})

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

    async def invoke_search_stream(
        self, search_request: SearchChatRequest
    ) -> AsyncGenerator[Any, Any]:
        yield {
            "event_type": StreamEvent.STREAM_START,
            "generation_id": "",
        }

        for interview in search_request.interviews:
            prompt: str = prompts.get_search_prompt(
                search_request.message, [], interview.text
            )

            output = self.client.text_generation(
                prompt=prompt,
                seed=42,
                grammar={"type": "json", "value": CitationList.model_json_schema()},  # type: ignore
            )

            yield {
                "event_type": StreamEvent.SEARCH_RESULTS,
                "text": output,
            }

        yield {"event_type": StreamEvent.STREAM_END, "finish_reason": "COMPLETE"}

    async def invoke_chat(self, chat_request: BaseChatRequest) -> dict[str, str]:
        return {"text": "Not implemented yet"}
