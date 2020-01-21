<?php

ini_set('display_errors',1);error_reporting(E_ALL);
require_once('oauth2-server-php/src/OAuth2/Autoloader.php');
OAuth2\Autoloader::register();
$publicKey  = file_get_contents('./keys/pubkey.pem');

// create storage
$storage = new OAuth2\Storage\Memory(array('keys' => array(
    'public_key'  => $publicKey,
)));

$server = new OAuth2\Server($storage, array(
    'use_jwt_access_tokens' => true,
    'issuer'=>'NKGKtcNwssToP5f7uhsEs4',
));

// verify the JWT Access Token in the request
if (!$server->verifyResourceRequest(OAuth2\Request::createFromGlobals())) {
    echo("Failed");
}
echo "Success!";
?>