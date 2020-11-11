import pytest
import brownie

from brownie import Wei


def test_should_not_harvest_not_tend(deployer, genericKeeper, strategy):
    genericKeeper.addHarvestStrategy(strategy, 60)
    genericKeeper.addTendStrategy(strategy, 10)
    strategy.setShouldHarvest(False)
    strategy.setShouldTend(False)
    assert genericKeeper.harvestable(strategy) == False
    assert genericKeeper.tendable(strategy) == False


def test_should_harvest_and_tend(deployer, genericKeeper, strategy, keeper, rando):
    genericKeeper.addHarvestStrategy(strategy, 60)
    genericKeeper.addTendStrategy(strategy, 10)
    strategy.setShouldHarvest(True)
    strategy.setShouldTend(True)
    assert genericKeeper.harvestable(strategy) == True
    assert genericKeeper.tendable(strategy) == True

    # Only keepers should be able to harvest
    with brownie.reverts():
        genericKeeper.harvest(strategy, {"from": rando})

    # Only keepers should be able to tend
    with brownie.reverts():
        genericKeeper.tend(strategy, {"from": rando})

    tx = genericKeeper.harvest(strategy, {"from": keeper})
    assert "HarvestedByKeeper" in tx.events

    tx = genericKeeper.tend(strategy, {"from": keeper})
    assert "TendedByKeeper" in tx.events
