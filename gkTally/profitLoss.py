import csv
import argparse
from datetime import datetime


def parseArgs():
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
profitLossIncludeList = ["bought", "sold"]
# exclude list - transations that needs to be excluded
excludeList = ["Bought 100 AAPL"]
# Investment List - transactions that needs to be considered as investment
investmentList = ["funding", "wire"]


class transactionFinder:
    def __init__(self, in_file):
        self.in_f = in_file
        self.profitL = 0.0
        self.firstDate = ""
        self.totalInv = 0.0

    def strFind(self, s, key):
        for i in key:
            if ((s.lower()).find(i.lower())) != -1:
                return True
        return False

    def isProfitLoss(self, s):
        return self.strFind(s, profitLossIncludeList) and (
            not self.strFind(s, excludeList)
        )

    def isInvestment(self, s):
        return self.strFind(s, investmentList)

    def parseTransactions(self):
        with open(self.in_f, "r") as csv_file:
            csvHandler = csv.DictReader(csv_file)
            loopCount = 0
            for row in csvHandler:
                desc = row["DESCRIPTION"]
                if not desc:
                    continue
                # print(f"Processing {loopCount} {desc}")
                if self.isProfitLoss(desc):
                    if self.firstDate == "":
                        self.firstDate = row["DATE"]
                    self.profitL += float(row["AMOUNT"])

                elif self.isInvestment(desc):
                    self.totalInv += float(row["AMOUNT"])
                loopCount += 1

    def getTotProfitLoss(self):

        self.total_per_profit = (100 * self.profitL) / self.totalInv
        return self.total_per_profit

    def calProfitPerYear(self):
        None
        # date_format = "%m/%d/%Y"
        # d1 = datetime.today()
        # d2 = datetime.strptime(firstDate, date_format)
        # delta = d1 - d2
        # per_profit = (365 * profitL) / delta.days


if __name__ == "__main__":
    args = parseArgs()
    tx_parser = transactionFinder(args.infile)
    tx_parser.parseTransactions()
    print(f"total profit/loss till date ($): {tx_parser.profitL:.2f}")
    print("date of first investment: ", tx_parser.firstDate)
    print(f"percentage profit:{tx_parser.getTotProfitLoss():.2f}")
