import pytest
import brownie

from brownie import Wei


def test_adding_should_emit_event(deployer, genericKeeper, strategy):
    tx = genericKeeper.addStrategy(strategy, 60, 10)
    assert "HarvestStrategyAdded" in tx.events
    assert "TendStrategyAdded" in tx.events


def test_modifying_should_emit_event(deployer, genericKeeper, strategy):
    # Shouldn't be able to modify non existing strategies
    with brownie.reverts():
        genericKeeper.updateRequiredHarvestAmount(strategy, 1)
    with brownie.reverts():
        genericKeeper.updateRequiredTendAmount(strategy, 1)

    genericKeeper.addStrategy(strategy, 60, 10)

    tx = genericKeeper.updateRequiredHarvestAmount(strategy, 1)
    assert "HarvestStrategyModified" in tx.events

    tx = genericKeeper.updateRequiredTendAmount(strategy, 2)
    assert "TendStrategyModified" in tx.events


def test_removing_should_emit_event(deployer, genericKeeper, strategy):
    # Shouldn't be able to remove non existing strategies
    with brownie.reverts():
        genericKeeper.removeHarvestStrategy(strategy)
    with brownie.reverts():
        genericKeeper.removeTendStrategy(strategy)

    genericKeeper.addStrategy(strategy, 60, 10)
    tx = genericKeeper.removeHarvestStrategy(strategy)
    assert "HarvestStrategyRemoved" in tx.events

    tx = genericKeeper.removeTendStrategy(strategy)
    assert "TendStrategyRemoved" in tx.events


def test_should_not_allow_duplicates(deployer, genericKeeper, strategy):
    genericKeeper.addStrategy(strategy, 60, 10)
    with brownie.reverts():
        genericKeeper.addStrategy(strategy, 60, 0)

    with brownie.reverts():
        genericKeeper.addStrategy(strategy, 0, 10)


def test_removed_strategy_should_revert_workable_actions(
    deployer, genericKeeper, strategy, keeper, rando
):
    genericKeeper.addStrategy(strategy, 60, 10)

    strategy.setShouldHarvest(True)
    strategy.setShouldTend(True)

    genericKeeper.removeHarvestStrategy(strategy)
    genericKeeper.removeTendStrategy(strategy)

    with brownie.reverts():
        genericKeeper.harvestable(strategy)

    with brownie.reverts():
        genericKeeper.tendable(strategy)
