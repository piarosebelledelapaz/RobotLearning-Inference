import argparse
import json
import time
from pathlib import Path

from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig


DEFAULT_POSE_PATH = Path(__file__).with_name("fixed_start_pose.json")


def load_pose(path: Path) -> dict[str, float]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return {key: float(value) for key, value in data["pose"].items()}


def interpolate_pose(
    current: dict[str, float],
    target: dict[str, float],
    alpha: float,
) -> dict[str, float]:
    return {
        key: current[key] + (target[key] - current[key]) * alpha
        for key in target
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Move the SO101 follower to the dataset-derived fixed start pose."
    )
    parser.add_argument("--port", default="COM6")
    parser.add_argument("--id", default="robot_learning_follower")
    parser.add_argument("--calibration-dir", default="calibration")
    parser.add_argument("--pose-path", type=Path, default=DEFAULT_POSE_PATH)
    parser.add_argument("--duration-s", type=float, default=3.0)
    parser.add_argument("--fps", type=float, default=30.0)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    target = load_pose(args.pose_path)
    print("Target start pose:")
    for key, value in target.items():
        print(f"  {key}: {value:.3f}")

    if args.dry_run:
        return

    config = SO101FollowerConfig(
        port=args.port,
        id=args.id,
        calibration_dir=Path(args.calibration_dir),
        cameras={},
        disable_torque_on_disconnect=False,
    )

    robot = SO101Follower(config)
    robot.connect()
    try:
        observation = robot.get_observation()
        current = {key: float(observation[key]) for key in target}

        steps = max(1, int(args.duration_s * args.fps))
        sleep_s = 1.0 / args.fps
        for step in range(1, steps + 1):
            alpha = step / steps
            robot.send_action(interpolate_pose(current, target, alpha))
            time.sleep(sleep_s)

        robot.send_action(target)
        print("Reached fixed start pose.")
    finally:
        robot.disconnect()


if __name__ == "__main__":
    main()
