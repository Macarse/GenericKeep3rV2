import pytest
import brownie


def test_harvest_only(deployer, genericKeeper, MockStrategy, vault):
    strategies = [deployer.deploy(MockStrategy, vault) for _ in range(3)]
    [genericKeeper.addStrategy(s, 60, 0) for s in strategies]

    assert strategies == genericKeeper.strategies()


def test_tend_only(deployer, genericKeeper, MockStrategy, vault):
    strategies = [deployer.deploy(MockStrategy, vault) for _ in range(3)]
    [genericKeeper.addStrategy(s, 0, 10) for s in strategies]

    assert strategies == genericKeeper.strategies()


def test_harvest_tend(deployer, genericKeeper, MockStrategy, vault):
    strategies = [deployer.deploy(MockStrategy, vault) for _ in range(3)]
    [genericKeeper.addStrategy(s, 10, 10) for s in strategies]

    assert strategies == genericKeeper.strategies()
