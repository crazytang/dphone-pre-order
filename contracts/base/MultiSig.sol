// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "../dependencies/ECDSA.sol";

abstract contract MultiSig {

    address[] public operators;
    uint8 public operator_limited_num;
    mapping(bytes32 => address[]) public signed_operators;

    using ECDSA for bytes32;
    event ChangedOperator(address old_operator, address new_operator);

    function _findOpt(address sigaddr, bool[] memory bops) private view returns (bool)
    {
        for (uint8 i = 0; i < operators.length; i++) {
            //emit log_named_address("operators", operators[i]);
            if (operators[i] != address(0x0)) {
                if (bops[i] == false) {
                    if (operators[i] == sigaddr) {
                        //emit log_named_address("find", operators[i]);
                        bops[i] = true;
                        //emit log("set true");
                        return true;
                    }
                }
            } else {
                break;
            }
        }
        return false;
    }

    function _checkSigs(bytes32 hash, bytes[] memory sigs, uint8 numSigs) internal view returns (bool) {
        uint8 c = 0;
        //emit log_named_uint("sigs len", sigs.length);
        bool[] memory bops = new bool[](operators.length);
        for (uint8 i = 0; i < sigs.length; i++) {
            //emit log_named_bytes("txHash", txHash);
            if (!_findOpt(hash.recover(sigs[i]), bops)) {
                return false;
            }
            c++;
        }
        //emit log_named_uint("c", c);
        if (c > numSigs) {
            return true;
        } else {
            return false;
        }
    }

    function changeOperator(address _original_operator, address _new_operator, bytes[] calldata _sigs) external {
        bytes32 txHash = this.getChangeOperatorHash(_original_operator, _new_operator);
        require(_checkSigs(txHash, _sigs, 2), "MultiSig: Only operators can changeOperator()");

        for (uint256 i=0; i<operators.length; i++) {
            if (operators[i] ==  _original_operator) {
                operators[i] = _new_operator;
                emit ChangedOperator(_original_operator, _new_operator);
                break;
            }
        }

        revert('MultiSig: original operator is not exists.');
    }

    function getChangeOperatorHash(address _original_operator, address _new_operator) external pure returns (bytes32) {
        return keccak256(abi.encodePacked('changeOperator', uint160(_original_operator), uint160(_new_operator)));
    }

    function getAddSupportedTokenHash(address _token_address) external pure returns (bytes32) {
        return keccak256(abi.encodePacked('addSupportedToken', uint160(_token_address)));
    }

    function getModifyPhonePriceHash(address _token_address, uint256 _price) external pure returns (bytes32) {
        return keccak256(abi.encodePacked('modifyPhonePrice', uint160(_token_address), _price));
    }

    function getPreOrderFailHash() external pure returns(bytes32) {
        return keccak256(abi.encodePacked('preOrderFail'));
    }

    function getSetRecipientHash(address _recipient_address) external pure returns(bytes32) {
        return keccak256(abi.encodePacked('setRecipient', uint160(_recipient_address)));
    }

    function getPreOrderSucc() external pure returns(bytes32) {
        return keccak256(abi.encodePacked('preOrderSucc'));
    }
}
