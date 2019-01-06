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

contract c_00450052004300320030306b57fa3065304f30c830fc30af30f3306b95a23059308b59517d04 {
    using SafeMath for int256;
    struct s_30ed30b030c730fc30bf {string v_540d524d;int256 v_4fa1683c;bool v_8ca958f24e2d;}

    int256 internal v_7dcf767a884c91cf;    /*トークンの総発行量*/
    mapping(address=>int256) internal map0;    /*ユーザXのトークン保有量*/
    mapping(address=>mapping(address=>int256)) internal map1;    /*ユーザXからユーザYが送金可能なトークン量*/

    /*
    @function constructor 契約の開始
    @param v_63075b9a5024 トークンの総発行量として指定する値
    */
    constructor(int256 v_63075b9a5024) public {
        v_7dcf767a884c91cf = v_63075b9a5024.mul(int256(10)).exp(int256(18));
        map0[msg.sender] = v_7dcf767a884c91cf;
    }

    /*
    @function f_7dcf767a884c91cf306e78ba8a8d 総発行量の確認
    @return v_7dcf767a884c91cf トークンの総発行量
    */
    function f_7dcf767a884c91cf306e78ba8a8d() public view returns(int256){
        return (v_7dcf767a884c91cf);
    }

    /*
    @function f_6b8b9ad8306e78ba8a8d 残高の確認
    @param v_5bfe8c618005 残高を確認する対象ユーザ
    @return map0[v_5bfe8c618005] 残高を確認する対象ユーザの残高
    */
    function f_6b8b9ad8306e78ba8a8d(address v_5bfe8c618005) public view returns(int256){
        return (map0[v_5bfe8c618005]);
    }

    /*
    @function f_900191d153ef80fd306a91d1984d306e78ba8a8d 送金可能な金額の確認
    @param v_4fdd67098005 送金されるトークンの保有者
    @param v_900191d18005 送金を実行するユーザ
    @return map1[v_4fdd67098005][v_900191d18005] 送金されるトークンの保有者から送金を実行するユーザが送金可能な額
    */
    function f_900191d153ef80fd306a91d1984d306e78ba8a8d(address v_4fdd67098005, address v_900191d18005) public view returns(int256){
        return (map1[v_4fdd67098005][v_900191d18005]);
    }

    /*
    @function f_900191d1 送金
    @param v_900191d15148 送金先のユーザ
    @param v_900191d1984d 送金するトークン量
    */
    function f_900191d1(address v_900191d15148, int256 v_900191d1984d) public {
        require(map0[msg.sender] >= v_900191d1984d);
        map0[msg.sender] = map0[msg.sender].sub(v_900191d1984d);
        map0[v_900191d15148] = map0[v_900191d15148].add(v_900191d1984d);
        emit Transfer(msg.sender,v_900191d15148,v_900191d1984d);
    }

    /*
    @function f_7b2c00338005306b3088308b900191d1306e8a3153ef 第3者による送金の許可
    @param v_900191d18005 送金の実行権を与える対象のユーザ
    @param v_8a3153ef984d 送金者が送金可能とするトークン量
    */
    function f_7b2c00338005306b3088308b900191d1306e8a3153ef(address v_900191d18005, int256 v_8a3153ef984d) public {
        map1[msg.sender][v_900191d18005] = v_8a3153ef984d;
        emit Approval(msg.sender,v_900191d18005,v_8a3153ef984d);
    }

    /*
    @function f_7b2c00338005306b3088308b900191d1 第3者による送金
    @param v_88ab900191d18005 送金されるトークンの保有者
    @param v_900191d15148 送金先のユーザ
    @param v_900191d1984d 送金するトークンの量
    */
    function f_7b2c00338005306b3088308b900191d1(address v_88ab900191d18005, address v_900191d15148, int256 v_900191d1984d) public {
        require(map0[v_88ab900191d18005] >= v_900191d1984d);
        require(map1[v_88ab900191d18005][msg.sender] >= v_900191d1984d);
        map0[v_88ab900191d18005] = map0[v_88ab900191d18005].sub(v_900191d1984d);
        map1[v_88ab900191d18005][msg.sender] = map1[v_88ab900191d18005][msg.sender].sub(v_900191d1984d);
        map0[v_900191d15148] = map0[v_900191d15148].add(v_900191d1984d);
        emit Transfer(v_88ab900191d18005,v_900191d15148,v_900191d1984d);
    }
    event Transfer(address indexed from, address indexed to, int tokens);
    event Approval(address indexed tokenOwner, address indexed spender, int tokens);
}
