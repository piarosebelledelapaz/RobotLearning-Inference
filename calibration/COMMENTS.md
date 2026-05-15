to reuse the calibration file:

mkdir %USERPROFILE%\.cache\huggingface\lerobot\calibration\robots\so101_follower
mkdir %USERPROFILE%\.cache\huggingface\lerobot\calibration\teleoperators\so101_leader

copy "C:\Users\piade\UZH\SPRING2026\RobotLearning-Inference\calibration\robot_learning_follower.json" "%USERPROFILE%\.cache\huggingface\lerobot\calibration\robots\so101_follower\robot_learning_follower.json"

copy "C:\Users\piade\UZH\SPRING2026\RobotLearning-Inference\calibration\robot_learning_leader.json" "%USERPROFILE%\.cache\huggingface\lerobot\calibration\teleoperators\so101_leader\robot_learning_leader.json"