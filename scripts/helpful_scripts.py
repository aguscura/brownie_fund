from brownie import network, config, accounts, MockV3Aggregator 
from web3 import Web3

decimals = 8
starting_price = 200000000


#forked environments
forked_environments = ["mainnet-fork", "mainnet-fork-dev"]

#ganache-local is a network in "Ethereum" part where the contracts won't be deleted automaticaly.
local_environments = ["development", "ganache-local"]

def get_account():
    if (network.show_active() in local_environments or network.show_active() in forked_environments):
        return accounts[0]
    else: 
        return accounts.add(config["wallets"]["from_key"])


def deploy_mock_aggregator():
    print("Deploying mocks...")
    #IMPORTANT - Here, "MockV3Aggregator" is a list with all the Mock contracts.
    #We add the parameters that constructor needs.
    MockV3Aggregator.deploy(decimals, starting_price, {"from":get_account()})
    print("Mocks deployed!")