/*Configuration*/
var  ABI            = [{"constant":false,"inputs":[{"name":"lock","type":"bytes32"},{"name":"price","type":"uint256"}],"name":"deposit","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[{"name":"lock","type":"bytes32"},{"name":"key","type":"string"}],"name":"openHashLock","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"lock","type":"bytes32"}],"name":"getHashLock","outputs":[{"name":"","type":"string"},{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"lock","type":"bytes32"},{"name":"metadata","type":"string"}],"name":"createHashLock","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"anonymous":false,"inputs":[{"indexed":false,"name":"lock","type":"bytes32"}],"name":"hashLockCreatedEvent","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"lock","type":"bytes32"},{"indexed":false,"name":"key","type":"string"}],"name":"hashLockOpenedEvent","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"lock","type":"bytes32"}],"name":"newDepositEvent","type":"event"}];
var contractAddress = "0x796a52b3446ED0CaC17Ea7A332e8B4F83cC833cD";
var authServerURL   = "http://blockchain.mmlab.edu.gr/SOFIE/IAA/Authorization-Server/index.php";
/*End configuration*/ 