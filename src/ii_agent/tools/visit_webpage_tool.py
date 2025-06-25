from ii_agent.tools.base import (
    LLMTool,
    ToolImplOutput,
)
from typing import Any, Optional
import asyncio
import uuid

from ii_agent.core.event import EventType, RealtimeEvent
from ii_agent.tools.message_tool import MessageTool
from ii_agent.llm.message_history import MessageHistory
from ii_agent.tools.visit_webpage_client import (
    create_visit_client,
    WebpageVisitException,
    ContentExtractionError,
    NetworkError,
)
from ii_agent.utils.constants import VISIT_WEB_PAGE_MAX_OUTPUT_LENGTH


class VisitWebpageTool(LLMTool):
    name = "visit_webpage"
    description = "You should call this tool when you need to visit a webpage and extract its content. Returns webpage content as text."
    input_schema = {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "The url of the webpage to visit.",
            }
        },
        "required": ["url"],
    }
    output_type = "string"

    def __init__(
        self,
        max_output_length: int = VISIT_WEB_PAGE_MAX_OUTPUT_LENGTH,
        message_queue: asyncio.Queue | None = None,
    ):
        self.max_output_length = max_output_length
        self.visit_client = create_visit_client(max_output_length=max_output_length)
        self.message_queue = message_queue

    def _send_progress(self, text: str) -> None:
        """Send a progress update via the message queue."""
        if self.message_queue is None:
            return
        call_id = str(uuid.uuid4())
        self.message_queue.put_nowait(
            RealtimeEvent(
                type=EventType.TOOL_CALL,
                content={
                    "tool_call_id": call_id,
                    "tool_name": MessageTool.name,
                    "tool_input": {"text": text},
                },
            )
        )
        self.message_queue.put_nowait(
            RealtimeEvent(
                type=EventType.TOOL_RESULT,
                content={
                    "tool_call_id": call_id,
                    "tool_name": MessageTool.name,
                    "result": text,
                },
            )
        )

    async def _progress_loop(self, url: str) -> None:
        """Periodically notify the user that a URL is being fetched."""
        elapsed = 0
        try:
            while True:
                await asyncio.sleep(5)
                elapsed += 5
                self._send_progress(f"Fetching {url}... {elapsed}s elapsed")
        except asyncio.CancelledError:
            pass

    async def run_impl(
        self,
        tool_input: dict[str, Any],
        message_history: Optional[MessageHistory] = None,
    ) -> ToolImplOutput:
        url = tool_input["url"]
        if "arxiv.org/abs" in url:
            url = "https://arxiv.org/html/" + url.split("/")[-1]

        # Notify user and start progress updates
        self._send_progress(f"Starting fetch for {url}")
        progress_task = asyncio.create_task(self._progress_loop(url))

        try:
            output = await self.visit_client.forward_async(url)
            self._send_progress(f"Completed fetch for {url}")
            return ToolImplOutput(
                output,
                f"Webpage {url} successfully visited using {self.visit_client.name}",
                auxiliary_data={"success": True},
            )

        except ContentExtractionError:
            error_msg = f"Failed to extract content from {url} using {self.visit_client.name} tool. Please visit the webpage in a browser to manually verify the content or confirm that none is available."
            return ToolImplOutput(
                error_msg,
                f"Failed to extract content from {url}",
                auxiliary_data={"success": False},
            )

        except NetworkError:
            error_msg = f"Failed to access {url} using {self.visit_client.name} tool. Please check if the URL is correct and accessible from your browser."
            return ToolImplOutput(
                error_msg,
                f"Failed to access {url} due to network error",
                auxiliary_data={"success": False},
            )

        except WebpageVisitException:
            error_msg = f"Failed to visit {url} using {self.visit_client.name} tool. Please visit the webpage in a browser to manually verify the content."
            return ToolImplOutput(
                error_msg,
                f"Failed to visit {url}",
                auxiliary_data={"success": False},
            )
        finally:
            progress_task.cancel()
