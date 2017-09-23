"""
This is the module for data library
"""

import csv


def stocks_info_from_exchanges():
    """
    Read basic stock info from csv file downloaded from exchanges
    """

    exchanges = ["NYSE", "NASDAQ", "AMEX"]
    stockinfo = dict()

    for exchange in exchanges:
        filename = "datafile\\" + exchange + ".csv"
        symbols = []
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                symbols.append(row.copy())
                stockinfo[exchange] = symbols
    return stockinfo


def test():
    """Testing Docstring"""
    pass

if __name__=='__main__':
    test()
