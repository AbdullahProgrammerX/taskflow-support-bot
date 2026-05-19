from openai import OpenAI

from src.config import settings

DEFAULT_SYSTEM_PROMPT = (
    "You are a helpful support assistant. "
    "Answer clearly and concisely in the same language as the user."
)


def get_client() -> OpenAI:
    if not settings.api_key_configured:
        raise ValueError(
            "OPENAI_API_KEY is not set. Copy .env.example to .env and add your key."
        )
    return OpenAI(api_key=settings.openai_api_key)


def chat(message: str, system_prompt: str | None = None) -> tuple[str, str]:
    """Send a user message to the chat model. Returns (answer, model_name)."""
    messages: list[dict[str, str]] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    else:
        messages.append({"role": "system", "content": DEFAULT_SYSTEM_PROMPT})
    messages.append({"role": "user", "content": message})
    return chat_messages(messages)


def chat_messages(messages: list[dict[str, str]]) -> tuple[str, str]:
    """Send a full message list to the chat model. Returns (answer, model_name)."""
    client = get_client()
    response = client.chat.completions.create(
        model=settings.openai_chat_model,
        messages=messages,
    )
    answer = response.choices[0].message.content or ""
    return answer, settings.openai_chat_model
