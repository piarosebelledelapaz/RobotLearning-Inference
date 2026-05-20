import argparse
import os
import subprocess
from datetime import datetime
from pathlib import Path


run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
workspace = Path(__file__).resolve().parent

parser = argparse.ArgumentParser(description="Run a LeRobot policy on the SO101 follower.")
parser.add_argument(
    "--policy-path",
    default=os.environ.get(
        "POLICY_PATH",
        str(workspace / "artifacts" / "policies" / "clippatch16_batch32_030000"),
    ),
)
parser.add_argument("--dataset-name", default="eval_policy")
parser.add_argument("--robot-port", default=os.environ.get("ROBOT_PORT", "/dev/ttyACM0"))
parser.add_argument("--robot-id", default=os.environ.get("ROBOT_ID", "robot_learning_follower"))
parser.add_argument("--camera-index", default=os.environ.get("CAMERA_INDEX", "0"))
parser.add_argument("--camera-fps", type=int, default=int(os.environ.get("CAMERA_FPS", "30")))
parser.add_argument("--device", default=os.environ.get("POLICY_DEVICE", "cuda"))
parser.add_argument("--vcodec", default=os.environ.get("DATASET_VCODEC", "h264"))
parser.add_argument("--num-episodes", type=int, default=int(os.environ.get("NUM_EPISODES", "1")))
parser.add_argument("--display-data", default=os.environ.get("DISPLAY_DATA", "true"))
parser.add_argument("--task-name", default=os.environ.get("TASK_NAME", "Towel folding"))
parser.add_argument(
    "--episode-time-s",
    type=float,
    default=float(os.environ["EPISODE_TIME_S"]) if os.environ.get("EPISODE_TIME_S") else None,
)
args = parser.parse_args()

policy_path = args.policy_path
candidate_policy_path = Path(policy_path).expanduser()
if candidate_policy_path.exists():
    policy_path = str(candidate_policy_path.resolve())
elif "/" in policy_path or "\\" in policy_path:
    raise FileNotFoundError(
        f"Policy path does not exist: {policy_path}. "
        "Pass the folder that contains config.json and model.safetensors."
    )

camera_config = (
    "{ wrist: {type: opencv, index_or_path: "
    f"{args.camera_index}, width: 640, height: 480, fps: {args.camera_fps}"
    " }"
    " }"
)

cmd = [
    "lerobot-record",
    "--robot.type=so101_follower",
    f"--robot.port={args.robot_port}",
    f"--robot.id={args.robot_id}",
    "--robot.calibration_dir=calibration",
    f"--robot.cameras={camera_config}",
    f"--display_data={args.display_data}",
    "--play_sounds=false",
    f"--dataset.repo_id=local/{args.dataset_name}_{run_id}",
    f"--dataset.single_task={args.task_name}",
    f"--dataset.num_episodes={args.num_episodes}",
    "--dataset.push_to_hub=false",
    f"--dataset.vcodec={args.vcodec}",
    f"--policy.device={args.device}",
    f"--policy.path={policy_path}",
]

if args.episode_time_s is not None:
    cmd.append(f"--dataset.episode_time_s={args.episode_time_s}")

subprocess.run(cmd, check=True)

# Python 3.12 is required for multi_task_dit.
# pip install "lerobot[multi_task_dit]"
