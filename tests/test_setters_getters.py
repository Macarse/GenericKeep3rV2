import pytest
import brownie


def test_initial_values(deployer, genericKeeper, keep3r):
    genericKeeper.name() == "Generic Vault V2 Strategy Keep3r"
    genericKeeper.governor() == deployer
    genericKeeper.keep3r() == keep3r


def test_add_strategy_should_have_harvest_or_tend(deployer, genericKeeper, strategy):
    with brownie.reverts():
        genericKeeper.addStrategy(strategy, 0, 0)
