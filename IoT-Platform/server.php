<?php
require_once ('ctcore.php');
require_once ('keccak.php');
$contact_address = "0xadc6d997d6f3cff7ac482569574c0be131c49c3b";
$ACP_public_key  = "46E363VX0wsdDgYavCAZy/TiztlDCh0eofhKatyq8Rg=";

$ctcore = new CTCore();
if (isset($_GET['authtype']) && $_GET['authtype'] ==1)
{
    echo '{"token":"' .$ctcore->createRandomToken64().'","ACP":"'.$contact_address.'", "ACPPubKeyBase64":"'.$ACP_public_key.'"}';
}
else if (isset($_GET['authtype']) && $_GET['authtype'] ==2)
{
    $token = $ctcore->createRandomToken64();
    echo '{"token":"' .$token.'","ACP":"'.$contact_address.'", "ACPPubKeyBase64":"'.$ACP_public_key.'","hmacToken":"'.base64_encode($ctcore->hmac($token)).'"}';
}
else if (isset($_GET['authtype']) && $_GET['authtype'] ==3)
{
    $token        = $ctcore->createRandomToken64();
    $challenge    = $_GET['challenge'] ;
    $hskchallenge = base64_encode($ctcore->hmac($token)); 
    echo '{"token":"' .$token.'","ACP":"0xadc6d997d6f3cff7ac482569574c0be131c49c3b", "ACPPubKeyBase64":"46E363VX0wsdDgYavCAZy/TiztlDCh0eofhKatyq8Rg=","HashHmacChallenge":"'.KeccakHash::hash($hskchallenge,256).'"}';
}
else if(isset($_GET['token']))
{
    $plaintext = "Hello world";
    echo base64_encode($ctcore->encryptData($_GET['token'],$plaintext));
    
}

?>
