import pytest
import brownie

from brownie import Wei


def test_should_not_harvest(deployer, genericKeeper, strategy):
    genericKeeper.addHarvestStrategy(strategy, 60)
    strategy.setShouldHarvest(False)
    assert genericKeeper.harvestable(strategy) == False


def test_should_harvest(deployer, genericKeeper, strategy, keeper, rando):
    genericKeeper.addHarvestStrategy(strategy, 60)
    strategy.setShouldHarvest(True)
    assert genericKeeper.harvestable(strategy) == True

    # Only keepers should be able to harvest
    with brownie.reverts():
        genericKeeper.harvest(strategy, {"from": rando})

    tx = genericKeeper.harvest(strategy, {"from": keeper})
    assert "HarvestedByKeeper" in tx.events


def test_harvest_when_not_harvestable(deployer, genericKeeper, strategy, keeper):
    genericKeeper.addHarvestStrategy(strategy, 60)
    strategy.setShouldHarvest(False)
    with brownie.reverts():
        genericKeeper.harvest(strategy, {"from": keeper})
