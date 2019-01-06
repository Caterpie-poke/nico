「NFTトークンであるERC721の契約」

第0条　記録される項目
    （任意のトークンID）の所有者
    （任意のトークンID）の操作可能者
    （参加者）の持つトークン数
    （所有者）のトークンに対して（任意の者）が操作可能かどうか

第1条　トークン量の確認（balanceOf）
    入力：
        対象者
    要件：
        対象者　NOT=　0x0
    出力：
        対象者の持つトークン数

第2条　所有者の確認（ownerOf）
    入力：
        対象トークンID
    出力：
        対象トークンIDの所有者

第3条　安全な送付（safeTransferFrom）
    入力：
        送付元
        送付先
        送付トークンID
    要件：
        あなた＝送付トークンIDの所有者　または　あなた＝送付トークンIDの操作可能者　または　送付トークンIDの所有者のトークンに対してあなたが操作可能かどうか＝はい
        送付トークンIDの所有者 NOT= 0x0
        送付トークンIDの所有者＝送付元
        送付先 NOT= 0x0
        送付元の持つトークン数 ＞ 0
    本文：
        送付トークンIDの操作可能者を0x0とする
        送付元の持つトークン数を1だけ減らす
        送付トークンIDの所有者を送付先にする
        送付先の持つトークン数を1だけ増やす
        SOL{emit Transfer(「送付元」,「送付先」,「送付トークンID」)}
        もし送付先＝コントラクトならば
            SOL{bytes4 retval = ERC721TokenReceiver(「送付先」).onERC721Received(「あなた」,「送付元」,「送付トークンID」, '');}
            SOL{require(retval == 0x150b7a02)}

第4条　第3者からの送付（transferFrom）
    入力：
        送付元
        送付先
        送付トークンID
    要件：
        あなた＝送付トークンIDの所有者　または　あなた＝送付トークンIDの操作可能者　または　送付トークンIDの所有者のトークンに対してあなたが操作可能かどうか＝はい
        送付トークンIDの所有者 NOT= 0x0
        送付トークンIDの所有者＝送付元
        送付先 NOT= 0x0
        送付元の持つトークン数 ＞ 0
    本文：
        送付トークンIDの操作可能者を0x0とする
        送付元の持つトークン数を1だけ減らす
        送付トークンIDの所有者を送付先にする
        送付先の持つトークン数を1だけ増やす
        SOL{emit Transfer(「送付元」,「送付先」,「送付トークンID」)}

第5条　特定トークンの操作権の付与（approve）
    入力：
        付与対象者
        対象トークンID
    要件：
        あなた＝対象トークンIDの所有者　または　あなた＝対象トークンIDの操作可能者　または　対象トークンIDの所有者のトークンに対してあなたが操作可能かどうか＝はい
        対象トークンIDの所有者 NOT= 0x0
        付与対象者 NOT= 対象トークンIDの所有者
    本文：
        対象トークンIDの操作可能者を付与対象者とする
        対象トークンIDの所有者として対象トークン所有者をおく
        SOL{emit Approval(「対象トークン保有者」,「付与対象者」,「対象トークンID」)}

第6条　所有する全トークンの操作権の付与（setApprovalForAll）
    入力：
        付与対象者
        許可または不許可
    要件：
        付与対象者 NOT= 0x0
        あなたのトークンに対して付与対象者が操作可能かどうかを許可または不許可とする
        SOL{emit ApprovalForAll(「あなた」,「付与対象者」,「許可または不許可」)}

第7条　操作権の確認（getApproved）
    入力：
        対象トークンID
    要件：
        対象トークンIDの所有者 NOT= 0x0
    出力：
        対象トークンIDの操作可能者

第8条　全トークンに対する操作権の有無の確認（isApprovedForAll）
    入力：
        トークン所持者
        操作実行者
    要件：
        トークン所持者 NOT= 0x0
        操作実行者 NOT= 0x0
    出力：
        トークン所持者のトークンに対して操作実行者が操作可能かどうか

第9条　Solidity
    event Transfer(address indexed _from, address indexed _to, uint256 indexed _tokenId);
    event Approval(address indexed _owner, address indexed _approved, uint256 indexed _tokenId);
    event ApprovalForAll(address indexed _owner, address indexed _operator, bool _approved);

    function safeTransferFrom(address _from, address _to, uint256 _tokenId, bytes _data) external {
        address tokenOwner = idToOwner[_tokenId];
        require(
            tokenOwner == msg.sender
            || getApproved(_tokenId) == msg.sender
            || ownerToOperators[tokenOwner][msg.sender]
        );
        require(tokenOwner != address(0));
        require(tokenOwner == _from);
        require(_to != address(0));

        if(idToApprovals[_tokenId] != 0) {
            delete idToApprovals[_tokenId];
        }
        assert(ownerToNFTokenCount[_from] > 0);
        ownerToNFTokenCount[_from] = ownerToNFTokenCount[_from] - 1;
        idToOwner[_tokenId] = _to;
        ownerToNFTokenCount[_to] = ownerToNFTokenCount[_to].add(1);
        emit Transfer(_from, _to, _tokenId);

        if (_to.isContract()) {
          bytes4 retval = ERC721TokenReceiver(_to).onERC721Received(msg.sender, _from, _tokenId, _data);
          require(retval == MAGIC_ON_ERC721_RECEIVED);
        }
    }


