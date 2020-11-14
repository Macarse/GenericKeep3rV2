// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.6.8;

import "../../interfaces/chainlink/IChainLinkFeed.sol";

contract MockGasOracle is IChainLinkFeed {
    int256 mockedGas = 19000000000000000000;

    function latestAnswer() public view override returns (int256) {
        return mockedGas;
    }

    function setMockedGas(int256 _mockedGas) public {
        mockedGas = _mockedGas;
    }
}
