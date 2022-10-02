# Beancount Importer
This repository will utilize the Plaid API to generate [beancount](https://github.com/beancount/beancount) files to automate the process of tracking personal expenses from both bank accounts and credit cards. Using the API, we can easily get transaction information, categorize transactions by their type (eg. restaurants, groceries, etc..), and synchronize this information across multiple types of accounts into one beancount file.

## Setup
Requires a .env file within the main directory to be set with the following environment variables (no quotation marks):
* `CLIENT_ID` -> Plaid API application client ID
* `SECRET` -> Plaid API application secret for development mode
* `ACCESS_TOKENS` -> Access tokens for Plaid links, separated by a space (more detail below)
* `START_DATE` -> Date to begin tracking transactions (%Y-%m-%d)

To retrieve the access tokens for linked accounts, clone [Plaid's Quickstart](https://github.com/plaid/quickstart) repository, and follow the instructions in the README to link your accounts and get access tokens. If you have more than one account, separate each access code with a space. The type of account that the access code refers to (eg. Discover, Chase) is determined by the API when connecting to the account.

