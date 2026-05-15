To reuse the calibration files, copy them into LeRobot's Hugging Face cache.

The follower file belongs under:

```text
~/.cache/huggingface/lerobot/calibration/robots/so101_follower/
```

The leader file belongs under:

```text
~/.cache/huggingface/lerobot/calibration/teleoperators/so101_leader/
```

## Windows

From this repo:

```bat
mkdir %USERPROFILE%\.cache\huggingface\lerobot\calibration\robots\so101_follower
mkdir %USERPROFILE%\.cache\huggingface\lerobot\calibration\teleoperators\so101_leader

copy "C:\Users\piade\UZH\SPRING2026\RobotLearning-Inference\calibration\robot_learning_follower.json" "%USERPROFILE%\.cache\huggingface\lerobot\calibration\robots\so101_follower\robot_learning_follower.json"
copy "C:\Users\piade\UZH\SPRING2026\RobotLearning-Inference\calibration\robot_learning_leader.json" "%USERPROFILE%\.cache\huggingface\lerobot\calibration\teleoperators\so101_leader\robot_learning_leader.json"
```

## Linux

If the repo is already cloned on the Linux machine:

```bash
cd RobotLearning-Inference

mkdir -p ~/.cache/huggingface/lerobot/calibration/robots/so101_follower
mkdir -p ~/.cache/huggingface/lerobot/calibration/teleoperators/so101_leader

cp calibration/robot_learning_follower.json ~/.cache/huggingface/lerobot/calibration/robots/so101_follower/robot_learning_follower.json
cp calibration/robot_learning_leader.json ~/.cache/huggingface/lerobot/calibration/teleoperators/so101_leader/robot_learning_leader.json
```

If the calibration files are only on this Windows machine, copy them to Linux
first. Replace `<linux-user>`, `<linux-host>`, and the destination path:

```bash
scp calibration/robot_learning_follower.json <linux-user>@<linux-host>:~/RobotLearning-Inference/calibration/
scp calibration/robot_learning_leader.json <linux-user>@<linux-host>:~/RobotLearning-Inference/calibration/
```

Then run the Linux `mkdir -p` and `cp` commands above on the Linux machine.

To check that LeRobot should find the files:

```bash
ls -l ~/.cache/huggingface/lerobot/calibration/robots/so101_follower/robot_learning_follower.json
ls -l ~/.cache/huggingface/lerobot/calibration/teleoperators/so101_leader/robot_learning_leader.json
```
