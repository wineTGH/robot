#! /bin/bash

rsync --filter=':- .gitignore' -azP . robot@reset-robot.local:~/robot
ssh robot@reset-robot.local 'cd ~/robot && ~/.local/bin/uv sync --no-dev'
