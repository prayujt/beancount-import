#!/usr/bin/env python3

from dotenv import dotenv_values
from datetime import datetime, timedelta

import plaid
from plaid.api import plaid_api

from plaid.model.country_code import CountryCode

from plaid.model.transactions_get_request_options \
    import TransactionsGetRequestOptions
from plaid.model.transactions_get_request import TransactionsGetRequest

from plaid.model.accounts_get_request import AccountsGetRequest

from plaid.model.institutions_get_by_id_request \
    import InstitutionsGetByIdRequest

config = dotenv_values()

access_tokens = {}

configuration = plaid.Configuration(
    host=plaid.Environment.Development,
    api_key={
        'clientId': config["CLIENT_ID"],
        'secret': config["SECRET"],
    }
)

start_date = config["START_DATE"]

# keep the end date always one ahead of the current date to retrieve
# every transaction to date
end_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")


api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

# for each access token supplied, map the institution name to that token
for token in config["ACCESS_TOKENS"].split(' '):
    request = AccountsGetRequest(access_token=token)
    response = client.accounts_get(request)
    institution_id = response['item']['institution_id']
    request = InstitutionsGetByIdRequest(
        institution_id=institution_id,
        country_codes=[CountryCode("US")],
    )
    response = client.institutions_get_by_id(request)
    access_tokens[response['institution']['name']] = token

for (institution, access_token) in access_tokens.items():
    print(institution + ":")
    request = TransactionsGetRequest(
        access_token=access_token,
        start_date=datetime.strptime(start_date, '%Y-%m-%d').date(),
        end_date=datetime.strptime(end_date, '%Y-%m-%d').date(),
    )
    response = client.transactions_get(request)
    transactions = response['transactions']

    while len(transactions) < response['total_transactions']:
        options = TransactionsGetRequestOptions()
        options.offset = len(transactions)

        request = TransactionsGetRequest(
            access_token=access_token,
            start_date=datetime.strptime(start_date, '%Y-%m-%d').date(),
            end_date=datetime.strptime(end_date, '%Y-%m-%d').date(),
            options=options
        )
        response = client.transactions_get(request)
        transactions += response['transactions']

    for transaction in transactions:
        name = transaction['name'] if transaction['merchant_name'] is None \
            else transaction['merchant_name']
        print(transaction['date'], name, transaction['amount'])
    print()
