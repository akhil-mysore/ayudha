import csv
import argparse
from datetime import datetime


def parse_args():
    """
    Parse command line arguments """
    parser = argparse.ArgumentParser(description="profit loss")
    parser.add_argument(
        "-i",
        dest="infile",
        type=str,
        nargs="?",
        default="transactions.csv",
        help="input transaction csv file ",
    )
    args = parser.parse_args()
    return args


# string containing key words to decide if a transaction is to be considered for
# profit loss calculation
profit_loss = ["bought", "sold"]
investment = ["funding", "wire"]


class transaction_finder:
    def __init__(self, in_file):
        self.in_f = in_file
        self.profit_l = 0.0
        self.first_date = ""
        self.total_inv = 0.0

    def str_find(self, s, key):
        for i in key:
            if ((s.lower()).find(i)) != -1:
                return True
        return False

    def is_profit_loss(self, s):
        return self.str_find(s, profit_loss)

    def is_investment(self, s):
        return self.str_find(s, investment)

    def parse_transactions(self):
        with open(self.in_f, "r") as csv_file:
            csvHandler = csv.DictReader(csv_file)
            loopCount = 0
            first_trade = True
            for row in csvHandler:
                desc = row["DESCRIPTION"]
                if not desc:
                    continue
                # print(f"Processing {loopCount} {desc}")
                if self.is_profit_loss(desc):
                    if first_trade:
                        self.first_date = row["DATE"]
                        first_trade = False
                    self.profit_l += float(row["AMOUNT"])
                elif self.is_investment(desc):
                    self.total_inv += float(row["AMOUNT"])
                loopCount += 1

    def get_tot_profit_loss(self):

        self.total_per_profit = (100 * self.profit_l) / self.total_inv
        return self.total_per_profit

    def cal_profit_per_year(self):
        None
        # date_format = "%m/%d/%Y"
        # d1 = datetime.today()
        # d2 = datetime.strptime(first_date, date_format)
        # delta = d1 - d2
        # per_profit = (365 * profit_l) / delta.days


if __name__ == "__main__":
    args = parse_args()
    tx_parser = transaction_finder(args.infile)
    tx_parser.parse_transactions()
    print("total profit/loss till date ($): ", "%.2f" % tx_parser.profit_l)
    print("date of first investment: ", tx_parser.first_date)
    print(
        "percentage profit: ", tx_parser.get_tot_profit_loss(),
    )
