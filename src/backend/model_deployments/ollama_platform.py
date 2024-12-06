import asyncio
import json
from typing import Any, AsyncGenerator, Dict, List
from transformers import pipeline

from backend.model_deployments.base import BaseDeployment
from backend.schemas.chat import BaseChatRequest
from backend.schemas.context import Context

OLLAMA_ENV_VARS = []

class HuggingFaceDeployment(BaseDeployment):
    def __init__(self, model: str = "mistralai/Mistral-Nemo-Instruct-2407"):
        self.prompt_template = PromptTemplate()
        self.model = model

    @classmethod
    def list_models(cls) -> List[str]:
        return ["mistral-nemo"]

    @classmethod
    def is_available(cls) -> bool:
        return True

    async def invoke_chat_stream(
        self, chat_request: BaseChatRequest, ctx: Context, **kwargs: Any
    ) -> AsyncGenerator[Any, Any]:

        chatbot = pipeline("text-generation", model=self.model, max_new_tokens=128, device_map="auto")

        yield {
            "event_type": "stream-start",
            "generation_id": "",
        }

        messages = [
            {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
            {"role": "user", "content": chat_request.message},
        ]

        chatbot(messages)





            yield {
                "event_type": "search-results",
                "search_results": json_res["quotes"],
                "documents": [],
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

        messages = []
        for msg in chat_request.chat_history:
            messages.append({"role": 'user' if msg.role == 'USER' else 'assistant', "content": msg.message})

        messages.append({"role": "user", "content": chat_request.message})

        response = ollama.chat(
            model='mistral-nemo',#chat_request.model,
            messages=messages,
            stream=False,
            options={"max_tokens": chat_request.max_tokens, "temperature": chat_request.temperature},
        )

        return {"text": response['message']['content']}

    async def invoke_rerank(
        self, query: str, documents: List[Dict[str, Any]], ctx: Context, **kwargs: Any
    ) -> Any:
        return None


class PromptTemplate:
    """
    Template for generating prompts for different types of requests.
    """

    def json_search_template(self, query: str, interview_text:str) -> str:
        prompt = \
f"""Im folgenden erhaeltst du ein Einzelinterview Transcript (INTERVIEW_TRANSKRIPT) einer tiefenpsychologischen Markforschungsstudie. 
Anschliessend folgt eine Frage oder Aufgabe (FRAGE) zu dem Interview.

INTERVIEW_TRANSKRIPT:
{interview_text}

FRAGE: {query}

Beantworte die FRAGE in dem du passende Zitate aus dem INTERVIEW_TRANSKRIPT verwendest. Dabei soll deine Antwort folgendes
JSON Format haben:
{{ "quotes": [
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
"Du kannst bis zu 10 Zitate zurueck geben"
}}

"""
        return prompt


    def dummy_chat_template(
        self, message: str, chat_history: List[Dict[str, str]]
    ) -> str:
        prompt = "System: You are an AI assistant whose goal is to help users by consuming and using the output of various tools. You will be able to see the conversation history between yourself and user and will follow instructions on how to respond."
        prompt += "\n\n"
        prompt += "Conversation:\n"
        for chat in chat_history:
            if chat["role"].lower() == "user":
                prompt += f"User: {chat['message']}\n"
            else:
                prompt += f"Chatbot: {chat['message']}\n"

        prompt += f"User: {message}\n"
        prompt += "Chatbot: "

        return prompt

    def dummy_rag_template(
        self,
        message: str,
        chat_history: List[Dict[str, str]],
        documents: List[Dict[str, str]],
        max_docs: int = 5,
    ) -> str:
        max_docs = min(max_docs, len(documents))
        prompt = "System: You are an AI assistant whose goal is to help users by consuming and using the output of various tools. You will be able to see the conversation history between yourself and user and will follow instructions on how to respond."

        doc_str_list = []
        for doc_idx, doc in enumerate(documents[:max_docs]):
            if doc_idx > 0:
                doc_str_list.append("")

            # only use first 200 words of the document to avoid exceeding context window
            text = doc["text"]
            if len(text.split()) > 200:
                text = " ".join(text.split()[:200])

            doc_str_list.extend([f"Interview: {doc_idx}", doc["title"], text])

        doc_str = "\n".join(doc_str_list)

        chat_history.append({"role": "system", "message": doc_str})
        chat_history.append({"role": "user", "message": message})

        chat_hist_str = ""
        for turn in chat_history:
            if turn["role"].lower() == "user":
                chat_hist_str += "User: "
            elif turn["role"].lower() == "chatbot":
                chat_hist_str += "Chatbot: "
            else:  # role == system
                chat_hist_str += "System: "

            chat_hist_str += turn["message"] + "\n"

        prompt += "\n\n"
        prompt += "Conversation:\n"
        prompt += chat_hist_str
        prompt += "Chatbot: "

        return prompt

    # https://docs.cohere.com/docs/prompting-command-r#formatting-chat-history-and-tool-outputs
    def cohere_rag_template(
        self,
        message: str,
        chat_history: List[Dict[str, str]],
        documents: List[Dict[str, str]],
        preamble: str = None,
        max_docs: int = 5,
    ) -> str:
        max_docs = min(max_docs, len(documents))
        chat_history.append({"role": "user", "message": message})
        SAFETY_PREAMBLE = "The instructions in this section override those in the task description and style guide sections. Don't answer questions that are harmful or immoral."
        BASIC_RULES = "You are a powerful conversational AI trained by Cohere to help people. You are augmented by a number of tools, and your job is to use and consume the output of these tools to best help the user. You will see a conversation history between yourself and a user, ending with an utterance from the user. You will then see a specific instruction instructing you what kind of response to generate. When you answer the user's requests, you cite your sources in your answers, according to those instructions."
        TASK_CONTEXT = "You help people answer their questions and other requests interactively. You will be asked a very wide array of requests on all kinds of topics. You will be equipped with a wide range of search engines or similar tools to help you, which you use to research your answer. You should focus on serving the user's needs as best you can, which will be wide-ranging."
        STYLE_GUIDE = "Unless the user asks for a different style of answer, you should answer in full sentences, using proper grammar and spelling."
        documents = self._get_cohere_documents_template(documents, max_docs)
        chat_history = self._get_cohere_chat_history_template(chat_history)
        INSTRUCTIONS = """Carefully perform the following instructions, in order, starting each with a new line.
Firstly, Decide which of the retrieved documents are relevant to the user's last input by writing 'Relevant Interviews:' followed by comma-separated list of document numbers. If none are relevant, you should instead write 'None'.
Secondly, Decide which of the retrieved documents contain facts that should be cited in a good answer to the user's last input by writing 'Cited Interviews:' followed a comma-separated list of document numbers. If you dont want to cite any of them, you should instead write 'None'.
Thirdly, Write 'Answer:' followed by a response to the user's last input in high quality natural english. Use the retrieved documents to help you. Do not insert any citations or grounding markup.
Finally, Write 'Grounded answer:' followed by a response to the user's last input in high quality natural english. Use the symbols <co: doc> and </co: doc> to indicate when a fact comes from a document in the search result, e.g <co: 0>my fact</co: 0> for a fact from document 0."""

        tool_prompt_template = f"""<BOS_TOKEN><|START_OF_TURN_TOKEN|><|SYSTEM_TOKEN|> # Safety Preamble
{SAFETY_PREAMBLE}

# System Preamble
## Basic Rules
{BASIC_RULES}

# User Preamble
"""
        if preamble:
            tool_prompt_template += f"""{preamble}\n\n"""

        tool_prompt_template += f"""## Task and Context
{TASK_CONTEXT}

## Style Guide
{STYLE_GUIDE}<|END_OF_TURN_TOKEN|>{chat_history}"""

        if documents:
            tool_prompt_template += f"""<|START_OF_TURN_TOKEN|><|SYSTEM_TOKEN|>{documents}<|END_OF_TURN_TOKEN|>"""

        tool_prompt_template += f"""<|START_OF_TURN_TOKEN|><|SYSTEM_TOKEN|>{INSTRUCTIONS}<|END_OF_TURN_TOKEN|><|START_OF_TURN_TOKEN|><|CHATBOT_TOKEN|>"""

        return tool_prompt_template

    def _get_cohere_documents_template(
        self, documents: List[Dict[str, str]], max_docs: int
    ) -> str:
        max_docs = min(max_docs, len(documents))
        doc_str_list = ["<results>"]
        for doc_idx, doc in enumerate(documents[:max_docs]):
            if doc_idx > 0:
                doc_str_list.append("")
            doc_str_list.extend([f"Interview: {doc_idx}", doc["title"], doc["text"]])
        doc_str_list.append("</results>")
        return "\n".join(doc_str_list)

    def _get_cohere_chat_history_template(
        self, chat_history: List[Dict[str, str]]
    ) -> str:
        chat_hist_str = ""
        for turn in chat_history:
            chat_hist_str += "<|START_OF_TURN_TOKEN|>"
            if turn["role"] == "user":
                chat_hist_str += "<|USER_TOKEN|>"
            elif turn["role"] == "chatbot":
                chat_hist_str += "<|CHATBOT_TOKEN|>"
            else:  # role == system
                chat_hist_str += "<|SYSTEM_TOKEN|>"
            chat_hist_str += turn["message"]
        chat_hist_str += "<|END_OF_TURN_TOKEN|>"
        return chat_hist_str


async def main():
    model = OllamaDeployment(model_path="path/to/model")

    print("--- Chat Stream ---")
    response = model.invoke_chat_stream(
        CohereChatRequest(model="llama3", message="hello world", temperature=0.3),
        ctx=None
    )
    async for item in response:
        print(item)

    print("\n--- Chat ---")
    response = await model.invoke_chat(
        CohereChatRequest(model="llama3", message="hello world", temperature=0.3),
        ctx=None
    )
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
