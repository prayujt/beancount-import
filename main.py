#!/usr/bin/env python3

from dotenv import dotenv_values
import plaid
from plaid.api import plaid_api
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from datetime import datetime
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.model.transactions_get_request import TransactionsGetRequest

config = dotenv_values()

configuration = plaid.Configuration(
    host=plaid.Environment.Development,
    api_key={
        'clientId': config["CLIENT_ID"],
        'secret': config["SECRET"],
    }
)

access_token_discover = config["DISCOVER_ACCESS_TOKEN"]
access_token_boa = config["BOA_ACCESS_TOKEN"]

access_token = access_token_discover

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

# request = TransactionsSyncRequest(
#     access_token=access_token,
# )
# response = client.transactions_sync(request)
# transactions = response['added']
# print(response['next_cursor'])

# while (response['has_more']):
#     request = TransactionsSyncRequest(
#         access_token=access_token,
#         cursor=response['next_cursor']
#     )
#     response = client.transactions_sync(request)
#     transactions += response['added']

# for transaction in transactions:
    # print(transaction)
    # print(str(transaction['date']))

request = TransactionsGetRequest(
    access_token=access_token,
    start_date=datetime.strptime('2022-09-24', '%Y-%m-%d').date(),
    end_date=datetime.strptime('2050-12-01', '%Y-%m-%d').date(),
)
response = client.transactions_get(request)
transactions = response['transactions']

while len(transactions) < response['total_transactions']:
    options = TransactionsGetRequestOptions()
    options.offset = len(transactions)

    request = TransactionsGetRequest(
        access_token=access_token,
        start_date=datetime.strptime('2022-09-24', '%Y-%m-%d').date(),
        end_date=datetime.strptime('2050-12-01', '%Y-%m-%d').date(),
        options=options
    )
    response = client.transactions_get(request)
    transactions += response['transactions']

for transaction in transactions:
    print(transaction['date'])
