contract ERC20 {

    uint internal _totalSupply;
    mapping(address=>uint) internal balanses;
    mapping(address=>mapping(address=>uint)) internal allowed;

    event Transfer(address indexed from, address indexed to, uint tokens);
    event Approval(address indexed tokenOwner, address indexed spender, uint tokens);

    constructor(uint ts) public {
        _totalSupply = ts * 10**18;
        balances[msg.sender] = _totalSupply;
    }

    function totalSupply() public view returns (uint){
        return _totalSupply;
    }
    function balanceOf(address tokenOwner) public view returns (uint){
        return balances[tokenOwner];
    }
    function allowance(address tokenOwner, address spender) public view returns (uint){
        return allowed[tokenOwner][spender];
    }
    function transfer(address to, uint tokens) public returns (bool){
        require(to != 0x0);
        require(balances[msg.sender]>=tokens);
        balances[msg.sender]-=tokens;
        balances[to]+=tokens;
        emit Transfer(msg.sender, to, tokens);
        return true;
    }
    function approve(address spender, uint tokens) public returns (bool){
        require(spender != 0x0);
        allowed[msg.sender][spender] = tokens;
        emit Approval(msg.sender, spender, tokens);
        return true;
    }
    function transferFrom(address from, address to, uint tokens) public returns (bool){
        require(to != 0x0);
        require(tokens <= balances[from]);
        require(tokens <= allowed[from][msg.sender]);
        allowed[from][msg.sender] -= tokens;
        balances[from] -= tokens;
        balances[to] += tokens;
        emit Transfer(from, to, tokens);
        return true;
    }
}
