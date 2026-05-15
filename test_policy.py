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
parser.add_argument("--vcodec", default=os.environ.get("DATASET_VCODEC", "libx264"))
parser.add_argument("--num-episodes", type=int, default=int(os.environ.get("NUM_EPISODES", "1")))
args = parser.parse_args()

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
    "--display_data=false",
    "--play_sounds=false",
    f"--dataset.repo_id=local/{args.dataset_name}_{run_id}",
    "--dataset.single_task=Towel folding",
    f"--dataset.num_episodes={args.num_episodes}",
    "--dataset.push_to_hub=false",
    f"--dataset.vcodec={args.vcodec}",
    f"--policy.device={args.device}",
    f"--policy.path={args.policy_path}",
]

subprocess.run(cmd, check=True)

# Python 3.12 is required for multi_task_dit.
# pip install "lerobot[multi_task_dit]"
