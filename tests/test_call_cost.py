import pytest
import brownie

from brownie import Wei


def test_harvest_call_cost(deployer, genericKeeper, strategy2):
    # Taking an example of gas cost from
    # https://etherscan.io/tx/0x88b7e6096b48e357494d1650ee18c002b0ae553bd28624863356c4b117164e93
    genericKeeper.addStrategy(strategy2, 351000, 0)

    strategy2.setAcceptableCallCost(Wei("0.03 ether"))
    assert genericKeeper.harvestable(strategy2) == True

    strategy2.setAcceptableCallCost(Wei("0.01 ether"))
    assert genericKeeper.harvestable(strategy2) == False


def test_tend_call_cost(deployer, genericKeeper, strategy2):
    # Taking an example of gas cost from
    # https://etherscan.io/tx/0x88b7e6096b48e357494d1650ee18c002b0ae553bd28624863356c4b117164e93
    genericKeeper.addStrategy(strategy2, 0, 351000)

    strategy2.setAcceptableCallCost(Wei("0.03 ether"))
    assert genericKeeper.tendable(strategy2) == True

    strategy2.setAcceptableCallCost(Wei("0.01 ether"))
    assert genericKeeper.tendable(strategy2) == False
