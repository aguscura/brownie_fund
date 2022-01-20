# When importing contracts, we use the name of the contract - NOT THE NAME OF THE FILE .sol 

from ast import IsNot
from brownie import FundMe, MockV3Aggregator, config, network
from scripts.helpful_scripts import deploy_mock_aggregator, get_account, local_environments

def deploy_fund_me():

    print("*************************")

    account = get_account()
    print(f"The active network is {network.show_active()}")
    
    #IMPORTANT - below code runs in a persistant network, rinkeby in this case
    #To VERIFY it in Etherscan we need to make it public (public_source)
    #The PriceFeed contract need to be a parameter now (we set the PriceFeed variable in the Constructor)
    #So, at the time of deploying, we are setting the PriceFeed contract.
    #But we will deploy this only 1 time. Once the mock is deployed we don't need to deploy it again.
    
    if network.show_active() not in local_environments:
            price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else: 
        if len(MockV3Aggregator) <= 0:
            deploy_mock_aggregator()

        price_feed_address = MockV3Aggregator[-1].address # [-1] is the most recent contract deployed. 

    fund_me = FundMe.deploy(
                            price_feed_address,
                            {"from":account}, 
                            publish_source=config["networks"][network.show_active()]["verify"]
                            )

    #La f antes del print es porque imprimimos una variable luego.
    print(f"Contract deployed to {fund_me.address}")
    return fund_me 

def main():
    deploy_fund_me()

