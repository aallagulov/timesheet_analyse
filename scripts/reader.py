import argparse
import csv
from datetime import datetime
from datetime import timedelta

DAY_OF_YEAR_FMT = '%Y-%m-%d'
DAY_TIME_FMT = DAY_OF_YEAR_FMT + ' ' + '%H:%M'

headers = [
    'DATE',
    'TIME1',
    'TIME2',
    'TICKET',
    'COMMENT'
]

POSSIBLE_TAGS = [
    'QA',
    'TEST',
    'CODE',
    'DEV',
    'OTHER',
    'REVIEW',
    'FIX_REVIEW',
    'REQ',
    'MERGE',
    'SPEC',
    'DEPLOY'
]

def parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--csv',
        help='Path to CSV file.',
        required=True)
    parser.add_argument(
        '--start',
        help='Start date for collecting statistic',
        required=False)
    parser.add_argument(
        '--end',
        help='End date for collecting statistic',
        required=False)
    
    cli_args = parser.parse_args()
    return cli_args

if __name__ == '__main__':
    cli_args = parse_cli_args()
    fname = cli_args.csv
    
    start_dt = datetime.min
    if cli_args.start:
        # the start of that day
        start_dt = datetime.strptime(cli_args.start, DAY_OF_YEAR_FMT)
    end_dt = datetime.max
    if cli_args.end:
        # the end of that day
        end_dt = datetime.strptime(cli_args.end, DAY_OF_YEAR_FMT) + timedelta(days=1)

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
            
            # sometimes this key isn't found
            if not 'COMMENT' in line_result:
                continue

            split_comment = line_result['COMMENT'].split(':')
            tag = split_comment[0]
            # checking only tagged comments
            if tag and tag in POSSIBLE_TAGS:
                line_result['TYPE'] = tag
 
                dt1 = datetime.strptime(line_result['DATE'] + ' ' + line_result['TIME1'], DAY_TIME_FMT)
                dt2 = datetime.strptime(line_result['DATE'] + ' ' + line_result['TIME2'], DAY_TIME_FMT)
                
                if start_dt > dt1:
                    continue
                if end_dt < dt2:
                    continue

                time_delta = dt2 - dt1 
                secons = time_delta.seconds   
                line_result['TIME_DELTA'] = secons
                seconds_at_all += secons
                
                current_time_delta = seconds_per_type.get(line_result['TYPE'], 0)
                seconds_per_type[line_result['TYPE']] = current_time_delta + line_result['TIME_DELTA']
                
                result.append(line_result)
 
    for t, s in seconds_per_type.items():
        percents_per_type[t] = s/seconds_at_all
        
    # I wrote wrong tag =(
    if 'CODE' in percents_per_type:
        percents_per_type['CODE'] = percents_per_type.pop('DEV', None)
                
    print('====================TOTAL====================', end='\n')
    print(seconds_at_all, end='\n')
    print('====================TAGS=====================', end='\n')
    for t, p in sorted(percents_per_type.items(), key=lambda x: x[1], reverse=True):
        s = seconds_per_type[t]
        print(t+" "+"{:.2%}".format(p)+" "+"{} seconds".format(s), end='\n')
  
    exit(0)