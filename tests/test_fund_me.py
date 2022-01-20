import pytest
from scripts.helpful_scripts import get_account, local_environments
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions

def test_can_fund_and_withdraw():

    account = get_account()
    fund_me = deploy_fund_me()

    #adding +100 just in case we need a little bit more fee
    entrance_fee = fund_me.getEntranceFee() + 100

    # Fund TEST
    tx = fund_me.fund({"from":account, "value":entrance_fee})
    tx.wait(1) #wait 1 block.
    assert(fund_me.addressToAmountFunded(account.address) == entrance_fee)

    # Withdraw TEST
    tx2 = fund_me.withdraw({"from":account})
    tx2.wait(1)
    assert(fund_me.addressToAmountFunded(account.address) == 0)

def test_owner_withdraw():
    # Owner withdraw test
    if network.show_active() not in local_environments:
        pytest.skip("We will only test if network is local")

    #deploying.
    fund_me = deploy_fund_me()

    #adding a blank random account.
    bad_actor = accounts.add()
    
    #IMPORTANT -We're saying: "if we call the withdraw function from bad_actor it's ok if transaction reverts."
    # si llamo a withdraw desde bad_actor, me tiene que tirar la excepción para pasar el test.
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from":bad_actor})
    
    
