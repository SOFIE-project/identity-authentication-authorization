/*Configuration*/
var  ABI            = [{"constant":false,"inputs":[{"name":"lock","type":"bytes32"},{"name":"price","type":"uint256"}],"name":"deposit","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[{"name":"lock","type":"bytes32"},{"name":"key","type":"string"}],"name":"openHashLock","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"lock","type":"bytes32"}],"name":"getHashLock","outputs":[{"name":"","type":"string"},{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"lock","type":"bytes32"},{"name":"metadata","type":"string"}],"name":"createHashLock","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"anonymous":false,"inputs":[{"indexed":false,"name":"lock","type":"bytes32"}],"name":"hashLockCreatedEvent","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"lock","type":"bytes32"},{"indexed":false,"name":"key","type":"string"}],"name":"hashLockOpenedEvent","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"lock","type":"bytes32"}],"name":"newDepositEvent","type":"event"}];
var contractAddress = "0x796a52b3446ED0CaC17Ea7A332e8B4F83cC833cD" // Rinkeby
var web3Provider    = "http://195.251.234.25:8546"; 
var ethAccountAddr  = "0xD41e00c8F1474e337142f2F860Fb7dEb9e1492E3"; // ***Account must be unlocked***
var authServerURL   = "acp.mmlab.edu.gr";
/*End configuration*/

const http = require('http')
const Web3 = require('web3');
const web3 = new Web3(new Web3.providers.HttpProvider(web3Provider));
console.log("Connected to rpc server...");
var access = web3.eth.Contract(ABI,contractAddress);
access.events.newDepositEvent(depositEventHandler);

function createHashLock(data){
    console.log(`HashLock API invoked lock=${data.lock}, metadata=${data.metadata}`)
    access.methods.createHashLock(data.lock, data.metadata).send({from:ethAccountAddr,gas: 3000000},function(error, result) { 
        if (!error)
        {
            console.log(`Hashlock creation invoked`);  
        }else
        {
            console.log("Error: " + error); 
        } 
    })
}

function depositEventHandler(error,result)
{
    console.log("New deposit event")
    var lock = result.args.lock
    var nonce = ''
    access.methods.getHashLock(lock).call().then(function(result){
        nonce = result.nonce;
        console.log(`Will request the key for ${nonce}`);
        var post_data = `{"nonce":"${nonce}"}`;
    
        var post_options = {
            host: authServerURL,
            port: '80',
            path: '/?api=newDepositEvent',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(post_data)
            }
        };

        var key =''
        var post_req = http.request(post_options, function(response) {
            response.on('data', function (data) {
                key += data;
            })
            response.on('end', function() {
                access.methods.openHashLock(lock, key).send({from:ethAccountAddr,gas: 3000000},function(error, result) { 
                    if (!error)
                    {
                        console.log(`Hashlock unlock invoked`);  
                    }else
                    {
                        console.log("Error: " + error); 
                    } 
                });
            })
        })

        post_req.write(post_data);
        post_req.end();
    });
    
}

const server = http.createServer(function(request, response) {
    if (request.method == 'POST') {
        var body = ''
        request.on('data', function(data) {
            body += data
        })
        request.on('end', function() {
            if(request.url == "/createhashlock") {
                createHashLock(JSON.parse(body))
            }
            response.writeHead(200, {'Content-Type': 'text/html'})
            response.end()
        })
}
});

const port = 3000
const host = '127.0.0.1'
server.listen(port, host)
console.log(`Listening at http://${host}:${port}`)