# RobotLearning Inference

## 1. Clone the repo:

```bash
git clone <repo-url>
cd RobotLearning-Inference
```

## 2. Download the checkpoint from Hugging Face into `artifacts/policies/`:

```bash
POLICY_REPO_ID="piarosebelledelapaz/${MODEL_NAME}"
POLICY_CHECKPOINT="${MODEL_NAME}_${N_CHECKPOINT}"

python scripts/download_from_hf.py \
  --policy-repo-id "$POLICY_REPO_ID" \
  --policy-allow-pattern "checkpoints/${N_CHECKPOINT}/pretrained_model/*" \
  --policy-dir "artifacts/policies/${POLICY_CHECKPOINT}"
```

For the 3 evaluations: we used `MODEL_NAME = "multitask_dit_so101plain_clippatch16_bs32"` and `N_CHECKPOINT = "030000"`

For the challenge task: we varied `MODEL_NAME = ["multitask_dit_so101plain_clippatch16_bs32", " multitask-dit-so101-mixed", "multitask-dit-so101-mixed-no-random-crop-bs64"]` and `N_CHECKPOINT = ["030000", "005000", "010000"]`

## 3. Run inference script:

For normal evaluation (loads the `model=multitask_dit_so101plain_clippatch16_bs32` as default):
```bash
bash run_eval_towel_challenge.sh
``` 

For the challenge:
```bash
POLICY_PATH={$POLICY_PATH} bash run_eval_towel_folding.sh
```


