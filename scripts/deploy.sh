#! /bin/bash

rsync --filter=':- .gitignore' -azP . robot@reset-robot.local:~/robot-code
ssh robot@reset-robot.local 'cd ~/robot-code && ~/.local/bin/uv sync'