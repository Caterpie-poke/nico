pragma solidity ^0.4.24;
contract Trade {
    struct Data {
        string name;
        uint value;
        bool sale;
    }
    Data[] datas;
    mapping(uint=>address) idToOwner;
    mapping(address=>uint) ownedTokenCount;
    mapping(address=>uint) profits;

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
    function getProfit() external view returns(uint){
        return profits[msg.sender];
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

    function buy(uint id) external payable {
        require(id < datas.length);
        require(datas[id].value == msg.value);
        ownedTokenCount[idToOwner[id]] -= 1;
        profits[idToOwner[id]] += msg.value;
        idToOwner[id] = msg.sender;
        ownedTokenCount[msg.sender] += 1;
        datas[id].sale = false;
    }

    function withdraw() external {
        uint amount = profits[msg.sender];
        require(amount > 0);
        profits[msg.sender] = 0;
        msg.sender.transfer(amount);
    }
}