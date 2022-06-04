import csv
import sys
import time
from etherscan.accounts import Account
import datetime
import dateutil.parser
import requests
import json
import argparse


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


parser = argparse.ArgumentParser()
parser.add_argument(
    "--verbose", help="increase output verbosity for debugging", action="store_true")
parser.add_argument("--sample", help="file containing sample contracts")
args = parser.parse_args()
verbose = args.verbose
if (not args.sample):
    ponzi_file = "./data/others/ponzi.csv"
else:
    ponzi_file = args.sample


# %%
key = "Y7ZP1HMWF1HTTB6EMAUYZDFF8RKQTVJHTU"
ponzi = []
starting_date = datetime.datetime.strptime("2015-08-30", "%Y-%m-%d")
filename_price = './data/others/ether_price.csv'
prices = {}


# %%
# in tx = number of input transactions
# out tx = number of output transactions
# in eth = amount of incoming ETH
# out eth = amount of outgoing ETH
# in usd = amount of incoming USD
# out usd = amount of outgoing USD
# paying = number of distinct addresses sending ETH
# paid = number of distinct addresses receiving ETH
# date 1st tx = date of the first transaction
# date last tx = date of the last transaction
print("Address, In Tx, Out Tx, In ETH, Out ETH, In USD, Out USD, Paying, Paid, date 1st tx, date last tx")
with open(filename_price, mode='r') as price_file:
    if (verbose):
        print("Retrieving exchange rates... ", end=" ")
    sys.stdout.flush()

    csv_reader = csv.DictReader(price_file)
    for row in csv_reader:
        dlong = dateutil.parser.parse(row['Date(UTC)'])
        date = dlong.strftime('%Y-%m-%d')
        prices[date] = float(row['Value'])
    if (verbose):
        print("done (last date ", date, ")")


def get_exchangerate(date):
    if date in prices:
        return prices[date]
    else:
        urll = 'https://api.coingecko.com/api/v3/coins/ethereum/history?date='
        dlong = dateutil.parser.parse(date)
        date = dlong.strftime('%d-%m-%Y')
        try:
            url = urll+date
            resp = requests.get(url)
            json_file = json.loads(resp.text)
            json_prices = json_file['market_data']
            json_current_prices = json_prices['current_price']
            json_current_usd = json_current_prices['usd']
            # print(json_current_usd,date)
        except:
            print("JSON format error", url)
            exit(-1)
            return 0
        prices[date] = json_current_usd
        # print(date,prices[date])
        return json_current_usd


# %%
with open(ponzi_file) as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        addr = row[0]
        ponzi.append(addr)

for addr in ponzi:
    if (verbose):
        print("Retrieving transactions of contract ", addr, "... ", end=" ")
    sys.stdout.flush()
    api = Account(address=addr, api_key=key)
    text = api.get_transaction_page(internal=False, page=1, offset=10000)
    tint = api.get_transaction_page(internal=True, page=1, offset=10000)
    if (verbose):
        print("done")

    count_text = 0
    count_tint = 0
    eth_text = 0
    eth_tint = 0
    usd_text = 0
    usd_tint = 0
    users_text = set()
    users_tint = set()
    date_first_tx = ''
    date_last_tx = ''

    if (verbose):
        print("External transactions")
    for t in text:
        if (t['isError'] == '0'):
            rawdate = datetime.datetime.fromtimestamp(int(t['timeStamp']))
            date = rawdate.strftime('%Y-%m-%d')
            if (rawdate < starting_date):
                date = starting_date.strftime('%Y-%m-%d')
            if (date_first_tx == ''):
                date_first_tx = date
            eth_text += int(t['value'])
            usd_text += int(t['value']) * (10 ** -18) * get_exchangerate(date)
            if (int(t['value']) > 0):
                users_text |= {t['from']}
            count_text += 1
        if (verbose):
            s = 'from: ' + t['from'] + ',' + 'to: ' + t['to'] + ', eth: ' + str(float(
                t['value']) * 10 ** -18) + ', block: ' + t['blockNumber'] + ', isError : ' + t['isError']
            print(s)

    if (verbose):
        print("Internal transactions")
    for t in tint:
        if (t['isError'] != '0'):
            continue
        rawdate = datetime.datetime.fromtimestamp(int(t['timeStamp']))
        date = rawdate.strftime('%Y-%m-%d')
        if (rawdate < starting_date):
            date = starting_date.strftime('%Y-%m-%d')
        if (t['from'] == addr):  # internal transaction from contract to t['to']
            eth_tint += int(t['value'])
            usd_tint += int(t['value']) * (10 ** -18) * get_exchangerate(date)
            count_tint += 1
            if (int(t['value']) > 0):
                users_tint |= {t['to']}
        elif (t['to'] == addr):  # internal transaction from t['from'] to contract
            eth_text += int(t['value'])
            usd_text += int(t['value']) * (10 ** -18) * get_exchangerate(date)
            count_text += 1
            if (int(t['value']) > 0):
                users_text |= {t['from']}
        if (verbose):
            s = 'from: ' + t['from'] + ',' + 'to: ' + t['to'] + ', eth: ' + str(float(
                t['value']) * 10 ** -18) + ',' + t['blockNumber'] + ', isError : ' + t['isError']
            print(s)

    if (text):
        date_first_text = datetime.datetime.fromtimestamp(
            int(text[0]['timeStamp'])).strftime('%Y-%m-%d')
        date_last_text = datetime.datetime.fromtimestamp(
            int(text[-1]['timeStamp'])).strftime('%Y-%m-%d')

        if (tint):
            date_first_tint = datetime.datetime.fromtimestamp(
                int(tint[0]['timeStamp'])).strftime('%Y-%m-%d')
            date_last_tint = datetime.datetime.fromtimestamp(
                int(tint[-1]['timeStamp'])).strftime('%Y-%m-%d')

            if (date_first_tint < date_first_text):
                date_first_tx = date_first_tint
            else:
                date_first_tx = date_first_text

            if (date_last_tint > date_last_text):
                date_last_tx = date_last_tint
            else:
                date_last_tx = date_last_text
        else:
            date_first_tx = date_first_text
            date_last_tx = date_last_text

    s = addr + ','
    # External transactions
    s += str(count_text) + ','
    # External transactions
    s += str(count_tint) + ','
    # External ETH
    s += str(float(eth_text) * (10 ** -18)) + ','
    # Internal ETH
    s += str(float(eth_tint) * (10 ** -18)) + ','
    # External USD
    s += str(float(usd_text)) + ','
    # Internal USD
    s += str(float(usd_tint)) + ','
    # Paying
    s += str(len(users_text)) + ','
    # Paid
    s += str(len(users_tint)) + ','
    # Date first transaction
    s += str(date_first_tx) + ','
    # Date last transaction
    s += str(date_last_tx)

    print(s)
