import json
import web3
import time
from web3 import Web3, HTTPProvider
from solcx import compile_source
from web3.contract import ConciseContract

# Solidity source code
# user=Web3.toChecksumAddress(user)
import pickle
contract_source_code = '''
pragma solidity 0.5.7;
contract EtherFeeds{
	address admin;
	uint numMembers;
	uint PeriodInMinutes = 600;
	//mapping (address => memberProposal) addProposals;
	mapping (address => int) member;
	mapping (address => bool) isMember;
	// Q&A Structs
	struct Question{
		uint256 hash;
		uint256 bounty; // denominated in WEI. 1 ether = 10^18 wei
		address askerAddr;
		mapping(uint256 => Answer) answers;
		mapping(address => bool) isAnswered;
		//mapping(uint256 => uint256) indexes;
		uint minTimetoAnswer;

		uint numAnswers;
		bool settled;
		// bool isValue; // checks for existence of key
	}

	struct Answer{
	    address answererAddr;
	    uint256 answerHash;
	    uint256 numUpvotes;
	    uint256 numDownvotes;

	   // bool isValue;
	    mapping(address => bool) voted;
	}

	mapping (uint256 => Question) public questions;


	//Constructor
	constructor() public{
    	admin = msg.sender; //initialising admin address
		isMember[admin]=true;
	}

	modifier onlyAdmin () {
	    require(msg.sender == admin, "Only admin can add new member");
	    _;
	}

	modifier onlyMembers () {
	    require(isMember[msg.sender], "not a member of the DAO");
	    _;
	}

	function kill() public{
	    //The admin has the right to kill the contract at any time.
	    //Take care that no one else is able to kill the contract
	    require (msg.sender == admin , "Only admin can kill");
	    selfdestruct(msg.sender);
	}

	function addMember(address memberAddress)  public onlyAdmin {
	    //Anyone on the network can become a student if not one already
	    //Remember to assign the new student a unique roll number

	    require(isMember[msg.sender] != true, "Already a member");
	    //member[memberAddress] = memberID++;
	    isMember[memberAddress] = true;

	}


	function isMemberOf(address memberAddress) public view returns (bool){
	    return isMember[memberAddress];
	}
// Governance



// Q&A functions

	function addQuestion(uint256 questionHash, uint256 bounty, uint minTimetoAnswer) onlyMembers public {
	    questions[questionHash] = Question({
	        askerAddr: msg.sender,
	        hash: questionHash,
	        bounty: bounty,
	        numAnswers: 0,
	        settled: false,
	        minTimetoAnswer: now + minTimetoAnswer * 1 minutes
	    });
	}

	function answer(uint256 questionHash, uint256 answerHash) onlyMembers public {
	    require(!questions[questionHash].isAnswered[msg.sender] && !questions[questionHash].settled);
	    questions[questionHash].answers[answerHash] = Answer({
	        answererAddr: msg.sender,
	        answerHash: answerHash,
	        numUpvotes: 0,
	        numDownvotes: 0
	        });
	}

	function voteOnAnswer(uint256 questionHash, uint256 answerHash, bool vote)  onlyMembers public {
	    require(!questions[questionHash].settled);
	    if (vote)
	        questions[questionHash].answers[answerHash].numUpvotes++;
	    else
	        questions[questionHash].answers[answerHash].numDownvotes++;
	}
}
'''

wallet_private_key   = 'CDD46AA3C0F33B3283CEC649C0C09BC374D90999683077373A843BA0363B162F'
wallet_address       = '0x29246a5B71c9876E71B58f79f49D5F1454D87686'


compiled_sol = compile_source(contract_source_code) # Compiled source code
contract_interface = compiled_sol['<stdin>:EtherFeeds']

# web3.py instance
w3 = Web3(HTTPProvider('https://ropsten.infura.io/v3/0d917ac7376a4526a3a9cb9306bfec30'))
w3.eth.enable_unaudited_features()

# set pre-funded account as sender
w3.eth.defaultAccount = wallet_address
acct = w3.eth.account.privateKeyToAccount(wallet_private_key)

# Instantiate and deploy contract
EtherFeeds = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# Submit the transaction that deploys the contract
tx_hash = EtherFeeds.constructor().buildTransaction({
    'from': acct.address,
    'nonce': w3.eth.getTransactionCount(acct.address),
    'gas': 1728712,
    'gasPrice': w3.toWei('21', 'gwei')})
signed = acct.signTransaction(tx_hash)
txn_hash=w3.eth.sendRawTransaction(signed.rawTransaction)
tx_receipt =w3.eth.waitForTransactionReceipt(txn_hash)

admin = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=contract_interface['abi'],
)

# print(tx_receipt.contractAddress)
# print(type(contract_interface['abi']))

dbfile = open('contract_addr', 'wb')
pickle.dump(tx_receipt.contractAddress, dbfile)
dbfile.close()

dbfile = open('contract_abi', 'wb')
pickle.dump(contract_interface['abi'], dbfile)
dbfile.close()
