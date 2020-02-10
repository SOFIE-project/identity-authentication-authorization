'''
This script creates test accounts using Indy SDK test ledger
Make sure the ledger is running:
ocker run -itd -p 9701-9708:9701-9708 indy_pool
'''
from indy import anoncreds, crypto, did, ledger, pool, wallet
from indy.error import ErrorCode, IndyError
import json
import sys
import asyncio
import os 

pool_name             = 'Test_pool'
pool_genesis_txn_path = os.getcwd()+'/indy_sample_genesis_txn'
'''
This Steward is part of the indy-sdk testing network
'''
steward = {
    'name': "Steward",
    'wallet_config': json.dumps({'id': 'steward_wallet', "storage_config":{"path":"indy_wallets"}}),
    'wallet_credentials': json.dumps({'key': 'steward_wallet_key'}),
    'seed': '000000000000000000000000Steward1'
}

endorser = {
    'name': "Endorser",
    'wallet_config': json.dumps({'id': 'endorser_wallet',"storage_config":{"path":"indy_wallets"}}),
    'wallet_credentials': json.dumps({'key': 'endorser_wallet_key'}),
    'seed': '00000000000000000000000Endorser1' #used only for testing
}

user = {
    'wallet_config': json.dumps({'id': 'user_wallet',"storage_config":{"path":"indy_wallets"}}),
    'wallet_credentials': json.dumps({'key': 'user_wallet_key'}),
    'seed': '000000000000000000000000000User1', #used only for testing
    'msk' : 'msk_key'
}

server = {
    'wallet_config': json.dumps({'id': 'server_wallet',"storage_config":{"path":"indy_wallets"}}),
    'wallet_credentials': json.dumps({'key': 'server_wallet_key'}),
    'seed': '0000000000000000000000000Server1', #used only for testing
    'msk' : 'msk_key'
}

async def setup():
    print("1. Creating pool")
    pool_config = json.dumps({"genesis_txn": str(pool_genesis_txn_path)})
    await pool.set_protocol_version(2)
    try:
        await pool.create_pool_ledger_config(pool_name, pool_config)
    except IndyError as ex:
        if ex.error_code == ErrorCode.PoolLedgerConfigAlreadyExistsError:
            pass

    print("2. Opening pool")
    pool_handle = await pool.open_pool_ledger(pool_name, pool_config)
    #################################################
    print("3. Creating Steward wallet and DID")
    try:
        await wallet.create_wallet(steward['wallet_config'], steward['wallet_credentials'])
    except IndyError as ex:
        if ex.error_code == ErrorCode.WalletAlreadyExistsError:
            pass
    steward['wallet']               = await wallet.open_wallet(steward['wallet_config'], steward['wallet_credentials'])        
    steward['did_info']             = json.dumps({'seed': steward['seed']})
    steward['did'], steward['key']  = await did.create_and_store_my_did(steward['wallet'], steward['did_info'])
    #################################################
    print("4. Creating Endorser wallet, DID, and storing it in the ledger")
    try:
        await wallet.create_wallet(endorser['wallet_config'], endorser['wallet_credentials'])
    except IndyError as ex:
        if ex.error_code == ErrorCode.WalletAlreadyExistsError:
            pass
    endorser['wallet']               = await wallet.open_wallet(endorser['wallet_config'], endorser['wallet_credentials'])
    endorser['did_info']             = json.dumps({'seed': endorser['seed']})       
    endorser['did'], endorser['key'] = await did.create_and_store_my_did(endorser['wallet'], endorser['did_info'])
    nym_request                      = await ledger.build_nym_request(steward['did'], endorser['did'], endorser['key'], None, 'TRUST_ANCHOR')
    await ledger.sign_and_submit_request(pool_handle, steward['wallet'], steward['did'], nym_request)
    print("...Endorser DID: " + endorser['did'])
    #################################################
    print("5. Creating user wallet, DID, storing it in the ledger, and creating master secret key")
    try:
        await wallet.create_wallet(user['wallet_config'], user['wallet_credentials'])
    except IndyError as ex:
        if ex.error_code == ErrorCode.WalletAlreadyExistsError:
            pass
    user['wallet']           = await wallet.open_wallet(user['wallet_config'], user['wallet_credentials']) 
    user['did_info']         = json.dumps({'seed': user['seed']})       
    user['did'], user['key'] = await did.create_and_store_my_did(user['wallet'], user['did_info'])
    nym_request              = await ledger.build_nym_request(endorser['did'], user['did'], user['key'], None, None)
    await ledger.sign_and_submit_request(pool_handle, endorser['wallet'], endorser['did'], nym_request)
    try:
        await anoncreds.prover_create_master_secret(usawait wallet.close_wallet(server['wallet'])er['wallet'], user['msk'])
    except IndyError as ex:
        if ex.error_code == ErrorCode.AnoncredsMasterSecretDuplicateNameError:
            pass 
    print("...User DID: " + user['did'])
    #################################################
    '''
    The following is used for verifying DIDs without the pool
    '''
    print("6. Creating server wallet")
    try:
        await wallet.create_wallet(server['wallet_config'], server['wallet_credentials'])
    except IndyError as ex:
        if ex.error_code == ErrorCode.WalletAlreadyExistsError:
            pass
    #################################################
    '''
    The following is used for verifying DIDs without the pool
    '''
    print("7. Storing user verkey in server's wallet")
    server['wallet'] = await wallet.open_wallet(server['wallet_config'], server['wallet_credentials'])
    await did.store_their_did(server['wallet'],json.dumps({"did": user['did'], "verkey": user['key']})) 
    #################################################

    print("Cleaning up")
    await wallet.close_wallet(steward['wallet'])
    await wallet.close_wallet(endorser['wallet'])
    await wallet.close_wallet(user['wallet'])
    await wallet.close_wallet(server['wallet'])
    await pool.close_pool_ledger(pool_handle)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup())
    loop.close()

if __name__ == '__main__':
    main()