// SPDX-License-Identifier: MIT
pragma solidity >=0.6.8;

interface IUniswapV2SlidingOracle {
    function current(
        address tokenIn,
        uint256 amountIn,
        address tokenOut
    ) external view returns (uint256);
}
