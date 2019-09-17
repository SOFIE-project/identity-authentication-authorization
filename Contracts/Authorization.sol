pragma solidity ^0.4.25;

contract Authorization {
    
    struct hashLock
    {
        address owner;
        string  metadata;
        uint    deposit;
        address client;
    }

    event hashLockCreatedEvent (
       bytes32 lock
    );

    event hashLockOpenedEvent (
       bytes32 lock,
       string  key
    );

    event newDepositEvent (
       bytes32 lock
    );

    mapping(bytes32 => hashLock) private hashLocks;
    
    function createHashLock( bytes32 lock, string metadata ) external {  
        //TODO check if lock exists
        hashLock storage hashLockRecord = hashLocks[lock];
        hashLockRecord.metadata = metadata;
        hashLockRecord.owner    = msg.sender;
        emit hashLockCreatedEvent(lock);
    }
    
    function deposit(bytes32 lock, uint price) payable external {
        hashLock storage hashLockRecord = hashLocks[lock];
        hashLockRecord.deposit  = price;
        hashLockRecord.client   = msg.sender;
        emit newDepositEvent(lock);
    }
    
    function openHashLock(bytes32 lock, string key ) external { 
        hashLock storage hashLockRecord = hashLocks[lock];
        bytes32 h = keccak256(abi.encodePacked(key));
        if( h == lock )
        {
            hashLockRecord.owner.transfer(hashLockRecord.deposit);
            hashLockRecord.deposit = 0;
            emit hashLockOpenedEvent(lock, key);
        }
    }

    function getHashLock (bytes32 lock) external view returns (string, address) {
        hashLock storage hashLockRecord = hashLocks[lock];
        return(hashLockRecord.metadata, hashLockRecord.owner);
    }

}

