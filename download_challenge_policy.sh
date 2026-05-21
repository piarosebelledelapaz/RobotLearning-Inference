#!/usr/bin/env bash
set -euo pipefail

# Run from the repository root, even when this script is launched elsewhere.
cd "$(dirname "$0")"

REPO_ID="${REPO_ID:-piarosebelledelapaz/multitask-dit-so101-mixed}"
REVISION="${REVISION:-main}"
CHECKPOINT_STEP="${CHECKPOINT_STEP:-010000}"
POLICY_DIR="${POLICY_DIR:-artifacts/policies/mixed_010000}"
POLICY_PATH="${POLICY_PATH:-${POLICY_DIR}/checkpoints/${CHECKPOINT_STEP}/pretrained_model}"

if ! command -v huggingface-cli >/dev/null 2>&1; then
  python -m pip install -U huggingface_hub
fi

huggingface-cli download "$REPO_ID" \
  --repo-type model \
  --revision "$REVISION" \
  --include "checkpoints/${CHECKPOINT_STEP}/pretrained_model/*" \
  --local-dir "$POLICY_DIR"

if [ ! -d "$POLICY_PATH" ]; then
  echo "Expected policy path was not created: $POLICY_PATH" >&2
  exit 1
fi

printf "\nDownloaded challenge policy to:\n  %s\n" "$POLICY_PATH"
printf "\nRun inference with:\n  POLICY_PATH=%q bash run_eval_towel_folding.sh\n" "$POLICY_PATH"
