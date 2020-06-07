import subprocess
import random
import time


IDS = [id + 1 for id in range(16)]

while True:
    id1, id2 = random.sample(IDS, k=2)
    for i in [3, 2, 1]:
        print(f"Match id:{id1} vs id:{id2} will be launched in {i} seconds...")
        time.sleep(1)
    cmd = f"python3 run_bot_attacker.py --id {id1}"
    cmd += f"& python3 run_bot_attacker.py --id {id2}"
    subprocess.call(cmd, shell=True)
