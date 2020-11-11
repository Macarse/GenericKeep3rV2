import pytest
import brownie

from brownie import Wei


def test_should_not_tend(deployer, genericKeeper, strategy):
    genericKeeper.addTendStrategy(strategy, 10)
    strategy.setShouldTend(False)
    assert genericKeeper.tendable(strategy) == False


def test_should_harvest(deployer, genericKeeper, strategy, keeper, rando):
    genericKeeper.addTendStrategy(strategy, 10)
    strategy.setShouldTend(True)
    assert genericKeeper.tendable(strategy) == True

    # Only keepers should be able to tend
    with brownie.reverts():
        genericKeeper.tend(strategy, {"from": rando})

    tx = genericKeeper.tend(strategy, {"from": keeper})
    assert "TendedByKeeper" in tx.events


def test_tend_when_not_tendable(deployer, genericKeeper, strategy, keeper):
    genericKeeper.addTendStrategy(strategy, 10)
    strategy.setShouldTend(False)
    with brownie.reverts():
        genericKeeper.tend(strategy, {"from": keeper})
