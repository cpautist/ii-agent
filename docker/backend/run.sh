LLM_CLIENT="${LLM_CLIENT:-anthropic-direct}"
MODEL_NAME="${MODEL_NAME:-claude-sonnet-4@20250514}"

if [ -n "$PROJECT_ID" ] && [ -n "$REGION" ]; then
  echo "Using Vertex Client"
  echo "PROJECT_ID: $PROJECT_ID"
  echo "REGION: $REGION"
  exec xvfb-run --auto-servernum python ws_server.py \
    --project-id "$PROJECT_ID" \
    --region "$REGION" \
    --llm-client "$LLM_CLIENT" \
    --model-name "$MODEL_NAME"
else
  echo "Using Anthropic Client, reading ANTHROPIC_API_KEY from .env"
  exec xvfb-run --auto-servernum python ws_server.py \
    --llm-client "$LLM_CLIENT" \
    --model-name "$MODEL_NAME"
fi
