// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.6.8;

import "@openzeppelinV3/contracts/token/ERC20/IERC20.sol";
import "@openzeppelinV3/contracts/math/SafeMath.sol";
import "@openzeppelinV3/contracts/math/SafeMath.sol";
import {BaseStrategy} from "@yearnvaults/contracts/BaseStrategy.sol";

/*
 * MockStrategy
 */

contract MockStrategy is BaseStrategy {
    using SafeMath for uint256;

    bool public shouldHarvest;
    bool public shouldTend;

    constructor(address _vault) public BaseStrategy(_vault) {
        shouldHarvest = true;
        shouldTend = true;
    }

    function setShouldHarvest(bool _shouldHarvest) public {
        shouldHarvest = _shouldHarvest;
    }

    function setShouldTend(bool _shouldTend) public {
        shouldTend = _shouldTend;
    }

    function name() external pure override returns (string memory) {
        return "MockStrategy";
    }

    function estimatedTotalAssets() public view override returns (uint256) {
        return 0;
    }

    function prepareReturn(uint256 _debtOutstanding) internal override returns (uint256 _profit) {
        return 0;
    }

    function adjustPosition(uint256 _debtOutstanding) internal override {}

    function exitPosition() internal override {}

    function tendTrigger(uint256 callCost) public view override returns (bool) {
        return shouldTend;
    }

    function harvestTrigger(uint256 callCost) public view override returns (bool) {
        return shouldHarvest;
    }

    function liquidatePosition(uint256 _amountNeeded) internal override returns (uint256 _amountFreed) {
        return 0;
    }

    function prepareMigration(address _newStrategy) internal override {}

    function protectedTokens() internal view override returns (address[] memory) {
        return new address[](0);
    }
}
