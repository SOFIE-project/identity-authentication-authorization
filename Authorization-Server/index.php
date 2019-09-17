<?php

require_once ('keccak.php');
    /*
    * For the first scenario of  WF-IoT (https://mm.aueb.gr/publications/2019-WF-IoT.pdf),
    * we extended the library. 
    *
    * The output is a json with the following fields:
    *    "expires_in"
    *    "token_type"
    *    "scope"
    *    "e_s_token"
    *    "e_thing_pop"
    *    "pop":"
    *    "h"
    *    "rest_of_info_hash" 
    */

    /* Begin configuration */
    $psk      = "B395B9E6C9F81"; //The secret key pre-shared between the device and the authorization server, 128 bit key  base64 encoded
    $msk      = "jOhkR0z4HWQQmoqCMKdN2Jkn8QZeXwJALDBmYJH5gyc="; //A secret key used in an hmac function for producing the token encryption keys
    $IAAagent = "http://127.0.0.1:3000"; //The URL of the IAA blockchain agent
    /* End configuration */

    function encryptData( $keyIV, $plaintext)
    {
        $cipher = "aes-128-gcm";
        $key = substr($keyIV, 0, 16);
        $iv  = substr($keyIV, 16, 12);
        $ciphertext = openssl_encrypt($plaintext, $cipher, $key, $options=0, $iv, $tag,"",16); 
        return $ciphertext.$tag.$iv;
    }

    function generateTokenEncryptionKey($seed =null)
    {
        global $msk;
        if ($seed == null )
            $random = openssl_random_pseudo_bytes(16);
        else 
            $random = base64_decode($seed);
        $key    = hash_hmac('sha256', $random , base64_decode($msk),true);
        $lock   = keccakHash::hash(base64_encode(substr($key, 0, 28)),256, true);

        return array($random, $key, "0x".bin2hex($lock));
    }

    function agentCreateHashLock($lock, $metadata)
    {
        global $IAAagent;
        $data = array("lock" => $lock, "metadata" => $metadata);   
        $postdata = json_encode($data);

        $opts = array('http' =>
            array(
                'method'  => 'POST',
                'header'  => 'Content-type: application/json',
                'content' => $postdata
            )
        );
        $context = stream_context_create($opts);
        file_get_contents("$IAAagent/createhashlock", false, $context);
    }

    if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
          header('Access-Control-Allow-Origin: *');
          header('Access-Control-Allow-Headers: Authorization,Content-Type');
          exit;
    }
    
    /*
     * Call back from IAA agent
     */ 
    if(isset($_GET['api']) && $_GET['api'] == 'newDepositEvent')
    {
        $postdata = file_get_contents('php://input');
        $data     = json_decode($postdata, true);
        $keypair  = generateTokenEncryptionKey($data["nonce"]); 
        $key      = base64_encode(substr($keypair[1], 0, 28));  
        echo "key ". $key;
    }
    
    /*
     * The client interacts directly with the OAuth Server
     */ 
    if(isset($_GET['method']) && $_GET['method'] == 'direct')
    {      
        ini_set('display_errors',1);error_reporting(E_ALL);
        require_once('oauth2-server-php/src/OAuth2/Autoloader.php');
        OAuth2\Autoloader::register();
        $clients = array('sofie' => array('client_secret' => 'sofie!'));
        $storage = new OAuth2\Storage\Memory(array('client_credentials' => $clients));
        $server = new OAuth2\Server($storage);
        $grantType = new OAuth2\GrantType\ClientCredentials($storage);
        $server->addGrantType($grantType);
        $request = OAuth2\Request::createFromGlobals();
        $response = $server->handleTokenRequest($request);
        $plaintoken = $response->getParameter("access_token");
        $keypair = generateTokenEncryptionKey();
        $response->addParameters(array("lock"=>$keypair[2]));
        $response->setParameter("access_token",base64_encode(encryptData($keypair[1],$plaintoken)));
        $response->setHttpHeaders(array('Access-Control-Allow-Origin' => "*"));
        $response->send();
        agentCreateHashLock($keypair[2],"{\"nonce\":\"".base64_encode($keypair[0])."\"}");
    }
    
    /*
    *  In the first scenario, we insert a key (AS1ThingKey) for symmetric encryption, 
    *  between the AS and the Thing. 
    */
    /*
    $AS1ThingKey = '/home/dimitrios-d/OAuth2BlockChainKeys/AS1Thingkey'; 
    $symetricKey = trim(file_get_contents($AS1ThingKey));
    $storage = new OAuth2\Storage\Memory(array(
        'keys' => array(
            'private_key' => $symetricKey, // The appropriate key for HS256.
            'encryption_algorithm'  => 'HS256' // "RS256" is the default
        ),
        // add a Client ID for testing
        'client_credentials' => array(
            'theClient' => array('client_secret' => 'thePassword')
        ),
    ));
    $server = new OAuth2\Server($storage, array(
        'use_jwt_access_tokens_sophie_experiments' => true,
        'issuer' => 'AS_1',
        'subject' => 'SFA1',   
        'scope' => 'Blockchain with IoT'
    ));
    $server->setKeys($AS1ThingKey); 
    $server->addGrantType(new OAuth2\GrantType\ClientCredentials($storage)); 
    $server->handleTokenRequestForSophie( "Scenario1", OAuth2\Request::createFromGlobals())->send();
    */
?>