// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.6.8;

import "@openzeppelinV3/contracts/math/SafeMath.sol";
import "../../interfaces/IKeep3rV1.sol";

contract MockKeep3r is IKeep3rV1 {
    using SafeMath for uint256;

    address public keeper;
    address public keeperHelper;

    constructor(address _keeper, address _keeperHelper) public {
        keeper = _keeper;
        keeperHelper = _keeperHelper;
    }

    function KPRH() external override returns (address) {
        return keeperHelper;
    }

    function name() external override returns (string memory) {
        return "MockKeep3r";
    }

    function isKeeper(address _keeper) external override returns (bool) {
        return (_keeper == keeper);
    }

    function worked(address _keeper) external override {}

    function addKPRCredit(address job, uint256 amount) external override {}

    function addJob(address job) external override {}
}
