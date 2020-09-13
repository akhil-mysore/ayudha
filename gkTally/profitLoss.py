#!/usr/bin/python3

import csv
import argparse
from datetime import datetime

date_format = "%m/%d/%Y"

def parse_args():
    '''
    Parse command line arguments '''
    parser = argparse.ArgumentParser(description="profit loss")
    parser.add_argument(
        "-i",
        dest="infile",
        type=str,
        nargs="?",
        default="./transactions.csv",
        help="input transaction csv file ",
    )
    args = parser.parse_args()
    return args

# string containing key words to decide if a transaction is to be considered for
# profit loss calculation
profit_loss = ["bought", "sold"]
investment = ["funding", "wire"]


def str_find(s, key):
    for i in key:
        if ((s.lower()).find(i)) != -1:
            return True
    return False


def is_profit_loss(s):
    return str_find(s, profit_loss)


def is_investment(s):
    return str_find(s, investment)


def cal_tot_profit_loss(profit_l, total_inv):

    total_per_profit = (100 * profit_l) / total_inv
    return total_per_profit


def cal_profit_per_year():
    None
    # d1 = datetime.today()
    # d2 = datetime.strptime(first_date, date_format)
    # delta = d1 - d2
    # per_profit = (365 * profit_l) / delta.days


if __name__ == "__main__":
    args = parse_args()
    with open( args.infile, 'r' ) as csv_file:
        csvHandler = csv.DictReader( csv_file )

        profit_l = 0.0
        first_trade = True
        total_inv = 0.0

        loopCount = 0
        for row in csvHandler:
            desc = row[ 'DESCRIPTION' ]
            if not desc:
                continue
            print( f'Processing {loopCount} {desc}' )
            if is_profit_loss( desc ):
                if first_trade:
                    first_date = row["DATE"]
                    first_trade = False
                profit_l += float( row["AMOUNT"] )
            elif is_investment( desc ):
                total_inv += float( row["AMOUNT"] )
            loopCount+= 1

    print("total profit till date ($): ", "%.2f" % profit_l)
    print("date of first investment: ", first_date)
    print(
        "percentage profit: ", cal_tot_profit_loss(profit_l, total_inv),
    )
