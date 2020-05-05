# For testing packets captured like:
# record traffic

import json
import re
import pandas as pd

def set_regex():
    '''
    Open the PCAP regular expressions and compile.
    Make empty lists per field for parsed data.
    Edit regex in re.json.
    '''

    with open('re.json') as f:
        regex = json.loads(f.read())

    for field in regex:
        dx = regex.index(field)
        re_str = field['regex'].replace('\\\\', '\\')
        #print(re_str)
        regex[dx]['compiled'] = re.compile(re_str)
        regex[dx]['data'] = list()

    return regex


def parse(txt_file, regex, output='export.csv'):
    '''
    Parse PCAP as text, such as from:
    Connection 1: sudo tcpdump -i eth0 -nn -c 5 -vvvv > tmp.txt
    Connection 2: sudo tcpreplay -i eth0 -K --loop 1 messenger.pcap
    I'm not sure the effect verbosity level has on the regex.
    '''

    with open(txt_file, 'r') as f: pcap = f.read()
    
    pcap = pcap.replace('\n    ', ' ') # In triple verbose, newline made
    
    pcap = pcap.split('\n')[:-1]

    # Parse each line per field
    def find(field, line):
        #add try except and capture exception
        x = field['compiled'].search(line).group(1)
        return x

    for line in pcap:
        for field in regex:
            #add try except and capture exception
            try:
                dx = regex.index(field)
                x = field['compiled'].search(line).group(1)
            except Exception as e:
                x = e
            regex[dx]['data'].append(x)
        

    # Make dataframe
    d = dict()
    for field in regex:
        dx = regex.index(field)
        d[field['name']] = regex[dx]['data']
    
    df = pd.DataFrame(d)

    df.to_csv(output, index=False)

    return df


if __name__ == '__main__':
    r = set_regex()
    parse('../tmp.txt', r)
