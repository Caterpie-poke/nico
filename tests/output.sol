pragma solidity ^0.4.24;
library SafeMath {
    function mul(int256 a, int256 b) internal pure returns(int256){
        if (a == 0) {
            return 0;
        }
        int256 c = a * b;
        require(c / a == b, 'Mul Err');
        return c;
    }
    function div(int256 a, int256 b) internal pure returns(int256){
        require(b != 0, 'Div Err');
        int256 c = a / b;
        return c;
    }
    function sub(int256 a, int256 b) internal pure returns(int256){
        int256 c = a - b;
        if(b >= 0){
            require(c <= a, 'Sub Err');
        } else {
            require(c > a, 'Sub Err');
        }
        return c;
    }
    function add(int256 a, int256 b) internal pure returns(int256){
        int256 c = a + b;
        if(b >= 0){
            require(c >= a, 'Add Err');
        } else {
            require(c < a, 'Add Err');
        }
        return c;
    }
    function mod(int256 a, int256 b) internal pure returns(int256){
        require(b != 0, 'Mod Err');
        return a % b;
    }
    function exp(int256 a, int256 b) internal pure returns(int256){
        require(b >= 0, 'Exp Err');
        int256 c = 1;
        for(int256 i = 0 ; i < b ; i++){
            c = mul(c, a);
        }
        return c;
    }
}

contract c_ERC20に基づくトークンに関する契約 {
    using SafeMath for int256;

    int256 internal v_総発行量;
    mapping(address=>int256) internal map3;
    mapping(address=>mapping(address=>int256)) internal map2;

    function constructor(int256 v_総発行量の指定値) public {
        v_総発行量 = v_総発行量の指定値.mul(int(10));
        map3[msg.sender] = v_総発行量;
    }

    function totalSupply() public view returns(int256){
        return (v_総発行量);
    }

    function balanceOf(address v_対象者) public view returns(int256){
        return (map3[v_対象者]);
    }

    function allowance(address v_対象者, address v_送金者) public view returns(int256){
        return (map2[v_対象者][v_送金者]);
    }

    function transfer(address v_対象者, int256 v_送金額) public returns(bool){
        require(v_対象者 != 0x0);
        require(map3[msg.sender] >= v_送金額);
        map3[msg.sender] = map3[msg.sender].sub(v_送金額);
        map3[v_対象者] = map3[v_対象者].add(v_送金額);
        emit Transfer(msg.sender, v_対象者, v_送金額);
        return (true);
    }

    function approve(address v_対象者, int256 v_指定額) public returns(bool){
        require(v_送金者 != 0x0);
        map2[msg.sender][v_対象者] = v_指定額;
        return (true);
    }

    function transferFrom(address v_被送金者, address v_対象者, int256 v_送金額) public returns(bool){
        require(v_対象者 != 0x0);
        require(map3[v_被送金者] >= v_送金額);
        require(map2[v_被送金者][msg.sender] >= v_送金額);
        map3[v_被送金者] = map3[v_被送金者].sub(v_送金額);
        map3[v_対象者] = map3[v_対象者].add(v_送金額);
        return (true);
    }

    function hogege(uint p1) external returns(bytes4){
        uint cast = uint(v_総発行量);
        return bytes4(keccak256('transfer(address,uint)returns(bool)'));
    }
}
