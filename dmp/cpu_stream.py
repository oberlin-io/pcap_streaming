import subprocess
import threading
import json
from time import sleep
import re

def stream():
    netcat_port = 4445
    cmd = """mpstat |grep all |awk '{print "timestamp",$1,$2,"usr",$4,"nice",$5,"sys",$6}'"""
    while True:
        process = subprocess.Popen(['mpstat'], stdout=subprocess.PIPE)
        stdout = process.communicate()[0].decode('utf-8')
        stdout = stdout.split('\n')
        

        re_date = re.compile('\d{2}/\d{2}/\d{4}')
        date = re_date.findall(stdout[0])[0]  
        
        stdout2 = stdout[2].split(' ')
        stdout3 = stdout[3].split(' ')
        while '' in stdout2: stdout2.remove('')
        while '' in stdout3: stdout3.remove('')
        d = dict()
        d['instance'] = 'instance-1'
        d['date'] = date
        for field in stdout2:
            if ':' in field:
                d['time'] = stdout3[stdout2.index(field)]
            elif 'M' in field:
                d['ampm'] = stdout3[stdout2.index(field)]
            else:
                d[field.replace('%','')] = stdout3[stdout2.index(field)]

        j = json.dumps(d)
        subprocess.run("printf '{}\n'".format(j), shell=True)

        sleep(2)
        
if __name__ == '__main__':
    stream()

