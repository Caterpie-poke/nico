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

contract c_00450074006800650072309275283044305f30ed30b030c730fc30bf58f28cb7306b95a23059308b59517d04 {
    using SafeMath for int256;
    struct s_30ed30b030c730fc30bf {string v_540d524d;int256 v_4fa1683c;bool v_8ca958f24e2d;}

    s_30ed30b030c730fc30bf[] internal v_30c730fc30bf30ea30b930c8;    /*ログデータのリスト*/
    mapping(int256=>address) internal map2;    /*ログIDであるXが指すログデータの保有者*/
    mapping(address=>int256) internal map3;    /*ユーザXが持つログデータの個数*/
    mapping(address=>int256) internal map4;    /*ユーザXが持つ総販売利益*/

    /*
    @function register データ登録
    @param v_65b0898f540d79f0 新規に追加するログデータの名前
    @param v_65b0898f4fa1683c 新規に追加するログデータの価格
    @localVar v_65b0898f30ed30b0 新規に追加するログデータ
    @localVar v_65b0898f00490044 新規ログのID
    @return v_65b0898f00490044 新規ログのID
    */
    function register(string memory v_65b0898f540d79f0, int256 v_65b0898f4fa1683c) public returns(int256){
        s_30ed30b030c730fc30bf memory v_65b0898f30ed30b0;
        v_65b0898f30ed30b0.v_540d524d = v_65b0898f540d79f0;
        v_65b0898f30ed30b0.v_4fa1683c = v_65b0898f4fa1683c;
        v_65b0898f30ed30b0.v_8ca958f24e2d = false;
        v_30c730fc30bf30ea30b930c8.push(v_65b0898f30ed30b0);
        int256 v_65b0898f00490044 = int256(v_30c730fc30bf30ea30b930c8.length).sub(int256(1));
        map2[v_65b0898f00490044] = msg.sender;
        map3[msg.sender] = map3[msg.sender].add(int256(1));
        return (v_65b0898f00490044);
    }

    /*
    @function f_30c730fc30bf60c55831306e78ba8a8d データ情報の確認
    @param v_5bfe8c6100490044 参照するデータのID
    @localVar v_5bfe8c6130c730fc30bf 対象データ
    @return v_5bfe8c6130c730fc30bf.v_540d524d 対象データの名前
    @return v_5bfe8c6130c730fc30bf.v_4fa1683c 対象データの価格
    @return v_5bfe8c6130c730fc30bf.v_8ca958f24e2d 対象データの販売中
    */
    function f_30c730fc30bf60c55831306e78ba8a8d(int256 v_5bfe8c6100490044) public view returns(string memory, int256, bool){
        s_30ed30b030c730fc30bf memory v_5bfe8c6130c730fc30bf = v_30c730fc30bf30ea30b930c8[uint256(v_5bfe8c6100490044)];
        return (v_5bfe8c6130c730fc30bf.v_540d524d, v_5bfe8c6130c730fc30bf.v_4fa1683c, v_5bfe8c6130c730fc30bf.v_8ca958f24e2d);
    }

    /*
    @function f_4fdd67098005306e78ba8a8d 保有者の確認
    @param v_5bfe8c6100490044 確認を行う対象のデータID
    @return map2[v_5bfe8c6100490044] 確認を行う対象のデータIDの保有者
    */
    function f_4fdd67098005306e78ba8a8d(int256 v_5bfe8c6100490044) public view returns(address){
        return (map2[v_5bfe8c6100490044]);
    }

    /*
    @function f_30c730fc30bf4fdd67096570306e78ba8a8d データ保有数の確認
    @return map3[msg.sender] あなたの保有データ数
    */
    function f_30c730fc30bf4fdd67096570306e78ba8a8d() public view returns(int256){
        return (map3[msg.sender]);
    }

    /*
    @function f_8ca958f2522976ca306e78ba8a8d 販売利益の確認
    @return map4[msg.sender] あなたの販売利益
    */
    function f_8ca958f2522976ca306e78ba8a8d() public view returns(int256){
        return (map4[msg.sender]);
    }

    /*
    @function f_30c730fc30bf306e8ca958f2 データの販売
    @param v_5bfe8c6100490044 販売対象のデータID
    */
    function f_30c730fc30bf306e8ca958f2(int256 v_5bfe8c6100490044) public {
        require(map2[v_5bfe8c6100490044] == msg.sender);
        require(v_30c730fc30bf30ea30b930c8[uint256(v_5bfe8c6100490044)].v_8ca958f24e2d == false);
        v_30c730fc30bf30ea30b930c8[uint256(v_5bfe8c6100490044)].v_8ca958f24e2d = true;
    }

    /*
    @function f_30c730fc30bf306e8ca958f24e2d6b62 データの販売中止
    @param v_5bfe8c6100490044 販売中止とする対象のデータID
    */
    function f_30c730fc30bf306e8ca958f24e2d6b62(int256 v_5bfe8c6100490044) public {
        require(map2[v_5bfe8c6100490044] == msg.sender);
        require(v_30c730fc30bf30ea30b930c8[uint256(v_5bfe8c6100490044)].v_8ca958f24e2d == true);
        v_30c730fc30bf30ea30b930c8[uint256(v_5bfe8c6100490044)].v_8ca958f24e2d = false;
    }

    /*
    @function f_4fa1683c65395b9a 価格改定
    @param v_5bfe8c6100490044 価格を変更するデータのID
    @param v_65b0898f4fa1683c 変更後の新しい価格
    */
    function f_4fa1683c65395b9a(int256 v_5bfe8c6100490044, int256 v_65b0898f4fa1683c) public {
        require(v_30c730fc30bf30ea30b930c8[uint256(v_5bfe8c6100490044)].v_8ca958f24e2d == false);
        v_30c730fc30bf30ea30b930c8[uint256(v_5bfe8c6100490044)].v_4fa1683c = v_65b0898f4fa1683c;
    }

    /*
    @function f_30c730fc30bf306e8cfc5165 データの購入
    @param v_5bfe8c6100490044 購入対象のデータのID
    @localVar v_65e74fdd67098005 購入前の保有者
    */
    function f_30c730fc30bf306e8cfc5165(int256 v_5bfe8c6100490044) public payable{
        require(v_5bfe8c6100490044 < int256(v_30c730fc30bf30ea30b930c8.length));
        require(v_30c730fc30bf30ea30b930c8[uint256(v_5bfe8c6100490044)].v_8ca958f24e2d == true);
        require(v_30c730fc30bf30ea30b930c8[uint256(v_5bfe8c6100490044)].v_4fa1683c == int256(msg.value));
        address v_65e74fdd67098005 = map2[v_5bfe8c6100490044];
        map2[v_5bfe8c6100490044] = msg.sender;
        map3[v_65e74fdd67098005] = map3[v_65e74fdd67098005].sub(int256(1));
        map4[v_65e74fdd67098005] = map4[v_65e74fdd67098005].add(int256(msg.value));
        map3[msg.sender] = map3[msg.sender].add(int256(1));
        v_30c730fc30bf30ea30b930c8[uint256(v_5bfe8c6100490044)].v_8ca958f24e2d = false;
    }

    /*
    @function f_8ca958f2522976ca306e53d7305153d6308a 販売利益の受け取り
    @localVar v_7dcf522976ca 総利益
    */
    function f_8ca958f2522976ca306e53d7305153d6308a() public {
        int256 v_7dcf522976ca = map4[msg.sender];
        require(v_7dcf522976ca > int256(0));
        map4[msg.sender] = int256(0);
        address(msg.sender).transfer(uint256(v_7dcf522976ca));
    }
}
