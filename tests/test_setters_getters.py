import pytest
from brownie import Wei


def test_initial_values(deployer, genericKeeper):
    genericKeeper.name() == "Generic Vault V2 Strategy Keep3r"
    genericKeeper.governor() == deployer
