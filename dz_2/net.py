import subprocess
import sys
import os

def check_size(pkt_size, host):
    ping = subprocess.Popen(f'ping -M do -c 1 -s {pkt_size} {host}', shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    for item in iter(ping.stdout.readline, b''):
        item = item.decode(encoding='utf-8')
        if     'is too large' in item \
            or 'message too long' in item \
            or '100% packet loss' in item \
            or '100.0% packet loss' in item:
            return False
    return True


try:
    host = os.environ['HOST']
except KeyError:
    print('environment variable HOST is not set.')
    sys.exit(1)

ping = subprocess.Popen(f'ping -M do -c 1 -s {10000} {host}', shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
for item in iter(ping.stderr.readline, b''):
    if 'Name or service not known' in item.decode(encoding='utf-8'):
        print('ERROR: Name or service not known or incorrect')
        exit(0)

l_value = 0
r_value = 5000
while l_value + 1 < r_value:
    mid = (l_value + r_value) // 2
    if check_size(mid, host):
        l_value = mid
    else:
        r_value = mid

print('Minimum MTU without headers:', l_value)