import argparse
import logging
import uvicorn
import os

from ii_agent.server.app import create_app
from utils import parse_common_args

# Ensure INFO-level log output is visible on the console
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

logger = logging.getLogger(__name__)


def main():
    """Main entry point for the WebSocket server."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="WebSocket Server for interacting with the Agent"
    )
    parser = parse_common_args(parser)
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to run the server on",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run the server on",
    )
    args = parser.parse_args()

    # Build client-specific kwargs for default settings
    client_kwargs = {
        "model_name": args.model_name,
    }
    if args.llm_client == "anthropic-direct":
        client_kwargs["use_caching"] = False
        client_kwargs["project_id"] = args.project_id
        client_kwargs["region"] = args.region
    elif args.llm_client == "openai-direct":
        client_kwargs["azure_model"] = args.azure_model
        client_kwargs["cot_model"] = args.cot_model
    elif args.llm_client == "openrouter-direct":
        client_kwargs["cot_model"] = args.cot_model

    # Echo presence of optional API keys
    for var in ("TAVILY_API_KEY", "GOOGLE_API_KEY"):
        logger.info("%s=%s", var, "SET" if os.getenv(var) else "NOT SET")

    # Create the FastAPI app
    app = create_app(args, client_kwargs)

    # Start the FastAPI server
    logger.info(f"Starting WebSocket server on {args.host}:{args.port}")
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
