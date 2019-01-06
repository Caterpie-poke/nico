「Etherを用いたログデータ売買に関する契約」

第0条　台帳に記録される情報
    ログデータのリスト（以下、データリストと呼ぶ）
    ログIDであるXが指すログデータの保有者（以下、Xの保有者と呼ぶ）
    ユーザXが持つログデータの個数（以下、Xの保有データ数と呼ぶ）
    ユーザXが持つ総販売利益（以下、Xの販売利益と呼ぶ）

第1条　データ登録(register)
    パラメータ：
        新規に追加するログデータの名前（以下、新規名称と呼ぶ）
        新規に追加するログデータの価格（以下、新規価格と呼ぶ）
    新規に追加するログデータ（以下、新規ログと呼ぶ）を定義する
    新規ログの名前を新規名称とする
    新規ログの価格を新規価格とする
    新規ログの販売中をfalseとする
    データリストに新規ログを追加する
    データリストのサイズー1として新規ログのID（以下、新規IDと呼ぶ）を定義する
    新規IDの保有者をあなたとする
    あなたの保有データ数を1だけ増やす
    新規IDを出力として得る

第2条　データ情報の確認
    パラメータ：
        参照するデータのID（以下、対象IDと呼ぶ）
    データリストの対象ID番目として対象データを定義する
    対象データの名前・対象データの価格・対象データの販売中を出力として得る

第3条　保有者の確認
    パラメータ：
        確認を行う対象のデータID（以下、対象IDと呼ぶ）
    対象IDの保有者を出力として得る

第4条　データ保有数の確認
    あなたの保有データ数を出力として得る

第5条　販売利益の確認
    あなたの販売利益を出力として得る

第6条　データの販売
    パラメータ：
        販売対象のデータID（以下、対象IDと呼ぶ）
    要件1　対象IDの保有者＝あなた
    要件2　データリストの対象ID番目の販売中＝false
    データリストの対象ID番目の販売中をtrueとする

第7条　データの販売中止
    パラメータ：
        販売中止とする対象のデータID（以下、対象IDと呼ぶ）
    要件1　対象IDの保有者＝あなた
    要件2　データリストの対象ID番目の販売中＝true
    データリストの対象ID番目の販売中をfalseとする

第8条　価格改定
    パラメータ：
        価格を変更するデータのID（以下、対象IDと呼ぶ）
        変更後の新しい価格（以下、新規価格と呼ぶ）
    要件1　データリストの対象ID番目の販売中＝false
    データリストの対象ID番目の価格を新規価格とする

第9条　データの購入
    パラメータ：
        購入対象のデータのID（以下、対象IDと呼ぶ）
        ETH
    要件1　対象ID＜データリストのサイズ
    要件2　データリストの対象ID番目の販売中＝true
    要件3　データリストの対象ID番目の価格＝受け取ったETH
    対象IDの保有者として購入前の保有者（以下、旧保有者と呼ぶ）を定義する
    対象IDの保有者をあなたとする
    旧保有者の保有データ数を1だけ減らす
    旧保有者の販売利益を受け取ったETHだけ増やす
    あなたの保有データ数を1だけ増やす
    データリストの対象ID番目の販売中をfalseとする

第10条　販売利益の受け取り
    あなたの販売利益として総利益を定義する
    要件1　総利益＞0
    あなたの販売利益を0とする
    本契約のアドレスが持つETHから、総利益をあなたへ送金する
