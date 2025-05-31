from argparse import ArgumentParser
import uuid
from pathlib import Path
import yaml
from ii_agent.utils import WorkspaceManager
from ii_agent.utils.constants import DEFAULT_MODEL, MODEL_CAPABILITIES


def _infer_llm_client(model_name: str) -> str | None:
    """Infer the LLM client from the model name using ``MODEL_CAPABILITIES``."""
    model_info = MODEL_CAPABILITIES.get(model_name, {})
    return model_info.get("provider")


def parse_common_args(parser: ArgumentParser):
    config = {}
    config_path = Path(__file__).resolve().parent / "agent_config.yaml"
    if config_path.exists():
        with open(config_path, "r") as f:
            config = yaml.safe_load(f) or {}

    # Determine defaults for model and client. If the client is not
    # specified in the configuration, infer it from the model name using
    # ``MODEL_TO_PROVIDER_MAP``.
    model_default = config.get("model_name", DEFAULT_MODEL)
    client_default = config.get("llm_client") or None

    parser.add_argument(
        "--workspace",
        type=str,
        default="./workspace",
        help="Path to the workspace",
    )
    parser.add_argument(
        "--logs-path",
        type=str,
        default="agent_logs.txt",
        help="Path to save logs",
    )
    parser.add_argument(
        "--needs-permission",
        "-p",
        help="Ask for permission before executing commands",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--use-container-workspace",
        type=str,
        default=None,
        help="(Optional) Path to the container workspace to run commands in.",
    )
    parser.add_argument(
        "--docker-container-id",
        type=str,
        default=None,
        help="(Optional) Docker container ID to run commands in.",
    )
    parser.add_argument(
        "--minimize-stdout-logs",
        help="Minimize the amount of logs printed to stdout.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--project-id",
        type=str,
        default=None,
        help="Project ID to use for Anthropic",
    )
    parser.add_argument(
        "--region",
        type=str,
        default=None,
        help="Region to use for Anthropic",
    )
    parser.add_argument(
        "--llm-client",
        type=str,
        default=client_default,
        choices=["anthropic-direct", "openai-direct", "openrouter-direct"],
        help="LLM backend to use",
    )
    parser.add_argument(
        "--model-name",
        type=str,
        default=model_default,
        help="Model name to use with the selected backend",
    )
    parser.add_argument(
        "--context-manager",
        type=str,
        default="file-based",
        choices=["file-based", "standard"],
        help="Type of context manager to use (file-based or standard)",
    )
    # Example for CLI override of a provider option
    parser.add_argument(
        "--anthropic-thinking-tokens",
        type=int,
        default=None,
        help="Specific provider option: thinking_tokens for Anthropic client."
    )

    original_parse_args = parser.parse_args

    def _parse_args(*pargs, **kwargs):
        args = original_parse_args(*pargs, **kwargs)
        if args.llm_client is None:
            inferred_client = _infer_llm_client(args.model_name)
            if inferred_client:
                args.llm_client = inferred_client
            else:
                # Default to openrouter if model not in MODEL_CAPABILITIES or provider not specified
                print(f"Warning: Could not infer LLM client for model '{args.model_name}'. Defaulting to 'openrouter-direct'.")
                args.llm_client = "openrouter-direct"

        # Load provider_options from agent_config.yaml
        loaded_provider_options = config.get("provider_options", {})
        args.provider_options = loaded_provider_options.get(args.llm_client, {})

        # Allow CLI overrides for specific provider options
        if args.llm_client == 'anthropic-direct' and args.anthropic_thinking_tokens is not None:
            args.provider_options['thinking_tokens'] = args.anthropic_thinking_tokens

        return args

    parser.parse_args = _parse_args  # type: ignore[assignment]

    return parser


def create_workspace_manager_for_connection(
    workspace_root: str, use_container_workspace: bool = False
):
    """Create a new workspace manager instance for a websocket connection."""
    # Create unique subdirectory for this connection
    connection_id = str(uuid.uuid4())
    workspace_path = Path(workspace_root).resolve()
    connection_workspace = workspace_path / connection_id
    connection_workspace.mkdir(parents=True, exist_ok=True)

    # Initialize workspace manager with connection-specific subdirectory
    workspace_manager = WorkspaceManager(
        root=connection_workspace,
        container_workspace=use_container_workspace,
    )

    return workspace_manager, connection_id
