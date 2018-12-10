interface ERC20Interface {
    function totalSupply() public view returns (uint);
    function balanceOf(address tokenOwner) public view returns (uint balance);
    function allowance(address tokenOwner, address spender) public view returns (uint remaining);
    function transfer(address to, uint tokens) public returns (bool success);
    function approve(address spender, uint tokens) public returns (bool success);
    function transferFrom(address from, address to, uint tokens) public returns (bool success);

    event Transfer(address indexed from, address indexed to, uint tokens);
    event Approval(address indexed tokenOwner, address indexed spender, uint tokens);
}

contract ERC20 is ERC20Interface {
    /*optional ver1
    string public constant name = "Test Token";
    string public constant symbol = "TTC";
    uint8 public constant decimals = 18;
    */
    uint public _totalSupply;

    mapping(address=>uint) public balanses;
    mapping(address=>mapping(address=>uint)) public allowed;

    constructor(uint ts) public {
        _totalSupply = ts * 10**18;
        balances[msg.sender] = _totalSupply;
    }

    /*optional ver2
    function name() public pure returns(string){
        return 'Test Token';
    }
    function symbol() public pure returns(string){
        return 'TTC';
    }
    function decimals() public pure returns(uint8){
        return 18;
    }
    */

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
        balances[from] -= tokens;
        balances[to] += tokens;
        emit Transfer(from, to, tokens);
        return true;
    }
}
