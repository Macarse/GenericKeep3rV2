// SPDX-License-Identifier: MIT

pragma solidity >=0.6.8;

import "@openzeppelinV3/contracts/math/SafeMath.sol";

import "../../interfaces/Keep3r/IStrategyKeep3r.sol";
import "../../interfaces/yearn/IBaseStrategy.sol";

import "../utils/Governable.sol";
import "../utils/CollectableDust.sol";

import "./Keep3rAbstract.sol";

contract GenericKeep3rV2 is Governable, CollectableDust, Keep3r, IStrategyKeep3r {
    using SafeMath for uint256;

    mapping(address => uint256) public requiredHarvest;
    mapping(address => uint256) public requiredTend;

    constructor(address _keep3r) public Governable(msg.sender) CollectableDust() Keep3r(_keep3r) {}

    // Setters
    function addHarvestStrategy(address _strategy, uint256 _requiredHarvest) external override onlyGovernor {
        require(requiredHarvest[_strategy] == 0, "crv-strategy-keep3r::add-harvest-strategy:strategy-already-added");
        _setRequiredHarvest(_strategy, _requiredHarvest);
        emit HarvestStrategyAdded(_strategy, _requiredHarvest);
    }

    function addTendStrategy(address _strategy, uint256 _requiredTend) external override onlyGovernor {
        require(requiredTend[_strategy] == 0, "crv-strategy-keep3r::add-tend-strategy:strategy-already-added");
        _setRequiredTend(_strategy, _requiredTend);
        emit TendStrategyAdded(_strategy, _requiredTend);
    }

    function updateRequiredHarvestAmount(address _strategy, uint256 _requiredHarvest) external override onlyGovernor {
        require(requiredHarvest[_strategy] > 0, "crv-strategy-keep3r::update-required-harvest:strategy-not-added");
        _setRequiredHarvest(_strategy, _requiredHarvest);
        emit HarvestStrategyModified(_strategy, _requiredHarvest);
    }

    function updateRequiredTendAmount(address _strategy, uint256 _requiredTend) external override onlyGovernor {
        require(requiredTend[_strategy] > 0, "crv-strategy-keep3r::update-required-tend:strategy-not-added");
        _setRequiredTend(_strategy, _requiredTend);
        emit TendStrategyModified(_strategy, _requiredTend);
    }

    function removeHarvestStrategy(address _strategy) external override onlyGovernor {
        require(requiredHarvest[_strategy] > 0, "crv-strategy-keep3r::remove-harvest-strategy:strategy-not-added");
        requiredHarvest[_strategy] = 0;
        emit HarvestStrategyRemoved(_strategy);
    }

    function removeTendStrategy(address _strategy) external override onlyGovernor {
        require(requiredTend[_strategy] > 0, "crv-strategy-keep3r::remove-tend-strategy:strategy-not-added");
        requiredTend[_strategy] = 0;
        emit TendStrategyRemoved(_strategy);
    }

    function setKeep3r(address _keep3r) external override onlyGovernor {
        _setKeep3r(_keep3r);
        emit Keep3rSet(_keep3r);
    }

    function _setRequiredHarvest(address _strategy, uint256 _requiredHarvest) internal {
        require(_requiredHarvest > 0, "crv-strategy-keep3r::set-required-harvest:should-not-be-zero");
        requiredHarvest[_strategy] = _requiredHarvest;
    }

    function _setRequiredTend(address _strategy, uint256 _requiredTend) internal {
        require(_requiredTend > 0, "crv-strategy-keep3r::set-required-tend:should-not-be-zero");
        requiredTend[_strategy] = _requiredTend;
    }

    // Getters
    function name() external pure override returns (string memory) {
        return "Generic Vault V2 Strategy Keep3r";
    }

    function harvestable(address _strategy) public view override returns (bool) {
        require(requiredHarvest[_strategy] > 0, "crv-strategy-keep3r::harvestable:strategy-not-added");
        return IBaseStrategy(_strategy).harvestTrigger(requiredHarvest[_strategy]);
    }

    function tendable(address _strategy) public view override returns (bool) {
        require(requiredTend[_strategy] > 0, "crv-strategy-keep3r::tendable:strategy-not-added");
        return IBaseStrategy(_strategy).tendTrigger(requiredTend[_strategy]);
    }

    // Keep3r actions
    function harvest(address _strategy) external override paysKeeper {
        require(harvestable(_strategy), "crv-strategy-keep3r::harvest:not-workable");
        _harvest(_strategy);
        emit HarvestedByKeeper(_strategy);
    }

    function tend(address _strategy) external override paysKeeper {
        require(tendable(_strategy), "crv-strategy-keep3r::tend:not-workable");
        _tend(_strategy);
        emit TendedByKeeper(_strategy);
    }

    // Governor keeper bypass
    function forceHarvest(address _strategy) external override onlyGovernor {
        _harvest(_strategy);
        emit HarvestedByGovernor(_strategy);
    }

    function forceTend(address _strategy) external override onlyGovernor {
        _tend(_strategy);
        emit TendedByGovernor(_strategy);
    }

    function _harvest(address _strategy) internal {
        IBaseStrategy(_strategy).harvest();
    }

    function _tend(address _strategy) internal {
        IBaseStrategy(_strategy).tend();
    }

    // Governable
    function setPendingGovernor(address _pendingGovernor) external override onlyGovernor {
        _setPendingGovernor(_pendingGovernor);
    }

    function acceptGovernor() external override onlyPendingGovernor {
        _acceptGovernor();
    }

    // Collectable Dust
    function sendDust(
        address _to,
        address _token,
        uint256 _amount
    ) external override onlyGovernor {
        _sendDust(_to, _token, _amount);
    }
}
