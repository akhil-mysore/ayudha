#!/usr/bin/python3

import pandas
import argparse
from datetime import datetime


date_format = "%m/%d/%Y"


def parse_args():
    parser = argparse.ArgumentParser(description="profit loss")
    parser.add_argument(
        "-i",
        dest="infile",
        type=str,
        nargs="?",
        default="other\\transactions.csv",
        help="input transaction file ",
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
    with open(args.infile) as csv_file:
        csv_reader = pandas.read_csv(
            csv_file, dtype={"DESCRIPTION": str, "AMOUNT": float}
        )
        index = 0
        profit_l = 0.0
        first_trade = True
        total_inv = 0.0
        for s in csv_reader["DESCRIPTION"]:
            if (type(s) == str) and (is_profit_loss(s)):
                if first_trade:
                    first_date = csv_reader["DATE"][index]
                    first_trade = False
                profit_l += csv_reader["AMOUNT"][index]
            elif (type(s) == str) and (is_investment(s)):
                total_inv += csv_reader["AMOUNT"][index]

            index += 1

    print("total profit till date ($) -", "%.2f" % profit_l)
    print("date of first investment - ", first_date)
    print(
        "percentage profit - ", cal_tot_profit_loss(profit_l, total_inv),
    )
