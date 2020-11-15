// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.6.8;

import "../../interfaces/chainlink/IChainLinkFeed.sol";

contract MockGasOracle is IChainLinkFeed {
    // From: 0x169E633A2D1E6c10dD91238Ba11c4A708dfEF37C
    int256 mockedGas = 18000000000;

    function latestAnswer() public view override returns (int256) {
        return mockedGas;
    }

    function setMockedGas(int256 _mockedGas) public {
        mockedGas = _mockedGas;
    }
}
