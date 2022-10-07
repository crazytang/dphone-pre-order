pragma solidity ^0.8.0;

import "../dependencies/ERC20Upgradeable.sol";

contract DPN is Initializable, ERC20Upgradeable {

    /// @dev 初始化
    function initialize() public initializer {
        __ERC20_init('dPhone Governance Token', 'DPN');
    }

}
