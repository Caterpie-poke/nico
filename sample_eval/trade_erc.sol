pragma solidity ^0.4.24;
import './erc20_sample.sol';

contract c_30c830fc30af30f3309275283044305f30ed30b030c730fc30bf58f28cb7306b95a23059308b59517d04 {
    using SafeMath for int256;
    struct s_30ed30b030c730fc30bf {string v_540d524d;int256 v_4fa1683c;bool v_8ca958f24e2d;}

    c_00450052004300320030306b57fa3065304f30c830fc30af30f3306b95a23059308b59517d04 ERC20 = c_00450052004300320030306b57fa3065304f30c830fc30af30f3306b95a23059308b59517d04(0x0000000000000000000000000000000000000000);
    s_30ed30b030c730fc30bf[] internal v_30c730fc30bf30ea30b930c8;    /*ログデータのリスト*/
    mapping(int256=>address) internal map2;    /*各ログデータIDに対するそのデータの保有者*/
    mapping(address=>int256) internal map3;    /*各ユーザが保有するログデータの個数*/

    /*
    @function register データ登録
    @param v_65b0898f540d79f0 新規ログデータの名前
    @param v_65b0898f4fa1683c 新規ログデータの価格
    @localVar v_65b0898f30ed30b0 新しく追加するログデータ
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
    @param v_53c2716700490044 参照するデータのID
    @localVar v_5bfe8c6130c730fc30bf 参照の対象となるデータ
    @return v_5bfe8c6130c730fc30bf.v_540d524d 参照の対象となるデータの名前
    @return v_5bfe8c6130c730fc30bf.v_4fa1683c 参照の対象となるデータの価格
    @return v_5bfe8c6130c730fc30bf.v_8ca958f24e2d 参照の対象となるデータの販売中
    */
    function f_30c730fc30bf60c55831306e78ba8a8d(int256 v_53c2716700490044) public view returns(string memory, int256, bool){
        s_30ed30b030c730fc30bf memory v_5bfe8c6130c730fc30bf = v_30c730fc30bf30ea30b930c8[uint256(v_53c2716700490044)];
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
    @param v_5bfe8c6100490044 購入対象のデータID
    @localVar v_900191d18a3153ef984d 本契約が動かせるあなたの所持トークン量
    @localVar v_65e74fdd67098005 購入前の対象IDの保有者
    */
    function f_30c730fc30bf306e8cfc5165(int256 v_5bfe8c6100490044) public {
        require(v_5bfe8c6100490044 < int256(v_30c730fc30bf30ea30b930c8.length));
        require(v_30c730fc30bf30ea30b930c8[uint256(v_5bfe8c6100490044)].v_8ca958f24e2d == true);
        int256 v_900191d18a3153ef984d = ERC20.f_900191d153ef80fd306a91d1984d306e78ba8a8d(msg.sender, address(this));
        require(v_900191d18a3153ef984d >= v_30c730fc30bf30ea30b930c8[uint256(v_5bfe8c6100490044)].v_4fa1683c);
        address v_65e74fdd67098005 = map2[v_5bfe8c6100490044];
        v_30c730fc30bf30ea30b930c8[uint256(v_5bfe8c6100490044)].v_8ca958f24e2d = false;
        map2[v_5bfe8c6100490044] = msg.sender;
        map3[v_65e74fdd67098005] = map3[v_65e74fdd67098005].sub(int256(1));
        map3[msg.sender] = map3[msg.sender].add(int256(1));
        ERC20.f_7b2c00338005306b3088308b900191d1(msg.sender, v_65e74fdd67098005, v_30c730fc30bf30ea30b930c8[uint256(v_5bfe8c6100490044)].v_4fa1683c);
    }
}
