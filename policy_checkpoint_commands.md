# Policy Checkpoint Commands

Run from the repo root:

```bash
cd RobotLearning-Inference
```

## Download

Mixed 5k:

```bash
python scripts/download_from_hf.py \
  --policy-repo-id piarosebelledelapaz/multitask-dit-so101-mixed \
  --policy-revision main \
  --policy-allow-pattern "checkpoints/005000/pretrained_model/*" \
  --policy-dir artifacts/policies/mixed_005000
```

Mixed 10k:

```bash
python scripts/download_from_hf.py \
  --policy-repo-id piarosebelledelapaz/multitask-dit-so101-mixed \
  --policy-revision main \
  --policy-allow-pattern "checkpoints/010000/pretrained_model/*" \
  --policy-dir artifacts/policies/mixed_010000
```

No crop bs64 5k:

```bash
python scripts/download_from_hf.py \
  --policy-repo-id piarosebelledelapaz/multitask-dit-so101-mixed-no-random-crop-bs64 \
  --policy-revision main \
  --policy-allow-pattern "checkpoints/005000/pretrained_model/*" \
  --policy-dir artifacts/policies/mixed_no_crop_bs64_005000
```

No crop bs64 10k:

```bash
python scripts/download_from_hf.py \
  --policy-repo-id piarosebelledelapaz/multitask-dit-so101-mixed-no-random-crop-bs64 \
  --policy-revision main \
  --policy-allow-pattern "checkpoints/010000/pretrained_model/*" \
  --policy-dir artifacts/policies/mixed_no_crop_bs64_010000
```

## Run Challenge

Mixed 5k:

```bash
POLICY_PATH=artifacts/policies/mixed_005000/checkpoints/005000/pretrained_model bash run_eval_towel_challenge.sh
```

Mixed 10k:

```bash
POLICY_PATH=artifacts/policies/mixed_010000/checkpoints/010000/pretrained_model bash run_eval_towel_challenge.sh
```

No crop bs64 5k:

```bash
POLICY_PATH=artifacts/policies/mixed_no_crop_bs64_005000/checkpoints/005000/pretrained_model bash run_eval_towel_challenge.sh
```

No crop bs64 10k:

```bash
POLICY_PATH=artifacts/policies/mixed_no_crop_bs64_010000/checkpoints/010000/pretrained_model bash run_eval_towel_challenge.sh
```

## Run Folding

Mixed 5k:

```bash
POLICY_PATH=artifacts/policies/mixed_005000/checkpoints/005000/pretrained_model bash run_eval_towel_folding.sh
```

Mixed 10k:

```bash
POLICY_PATH=artifacts/policies/mixed_010000/checkpoints/010000/pretrained_model bash run_eval_towel_folding.sh
```

No crop bs64 5k:

```bash
POLICY_PATH=artifacts/policies/mixed_no_crop_bs64_005000/checkpoints/005000/pretrained_model bash run_eval_towel_folding.sh
```

No crop bs64 10k:

```bash
POLICY_PATH=artifacts/policies/mixed_no_crop_bs64_010000/checkpoints/010000/pretrained_model bash run_eval_towel_folding.sh
```
