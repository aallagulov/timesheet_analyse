import argparse
from argparse import ArgumentParser
import csv
from datetime import datetime

FMT = '%H:%M'

headers = [
    'DATE',
    'TIME1',
    'TIME2',
    'TICKET',
    'COMMENT'
]

def parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--csv',
        help='Path to CSV file.',
        required=True)
    
    cli_args = parser.parse_args()
    return cli_args

if __name__ == '__main__':
    cli_args = parse_cli_args()
    fname = cli_args.csv
    
    seconds_at_all = 0
    seconds_per_type = {}
    percents_per_type = {}
    
    result = []
    with open(fname, newline='') as csvfile:
        tsh_reader = csv.reader(csvfile, delimiter=',')
        filtered = filter(lambda line: (line and not line[0].isspace()), tsh_reader)
        for row in filtered:
            line_result = {}
            for h, v in zip(headers, row):
                line_result[h] = v
            
            time_delta = datetime.strptime(line_result['TIME2'], FMT) - datetime.strptime(line_result['TIME1'], FMT) 
            secons = time_delta.seconds   
            line_result['TIME_DELTA'] = secons
            seconds_at_all += secons
            
            split_comment = line_result['COMMENT'].split(':')
            tag = split_comment[0]
            # checking only tagged comments
            if tag and len(split_comment)>1:
                line_result['TYPE'] = tag
                
                current_time_delta = seconds_per_type.get(line_result['TYPE'], 0)
                seconds_per_type[line_result['TYPE']] = current_time_delta + line_result['TIME_DELTA']
                
                result.append(line_result)
 
    for t, s in seconds_per_type.items():
        percents_per_type[t] = s/seconds_at_all
                
    print('seconds_at_all', end='\n')
    print(seconds_at_all, end='\n')
    print('seconds_per_type', end='\n')
    print(seconds_per_type, end='\n')
    print('percents_per_type', end='\n')
    for t, p in sorted(percents_per_type.items(), key=lambda x: x[1], reverse=True):
        print(t+" "+"{:.2%}".format(p), end='\n')
  
    exit(0)