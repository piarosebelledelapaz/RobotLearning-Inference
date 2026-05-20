#!/usr/bin/env bash
set -euo pipefail

# Run from the repository root, even when this script is launched elsewhere.
cd "$(dirname "$0")"

ENV_NAME="${ENV_NAME:-robotlearning-inference}"
ROBOT_PORT="${ROBOT_PORT:-/dev/ttyACM0}"
ROBOT_ID="${ROBOT_ID:-robot_learning_follower}"
CAMERA_INDEX="${CAMERA_INDEX:-0}"
CAMERA_FPS="${CAMERA_FPS:-20}"
POLICY_DEVICE="${POLICY_DEVICE:-cuda}"
DATASET_VCODEC="${DATASET_VCODEC:-h264_nvenc}"
POLICY_PATH="${POLICY_PATH:-artifacts/policies/clippatch16_batch32/checkpoints/030000/pretrained_model}"
NUM_ROLLOUTS="${NUM_ROLLOUTS:-5}"
START_POSE_PATH="${START_POSE_PATH:-fixed_start_pose.json}"
START_DURATION_S="${START_DURATION_S:-3.0}"
DISPLAY_DATA="${DISPLAY_DATA:-true}"
TASK_NAME="${TASK_NAME:-Towel folding}"
DATASET_PREFIX="${DATASET_PREFIX:-eval_towel_folding}"
EPISODE_TIME_S="${EPISODE_TIME_S:-15}"

if ! command -v conda >/dev/null 2>&1; then
  echo "conda was not found on PATH. Install Miniconda/Anaconda first." >&2
  exit 1
fi

if ! conda env list | awk '{print $1}' | grep -qx "$ENV_NAME"; then
  conda env create -f environment.yml
else
  conda env update -n "$ENV_NAME" -f environment.yml --prune
fi

eval "$(conda shell.bash hook)"
conda activate "$ENV_NAME"

policy_extra_args=()
if [ -n "$EPISODE_TIME_S" ]; then
  policy_extra_args+=(--episode-time-s "$EPISODE_TIME_S")
fi

for rollout in $(seq 1 "$NUM_ROLLOUTS"); do
  printf "\n=== Rollout %s/%s: moving to start pose ===\n" "$rollout" "$NUM_ROLLOUTS"
  python move_to_start_pose.py \
    --port "$ROBOT_PORT" \
    --id "$ROBOT_ID" \
    --pose-path "$START_POSE_PATH" \
    --duration-s "$START_DURATION_S"

  printf "\n=== Rollout %s/%s: running policy ===\n" "$rollout" "$NUM_ROLLOUTS"
  python test_policy.py \
    --robot-port "$ROBOT_PORT" \
    --robot-id "$ROBOT_ID" \
    --camera-index "$CAMERA_INDEX" \
    --camera-fps "$CAMERA_FPS" \
    --policy-path "$POLICY_PATH" \
    --device "$POLICY_DEVICE" \
    --vcodec "$DATASET_VCODEC" \
    --display-data "$DISPLAY_DATA" \
    --task-name "$TASK_NAME" \
    --dataset-name "${DATASET_PREFIX}_rollout_${rollout}" \
    --num-episodes 1 \
    "${policy_extra_args[@]}"

  printf "\n=== Rollout %s/%s: finished ===\n" "$rollout" "$NUM_ROLLOUTS"
done
