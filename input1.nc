「仮想通貨に関する契約書」

第1条　台帳に記録する項目
    総発行量
    （参加者）の残高
    創設者

第2条　指定量で仮想通貨の発行
    あなたが決められる値//考慮
        初期発行量
    総発行量を指定量とする
    創設者を操作実行者とする
    創設者の残高を総発行量とする
終了

第3条　対象者に送金額を送る
    入力
    要件
        あなた(msg.sender)の残高>送金額
    対象者の残高は対象者の残高+送金額
    実行者の残高を実行者の残高-送金額とする
    出力
終了

第4条　所持金の確認
    対象者の残高を得る
終了

/*----- Expected Output -----
contract inputs {
    int var7dcf767a884c91cf
    mapping(address=>int) map306e6b8b9ad8
    address var52758a2d8005

    constructor(int var63075b9a91cf) public {
        var7dcf767a884c91cf = var63075b9a91cf;
        var52758a2d8005 = msg.sender;
        map306e6b8b9ad8[var52758a2d8005] = var7dcf767a884c91cf;
    }
    function fun306b30929001308b(address var5bfe8c618005, int var900191d1984d) public {
        require(map306e6b8b9ad8[msg.sender] > var900191d1984d);
        map306e6b8b9ad8[var5bfe8c618005] = map306e6b8b9ad8 + var900191d1984d;
        map306e6b8b9ad8[msg.sender] = map306e6b8b9ad8 - var900191d1984d;
    }
    function fun6240630191d1306e78ba8a8d() public returns(int){
        return map306e6b8b9ad8[msg.sender];
    }
}
*/

/*----- Actual Output -----
contract <FileName> {
    int 総発行量
    mapping() 〜の残高
    創設者
    function で初期化(int 指定量) public {
        総発行量 = 指定量;
        創設者 = 操作実行者;
        map02[創設者] = 総発行量;
    }
    function にを送る(address 対象者,int 送金額) public {
        require(map02[操作実行者] > 送金額);
        map02[対象者] = map02[対象者] + 送金額;
        map02[実行者] = map02[実行者] - 送金額;
    }
    function 所持金の確認() public returns(int){
        return (map02[対象者]);
    }
}
*/

/*----- Corresponding Solidity Code -----
contract SampleCoin {
    int totalSupply;
    mapping(address=>int) balanceOf;
    address creater;

    constructor(int total) public {
        totalSupply = total;
        creater = msg.sender;
        balanceOf[creater] = totalSupply;
    }

    function sendCoin(address target, int amount) public {
        require(balanceOf[msg.sender] > amount);
        balanceOf[target]+=amount;
        balanceOf[msg.sender]-=amount;
    }
    function getBalance() public returns(int){
        return balanceOf[msg.sender];
    }
}
*/