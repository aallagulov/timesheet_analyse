import argparse
from argparse import ArgumentParser
import csv

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
    
    result = {}
    for h in headers:
        result[h] = []

    with open(fname, newline='') as csvfile:
        tsh_reader = csv.reader(csvfile, delimiter=',')
        for row in tsh_reader:
            for h, v in zip(headers, row):
                result[h].append(v)
                
    print(result)
  
    exit(0)