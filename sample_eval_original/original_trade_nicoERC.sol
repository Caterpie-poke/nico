//Nicoで記述したコントラクトを用いる場合
pragma solidity ^0.4.24;
import 'erc20_sample.sol'

contract Trade {
    c_00450052004300320030306b57fa3065304f30c830fc30af30f3306b95a23059308b59517d04 coin;
    struct Data {
        string name;
        uint value;
        bool sale;
    }
    Data[] datas;
    mapping(uint=>address) idToOwner;
    mapping(address=>uint) ownedTokenCount;

    constructor(address erc20) public {
        coin = c_00450052004300320030306b57fa3065304f30c830fc30af30f3306b95a23059308b59517d04(erc20);
    }

    function register(string n,uint price) external returns(uint){
        uint id = datas.push(Data({name:n, value:price, sale:false}))-1;
        idToOwner[id] = msg.sender;
        ownedTokenCount[msg.sender] += 1;
        return id;
    }

    function sell(uint id) external {
        require(idToOwner[id] == msg.sender);
        datas[id].sale = true;
    }
    function notForSale(uint id) external {
        require(idToOwner[id] == msg.sender);
        datas[id].sale = false;
    }

    //User must do approve(this_contract_address, price_or_more) before this function execution
    function buy(uint id) external {
        require(id < datas.length);
        require(datas[id].sale == true);
        require(coin.f_900191d153ef80fd306a91d1984d306e78ba8a8d(msg.sender, this) >= datas[id].value);
        address previousOwner = idToOwner[id];
        datas[id].sale = false;
        idToOwner[id] = msg.sender;
        ownedTokenCount[previousOwner] -= 1;
        ownedTokenCount[msg.sender] += 1;
        coin.f_7b2c00338005306b3088308b900191d1(msg.sender, previousOwner, datas[id].value);
    }
}