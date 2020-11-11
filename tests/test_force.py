import pytest
import brownie

from brownie import Wei


def test_force_calls(deployer, genericKeeper, strategy, rando):
    genericKeeper.addHarvestStrategy(strategy, 60)
    genericKeeper.addTendStrategy(strategy, 10)

    # Rando can't call force
    with brownie.reverts():
        genericKeeper.forceHarvest(strategy, {"from": rando})

    with brownie.reverts():
        genericKeeper.forceTend(strategy, {"from": rando})

    tx = genericKeeper.forceHarvest(strategy, {"from": deployer})
    assert "HarvestedByGovernor" in tx.events

    tx = genericKeeper.forceTend(strategy, {"from": deployer})
    assert "TendedByGovernor" in tx.events
