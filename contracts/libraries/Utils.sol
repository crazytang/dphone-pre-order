// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

library Utils {
    /**
     * @dev Returns true if `account` is a contract.
     *
     * [IMPORTANT]
     * ====
     * It is unsafe to assume that an address for which this function returns
     * false is an externally-owned account (EOA) and not a contract.
     *
     * Among others, `isContract` will return false for the following
     * types of addresses:
     *
     *  - an externally-owned account
     *  - a contract in construction
     *  - an address where a contract will be created
     *  - an address where a contract lived, but was destroyed
     * ====
     */
    function checkContract(address account) internal view {
        // This method relies on extcodesize, which returns 0 for contracts in
        // construction, since the code is only stored at the end of the
        // constructor execution.

        uint256 size;
        assembly {
            size := extcodesize(account)
        }
        require(size > 0, 'Utils: it is not contract address');
    }

    /// @dev 在指定误差范围内比较两个数字是否一致
    /// @param left_num 左边数字
    /// @param right_num 右边数字
    /// @param gap_max 误差范围
    /// @return 是否一致
    function amountEqualTo(uint256 left_num, uint256 right_num, uint256 gap_max) internal pure returns(bool) {
        uint256 gap;

        if (gap_max == 0) {
            gap_max = 1e10;
        }

        if (left_num >= right_num) {
            gap = left_num - right_num;
        } else {
            gap = right_num - left_num;
        }
        return gap <= gap_max;
    }


    /**
     * @dev Converts a `uint256` to its ASCII `string` decimal representation.
     */
    function uint256ToString(uint256 value) internal pure returns (string memory) {
        // Inspired by OraclizeAPI's implementation - MIT licence
        // https://github.com/oraclize/ethereum-api/blob/b42146b063c7d6ee1358846c198246239e9360e8/oraclizeAPI_0.4.25.sol

        if (value == 0) {
            return "0";
        }
        uint256 temp = value;
        uint256 digits;
        while (temp != 0) {
            digits++;
            temp /= 10;
        }
        bytes memory buffer = new bytes(digits);
        while (value != 0) {
            digits -= 1;
            buffer[digits] = bytes1(uint8(48 + uint256(value % 10)));
            value /= 10;
        }
        return string(buffer);
    }

    /// @dev 是否处于测试网
    /// @return bool
    function isTestNet() internal view returns (bool) {
        if (block.chainid == 3 // Ropsten
        || block.chainid == 4 // Rinkeby
        || block.chainid == 5 // Goerli
        || block.chainid == 42 // Kovan
            || block.chainid == 1337 // ganache
        ) {
            return true;
        }
        return false;
    }
}
