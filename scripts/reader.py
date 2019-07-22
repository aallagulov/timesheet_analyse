import argparse
from argparse import ArgumentParser

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

    print(cli_args.csv)

    exit(0)