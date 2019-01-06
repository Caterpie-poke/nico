「ERC20に基づくトークンに関する契約」

第0条　台帳に記録される情報
    トークンの総発行量（以下、総発行量と呼ぶ）
    各ユーザのトークン保有量（以下、Aの残高と呼ぶ）
    ユーザXのトークン保有量（以下、Xの残高と呼ぶ）
    各ユーザから各ユーザが送金可能なトークン量（以下、AからBが送金可能な額）
    ユーザXからユーザYが送金可能なトークン量（以下、XからYが送金可能額）
    int
    string
    address
    enum
第1条　契約の開始
    パラメータ：
        トークンの総発行量として指定する値（以下、指定値と呼ぶ）
    総発行量を指定値*10とする
    あなたの残高を総発行量とする

第2条　総発行量の確認
    総発行量を得る

第3条　残高の確認
    パラメータ：
        残高を確認する対象ユーザ（以下、対象者と呼ぶ）
    対象者の残高を得る

第4条　送金可能な金額の確認
    パラメータ：
        送金されるトークンの保有者（以下、保有者と呼ぶ）
        送金を実行するユーザ（以下、送金者と呼ぶ）
    保有者から送金者が送金可能な額を得る

第5条　送金
    パラメータ：
        送金先のユーザ（以下、送金先と呼ぶ）
        送金するトークン量（以下、送金額と呼ぶ）
    要件1　対象者が有効である
    要件2　あなたの残高 >= 送金額
    あなたの残高を送金額だけ減らす
    送金先の残高を送金額だけ増やす
    SOL{emit Transfer(「あなた」,「送金先」,「送金額」)}
    trueを得る

第6条　第3者による送金の許可
    パラメータ：
        送金を実行を認めるユーザ（以下、送金者と呼ぶ）
        送金者に送金を認めるトークン量（以下、許可額と呼ぶ）
    要件1　対象者が有効である
    あなたから送金者が送金可能な額を許可額とする
    SOL{emit Approval(「あなた」,「送金者」,「許可額」)}
    trueを得る

第7条　第3者による送金
    パラメータ：
        送金されるトークンの保有者（以下、被送金者と呼ぶ）
        送金先のユーザ（以下、送金先と呼ぶ）
        送金するトークンの量（以下、送金額と呼ぶ）
    要件1　送金先が有効である
    要件2　被送金者の残高 >= 送金額
    要件3　被送金者からあなたが送金可能な額 >= 送金額
    被送金者の残高を送金額だけ減らす
    被送金者からあなたが送金可能な額を送金額だけ減らす
    送金先の残高を送金額だけ増やす
    SOL{emit Transfer(「被送金者」,「送金先」,「送金額」)}
    trueを得る

第8条　Solidity
    event Transfer(address indexed from, address indexed to, int tokens);
    event Approval(address indexed tokenOwner, address indexed spender, int tokens);

