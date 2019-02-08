pragma solidity ^0.4.24;
import './erc20_sample.sol';

contract c_30c830fc30af30f3309275283044305f4e0d52d5752358f28cb7306b95a23059308b59517d04 {
    using SafeMath for int256;
    struct s_4e0d52d5752360c55831 {string v_540d524d;int256 v_4fa1683c;Enum0 v_8ca958f272b6614b;}
    enum Enum0 {v_8ca958f24e2d,v_8ca958f24f116b62}

    c_00450052004300320030306b57fa3065304f30c830fc30af30f3306b95a23059308b59517d04 ERC20 = c_00450052004300320030306b57fa3065304f30c830fc30af30f3306b95a23059308b59517d04(0x0000000000000000000000000000000000000000);
    s_4e0d52d5752360c55831[] internal v_4e0d52d5752330ea30b930c8;    /*不動産のリスト*/
    mapping(int256=>address) internal map0;    /*各不動産のIDに対するその不動産の保有者*/
    mapping(address=>int256) internal map1;    /*各ユーザが保有する不動産の個数*/

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
    @localVar v_900191d18a3153ef984d 本契約が送金可能なあなたの所持するトークンの量
    @localVar v_65e74fdd67098005 購入前の対象IDの不動産の保有者
    */
    function f_4e0d52d57523306e8cfc5165(int256 v_5bfe8c6100490044) public {
        require(v_5bfe8c6100490044 < int256(v_4e0d52d5752330ea30b930c8.length));
        require(v_4e0d52d5752330ea30b930c8[uint256(v_5bfe8c6100490044)].v_8ca958f272b6614b == Enum0.v_8ca958f24e2d);
        int256 v_900191d18a3153ef984d;
        v_900191d18a3153ef984d = ERC20.f_900191d153ef80fd306a91d1984d306e78ba8a8d(msg.sender, address(this));
        require(v_900191d18a3153ef984d >= v_4e0d52d5752330ea30b930c8[uint256(v_5bfe8c6100490044)].v_4fa1683c);
        address v_65e74fdd67098005 = map0[v_5bfe8c6100490044];
        v_4e0d52d5752330ea30b930c8[uint256(v_5bfe8c6100490044)].v_8ca958f272b6614b = Enum0.v_8ca958f24f116b62;
        map0[v_5bfe8c6100490044] = msg.sender;
        map1[v_65e74fdd67098005] = map1[v_65e74fdd67098005].sub(int256(1));
        map1[msg.sender] = map1[msg.sender].add(int256(1));
        ERC20.f_7b2c00338005306b3088308b900191d1(msg.sender, v_65e74fdd67098005, v_4e0d52d5752330ea30b930c8[uint256(v_5bfe8c6100490044)].v_4fa1683c);
    }
}
