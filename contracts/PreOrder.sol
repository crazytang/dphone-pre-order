// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./dependencies/Initializable.sol";
import "./dependencies/OwnableUpgradeable.sol";
import "./dependencies/ReentrancyGuardUpgradeable.sol";
import {IERC20Upgradeable as IERC20} from "./dependencies/IERC20Upgradeable.sol";
import "./base/MultiSig.sol";
import "./libraries/Utils.sol";

contract PreOrder is Initializable, MultiSig, OwnableUpgradeable, ReentrancyGuardUpgradeable {
    // participants
    address[] public users;

    // limited deposit tokens
    address[] public supported_tokens;

    // the difference of price in tokens. if address(0), meaning is ETH
    mapping(address => uint256) public phone_prices;

    // asset of users have deposited
    mapping(address => mapping(address => uint256)) public users_deposit;

    // the number of users having pre-ordered
    mapping(address => uint8) public users_pre_order_num;

    // pre-order is fail and refund the asset to users
    mapping(address => uint256) public refunds;

    // the recipient will be obtain all assets after the pre-order is succeeded
    address public asset_recipient;

    // these assets income
    mapping(address => uint256) public assets_income;

    bool pre_order_finished;


/*
    modifier operatorOnly() {
        require(isOperator(msg.sender), 'PreOrder: caller must be operator');
        _;
    }
*/

    modifier isNotFinished() {
        require(!pre_order_finished, 'PreOrder: This pre-order is finished');
        _;
    }

    event AddedSupportedToken(address token_address);
    event ModifiedPhonePrice(address token_address, uint256 old_price, uint256 new_price);
    event MakedPreOrderUsingETH(address indexed user_address, uint256 amount, uint256 order_num);
    event MakedPreOrderUsingToken(address indexed user_address, address token_address, uint256 amount, uint256 order_num);
    event PerOrderFailAndRefund(address[] token_addresses, uint256[] token_refund_amounts);
    event SetAssetRecipient(address recipient_address);
    event PerOrderSuccAndIncome(address[] token_addresses, uint256[] token_income_amounts);

    /// @dev 初始化
    function initialize(address[] calldata _operators) public initializer {
        __Ownable_init();
        __ReentrancyGuard_init();

        operator_limited_num = 3;

        if (_operators.length != operator_limited_num) {
            revert('operators num is no sufficient');
        }
        operators = _operators;
        if (supported_tokens.length == 0) {
            supported_tokens.push(address(0)); // meaning eth
        }
    }

    function addUserIfNotExists(address _user_address) private {
        for (uint256 i=0;i<users.length;i++) {
            if (_user_address == users[i]) {
                return;
            }
        }

        users.push(_user_address);
    }

    /// @dev set recipient to receive the assets
    /// @notice MultiSig is needed
    function setRecipient(address _recipient_address, bytes[] calldata _sigs) public isNotFinished {
        bytes32 txHash = this.getSetRecipientHash(_recipient_address);
        require(_checkSigs(txHash, _sigs, 2), "PreOrder: Only operators can setRecipient()");

        asset_recipient = _recipient_address;
        emit SetAssetRecipient(_recipient_address);
    }

    /// @dev the pre-order is successful
    /// @notice MultiSig is needed
    function preOrderSucc(bytes[] calldata _sigs) public isNotFinished {
        require(asset_recipient != address(0), 'PreOrder: The asset recipient is not set');

        bytes32 txHash = this.getPreOrderSucc();
        require(_checkSigs(txHash, _sigs, 2), "PreOrder: Only operators can preOrderSucc()");

        uint256[] memory assets_income_amount = new uint256[](supported_tokens.length);

        uint256 eth_balance = address(this).balance;
        if (eth_balance > 0) {
            (bool success, ) = asset_recipient.call{value: eth_balance}("");
            require(success, "PreOrder: ETH transfer failed in preOrderSucc()");
        }
        assets_income[address(0)] = eth_balance;
        assets_income_amount[0] = eth_balance;

        for (uint256 i=0; i<supported_tokens.length; i++) {
            if (supported_tokens[i] == address(0)) {
                continue;
            }

            uint256 token_balance = IERC20(supported_tokens[i]).balanceOf(address(this));
            if (token_balance > 0) {
                IERC20(supported_tokens[i]).transfer(asset_recipient, token_balance);
            }
            assets_income[supported_tokens[i]] = eth_balance;
            assets_income_amount[i] = token_balance;
        }

        rewardDpnToUsers();

        // clean user deposited data
        for (uint256 i=0;i<users.length;i++) {
            for (uint256 ii=0;ii<supported_tokens.length;ii++) {
                users_deposit[users[i]][supported_tokens[ii]] = 0;
            }
        }
        pre_order_finished = true;

        checkIntegrity();

        emit PerOrderSuccAndIncome(supported_tokens, assets_income_amount);
    }

    /// @dev it's need to reward the participants
    function rewardDpnToUsers() private {
        for (uint256 i=0; i<users.length; i++) {
            // todo transfer the DPN to user
        }
    }

    /// @dev add supported token address
    /// @notice MultiSig is needed
    function addSupportedToken(address _token_address, bytes[] calldata _sigs) public isNotFinished {
        require(_token_address != address(0), 'PreOrder: Token address is emtpy');
        bytes32 txHash = this.getAddSupportedTokenHash(_token_address);
        require(_checkSigs(txHash, _sigs, 2), "PreOrder: Only operators can addSupportedToken()");

        require(!this.isSupportedToken(_token_address), 'PreOrder: This token is exists');

        supported_tokens.push(_token_address);
        emit AddedSupportedToken(_token_address);
    }

    /// @dev modify the phone price
    /// @notice MultiSig is needed
    function modifyPhonePrice(address _token_address, uint256 _price, bytes[] calldata _sigs) public isNotFinished {
//        require(_token_address != address(0), 'PreOrder: Token address is emtpy');
        require(this.isSupportedToken(_token_address), 'PreOrder: This token is not supported to modify price');

        bytes32 txHash = this.getModifyPhonePriceHash(_token_address, _price);
        require(_checkSigs(txHash, _sigs, 2), "PreOrder: Only operators can modifyPhonePrice()");

        uint256 old_price = phone_prices[_token_address];
        phone_prices[_token_address] = _price;

        emit ModifiedPhonePrice(_token_address, old_price, _price);
    }

    /// @dev transfer the ETH to make preorder
    function makePreOrderUsingETH() public payable nonReentrant isNotFinished {
        uint256 price = phone_prices[address(0)];
        uint8 pre_order_num = uint8(msg.value / price);
        // avoiding half adjust
        if (price * pre_order_num > msg.value) {
            pre_order_num--;
        }

        users_pre_order_num[msg.sender] += pre_order_num;
        users_deposit[msg.sender][address(0)] += msg.value;

        addUserIfNotExists(msg.sender);

        checkIntegrity();

        emit MakedPreOrderUsingETH(msg.sender, msg.value, pre_order_num);
    }

    function makePreOrderFromReceive(address _user_address, uint256 _eth_amount) private isNotFinished {

        uint256 price = phone_prices[address(0)];
        uint8 pre_order_num = uint8(_eth_amount / price);
        // avoiding half adjust
        if (price * pre_order_num > _eth_amount) {
            pre_order_num--;
        }

        users_pre_order_num[_user_address] += pre_order_num;
        users_deposit[_user_address][address(0)] += _eth_amount;

        addUserIfNotExists(_user_address);

        checkIntegrity();

        emit MakedPreOrderUsingETH(_user_address, _eth_amount, pre_order_num);
    }

    /// @dev transfer the Token to make preorder
    function makePreOrderUsingToken(address _token_address, uint256 _amount) public isNotFinished {
        require(_token_address != address(0), 'PreOrder: Token address is emtpy');
        require(this.isSupportedToken(_token_address), 'PreOrder: This token is not supported to make preorder');

        IERC20 token = IERC20(_token_address);
        require(token.balanceOf(msg.sender) >= _amount, 'PreOrder: User token is insufficient funds');
        require(token.allowance(msg.sender, address(this)) >= _amount, 'PreOrder: User must approve at first');

        token.transferFrom(msg.sender, address(this), _amount);

        uint256 price = phone_prices[_token_address];
        uint8 pre_order_num = uint8(_amount / price);
        // avoiding half adjust
        if (price * pre_order_num > _amount) {
            pre_order_num--;
        }
        users_pre_order_num[msg.sender] += pre_order_num;

        users_deposit[msg.sender][_token_address] += _amount;

        addUserIfNotExists(msg.sender);

        checkIntegrity();

        emit MakedPreOrderUsingToken(msg.sender, _token_address, _amount, pre_order_num);
    }

    /// @dev Preoder is fail
    /// @notice MultiSig is needed
    function preOrderFail(bytes[] calldata _sigs) public isNotFinished{
        bytes32 txHash = this.getPreOrderFailHash();
        require(_checkSigs(txHash, _sigs, 2), "PreOrder: Only operators can preOrderFail()");

        for (uint256 i=0; i<users.length; i++) {
            address user_address = users[i];
            uint256 eth_amount = users_deposit[user_address][address(0)];
            if (eth_amount > 0) {
                require(address(this).balance >= eth_amount, 'PreOrder: contract eth balance is not correct');
                // eth
                (bool success, ) = user_address.call{value: eth_amount}("");
                require(success, "PreOrder: ETH transfer failed in preOrderFail()");

                refunds[address(0)] += eth_amount;
                users_deposit[users[i]][address(0)] = 0;
            }

            for (uint256 ii=0; ii<supported_tokens.length; ii++) {
                if (supported_tokens[ii] == address(0)) {
                    continue;
                }
                uint256 token_amount = users_deposit[user_address][supported_tokens[ii]];
                if (token_amount > 0) {
                    require(IERC20(supported_tokens[ii]).balanceOf(address(this)) >= token_amount, 'PreOrder: contract token balance is not correct');
                    IERC20(supported_tokens[ii]).transfer(user_address, token_amount);
                    refunds[supported_tokens[ii]] += token_amount;
                    users_deposit[users[i]][supported_tokens[ii]] = 0;
                }
            }
        }
        pre_order_finished = true;
        uint256[] memory refund_amounts = new uint256[](supported_tokens.length);
        for (uint256 i=0; i<supported_tokens.length; i++) {
            refund_amounts[i] = refunds[supported_tokens[i]];
        }

        checkIntegrity();

        emit PerOrderFailAndRefund(supported_tokens, refund_amounts);
    }

    function checkIntegrity() private {
        if (users.length == 0) {
            return;
        }

        uint256 users_eth_sum = 0;
        uint256 token_balance_sum = 0;
        for (uint256 i=0; i<users.length; i++) {
            users_eth_sum += users_deposit[users[i]][address(0)];
        }
//        revert(string(abi.encodePacked(Utils.uint256ToString(address(this).balance), '|', Utils.uint256ToString(users_eth_sum))));
        require(Utils.amountEqualTo(address(this).balance, users_eth_sum, 0), 'PreOrder: Integrity checking fail 1');

        for (uint256 i=0; i<supported_tokens.length; i++) {
            if (supported_tokens[i] == address(0)) {
                continue;
            }

            uint256 users_token_balance_sum = 0;
            for (uint256 ii=0; ii<users.length; ii++) {
                users_token_balance_sum += users_deposit[users[ii]][supported_tokens[i]];
            }

            require(Utils.amountEqualTo(IERC20(supported_tokens[i]).balanceOf(address(this)), users_token_balance_sum, 0),
                'PreOrder: Integrity checking fail 2');
        }
    }

    function getOperators() public view returns(address[] memory) {
        return operators;
    }

    function isOperator(address user_address) public view returns(bool) {
        bool is_operator = false;
        for (uint256 i=0; i<operator_limited_num; i++) {
            if (operators[i] == user_address) {
                is_operator = true;
                break;
            }
        }
        return is_operator;
    }

    function isSupportedToken(address _token_address) public view returns(bool) {
        for (uint256 i=0; i<supported_tokens.length; i++) {

            if (_token_address == supported_tokens[i]) {
                return true;
            }
        }
        return false;
    }

    function getUsers() public view returns(address[] memory) {
        return users;
    }

    function getAllSupportedTokens() public view returns(address[] memory) {
        return supported_tokens;
    }

    receive() external payable {
        makePreOrderFromReceive(msg.sender, msg.value);
//        revert('You need to call the makePreOrder function');
    }
}
