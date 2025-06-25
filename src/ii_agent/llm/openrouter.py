import os
import json
import random
import time
from typing import Any, Tuple, cast

import openai
from openai import (
    APIConnectionError as OpenAI_APIConnectionError,
)
from openai import (
    InternalServerError as OpenAI_InternalServerError,
)
from openai import (
    RateLimitError as OpenAI_RateLimitError,
)
from openai._types import (
    NOT_GIVEN as OpenAI_NOT_GIVEN,  # pyright: ignore[reportPrivateImportUsage]
)

from ii_agent.llm.openai import OpenAIDirectClient
from ii_agent.llm.base import (
    AssistantContentBlock,
    LLMMessages,
    ToolParam,
    TextPrompt,
    ToolCall,
    TextResult,
    ToolFormattedResult,
)
from ii_agent.llm.token_counter import TokenCounter


class OpenRouterClient(OpenAIDirectClient):
    """LLM client for OpenRouter (OpenAI-compatible API)."""

    DEEP_RESEARCH_TOKEN_THRESHOLD = 80_000

    def __init__(self, model_name: str, max_retries: int = 2, cot_model: bool = True):
        base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        api_key = os.getenv("OPENROUTER_API_KEY", "")
        headers = {
            "HTTP-Referer": os.getenv(
                "OPENROUTER_HTTP_REFERER",
                "https://github.com/IntelligentAgent/ii-agent",
            ),
            "X-Title": os.getenv("OPENROUTER_X_TITLE", "ii-agent"),
        }
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url,
            max_retries=max_retries,
            default_headers=headers,
        )
        self.model_name = model_name
        self.max_retries = max_retries
        self.cot_model = cot_model

    def generate(
        self,
        messages: LLMMessages,
        max_tokens: int,
        system_prompt: str | None = None,
        temperature: float = 0.0,
        tools: list[ToolParam] = [],
        tool_choice: dict[str, str] | None = None,
        thinking_tokens: int | None = None,
        tool_args: dict[str, Any] | None = None,
    ) -> Tuple[list[AssistantContentBlock], dict[str, Any]]:
        """Generate responses using the OpenRouter API."""

        openai_messages = []
        system_prompt_applied = False

        if system_prompt is not None:
            if not self.cot_model:
                system_message = {"role": "system", "content": system_prompt}
                openai_messages.append(system_message)
                system_prompt_applied = True

        for idx, message_list in enumerate(messages):
            if len(message_list) > 1:
                raise ValueError("Only one entry per message supported for openai")
            internal_message = message_list[0]

            current_message_text = ""
            is_user_prompt = False

            if str(type(internal_message)) == str(TextPrompt):
                internal_message = cast(TextPrompt, internal_message)
                current_message_text = internal_message.text
                is_user_prompt = True
                role = "user"
            elif str(type(internal_message)) == str(TextResult):
                internal_message = cast(TextResult, internal_message)
                message_content_obj = {"type": "text", "text": internal_message.text}
                openai_message = {"role": "assistant", "content": [message_content_obj]}
                openai_messages.append(openai_message)
                continue
            elif str(type(internal_message)) == str(ToolCall):
                internal_message = cast(ToolCall, internal_message)
                arguments_str = json.dumps(internal_message.tool_input)
                tool_call_payload = {
                    "type": "function",
                    "id": internal_message.tool_call_id,
                    "function": {
                        "name": internal_message.tool_name,
                        "arguments": arguments_str,
                    },
                }
                openai_message = {
                    "role": "assistant",
                    "tool_calls": [tool_call_payload],
                }
                openai_messages.append(openai_message)
                continue
            elif str(type(internal_message)) == str(ToolFormattedResult):
                internal_message = cast(ToolFormattedResult, internal_message)
                openai_message = {
                    "role": "tool",
                    "tool_call_id": internal_message.tool_call_id,
                    "content": internal_message.tool_output,
                }
                openai_messages.append(openai_message)
                continue
            else:
                raise ValueError(f"Unknown message type: {type(internal_message)}")

            if is_user_prompt:
                final_text = current_message_text
                if self.cot_model and system_prompt and not system_prompt_applied:
                    final_text = f"{system_prompt}\n\n{current_message_text}"
                    system_prompt_applied = True
                message_content_obj = {"type": "text", "text": final_text}
                openai_message = {"role": role, "content": [message_content_obj]}
                openai_messages.append(openai_message)

        if self.cot_model and system_prompt and not system_prompt_applied:
            openai_messages.insert(0, {"role": "user", "content": [{"type": "text", "text": system_prompt}]})

        if tool_choice is None:
            tool_choice_param = "auto" if len(tools) > 0 else OpenAI_NOT_GIVEN
        elif tool_choice["type"] == "any":
            tool_choice_param = "required"
        elif tool_choice["type"] == "auto":
            tool_choice_param = "auto"
        elif tool_choice["type"] == "tool":
            tool_choice_param = {"type": "function", "function": {"name": tool_choice["name"]}}
        else:
            raise ValueError(f"Unknown tool_choice type: {tool_choice['type']}")

        openai_tools = []
        for tool in tools:
            tool_def = {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.input_schema,
            }
            tool_def["parameters"]["strict"] = True
            openai_tool_object = {"type": "function", "function": tool_def}
            openai_tools.append(openai_tool_object)

        token_counter = TokenCounter()
        prompt_tokens = token_counter.count_tokens(openai_messages)

        force_tool_choice = False
        if (
            tool_args
            and tool_args.get("deep_research")
            and prompt_tokens > self.DEEP_RESEARCH_TOKEN_THRESHOLD
        ):
            tool_choice_param = "required"
            force_tool_choice = True

        response = None
        for retry in range(self.max_retries):
            try:
                extra_body = {}
                openai_max_tokens = max_tokens
                if self.cot_model:
                    extra_body["max_completion_tokens"] = max_tokens
                    openai_max_tokens = OpenAI_NOT_GIVEN
                if force_tool_choice:
                    extra_body["parallel_tool_calls"] = False
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=openai_messages,
                    tools=openai_tools if len(openai_tools) > 0 else OpenAI_NOT_GIVEN,
                    tool_choice=tool_choice_param,
                    max_tokens=openai_max_tokens,
                    extra_body=extra_body,
                )
                break
            except (
                OpenAI_APIConnectionError,
                OpenAI_InternalServerError,
                OpenAI_RateLimitError,
            ) as e:
                if retry == self.max_retries - 1:
                    raise e
                time.sleep(10 * random.uniform(0.8, 1.2))

        internal_messages = []
        assert response is not None
        openai_response_messages = response.choices
        if len(openai_response_messages) > 1:
            raise ValueError("Only one message supported for OpenAI")
        openai_response_message = openai_response_messages[0].message
        tool_calls = openai_response_message.tool_calls
        content = openai_response_message.content

        if tool_calls and content:
            raise ValueError("Only one of tool_calls or content should be present")
        elif not tool_calls and not content:
            raise ValueError("Either tool_calls or content should be present")

        if tool_calls:
            for tool_call_data in tool_calls:
                args_data = tool_call_data.function.arguments
                if isinstance(args_data, dict):
                    tool_input = args_data
                else:
                    tool_input = json.loads(args_data)
                internal_messages.append(
                    ToolCall(
                        tool_name=tool_call_data.function.name,
                        tool_input=tool_input,
                        tool_call_id=tool_call_data.id,
                    )
                )
                break
        elif content:
            internal_messages.append(TextResult(text=content))
        else:
            raise ValueError(f"Unknown message type: {openai_response_message}")

        assert response.usage is not None
        message_metadata = {
            "raw_response": response,
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens,
        }

        return internal_messages, message_metadata
