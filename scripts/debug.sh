ssh robot@reset-robot.local "echo 'cd ~/robot && nohup ./.venv/bin/python -m debugpy --listen reset-robot.local:5678 --wait-for-client ./main.py' | at now"
sleep 3
echo ==========
echo Task done!