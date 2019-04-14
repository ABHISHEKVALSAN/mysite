import json
import web3
import time
import pickle
from web3 import Web3, HTTPProvider
from solcx import compile_source
from web3.contract import ConciseContract


dbfile = open('/home/abhiavk/git/mysite/etherfeeds/contract_abi', 'rb')
contract_abi=pickle.load(dbfile)
dbfile.close()

dbfile = open('/home/abhiavk/git/mysite/etherfeeds/contract_addr', 'rb')
contract_addr=pickle.load(dbfile)
dbfile.close()

w3 = Web3(HTTPProvider('https://ropsten.infura.io/v3/0d917ac7376a4526a3a9cb9306bfec30'))
w3.eth.enable_unaudited_features()

admin = w3.eth.contract(
    address=contract_addr,
    abi=contract_abi,
)
# print(admin.functions.isMemberOf('0x29246a5B71c9876E71B58f79f49D5F1454D87686').call())
def authUser(user):
	return admin.functions.isMemberOf(user).call()
def addUser(user):
	user=Web3.toChecksumAddress(user)
	tx_hash=admin.functions.addMember(user).buildTransaction({
	    'from': '0x29246a5B71c9876E71B58f79f49D5F1454D87686',
	    'nonce': w3.eth.getTransactionCount('0x29246a5B71c9876E71B58f79f49D5F1454D87686'),
	    'gas': 1728712,
	    'gasPrice': w3.toWei('21', 'gwei')})
	signed = acct.signTransaction(tx_hash)
	txn_hash=w3.eth.sendRawTransaction(signed.rawTransaction)
	tx_receipt =w3.eth.waitForTransactionReceipt(txn_hash)
