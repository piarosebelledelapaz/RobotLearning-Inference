# RobotLearning Inference

## 1. Clone the repo:

```bash
git clone <repo-url>
cd RobotLearning-Inference
```

## 2. Create the conda environment:

```bash
conda env create -f environment.yml
conda activate robotlearning-inference
```

## 3. Run inference script:

For normal evaluation (loads the `model=multitask_dit_so101plain_clippatch16_bs32` as default):
```bash
bash run_eval_towel_folding.sh
``` 

For the challenge:
```bash
POLICY_PATH={$POLICY_PATH} bash run_eval_towel_folding.sh
```


