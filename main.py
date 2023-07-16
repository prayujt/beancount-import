#!/usr/bin/env python3

from dotenv import dotenv_values
from connection import Connection
import json

config = dotenv_values()

start_date = config["START_DATE"]

connection = Connection(
    config["ACCESS_TOKENS"],
    config["CLIENT_ID"],
    config["SECRET"]
)

custom_categories_file = open('accounts.json', 'r')
custom_categories = json.loads(custom_categories_file.read())

custom_accounts = custom_categories['accounts']
categories = custom_categories['categories']

beancount_file = open('transactions.beancount', 'w')

# TODO Find way to open categories before retrieving transactions
open_categories = set()
text = ""

for institution in connection.access_tokens.keys():
    accounts = connection.get_accounts(institution)
    for account in accounts:
        account_name = [acc['alias'] for acc in custom_accounts[institution]['accounts'] if acc['mask'] == account['mask']][0]
        if account['type'].value == 'credit':
            text += f"{start_date} open {'Liabilities:Credit'}:{custom_accounts[institution]['alias']}:{account_name}\n"
        elif account['type'].value == 'depository':
            text += f"{start_date} open {'Assets'}:{custom_accounts[institution]['alias']}:{account_name}\n"
text += '\n'

# for transaction in connection.get_transactions(start_date):
#     name = transaction['name'] if transaction['merchant_name'] is None \
#         else transaction['merchant_name']

#     print(
#         transaction['institution'],
#         transaction['date'],
#         name,
#         transaction['amount'],
#         transaction['category']
#     )
#     line1 = "{0} * \"{1}\"\n".format(transaction['date'], name)
#     line2 = "\t{0}:{1}\t{2} USD\n".format(
#         "Assets" if transaction['institution'] in banks.keys()
#             else "Liabilities:Credit",
#         banks[transaction['institution']] + ":Checking"
#             if transaction['institution'] in banks.keys()
#         else credit_cards[transaction['institution']],
#         transaction['amount']
#     )
#     possible_categories = {}
#     for category in transaction['category']:
#         if category in categories:
#             possible_categories[categories[category]] = \
#                 possible_categories.get(categories[category], 1)
#             open_categories.add(categories[category])
#         else:
#             possible_categories['General'] = \
#                 possible_categories.get('General', 1)
#             open_categories.add('General')

#     category = max(possible_categories, key=possible_categories.get)
#     line3 = "\tExpenses:{0}\t{1} USD\n".format(
#         category,
#         0 - transaction['amount']
#     )

#     text += line1 + line2 + line3 + '\n'

# for category in open_categories:
#     text = "{0} open Expenses:{1}\n".format(start_date, category) + text

beancount_file.write(text)
beancount_file.close()
