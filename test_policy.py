import argparse
import subprocess
from datetime import datetime
from pathlib import Path


run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
workspace = Path(__file__).resolve().parent

parser = argparse.ArgumentParser(description="Run a LeRobot policy on the SO101 follower.")
parser.add_argument(
    "--policy-path",
    type=Path,
    default=workspace / "outputs" / "clippatch16_batch32" / "checkpoints" / "030000" / "pretrained_model",
)
parser.add_argument("--dataset-name", default="eval_policy")
args = parser.parse_args()

cmd = [
    "lerobot-record",
    "--robot.type=so101_follower",
    "--robot.port=COM6",
    "--robot.id=robot_learning_follower",
    "--robot.calibration_dir=calibration",
    '--robot.cameras={ wrist: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 1',
    "--display_data=false",
    "--play_sounds=false",
    f"--dataset.repo_id=local/{args.dataset_name}_{run_id}",
    "--dataset.single_task=Towel folding",
    "--dataset.num_episodes=1",
    "--dataset.push_to_hub=false",
    "--dataset.vcodec=h264_nvenc",
    "--policy.device=cuda",
    f"--policy.path={args.policy_path}",
]

subprocess.run(cmd)

#python 3.12 required for multi_task_dit
#pip install lerobot[multi_task_dit]
