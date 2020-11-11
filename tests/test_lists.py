import pytest
import brownie

from brownie import Wei


def test_adding_should_emit_event(deployer, genericKeeper, strategy):
    tx = genericKeeper.addHarvestStrategy(strategy, 60)
    assert "HarvestStrategyAdded" in tx.events

    tx = genericKeeper.addTendStrategy(strategy, 10)
    assert "TendStrategyAdded" in tx.events


def test_modifying_should_emit_event(deployer, genericKeeper, strategy):
    # Shouldn't be able to modify non existing strategies
    with brownie.reverts():
        genericKeeper.updateRequiredHarvestAmount(strategy, 1)

    genericKeeper.addHarvestStrategy(strategy, 60)
    tx = genericKeeper.updateRequiredHarvestAmount(strategy, 1)
    assert "HarvestStrategyModified" in tx.events

    # Shouldn't be able to modify non existing strategies
    with brownie.reverts():
        genericKeeper.updateRequiredTendAmount(strategy, 1)

    genericKeeper.addTendStrategy(strategy, 10)
    tx = genericKeeper.updateRequiredTendAmount(strategy, 2)
    assert "TendStrategyModified" in tx.events


def test_removing_should_emit_event(deployer, genericKeeper, strategy):
    # Shouldn't be able to remove non existing strategies
    with brownie.reverts():
        genericKeeper.removeHarvestStrategy(strategy)

    genericKeeper.addHarvestStrategy(strategy, 60)
    tx = genericKeeper.removeHarvestStrategy(strategy)
    assert "HarvestStrategyRemoved" in tx.events

    # Shouldn't be able to remove non existing strategies
    with brownie.reverts():
        genericKeeper.removeTendStrategy(strategy)

    genericKeeper.addTendStrategy(strategy, 10)
    tx = genericKeeper.removeTendStrategy(strategy)
    assert "TendStrategyRemoved" in tx.events


def test_should_not_allow_duplicates(deployer, genericKeeper, strategy):
    genericKeeper.addHarvestStrategy(strategy, 60)
    with brownie.reverts():
        genericKeeper.addHarvestStrategy(strategy, 60)

    genericKeeper.addTendStrategy(strategy, 10)
    with brownie.reverts():
        genericKeeper.addTendStrategy(strategy, 10)


def test_removed_strategy_should_revert_workable_actions(
    deployer, genericKeeper, strategy, keeper, rando
):
    genericKeeper.addHarvestStrategy(strategy, 60)
    genericKeeper.addTendStrategy(strategy, 10)

    strategy.setShouldHarvest(True)
    strategy.setShouldTend(True)

    genericKeeper.removeHarvestStrategy(strategy)
    genericKeeper.removeTendStrategy(strategy)

    with brownie.reverts():
        genericKeeper.harvestable(strategy)

    with brownie.reverts():
        genericKeeper.tendable(strategy)
