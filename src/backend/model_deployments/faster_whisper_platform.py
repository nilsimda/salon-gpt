from typing import Any, Dict, List

import ollama

from backend.model_deployments.base import BaseDeployment
from backend.schemas.cohere_chat import CohereChatRequest
from backend.schemas.context import Context

FW_ENV_VARS = []

class FasterWhisperDeployment(BaseDeployment):
    def __init__(self, model_path: str = "llama3.2", template: str = None, ctx: Context = None):
        self.prompt_template = None
        self.template = template
        self.model = model_path

    @property
    def rerank_enabled(self) -> bool:
        return False

    @classmethod
    def list_models(cls) -> List[str]:
        return ["llama3.2", "mistral-nemo"]

    @classmethod
    def is_available(cls) -> bool:
        return True

    async def invoke_chat_stream(
        self, chat_request: CohereChatRequest, ctx: Context, **kwargs: Any
    ) -> Any:

        if not chat_request.model:
            chat_request.model = self.model

        if chat_request.max_tokens is None:
            chat_request.max_tokens = 200

        #if len(chat_request.documents) == 0:
        #    prompt = self.prompt_template.dummy_chat_template(
        #        chat_request.message, chat_request.chat_history
        #    )
        #else:
        #    prompt = self.prompt_template.dummy_rag_template(
        #        chat_request.message, chat_request.chat_history, chat_request.documents
        #    )

        stream = ollama.chat(
            model="mistral-nemo",#chat_request.model,
            messages=[{'role': 'user', 'content': chat_request.message}],
            stream=True,
            options={"max_tokens": chat_request.max_tokens, "temperature": chat_request.temperature},
        )

        yield {
            "event_type": "stream-start",
            "generation_id": "",
        }

        for item in stream:
            yield {
                "event_type": "text-generation",
                "text": item["message"]["content"],
            }

        yield {
            "event_type": "stream-end",
            "finish_reason": "COMPLETE",
            "response": {}
        }

    async def invoke_chat(
        self, chat_request: CohereChatRequest, ctx: Context, **kwargs: Any
    ) -> Any:

        if not chat_request.model:
            chat_request.model = self.model

        if chat_request.max_tokens is None:
            chat_request.max_tokens = 200

        response = ollama.chat(
            model="mistral-nemo",#chat_request.model,
            messages=[{'role': 'user', 'content': chat_request.message}],
            stream=False,
            options={"max_tokens": chat_request.max_tokens, "temperature": chat_request.temperature},
        )

        return {"text": response['message']['content']}

    async def invoke_rerank(
        self, query: str, documents: List[Dict[str, Any]], ctx: Context, **kwargs: Any
    ) -> Any:
        return None
