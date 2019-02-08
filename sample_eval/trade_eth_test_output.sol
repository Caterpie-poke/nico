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

contract c_00450074006800650072309275283044305f4e0d52d5752358f28cb7306b95a23059308b59517d04 {
    using SafeMath for int256;
    struct s_4e0d52d5752360c55831 {string v_540d524d;int256 v_4fa1683c;Enum0 v_8ca958f272b6614b;}
    enum Enum0 {v_8ca958f24e2d,v_8ca958f24f116b62}

    s_4e0d52d5752360c55831[] internal v_4e0d52d5752330ea30b930c8;    /*不動産のリスト*/
    mapping(int256=>address) internal map0;    /*各不動産のIDに対するその不動産の保有者*/
    mapping(address=>int256) internal map1;    /*各ユーザが保有する不動産の個数*/
    mapping(address=>int256) internal map2;    /*各ユーザが持つ総販売利益*/

    /*
    @function register 不動産登録
    @param v_65b0898f540d79f0 新規不動産の名前
    @param v_65b0898f4fa1683c 新規不動産の価格
    @localVar v_65b0898f4e0d52d57523 新しく追加する不動産
    @localVar v_65b0898f4e0d52d5752300490044 新規不動産のID
    @return v_65b0898f4e0d52d5752300490044 新規不動産のID
    */
    function register(string memory v_65b0898f540d79f0, int256 v_65b0898f4fa1683c) public returns(int256){
        s_4e0d52d5752360c55831 memory v_65b0898f4e0d52d57523;
        v_65b0898f4e0d52d57523.v_540d524d = v_65b0898f540d79f0;
        v_65b0898f4e0d52d57523.v_4fa1683c = v_65b0898f4fa1683c;
        v_65b0898f4e0d52d57523.v_8ca958f272b6614b = Enum0.v_8ca958f24f116b62;
        v_4e0d52d5752330ea30b930c8.push(v_65b0898f4e0d52d57523);
        int256 v_65b0898f4e0d52d5752300490044 = int256(v_4e0d52d5752330ea30b930c8.length).sub(int256(1));
        map0[v_65b0898f4e0d52d5752300490044] = msg.sender;
        map1[msg.sender] = map1[msg.sender].add(int256(1));
        return (v_65b0898f4e0d52d5752300490044);
    }

    /*
    @function f_4e0d52d5752360c55831306e78ba8a8d 不動産情報の確認
    @param v_53c2716700490044 参照する不動産のID
    @localVar v_5bfe8c614e0d52d57523 参照の対象となる情報
    @return v_5bfe8c614e0d52d57523.v_540d524d 参照の対象となる情報の名前
    @return v_5bfe8c614e0d52d57523.v_4fa1683c 参照の対象となる情報の価格
    @return v_5bfe8c614e0d52d57523.v_8ca958f272b6614b 参照の対象となる情報の販売状態
    */
    function f_4e0d52d5752360c55831306e78ba8a8d(int256 v_53c2716700490044) public view returns(string memory, int256, Enum0){
        s_4e0d52d5752360c55831 memory v_5bfe8c614e0d52d57523 = v_4e0d52d5752330ea30b930c8[uint256(v_53c2716700490044)];
        return (v_5bfe8c614e0d52d57523.v_540d524d, v_5bfe8c614e0d52d57523.v_4fa1683c, v_5bfe8c614e0d52d57523.v_8ca958f272b6614b);
    }

    /*
    @function f_4fdd67098005306e78ba8a8d 保有者の確認
    @param v_53c2716700490044 確認を行う対象の不動産のID
    @return map0[v_53c2716700490044] 確認を行う対象の不動産のIDの不動産の保有者
    */
    function f_4fdd67098005306e78ba8a8d(int256 v_53c2716700490044) public view returns(address){
        return (map0[v_53c2716700490044]);
    }

    /*
    @function f_4e0d52d575234fdd67096570306e78ba8a8d 不動産保有数の確認
    @return map1[msg.sender] あなたの保有する不動産数
    */
    function f_4e0d52d575234fdd67096570306e78ba8a8d() public view returns(int256){
        return (map1[msg.sender]);
    }

    /*
    @function f_8ca958f2522976ca306e78ba8a8d 販売利益の確認
    @return map2[msg.sender] あなたの販売利益
    */
    function f_8ca958f2522976ca306e78ba8a8d() public view returns(int256){
        return (map2[msg.sender]);
    }

    /*
    @function f_4e0d52d57523306e8ca958f2 不動産の販売
    @param v_5bfe8c6100490044 販売対象の不動産のID
    */
    function f_4e0d52d57523306e8ca958f2(int256 v_5bfe8c6100490044) public {
        require(map0[v_5bfe8c6100490044] == msg.sender);
        require(v_4e0d52d5752330ea30b930c8[uint256(v_5bfe8c6100490044)].v_8ca958f272b6614b == Enum0.v_8ca958f24f116b62);
        v_4e0d52d5752330ea30b930c8[uint256(v_5bfe8c6100490044)].v_8ca958f272b6614b = Enum0.v_8ca958f24e2d;
    }

    /*
    @function f_4e0d52d57523306e8ca958f24f116b62 不動産の販売休止
    @param v_5bfe8c6100490044 販売中止とする対象のデータID
    */
    function f_4e0d52d57523306e8ca958f24f116b62(int256 v_5bfe8c6100490044) public {
        require(map0[v_5bfe8c6100490044] == msg.sender);
        require(v_4e0d52d5752330ea30b930c8[uint256(v_5bfe8c6100490044)].v_8ca958f272b6614b == Enum0.v_8ca958f24e2d);
        v_4e0d52d5752330ea30b930c8[uint256(v_5bfe8c6100490044)].v_8ca958f272b6614b = Enum0.v_8ca958f24f116b62;
    }

    /*
    @function f_4fa1683c65395b9a 価格改定
    @param v_5bfe8c6100490044 価格を変更する不動産のID
    @param v_65b0898f4fa1683c 変更後の新しい価格
    */
    function f_4fa1683c65395b9a(int256 v_5bfe8c6100490044, int256 v_65b0898f4fa1683c) public {
        require(v_4e0d52d5752330ea30b930c8[uint256(v_5bfe8c6100490044)].v_8ca958f272b6614b == Enum0.v_8ca958f24f116b62);
        v_4e0d52d5752330ea30b930c8[uint256(v_5bfe8c6100490044)].v_4fa1683c = v_65b0898f4fa1683c;
    }

    /*
    @function f_4e0d52d57523306e8cfc5165 不動産の購入
    @param v_5bfe8c6100490044 購入対象の不動産のID
    @localVar v_65e74fdd67098005 購入前の保有者
    */
    function f_4e0d52d57523306e8cfc5165(int256 v_5bfe8c6100490044) public payable{
        require(v_5bfe8c6100490044 < int256(v_4e0d52d5752330ea30b930c8.length));
        require(v_4e0d52d5752330ea30b930c8[uint256(v_5bfe8c6100490044)].v_8ca958f272b6614b == Enum0.v_8ca958f24e2d);
        require(v_4e0d52d5752330ea30b930c8[uint256(v_5bfe8c6100490044)].v_4fa1683c == int256(msg.value));
        address v_65e74fdd67098005 = map0[v_5bfe8c6100490044];
        map0[v_5bfe8c6100490044] = msg.sender;
        v_4e0d52d5752330ea30b930c8[uint256(v_5bfe8c6100490044)].v_8ca958f272b6614b = Enum0.v_8ca958f24f116b62;
        map1[v_65e74fdd67098005] = map1[v_65e74fdd67098005].sub(int256(1));
        map2[v_65e74fdd67098005] = map2[v_65e74fdd67098005].add(int256(msg.value));
        map1[msg.sender] = map1[msg.sender].add(int256(1));
    }

    /*
    @function f_8ca958f2522976ca306e53d7305153d6308a 販売利益の受け取り
    @localVar v_7dcf522976ca 総利益
    */
    function f_8ca958f2522976ca306e53d7305153d6308a() public {
        int256 v_7dcf522976ca = map2[msg.sender];
        require(v_7dcf522976ca > int256(0));
        map2[msg.sender] = int256(0);
        address(msg.sender).transfer(uint256(v_7dcf522976ca));
    }
}
