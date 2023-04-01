import subprocess

args = ['ping' , 'yandex.ru']
ping_pocess = subprocess.Popen(args, stdout=subprocess.PIPE)

for line in ping_pocess.stdout:
    print(line.decode('cp866'))

args[1] ='youtube.com'
ping_pocess = subprocess.Popen(args, stdout=subprocess.PIPE)

for line in ping_pocess.stdout:
    print(line.decode('cp866'))
