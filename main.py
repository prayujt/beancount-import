#!/usr/bin/env python3

from dotenv import dotenv_values
from connection import Connection

config = dotenv_values()

start_date = config["START_DATE"]

connection = Connection(
    config["ACCESS_TOKENS"],
    config["CLIENT_ID"],
    config["SECRET"]
)

banks = {
    "Bank of America": "BoA",
}
credit_cards = {
    "Chase": "Chase",
    "Discover": "Discover",
}

beancount_file = open('transactions.beancount', 'w')

# TODO Find way to open categories before retrieving transactions
beancount_file.write("{0} open Expenses:General\n".format(start_date))

for institution in connection.access_tokens.keys():
    if institution in banks:
        beancount_file.write("{0} open Assets:{1}\n".format(
            start_date,
            banks[institution] + ":Checking"
        ))
    else:
        beancount_file.write("{0} open Liabilities:Credit:{1}\n".format(
            start_date,
            credit_cards[institution]
        ))

for transaction in connection.get_transactions(start_date):
    name = transaction['name'] if transaction['merchant_name'] is None \
        else transaction['merchant_name']

    print(
        transaction['institution'],
        transaction['date'],
        name,
        transaction['amount']
    )
    line1 = "{0} * \"{1}\"\n".format(transaction['date'], name)
    line2 = "\t{0}:{1}\t-{2} USD\n".format(
        "Assets" if transaction['institution'] in banks.keys()
            else "Liabilities:Credit",
        banks[transaction['institution']] + ":Checking"
            if transaction['institution'] in banks.keys()
        else credit_cards[transaction['institution']],
        transaction['amount']
    )
    line3 = "\tExpenses:General\t{0} USD\n".format(transaction['amount'])
    beancount_file.write(line1)
    beancount_file.write(line2)
    beancount_file.write(line3)

beancount_file.close()
