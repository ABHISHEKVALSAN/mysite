import json
import web3
import time
from eth_account import Account
from web3 import Web3, HTTPProvider
from solcx import compile_source
from web3.contract import ConciseContract
from django.contrib.auth.models import User
# Solidity source code
# user=Web3.toChecksumAddress(user)
import pickle
contract_source_code = '''
pragma solidity 0.5.7;
contract EtherFeeds{
	address admin;
	mapping (address => bool) isMember;

	constructor() public{
    	admin = msg.sender; //initialising admin address
		isMember[admin]=true;
	}

	function kill() public{
	    require (msg.sender == admin , "Only admin can kill");
	    selfdestruct(msg.sender);
	}

	modifier onlyAdmin () {
	    require(msg.sender == admin, "Only admin can add new member");
	    _;
	}

	modifier onlyMembers () {
	    require(isMember[msg.sender], "not a member of the DAO");
	    _;
	}

	function isMemberOf(address memberAddress) public view returns (bool){
	    return isMember[memberAddress];
	}

	function addMember(address memberAddress) public {
	    require(isMember[memberAddress] != true, "Already a member");
	    isMember[memberAddress] =true;

	}
}
'''

compiled_sol = compile_source(contract_source_code) # Compiled source code
contract_interface = compiled_sol['<stdin>:EtherFeeds']
print("Solidity compiled!!!")
# web3.py instance
w3 = Web3(HTTPProvider('https://ropsten.infura.io/v3/0d917ac7376a4526a3a9cb9306bfec30'))
w3.eth.enable_unaudited_features()
print("Connected to ropsten!!!")

# set pre-funded account as sender
wallet_signature   	 = 'CDD46AA3C0F33B3283CEC649C0C09BC374D90999683077373A843BA0363B162F'
wallet_address       = '0x29246a5B71c9876E71B58f79f49D5F1454D87686'

acct = w3.eth.account.privateKeyToAccount(wallet_signature)
print("Account created!!!")
# Instantiate and deploy contract
EtherFeeds = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
print("Contract object Etherfeeds created!!!")
# Submit the transaction that deploys the contract
tx_hash = EtherFeeds.constructor().buildTransaction({
    'from': acct.address,
    'nonce': w3.eth.getTransactionCount(acct.address),
    'gas': 1728712,
    'gasPrice': w3.toWei('21', 'gwei')})
signed = acct.signTransaction(tx_hash)
txn_hash=w3.eth.sendRawTransaction(signed.rawTransaction)
tx_receipt =w3.eth.waitForTransactionReceipt(txn_hash)
print("Contract constructed at address")
print(tx_receipt.contractAddress)


contract = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=contract_interface['abi'],
)
print("Contract object created!!!")

dbfile = open('contract_addr', 'wb')
pickle.dump(tx_receipt.contractAddress, dbfile)
dbfile.close()

dbfile = open('contract_abi', 'wb')
pickle.dump(contract_interface['abi'], dbfile)
dbfile.close()
print("Made pickle files")
