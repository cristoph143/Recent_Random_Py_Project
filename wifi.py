import subprocess

data = subprocess.check_output(['netsh','wlan','show','profiles']).decode('utf-8').split('\n')
wifis = line.split(':')[1][1:-1] for line in data if
