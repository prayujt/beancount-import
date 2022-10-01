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


beancount_file = open('transactions.beancount', 'w')

for transaction in connection.get_transactions(start_date):
    name = transaction['name'] if transaction['merchant_name'] is None \
        else transaction['merchant_name']

    print(
        transaction['institution'],
        transaction['date'],
        name,
        transaction['amount']
    )
    line1 = "{0} * \"{1}\"\n".format(start_date, name)
    line2 = "\tAssets:BoA:Checking\t-{0} USD\n".format(transaction['amount'])
    line3 = "\t Expenses:General\t{0} USD\n".format(transaction['amount'])
    beancount_file.write(line1)
    beancount_file.write(line2)
    beancount_file.write(line3)

beancount_file.close()
