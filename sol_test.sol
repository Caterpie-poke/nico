pragma solidity ^0.4.24;

contract C1 {
    function f1() public pure returns(bool){
        uint num = 123;
        return true;
    }
    function f2() public pure returns(string m){
        m = 'Hello World';
    }
}

interface I1 {
    function fi1() public view returns(string);
    function fi2(uint) public pure returns(uint);
}

contract C2 is C1 {
    function f3(uint n) public pure returns(uint){
        return n**2;
    }
}

contract C3_1 is C2,I1 {
    string stateMessage = 'This is state message';
    function fi1() public view returns(string){
        return stateMessage;
    }
    function fi2(uint) public pure returns(uint){
        return 2+3*4-2**3;
    }
}
contract C3_2 {
    string stateMessage = 'This is state message';
    function fi1() public view returns(string){
        return stateMessage;
    }
    function fi2(uint) public pure returns(uint){
        return 2+3*4-2**3;
    }
}