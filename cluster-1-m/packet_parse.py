import json
import re

class PacketParse(object):

    def __init__(self):
        pass

    def set_regex(self):
        '''
        Open the PCAP regular expressions and compile.
        Edit regex in re.json.
        regex are for:
        sudo tcpdump -i eth0 -nnc50 --dont-verify-checksums
        Some removed due to lessening verbosity to one line:
        { "name":   "protocol",
          "regex":  "proto[^\\(]+\\((\\d{1,3})\\)"},
        What effect does verbosity level of tcpdump have on the regex?
        '''

        with open('re.json') as f:
            regex = json.loads(f.read())

        for field in regex:
            dx = regex.index(field)
            re_str = field['regex'].replace('\\\\', '\\')
            regex[dx]['compiled'] = re.compile(re_str)
            regex[dx]['data'] = list()

        self.regex = regex


    def get_values(self, line):
        '''
        Run on each line of datastream, assuming each line is a packet.
        '''

        regex = self.regex
        d = dict()
        d['errors'] = list()

        for field in regex:
            #print(field['name'])
            try:
                dx = regex.index(field)
                value = field['compiled'].search(line).group(1)
            except Exception as e:
                value = None
                d['errors'].append({field['name']: str(e)})
            d[field['name']] = value

        return d

    
    def get_values_aslist(self, line):
        '''
        Run on each line of datastream, assuming each line is a packet.
        '''

        regex = self.regex
        #d = dict()
        #d['errors'] = list()
        d = list()

        for field in regex:
            #print(field['name'])
            try:
                dx = regex.index(field)
                value = field['compiled'].search(line).group(1)
            except Exception as e:
                value = None
                #d['errors'].append({field['name']: str(e)})
            
            #d[field['name']] = value
            d.append(value)

        return d

