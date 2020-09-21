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
# cash flow calculation
cashFlowIncludeKeys = ["put", "call"]

# Investment List - transactions that needs to be considered as investment
investmenKeys = ["funding", "wire"]


class transactionFinder:
    def __init__(self, in_file):
        self.in_f = in_file
        self.cashFlow = 0.0
        self.firstDate = ""
        self.totalInv = 0.0
        self.taxrate = 25

    def strFind(self, s, key):
        for i in key:
            if ((s.lower()).find(i.lower())) != -1:
                return True
        return False

    def isTxCashFlow(self, s):
        return self.strFind(s, cashFlowIncludeKeys)

    def isInvestment(self, s):
        return self.strFind(s, investmenKeys)

    def getCashflowTax(self):
        return self.cashFlow - ((self.cashFlow * self.taxrate) / 100)

    def parseInvestment(self, r):
        if r["DESCRIPTION"]:
            if self.isInvestment(r["DESCRIPTION"]):
                self.totalInv += float(r["AMOUNT"])

    def parseCashFlow(self, r):
        if r["SYMBOL"]:
            if self.isTxCashFlow(r["SYMBOL"]):
                self.cashFlow += float(r["AMOUNT"])
                if self.firstDate == "":
                    self.firstDate = r["DATE"]

    def parseTransactions(self):
        with open(self.in_f, "r") as csv_file:
            csvHandler = csv.DictReader(csv_file)
            for row in csvHandler:
                self.parseCashFlow(row)
                self.parseInvestment(row)

    def getTotcashFlowPer(self):
        return (100 * self.cashFlow) / self.totalInv

    def getTotcashFlowPerTax(self):
        return (100 * self.getCashflowTax()) / self.totalInv

    def calProfitPerYear(self):
        None
        # date_format = "%m/%d/%Y"
        # d1 = datetime.today()
        # d2 = datetime.strptime(firstDate, date_format)
        # delta = d1 - d2
        # per_profit = (365 * cashFlow) / delta.days


if __name__ == "__main__":
    args = parseArgs()
    tx_parser = transactionFinder(args.infile)
    tx_parser.parseTransactions()
    print(
        f"total cash flow till date in $:"
        f"{tx_parser.cashFlow:.2f}, "
        f"after tax - {tx_parser.getCashflowTax():.2f}"
    )
    print(
        f"percentage profit % :{tx_parser.getTotcashFlowPer():.2f},"
        f"after tax:{tx_parser.getTotcashFlowPerTax():.2f} "
    )
    print("date of first investment: ", tx_parser.firstDate)
