import subprocess
import chardet

args = ['ping', 'yandex.ru']
ping_pocess = subprocess.Popen(args, stdout=subprocess.PIPE)

for line in ping_pocess.stdout:
    result = chardet.detect(line)
    print(line.decode(result['encoding']))

args[1] = 'youtube.com'
ping_pocess = subprocess.Popen(args, stdout=subprocess.PIPE)

for line in ping_pocess.stdout:
    result = chardet.detect(line)
    print(line.decode(result['encoding']))
