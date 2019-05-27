pragma solidity ^0.4.24;

library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
        if (a == 0) {
            return 0;
        }
        uint256 c = a * b;
        require(c / a == b, 'Mul Err');
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b > 0, 'Div Err');
        uint256 c = a / b;
        return c;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b <= a, 'Sub Err');
        uint256 c = a - b;
        return c;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a, 'Add Err');
        return c;
    }
    function mod(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b != 0, 'Mod Err');
        return a % b;
    }
    function exp(uint256 a, uint256 b) internal pure returns(uint256){
        require(b >= 0, 'Exp Err');
        uint256 c = 1;
        for(uint256 i = 0 ; i < b ; i++){
            c = mul(c, a);
        }
        return c;
    }
    function mul(int256 a, int256 b) internal pure returns (int256) {
        if (a == 0) {
            return 0;
        }
        int256 c = a * b;
        require(c / a == b, 'Mul Err');
        return c;
    }
    function div(int256 a, int256 b) internal pure returns (int256) {
        require(b != 0, 'Div Err');
        int256 c = a / b;
        return c;
    }
    function sub(int256 a, int256 b) internal pure returns (int256) {
        int c = a - b;
        if(b >= 0){
            require(c <= a, 'Sub Err');
        } else {
            require(c > a, 'Sub Err');
        }
        return c;
    }
    function add(int256 a, int256 b) internal pure returns (int256) {
        int c = a + b;
        if(b >= 0){
            require(c >= a, 'Sub Err');
        } else {
            require(c < a, 'Sub Err');
        }
        return c;
    }
    function mod(int256 a, int256 b) internal pure returns (int256) {
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

contract c_00450052004300320030306b57fa3065304f4eee60f3901a8ca8306b95a23059308b59517d04 {
    using SafeMath for uint256;
    using SafeMath for int256;

    uint256 internal v_7dcf767a884c91cf;    /*仮想通貨の総発行量*/
    mapping(address=>uint256) internal map0;    /*人物Xの仮想通貨保有量*/
    mapping(address=>mapping(address=>uint256)) internal map1;    /*人物Xが人物Yに許可した送金可能な仮想通貨量*/

    /*
    @function constructor 新規発行
    @param v_63075b9a5024 仮想通貨の総発行量として指定された値
    */
    constructor(uint256 v_63075b9a5024) public {
        v_7dcf767a884c91cf = v_63075b9a5024.mul(uint256(10).exp(uint256(18)));
        map0[msg.sender] = v_7dcf767a884c91cf;
    }

    /*
    @function totalSupply 総発行量の確認
    @return v_7dcf767a884c91cf 仮想通貨の総発行量
    */
    function totalSupply() public view returns(uint256){
        return (v_7dcf767a884c91cf);
    }

    /*
    @function balanceOf 残高の確認
    @param v_5bfe8c618005 残高の確認を求める指定された人物
    @return map0[v_5bfe8c618005] 残高の確認を求める指定された人物の残高
    */
    function balanceOf(address v_5bfe8c618005) public view returns(uint256){
        require(v_5bfe8c618005 != address(0));
        return (map0[v_5bfe8c618005]);
    }

    /*
    @function allowance 送金可能な金額の確認
    @param v_4fdd67098005 送金される仮想通貨の保有者として指定された人物
    @param v_900191d18005 送金の実行者として指定された人物
    @return map1[v_4fdd67098005][v_900191d18005] 送金される仮想通貨の保有者として指定された人物から送金の実行者として指定された人物が送金可能な額
    */
    function allowance(address v_4fdd67098005, address v_900191d18005) public view returns(uint256){
        require(v_4fdd67098005 != address(0));
        require(v_900191d18005 != address(0));
        return (map1[v_4fdd67098005][v_900191d18005]);
    }

    /*
    @function transfer 送金
    @param v_900191d15148 送金先として指定された人物
    @param v_900191d1984d 送金額として指定された仮想通貨量
    */
    function transfer(address v_900191d15148, uint256 v_900191d1984d) public returns(bool){
        require(v_900191d15148 != address(0));
        require(map0[msg.sender] >= v_900191d1984d);
        map0[msg.sender] = map0[msg.sender].sub(v_900191d1984d);
        map0[v_900191d15148] = map0[v_900191d15148].add(v_900191d1984d);
        return true;
    }

    /*
    @function approve 第三者による送金の許可
    @param v_900191d18005 送金の実行権の保有者として指定された人物
    @param v_8a3153ef984d 送金者が送金可能とする指定された仮想通貨量
    */
    function approve(address v_900191d18005, uint256 v_8a3153ef984d) public returns(bool){
        require(v_900191d18005 != address(0));
        map1[msg.sender][v_900191d18005] = v_8a3153ef984d;
        return true;
    }

    /*
    @function transferFrom 第三者による送金
    @param v_88ab900191d18005 送金される仮想通貨の保有者として指定された人物
    @param v_900191d15148 送金先として指定された人物
    @param v_900191d1984d 指定された仮想通貨量
    */
    function transferFrom(address v_88ab900191d18005, address v_900191d15148, uint256 v_900191d1984d) public returns(bool){
        require(v_88ab900191d18005 != address(0));
        require(v_900191d15148 != address(0));
        require(map0[v_88ab900191d18005] >= v_900191d1984d);
        require(map1[v_88ab900191d18005][msg.sender] >= v_900191d1984d);
        map0[v_88ab900191d18005] = map0[v_88ab900191d18005].sub(v_900191d1984d);
        map1[v_88ab900191d18005][msg.sender] = map1[v_88ab900191d18005][msg.sender].sub(v_900191d1984d);
        map0[v_900191d15148] = map0[v_900191d15148].add(v_900191d1984d);
        return true;
    }
}
