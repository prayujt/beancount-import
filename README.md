# Plaid Sync
This repository will utilize the Plaid API to generate [beancount](https://github.com/beancount/beancount) files to automate the process of tracking personal expenses from both bank accounts and credit cards. Using the API, we can easily get transaction information, categorize transactions by their type (eg. restaurants, groceries, etc..), and synchronize this information across multiple types of accounts into one beancount file.

## Setup
Requires a .env file within the main directory to be set with the following environment variables:
* `CLIENT_ID` -> Plaid API application client ID
* `SECRET` -> Plaid API application secret for development mode
* `ACCESS_TOKENS` -> Access tokens for Plaid links (more detail below)
* `START_DATE` -> Date to begin tracking transactions (%Y-%m-%d)

To retrieve the access tokens for linked accounts, clone [Plaid's Quickstart](https://github.com/plaid/quickstart) repository, and follow the instructions in the README to link your accounts and get access tokens.

