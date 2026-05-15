import argparse
from pathlib import Path

from huggingface_hub import snapshot_download


def download_snapshot(
    repo_id: str,
    repo_type: str,
    revision: str,
    local_dir: Path,
) -> None:
    local_dir.mkdir(parents=True, exist_ok=True)
    snapshot_download(
        repo_id=repo_id,
        repo_type=repo_type,
        revision=revision,
        local_dir=local_dir,
        local_dir_use_symlinks=False,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download pinned Hugging Face model and dataset artifacts."
    )
    parser.add_argument("--policy-repo-id", required=True)
    parser.add_argument("--policy-revision", required=True)
    parser.add_argument("--dataset-repo-id")
    parser.add_argument("--dataset-revision")
    parser.add_argument(
        "--policy-dir",
        type=Path,
        default=Path("artifacts/policies/clippatch16_batch32_030000"),
    )
    parser.add_argument(
        "--dataset-dir",
        type=Path,
        default=Path("artifacts/datasets/so101_plain"),
    )
    args = parser.parse_args()

    download_snapshot(
        repo_id=args.policy_repo_id,
        repo_type="model",
        revision=args.policy_revision,
        local_dir=args.policy_dir,
    )

    if args.dataset_repo_id:
        if not args.dataset_revision:
            raise SystemExit("--dataset-revision is required with --dataset-repo-id")
        download_snapshot(
            repo_id=args.dataset_repo_id,
            repo_type="dataset",
            revision=args.dataset_revision,
            local_dir=args.dataset_dir,
        )


if __name__ == "__main__":
    main()
