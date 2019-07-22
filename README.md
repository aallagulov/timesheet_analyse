# timesheet_analyse
Just parsing logs and prepare some different slices

Usage:
>python3 scripts/reader.py --csv=timesheet_example/aallagulov.csv 
seconds_at_all
28800
seconds_per_type
{'QA': 1800, 'REQ': 2700, 'REVIEW': 3900, 'DEPLOY': 9900, 'DEV': 7200, 'FIX_REVIEW': 1800, 'OTHER': 1500}
percents_per_type
DEPLOY 34.38%
DEV 25.00%
REVIEW 13.54%
REQ 9.38%
QA 6.25%
FIX_REVIEW 6.25%
OTHER 5.21%