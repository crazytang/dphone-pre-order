// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "../dependencies/ERC20.sol";

contract USDCToken is ERC20 {
    constructor() ERC20('USD Coin', 'USDC') {
        _mint(msg.sender, 100_000_000 * 10e18);
    }
}
