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

for transaction in connection.get_transactions(start_date):
    name = transaction['name'] if transaction['merchant_name'] is None \
        else transaction['merchant_name']

    print(
        transaction['institution'],
        transaction['date'],
        name,
        transaction['amount']
    )
