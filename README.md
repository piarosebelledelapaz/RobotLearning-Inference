# RobotLearning Inference

Reproducible inference setup for the SO101 follower towel-folding policy.

## What is stored in Git

- Inference scripts: `test_policy.py`, `move_to_start_pose.py`
- Robot calibration: `calibration/`
- Fixed start pose: `fixed_start_pose.json`

Large generated assets are intentionally not stored in Git:

- `artifacts/` for downloaded policy checkpoints and optional datasets
- `outputs/` for local recordings and training output
- `dataset/` for local LeRobot datasets

## Artifact layout

Put the inference checkpoint here:

```text
artifacts/
  policies/
    clippatch16_batch32_030000/
      config.json
      model.safetensors
      policy_postprocessor.json
      policy_postprocessor_step_0_unnormalizer_processor.safetensors
      policy_preprocessor.json
      policy_preprocessor_step_4_normalizer_processor.safetensors
      train_config.json
```

For inference, you need only the `pretrained_model` files above. You do not need
`training_state/optimizer_state.safetensors`.

If you also want the training/evaluation dataset locally, put it at:

```text
artifacts/
  datasets/
    so101_plain/
      data/
      meta/
      videos/
```

## Linux setup

1. Clone the repo.

```bash
git clone <repo-url>
cd RobotLearning-Inference
```

2. Create the conda environment.

```bash
conda env create -f environment.yml
conda activate robotlearning-inference
```

If the environment already exists and `environment.yml` changed, update it:

```bash
conda env update -n robotlearning-inference -f environment.yml --prune
```

3. Install FFmpeg and camera/USB support.

```bash
sudo apt-get update
sudo apt-get install -y v4l-utils
```

4. Download the checkpoint from Hugging Face into `artifacts/policies/`.

Use exact Hugging Face revisions, preferably commit hashes, not floating branch
names like `main`.

Patch16 batch32 checkpoint, which matches the default inference path:

```bash
python scripts/download_from_hf.py \
  --policy-repo-id piarosebelledelapaz/multitask_dit_so101plain_clippatch16_bs32 \
  --policy-revision <patch16-model-commit-hash> \
  --policy-allow-pattern "checkpoints/030000/pretrained_model/*" \
  --policy-dir artifacts/policies/clippatch16_batch32_030000
```

If the downloaded files keep the Hugging Face folder structure, run inference
with `artifacts/policies/clippatch16_batch32_030000/checkpoints/030000/pretrained_model`.

Patch32 batch64 checkpoint:

```bash
python scripts/download_from_hf.py \
  --policy-repo-id piarosebelledelapaz/multitask_dit_so101plain_clippatch32_bs64 \
  --policy-revision <patch32-model-commit-hash> \
  --policy-dir artifacts/policies/clippatch32_batch64
```

If you also need the dataset locally, download it in the same reproducible step:

```bash
python scripts/download_from_hf.py \
  --policy-repo-id piarosebelledelapaz/multitask_dit_so101plain_clippatch16_bs32 \
  --policy-revision <patch16-model-commit-hash> \
  --policy-dir artifacts/policies/clippatch16_batch32_030000 \
  --dataset-repo-id Robot-Learning-Group45/so101_plain \
  --dataset-revision <dataset-commit-hash>
```

Then verify the files:

```bash
cd artifacts/policies/clippatch16_batch32_030000
sha256sum -c ../../../manifests/clippatch16_batch32_030000.sha256
cd -
```

5. Check the robot and camera device names.

```bash
ls /dev/ttyACM* /dev/ttyUSB*
v4l2-ctl --list-devices
```

6. Move the robot to the reproducible start pose.

```bash
python move_to_start_pose.py --port /dev/ttyACM0
```

7. Preview what the fixed start pose sees.

```bash
python preview_camera.py --camera-index 0 --fps 20
```

Press `s` to save a frame and `q` to close the preview.

8. Run inference.

```bash
python test_policy.py \
  --robot-port /dev/ttyACM0 \
  --camera-index 0 \
  --policy-path artifacts/policies/clippatch16_batch32_030000 \
  --device cuda \
  --vcodec h264
```

Use `--vcodec h264_nvenc` only on machines where FFmpeg can see an NVIDIA
hardware encoder. `h264` is slower but more portable.

For repeated evaluation rollouts where the arm should return to the fixed start
pose before every rollout, run:

```bash
NUM_ROLLOUTS=5 bash run_eval_towel_folding.sh
```

The script alternates:

```text
move_to_start_pose.py
test_policy.py --num-episodes 1
move_to_start_pose.py
test_policy.py --num-episodes 1
...
```

By default, the script waits for you to press Enter between rollouts. This is
useful over SSH when you want to inspect/reset the scene manually before the arm
moves again. For unattended runs, disable the pause:

```bash
WAIT_FOR_ENTER=false NUM_ROLLOUTS=5 bash run_eval_towel_folding.sh
```

Its Linux defaults match the lab inference setup:

```bash
ROBOT_PORT=/dev/ttyACM0
CAMERA_INDEX=0
CAMERA_FPS=20
POLICY_PATH=artifacts/policies/clippatch16_batch32/checkpoints/030000/pretrained_model
POLICY_DEVICE=cuda
DATASET_VCODEC=h264_nvenc
```

## Environment variables

The same values can be provided as environment variables:

```bash
export POLICY_PATH=artifacts/policies/clippatch16_batch32_030000
export ROBOT_PORT=/dev/ttyACM0
export ROBOT_ID=robot_learning_follower
export CAMERA_INDEX=0
export CAMERA_FPS=30
export POLICY_DEVICE=cuda
export DATASET_VCODEC=h264
python test_policy.py
```

## Reproducibility checklist

- Commit the code and calibration JSONs.
- Store the checkpoint and dataset on Hugging Face.
- Use Hugging Face commit hashes for `--policy-revision` and `--dataset-revision`.
- Record the checkpoint checksum.
- Record the Python version and installed package versions from the Linux machine:

```bash
python --version
python -m pip freeze > requirements-lock.txt
```

- Record the robot port, camera index, CUDA version, GPU model, and FFmpeg codec.
