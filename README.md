# RobotLearning Inference

## 1. Clone the repo (if needed):

```bash
git clone git@github.com:piarosebelledelapaz/RobotLearning-Inference.git
cd RobotLearning-Inference
```

## 2. Create the conda environment:

```bash
conda env create -f environment.yml
conda activate robotlearning-inference
```

## 3. Run inference script:

### For normal evaluation (loads the `model=multitask_dit_so101plain_clippatch16_bs32` as default):
```bash
bash run_eval_towel_folding.sh
``` 

### For the challenge:
```bash
POLICY_PATH={$POLICY_PATH} bash run_eval_towel_folding.sh
```

All model checkpoints used during the demo day are found in:
```text
artifacts/
  policies/
    clippatch16_batch32_030000/
    mixed_005000/
    mixed_010000/
    mixed_no_crop_bs64_005000/
    mixed_no_crop_bs64_010000/
```


### We tested 3 different policies (including 2 different checkpoints of the finetuned models) during the challenge.

Base model (original, same as the normal evaluation):
```bash
bash run_eval_towel_folding.sh
``` 


Finetuned model on mixed dataset with random cropping, batchsize=128 (005000 checkpoint):

```bash
POLICY_PATH=artifacts/policies/mixed_005000/checkpoints/005000/pretrained_model bash run_eval_towel_folding.sh
```

Finetuned model on mixed dataset with random cropping, batchsize=128 (010000 checkpoint):

```bash
POLICY_PATH=artifacts/policies/mixed_010000/checkpoints/010000/pretrained_model bash run_eval_towel_folding.sh
```

Finetuned model on mixed dataset without cropping, batchsize=64 (005000 checkpoint):

```bash
POLICY_PATH=artifacts/policies/mixed_no_crop_bs64_005000/checkpoints/005000/pretrained_model bash run_eval_towel_folding.sh
```

Finetuned model on mixed dataset without cropping, batchsize=64 (010000 checkpoint):

```bash
POLICY_PATH=artifacts/policies/mixed_no_crop_bs64_010000/checkpoints/010000/pretrained_model bash run_eval_towel_folding.sh
```
### Notes:
- Calibration files are provided and set up is needed to match the same fixed starting position of the robot arm during the demo day.

