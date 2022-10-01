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

# keep the end date always one ahead of the current date to retrieve
# every transaction to date


# for each access token supplied, map the institution name to that token

for transaction in connection.get_transactions("2022-09-20"):
    name = transaction['name'] if transaction['merchant_name'] is None \
        else transaction['merchant_name']
    print(transaction['date'], name, transaction['amount'])
    # print(transaction['category'], name)
print()
