from ii_agent.llm.base import LLMClient
from ii_agent.llm import get_client


class ClientFactory:
    """Factory for creating LLM clients based on model configuration."""

    def __init__(self, project_id: str = None, region: str = None):
        """Initialize the client factory with configuration.

        Args:
            project_id: Project ID for cloud services
            region: Region for cloud services
        """
        self.project_id = project_id
        self.region = region

    def create_client(self, model_name: str, **kwargs) -> LLMClient:
        """Create an LLM client based on the model name and configuration.

        Args:
            model_name: The name of the model to use
            **kwargs: Additional configuration options like thinking_tokens

        Returns:
            LLMClient: Configured LLM client instance

        """
        cleaned_name = model_name
        if model_name.startswith("openrouter/"):
            cleaned_name = model_name[len("openrouter/") :]
        elif model_name.startswith("or:"):
            cleaned_name = model_name[len("or:") :]

        try:
            return get_client(
                "openrouter",
                model_name=cleaned_name,
            )
        except Exception as exc:
            raise ValueError(
                f"Failed to instantiate OpenRouter client for model '{model_name}': {exc}"
            ) from exc
