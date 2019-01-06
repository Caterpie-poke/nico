pragma solidity ^0.4.24;
import './original_erc20_sample.sol';

contract Trade {
    ERC20 coin;
    struct Data {
        string name;
        uint value;
        bool sale;
    }
    Data[] datas;
    mapping(uint=>address) idToOwner;
    mapping(address=>uint) ownedTokenCount;

    constructor(address erc20) public {
        coin = ERC20(erc20);
    }

    function register(string n,uint price) external returns(uint){
        Data newData;
        newData.name = n;
        newData.value = price;
        newData.sale = false;
        datas.push(newData);
        uint id = datas.length - 1;
        idToOwner[id] = msg.sender;
        ownedTokenCount[msg.sender] += 1;
        return id;
    }

    function dataInfo(uint id) external view returns(string,uint,bool){
        Data memory d = datas[id];
        return (d.name, d.value, d.sale);
    }
    function getOwner(uint id) external view returns(address){
        return idToOwner[id];
    }
    function getTokenCount() external view returns(uint){
        return ownedTokenCount[msg.sender];
    }

    function sell(uint id) external {
        require(idToOwner[id] == msg.sender);
        datas[id].sale = true;
    }
    function notForSale(uint id) external {
        require(idToOwner[id] == msg.sender);
        datas[id].sale = false;
    }
    function changePrice(uint id,uint newPrice) external {
        require(datas[id].sale == false);
        datas[id].value = newPrice;
    }

    //User must do approve(this_contract_address, price_or_more) before this function execution
    function buy(uint id) external {
        require(id < datas.length);
        require(datas[id].sale == true);
        require(coin.allowance(msg.sender, this) >= datas[id].value);
        address previousOwner = idToOwner[id];
        datas[id].sale = false;
        idToOwner[id] = msg.sender;
        ownedTokenCount[previousOwner] -= 1;
        ownedTokenCount[msg.sender] += 1;
        coin.transferFrom(msg.sender, previousOwner, datas[id].value);
    }
}