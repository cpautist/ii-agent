<div align="center">
  <img src="assets/ii.png" width="200"/>




# II Agent

[![GitHub stars](https://img.shields.io/github/stars/Intelligent-Internet/ii-agent?style=social)](https://github.com/Intelligent-Internet/ii-agent/stargazers)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Blog](https://img.shields.io/badge/Blog-II--Agent-blue)](https://ii.inc/web/blog/post/ii-agent)
[![GAIA Benchmark](https://img.shields.io/badge/GAIA-Benchmark-green)](https://ii-agent-gaia.ii.inc/)
</div>

II-Agent is an open-source intelligent assistant designed to streamline and enhance workflows across multiple domains. It represents a significant advancement in how we interact with technology—shifting from passive tools to intelligent systems capable of independently executing complex tasks.

## Introduction
https://github.com/user-attachments/assets/d0eb7440-a6e2-4276-865c-a1055181bb33

## Overview

II Agent is built around providing an agentic interface to Anthropic Claude models. It offers:

## Table of Contents

- [Getting Started](#getting-started)
  - [System Requirements](#system-requirements)
  - [Installation](#installation)
  - [Environment Variable Configuration](#environment-variable-configuration)
  - [Running for Development](#running-for-development)
  - [Building Frontend for Production (Optional)](#building-frontend-for-production-optional)
  - [Troubleshooting](#troubleshooting)
- [Model Configuration](#model-configuration)
  - [`agent_config.yaml`](#agent_configyaml)
  - [`MODEL_CAPABILITIES` Constant](#model_capabilities-constant)
  - [Command-Line Overrides](#command-line-overrides)
  - [Examples of Switching Models](#examples-of-switching-models)
- [API Key Management](#api-key-management)
  - [Environment Variables for API Keys](#environment-variables-for-api-keys)
  - [Security Best Practices](#security-best-practices)
- [Performance and Cost Considerations](#performance-and-cost-considerations)
  - [Performance](#performance)
  - [Cost](#cost)
  - [Context Window](#context-window)
- [Core Capabilities](#core-capabilities)
- [Methods](#methods)
- [GAIA Benchmark Evaluation](#gaia-benchmark-evaluation)
- [Original Environment and Installation (Legacy)](#original-environment-and-installation-legacy---use-make-setup-for-new-setups)
- [Usage](#usage)
  - [Command Line Interface](#command-line-interface)
  - [Web Interface (Development)](#web-interface-development)
- [Project Structure](#project-structure)
- [Conclusion](#conclusion)
- [Acknowledgement](#acknowledgement)
- [Contributing](#contributing)
  - [Reporting Bugs and Suggesting Features](#reporting-bugs-and-suggesting-features)
  - [Pull Request (PR) Process](#pull-request-pr-process)
  - [Code Style and Conventions](#code-style-and-conventions)

## Getting Started

- A CLI interface for direct command-line interaction
- A WebSocket server that powers a modern React-based frontend
- Integration with Google Cloud's Vertex AI for API access to Anthropic models

## Getting Started

This section guides you through setting up the II Agent project on your local machine using Make.

### System Requirements

Before you begin, ensure your system meets the following requirements:
- **Python**: Version 3.10 or newer (e.g., 3.10, 3.11, 3.12).
- **Node.js**: LTS versions, specifically v18.x or v20.x.
- **Yarn**: Version 1.x (Classic).
- `pip` and `venv` (typically included with Python).

You can verify these using the `make check-reqs` command after cloning the repository.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Intelligent-Internet/ii-agent.git
    ```
    (Replace with the actual repository URL if different)

2.  **Navigate to the project directory:**
    ```bash
    cd ii-agent
    ```
    (Or your chosen repository name)

3.  **Run the main setup command:**
    ```bash
    make setup
    ```
    This command performs the following steps:
    *   Checks for system requirements (`check-reqs`).
    *   Sets up the backend Python environment:
        *   Creates a virtual environment at `.venv/` if it doesn't exist.
        *   Installs backend dependencies using `pip install .`.
    *   Sets up the frontend Node.js environment:
        *   Installs frontend dependencies using `yarn install` in the `frontend/` directory.
    *   Guides you on environment file setup (`setup-env`):
        *   Copies `frontend/.env.example` to `frontend/.env.local` if it doesn't exist.
        *   Reminds you to configure `.env.production` for backend API keys.

4.  **Activate the Python virtual environment:**
    The `make setup` command (specifically the `setup-backend` part) will create a Python virtual environment. You need to activate it manually in your current shell session to use the installed backend tools and dependencies:
    ```bash
    # On Linux or macOS:
    source .venv/bin/activate

    # On Windows (Git Bash or similar):
    # source .venv/Scripts/activate
    # On Windows (Command Prompt):
    # .\.venv\Scripts\activate.bat
    # On Windows (PowerShell):
    # .\.venv\Scripts\Activate.ps1
    ```

### Environment Variable Configuration

After running `make setup`, you need to configure your environment variables. The `make setup-env` target (called by `make setup`) helps prepare the necessary files.

1.  **Backend Configuration (`.env.production`):**
    -   This file is located in the project root.
    -   If it doesn't exist, you should create it by copying the example:
        ```bash
        cp .env.production.example .env.production
        ```
    -   Edit `.env.production` to add your API keys for your chosen Large Language Model (LLM) provider.
    -   **Key variables:** `OPENROUTER_API_KEY`, `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`. Set only the one you are actively using. Refer to `.env.production.example` for more details and other potential variables like `ANTHROPIC_PROJECT_ID` if using Vertex AI.

2.  **Frontend Configuration (`frontend/.env.local`):**
    -   This file is located in the `frontend/` directory.
    -   The `make setup-env` step (part of `make setup`) should have copied `frontend/.env.example` to `frontend/.env.local` if the latter didn't exist. If not, you can do it manually:
        ```bash
        cp frontend/.env.example frontend/.env.local
        ```
    -   Edit `frontend/.env.local` and ensure the `NEXT_PUBLIC_API_URL` is correctly set to point to your backend server. For local development, this is typically:
        ```
        NEXT_PUBLIC_API_URL=http://localhost:8000
        ```

### Running for Development

Once `make setup` has been completed and your environment variables are configured, you can start both the backend and frontend development servers with a single command from the project root:

```bash
yarn dev
```

**Explanation:**
- This command uses `concurrently` (defined in the root `package.json`) to run two scripts simultaneously:
    - `yarn run dev:backend`: This executes `./run_backend.sh`, which activates the Python virtual environment (from `.venv/`) and then starts the Python backend server (`ws_server.py`).
    - `yarn run dev:frontend`: This navigates into the `frontend/` directory and starts the Next.js frontend development server (`yarn dev`).
- The backend will typically run on `http://localhost:8000` and the frontend on `http://localhost:3000`.
- Output from both the backend and frontend will be interleaved in your terminal, prefixed with `[BACKEND]` or `[FRONTEND]`.
- If one process fails, `concurrently` will attempt to kill the other, ensuring you don't have orphaned processes.

**Important:**
- Ensure you have run `make setup` at least once before using `yarn dev` to create the Python virtual environment and install all dependencies.
- The `run_backend.sh` script handles the activation of the Python virtual environment, so you do not need to manually activate it in the terminal where you run `yarn dev`. However, if you intend to run Python commands directly (e.g., `python cli.py`), you will still need to activate the environment in that specific terminal session using `source .venv/bin/activate`.

### Building Frontend for Production (Optional)

If you want to create an optimized production build of the frontend (e.g., for deployment):
```bash
make build-frontend
```
This command runs `yarn build` within the `frontend` directory. The output will be in `frontend/.next/`.

### Troubleshooting

*   **`make check-reqs` fails:** Ensure you have installed the correct versions of Python, Node.js, and Yarn, and that they are available in your system's PATH.
*   **`ensurepip` warning during backend setup:** You might see a warning like `Error: Command '['/app/.venv/bin/python3', '-m', 'ensurepip', '--upgrade', '--default-pip']' returned non-zero exit status 1.`. This is generally non-critical if the rest of the `pip install .` command succeeds and your dependencies are installed.
*   **Frontend build warnings:** During `yarn build` (or `make build-frontend`), you might see warnings like:
    *   `@next/next/no-img-element`: Suggests using Next.js's `<Image />` component for better image optimization.
    *   `react-hooks/exhaustive-deps`: Indicates potentially missing dependencies in React `useEffect` hooks.
    These are linting/best-practice warnings and typically do not prevent the application from functioning.
*   **API Key Issues**: If the agent fails to connect to LLM services, double-check that the correct API keys are in `.env.production` and that there are no typos.
*   **Frontend Connection Issues**: If the web interface loads but cannot connect to the backend, verify `NEXT_PUBLIC_API_URL` in `frontend/.env.local` is correct and that the backend server (`ws_server.py`) is running.

## Model Configuration

Configuring the desired Large Language Model (LLM) is a key part of using II Agent. You can control the model, its provider, and specific options through `agent_config.yaml` and command-line arguments.

### `agent_config.yaml`

The primary way to set default model configurations is through the `agent_config.yaml` file in the project root. If this file doesn't exist, you can copy `agent_config.yaml.example` to create it.

Key settings in `agent_config.yaml`:

*   **`llm_client`**: Specifies the LLM backend to use.
    *   Examples: `"anthropic-direct"`, `"openai-direct"`, `"openrouter-direct"`.
    *   If commented out or not provided, the client might be inferred from `model_name` using the `MODEL_CAPABILITIES` map.
*   **`model_name`**: The exact model identifier string for the chosen client.
    *   Examples: `"anthropic/claude-3.5-sonnet-20240620"`, `"openai/gpt-4o"`, `"deepseek/deepseek-r1-0528:free"`.
*   **`provider_options`**: A dictionary to pass provider-specific settings to the LLM client during initialization.
    *   **For `anthropic-direct`**:
        ```yaml
        provider_options:
          anthropic-direct:
            thinking_tokens: 2048  # For "thinking" prompts
            # project_id: "your-gcp-project-id"  # If using Vertex AI
            # region: "your-gcp-region"          # If using Vertex AI
            # anthropic_api_key: "sk-ant-..."    # Direct Anthropic API key (can also be env var)
            # temperature: 0.8
        ```
    *   **For `openai-direct`**:
        ```yaml
        provider_options:
          openai-direct:
            # api_key: "sk-..."               # OpenAI API key (can also be env var)
            # base_url: "your_custom_openai_compatible_url" # For custom endpoints
            # temperature: 0.7
        ```
    *   **For `openrouter-direct`**:
        ```yaml
        provider_options:
          openrouter-direct:
            # openrouter_api_key: "sk-or-..." # OpenRouter API key (can also be env var)
            # default_headers:
            #   X-My-Custom-Header: "value"
            # route_preference: "performance"
            # fallback_models:
            #   - openai/o3
            #   - anthropic/claude-3.7-sonnet:beta
        ```

### `MODEL_CAPABILITIES` Constant

The file `src/ii_agent/utils/constants.py` defines a dictionary named `MODEL_CAPABILITIES`. This map contains metadata for various models, including:
*   `"provider"`: The default `llm_client` for that model.
*   `"supports_tools"`: A boolean indicating if the model generally supports tool usage. (Note: Actual tool performance can vary.)
*   `"context_window"`: An integer representing the approximate context window size in tokens.

This map is used by the system to:
*   Infer the `llm_client` if it's not explicitly set in `agent_config.yaml` or via CLI.
*   Potentially inform agent behavior based on model features (though this is more for future enhancements).

### Command-Line Overrides

You can override configurations from `agent_config.yaml` using command-line arguments when running `cli.py` or `ws_server.py` (which affects `yarn dev`):

*   `--llm-client <client_name>`: Overrides the `llm_client`.
    *   Example: `python cli.py --llm-client openai-direct`
*   `--model-name <model_identifier>`: Overrides the `model_name`.
    *   Example: `python cli.py --model-name openai/gpt-4o`
*   Specific Provider Option Overrides: Some provider options can also be overridden via dedicated CLI arguments.
    *   Example: `python cli.py --llm-client anthropic-direct --anthropic-thinking-tokens 1024` (overrides `thinking_tokens` for Anthropic).

### Examples of Switching Models

Here are a few examples of how to configure `agent_config.yaml` for different models/providers:

1.  **Using a specific OpenRouter model (e.g., Mistral Large 2 via OpenRouter):**
    ```yaml
    llm_client: openrouter-direct
    model_name: "mistralai/mistral-large-2" # Check OpenRouter for exact model string
    # provider_options:
    #   openrouter-direct:
    #     # Add any OpenRouter specific options here if needed
    ```

2.  **Using Anthropic direct (e.g., Claude 3.5 Sonnet):**
    ```yaml
    llm_client: anthropic-direct
    model_name: "claude-3.5-sonnet-20240620" # Use the official Anthropic model ID
    provider_options:
      anthropic-direct:
        thinking_tokens: 1024 # Optional: Adjust thinking tokens
        # Ensure ANTHROPIC_API_KEY is set in .env.production or provide it here:
        # anthropic_api_key: "sk-ant-..."
    ```

3.  **Using OpenAI direct (e.g., GPT-4o):**
    ```yaml
    llm_client: openai-direct
    model_name: "gpt-4o" # Use the official OpenAI model ID
    # provider_options:
    #   openai-direct:
    #     # Ensure OPENAI_API_KEY is set in .env.production or provide it here:
    #     # api_key: "sk-..."
    ```

Remember to set the corresponding API key in your `.env.production` file for the chosen provider.

## API Key Management

Securely managing API keys is essential when working with LLM providers, as these keys grant access to paid services.

### Environment Variables for API Keys

II Agent primarily uses environment variables for API key configuration. These should be set in a file named `.env.production` located in the project root. This file is specifically for backend configurations, including API keys.

Key environment variables for API providers:
*   `OPENROUTER_API_KEY`: For accessing models via OpenRouter.
*   `ANTHROPIC_API_KEY`: For accessing Anthropic models directly (not via Vertex AI).
*   `OPENAI_API_KEY`: For accessing OpenAI models directly.
*   `GOOGLE_APPLICATION_CREDENTIALS`: Path to your Google Cloud service account JSON file (if using Anthropic or other services via Vertex AI).

**Example `.env.production` content:**
```bash
# .env.production - Store your backend API keys here
# Set only the keys for the providers you are actively using.

# For OpenRouter
OPENROUTER_API_KEY=your_openrouter_api_key_here

# For direct Anthropic API
# ANTHROPIC_API_KEY=your_anthropic_api_key_here

# For direct OpenAI API
# OPENAI_API_KEY=your_openai_api_key_here

# For Google Cloud (e.g., Anthropic on Vertex AI)
# GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/gcp-service-account-key.json
# ANTHROPIC_PROJECT_ID=your_gcp_project_id_here # Also needed if using Vertex AI
# ANTHROPIC_REGION=your_gcp_region_here       # Also needed if using Vertex AI
```
Refer to `.env.production.example` for a template.

### Security Best Practices

*   **Never commit API keys to Git:** Ensure that `.env.production` (or any file containing live API keys) is listed in your `.gitignore` file. The project's `.gitignore` should already include `*.env.*` and `.env.production`.
*   **Do not share API keys publicly:** Avoid pasting them into issues, forums, or public code repositories.
*   **Principle of Least Privilege:** If your API provider allows, create API keys with the minimum necessary permissions for the agent's tasks. For example, restrict access to only the models you intend to use.
*   **Regularly review usage:** Monitor your API usage through your provider's dashboard to detect any unauthorized activity.
*   **Use environment variables for deployment:** When deploying the agent, use your hosting platform's mechanisms for setting environment variables securely. Do not hardcode keys into deployed code.

By following these practices, you can help protect your API keys and manage your LLM service costs effectively.

## Performance and Cost Considerations

When using LLM-based agents, it's important to consider both performance and cost implications.

### Performance

*   **Model Latency:** Different models have varying response times (latency). Larger, more complex models might be slower than smaller, faster ones. The choice of model can significantly impact the perceived speed of the agent.
*   **Model Size and Capabilities:** Larger models often (but not always) offer better reasoning capabilities and can handle more complex instructions. However, they might also have higher latency and cost.
*   **OpenRouter:** Services like OpenRouter can provide access to a variety of models from different providers. OpenRouter itself might add a small amount of latency, but it also offers features like fallback models or trying to find the "fastest" available model for a given class, which can be beneficial.
*   **Network Conditions:** Your network connection to the API provider will also affect response times.

### Cost

*   **API Usage is Typically Paid:** Most high-quality LLM providers charge based on the number of input and output tokens (pieces of words) processed by the model. Costs can vary significantly between models and providers.
*   **Monitor Your Usage:** Be sure to understand the pricing model of your chosen LLM provider(s) and monitor your usage regularly through their dashboards to avoid unexpected charges.
*   **Token Consumption:**
    *   **Input Tokens:** Include the system prompt, the conversation history, any tool definitions provided, and your current instruction.
    *   **Output Tokens:** Include the model's generated response, including any text, tool calls, or "thinking" steps.
    *   Longer conversations, verbose tool outputs, and complex instructions will consume more tokens and thus incur higher costs.
*   **Free Tiers/Credits:** Some providers offer free tiers or introductory credits, which can be useful for experimentation, but be mindful of their limits.

### Context Window

*   **Definition:** The context window of an LLM is the maximum number of tokens it can consider when generating a response. This includes both input (prompts, history) and output.
*   **Relevance:**
    *   A larger context window allows the model to "remember" more of the conversation history and consider more information from provided documents or tool outputs.
    *   Exceeding the context window can lead to errors or the model "forgetting" earlier parts of the conversation.
*   **`MODEL_CAPABILITIES`:** The `MODEL_CAPABILITIES` dictionary in `src/ii_agent/utils/constants.py` lists approximate context window sizes for various models. This can help you choose a model appropriate for your task's complexity and information density.
*   **Context Management:** The agent employs context management strategies (like truncating history) to try and stay within the model's limit, but very long interactions or extremely large inputs can still pose challenges.

Choosing the right model involves balancing performance, cost, and the specific capabilities required for your tasks. Experimentation and careful monitoring are key.

## Core Capabilities

II-Agent is a versatile open-source assistant built to elevate your productivity across domains:

| Domain | What II‑Agent Can Do |
|--------|----------------------|
| Research & Fact‑Checking | Multistep web search, source triangulation, structured note‑taking, rapid summarization |
| Content Generation | Blog & article drafts, lesson plans, creative prose, technical manuals, Website creations |
| Data Analysis & Visualization | Cleaning, statistics, trend detection, charting, and automated report generation |
| Software Development | Code synthesis, refactoring, debugging, test‑writing, and step‑by‑step tutorials across multiple languages |
| Workflow Automation | Script generation, browser automation, file management, process optimization |
| Problem Solving | Decomposition, alternative‑path exploration, stepwise guidance, troubleshooting |

## Methods

The II-Agent system represents a sophisticated approach to building versatile AI agents. Our methodology centers on:

1. **Core Agent Architecture and LLM Interaction**
   - System prompting with dynamically tailored context
   - Comprehensive interaction history management
   - Intelligent context management to handle token limitations
   - Systematic LLM invocation and capability selection
   - Iterative refinement through execution cycles

2. **Planning and Reflection**
   - Structured reasoning for complex problem-solving
   - Problem decomposition and sequential thinking
   - Transparent decision-making process
   - Hypothesis formation and testing

3. **Execution Capabilities**
   - File system operations with intelligent code editing
   - Command line execution in a secure environment
   - Advanced web interaction and browser automation
   - Task finalization and reporting
   - Specialized capabilities for various modalities (Experimental) (PDF, audio, image, video, slides)
   - Deep research integration

4. **Context Management**
   - Token usage estimation and optimization
   - Strategic truncation for lengthy interactions
   - File-based archival for large outputs

5. **Real-time Communication**
   - WebSocket-based interface for interactive use
   - Isolated agent instances per client
   - Streaming operational events for responsive UX

## GAIA Benchmark Evaluation

II-Agent has been evaluated on the GAIA benchmark, which assesses LLM-based agents operating within realistic scenarios across multiple dimensions including multimodal processing, tool utilization, and web searching.

We identified several issues with the GAIA benchmark during our evaluation:

- **Annotation Errors**: Several incorrect annotations in the dataset (e.g., misinterpreting date ranges, calculation errors)
- **Outdated Information**: Some questions reference websites or content no longer accessible
- **Language Ambiguity**: Unclear phrasing leading to different interpretations of questions

Despite these challenges, II-Agent demonstrated strong performance on the benchmark, particularly in areas requiring complex reasoning, tool use, and multi-step planning.

![GAIA Benchmark](assets/gaia.jpg)
You can view the full traces of some samples here: [GAIA Benchmark Traces](https://ii-agent-gaia.ii.inc/)

## Original Environment and Installation (Legacy - use `make setup` for new setups)

The following sections describe the original environment setup. For new installations, please use the `make setup` command as described in the "Getting Started" section.

### Environment Variables (Legacy)

Create a `.env` file in the root directory with the following variables:
(Note: The new `.env.production.example` and `make setup-env` target provide more current guidance.)
```bash
# Image and Video Generation Tool
OPENAI_API_KEY=your_openai_key
OPENAI_AZURE_ENDPOINT=your_azure_endpoint
# Search Provider
TAVILY_API_KEY=your_tavily_key
#JINA_API_KEY=your_jina_key
#FIRECRAWL_API_KEY=your_firecrawl_key
# For Image Search and better search results use SerpAPI
#SERPAPI_API_KEY=your_serpapi_key 

STATIC_FILE_BASE_URL=http://localhost:8000/

#If you are using Anthropic client
ANTHROPIC_API_KEY=
#If you are using Goolge Vertex (recommended if you have permission extra throughput)
#GOOGLE_APPLICATION_CREDENTIALS=
#If you are using OpenRouter
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

### Frontend Environment Variables (Legacy)

For the frontend, create a `.env` file in the frontend directory:
(Note: The `frontend/.env.example` and `make setup-env` target provide more current guidance.)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Agent Configuration

Create an `agent_config.yaml` file in the project root to customize the
default model and LLM backend. If present, these settings will be used
when running `cli.py` or `ws_server.py` without specifying the
`--llm-client` or `--model-name` arguments. If you omit `llm_client`,
the backend will be inferred from the model using the
`MODEL_TO_PROVIDER_MAP` constant. This same inference also applies when
providing `--model-name` on the command line without `--llm-client`.

```yaml
llm_client: openrouter-direct
model_name: deepseek/deepseek-r1-0528:free
```

The model name will determine the provider when `llm_client` is not
specified.

### Installation (Legacy)

(Superseded by `make setup`)
1. Clone the repository
2. Set up Python environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   ```

3. Set up frontend (optional):
   ```bash
   cd frontend
   npm install  # Or yarn install if you prefer and have yarn.lock
   ```

## Usage

This section describes how to use the different parts of the II Agent. For local development of the web interface, refer to the "Running the Application for Development" section above.

### Command Line Interface

Ensure your Python virtual environment is activated (`source .venv/bin/activate` or `.\.venv\Scripts\activate`).

If you want to use anthropic client, set `ANTHROPIC_API_KEY` in `.env.production` and run:
```bash
# Activate virtual environment if not already: source .venv/bin/activate
python cli.py 
```

If you want to use vertex, set `GOOGLE_APPLICATION_CREDENTIALS` (or ensure ADC is configured) in `.env.production` and run:
```bash
# Activate virtual environment if not already: source .venv/bin/activate
python cli.py --project-id YOUR_PROJECT_ID --region YOUR_REGION
```

If you want to use OpenRouter, set `OPENROUTER_API_KEY` in `.env.production` and run:
```bash
# Activate virtual environment if not already: source .venv/bin/activate
python cli.py --llm-client openrouter-direct --model-name <MODEL_NAME>
```

Options:
- `--project-id`: Google Cloud project ID
- `--region`: Google Cloud region (e.g., us-east5)
- `--workspace`: Path to the workspace directory (default: ./workspace)
- `--needs-permission`: Require permission before executing commands
- `--minimize-stdout-logs`: Reduce the amount of logs printed to stdout
- `--model-name`: Model to use with the selected backend

### Web Interface (Development)

For local development, the recommended way to run the web interface (backend server + frontend dev server) is using the unified command:
```bash
# Ensure Python virtual environment is activated
# source .venv/bin/activate (Linux/macOS)
# .\.venv\Scripts\activate (Windows)

yarn dev
```
This will start the backend on `http://localhost:8000` and the frontend on `http://localhost:3000`. Open `http://localhost:3000` in your browser.

(For production deployments or running components separately, see original individual component start instructions if needed, but `yarn dev` is preferred for typical development workflows.)

## Project Structure

- `cli.py`: Command-line interface
- `ws_server.py`: WebSocket server for the frontend
- `src/ii_agent/`: Core agent implementation
  - `agents/`: Agent implementations
  - `llm/`: LLM client interfaces
  - `tools/`: Tool implementations
  - `utils/`: Utility functions

## Conclusion

The II-Agent framework, architected around the reasoning capabilities of large language models like Claude 3.7 Sonnet, presents a comprehensive and robust methodology for building versatile AI agents. Through its synergistic combination of a powerful LLM, a rich set of execution capabilities, an explicit mechanism for planning and reflection, and intelligent context management strategies, II-Agent is well-equipped to address a wide spectrum of complex, multi-step tasks. Its open-source nature and extensible design provide a strong foundation for continued research and development in the rapidly evolving field of agentic AI.

## Acknowledgement

We would like to express our sincere gratitude to the following projects and individuals for their invaluable contributions that have helped shape this project:

- **AugmentCode**: We have incorporated and adapted several key components from the [AugmentCode project](https://github.com/augmentcode/augment-swebench-agent). AugmentCode focuses on SWE-bench, a benchmark that tests AI systems on real-world software engineering tasks from GitHub issues in popular open-source projects. Their system provides tools for bash command execution, file operations, and sequential problem-solving capabilities designed specifically for software engineering tasks.

- **Manus**: Our system prompt architecture draws inspiration from Manus's work, which has helped us create more effective and contextually aware AI interactions.

- **Index Browser Use**: We have built upon and extended the functionality of the [Index Browser Use project](https://github.com/lmnr-ai/index/tree/main), particularly in our web interaction and browsing capabilities. Their foundational work has enabled us to create more sophisticated web-based agent behaviors.

We are committed to open source collaboration and believe in acknowledging the work that has helped us build this project. If you feel your work has been used in this project but hasn't been properly acknowledged, please reach out to us.

## Contributing

We welcome contributions to II Agent! Whether you're fixing a bug, proposing a new feature, or improving documentation, your help is appreciated. Please follow these guidelines to make the contribution process smooth.

### Reporting Bugs and Suggesting Features

*   **Bugs:** If you find a bug, please open an issue on GitHub. Include as much detail as possible:
    *   Steps to reproduce the bug.
    *   Expected behavior.
    *   Actual behavior.
    *   Your system setup (OS, Python version, Node.js version, relevant package versions).
    *   Any relevant logs or screenshots.
*   **Features:** If you have an idea for a new feature or an enhancement to an existing one, please open an issue to discuss it first. This allows us to align on the scope and design before development work begins.

### Pull Request (PR) Process

1.  **Fork the Repository:** Create your own fork of the `Intelligent-Internet/ii-agent` repository on GitHub.
2.  **Create a Branch:** Create a new branch in your fork for your changes. Choose a descriptive branch name (e.g., `fix/login-bug`, `feature/new-tool-integration`).
    ```bash
    git checkout -b feature/my-new-feature
    ```
3.  **Make Your Changes:** Implement your fix or feature.
    *   Write clear, concise, and well-commented code.
    *   Follow the existing code style and conventions.
4.  **Run Linters and Formatters (Pre-commit Hooks):**
    This project uses pre-commit hooks to ensure code quality and consistency. Please install and set them up in your local environment:
    ```bash
    # Install pre-commit if you haven't already
    # pip install pre-commit

    # Set up the git hook scripts
    pre-commit install
    ```
    Before committing, the hooks defined in `.pre-commit-config.yaml` (e.g., black, ruff, mypy) will run automatically. Ensure all checks pass. You can also run them manually on all files:
    ```bash
    pre-commit run --all-files
    ```
5.  **Test Your Changes:** (If applicable) Add unit tests or integration tests for your changes. Ensure all existing and new tests pass.
6.  **Commit Your Changes:** Use clear and descriptive commit messages.
    ```bash
    git add .
    git commit -m "feat: Add support for X feature"
    ```
7.  **Push to Your Fork:**
    ```bash
    git push origin feature/my-new-feature
    ```
8.  **Submit a Pull Request:** Open a pull request from your branch to the `main` branch (or relevant development branch) of the `Intelligent-Internet/ii-agent` repository.
    *   Provide a clear title and description for your PR.
    *   Explain the changes you've made and why.
    *   Reference any related GitHub issues (e.g., "Fixes #123").
9.  **Address Feedback:** Be prepared to address any feedback or requested changes from the maintainers.

### Code Style and Conventions

*   Follow PEP 8 for Python code.
*   Use type hints for Python code.
*   Maintain consistency with the existing codebase.

Thank you for contributing to II Agent!
