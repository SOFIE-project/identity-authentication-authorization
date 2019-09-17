async function createKeyIV(base64Token, hmacKey64)
{
    var hmacKey   = base64ToArrayBuffer(hmacKey64);
    var key       = await window.crypto.subtle.importKey("raw", hmacKey,{ name: "HMAC",hash: {name: "SHA-256"},}, false, ["sign", "verify"]);
    var hmac      = await window.crypto.subtle.sign({name: "HMAC",},key,base64ToArrayBuffer(base64Token));
    return hmac;
}

async function hmac(input64, hmacKey64)
{
    var hmacKey   = base64ToArrayBuffer(hmacKey64);
    var key       = await window.crypto.subtle.importKey("raw", hmacKey,{ name: "HMAC",hash: {name: "SHA-256"},}, false, ["sign", "verify"]);
    var hmac      = await window.crypto.subtle.sign({name: "HMAC",},key,base64ToArrayBuffer(input64));
    key           = await window.crypto.subtle.importKey("raw", hmac,{ name: "HMAC",hash: {name: "SHA-256"},}, false, ["sign", "verify"]);
    hmac          = await window.crypto.subtle.sign({name: "HMAC",},key,base64ToArrayBuffer(input64));
    return hmac;
}

async function encryptData(base64Key, data)
{
    var arrayKey   = base64ToArrayBuffer(base64Key);
    var key        = await window.crypto.subtle.importKey("raw", arrayKey.slice(0,16),{ name: "AES-GCM",}, false, ["encrypt", "decrypt"]);
    var ciphertext = await window.crypto.subtle.encrypt({name: "AES-GCM",iv: arrayKey.slice(16,32),tagLength: 128,},key,stringToArrayBuffer(data));
    return ciphertext;
}

async function decryptData(base64Key, data)
{
    var arrayKey   = base64ToArrayBuffer(base64Key);
    var key        = await window.crypto.subtle.importKey("raw", arrayKey.slice(0,16),{ name: "AES-GCM",}, false, ["encrypt", "decrypt"]);
    var plaintext = await window.crypto.subtle.decrypt({name: "AES-GCM",iv: arrayKey.slice(16,32),tagLength: 128,},key,base64ToArrayBuffer(data));
    return plaintext;
}

function base64ToArrayBuffer(base64) {
    
    return base64ToUint8Array(base64).buffer;
}

function arrayBufferToBase64(buffer) {
    var bytes = new Uint8Array(buffer);
    return Uint8ArrayToBase64(bytes);
    
}

function Uint8ArrayToBase64(bytes){
    var binary = '';
    var len = bytes.byteLength;
    for (let i = 0; i < len; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return btoa(binary);
}

function base64ToUint8Array(base64){
    var binary_string =  window.atob(base64);
    var len = binary_string.length;
    var bytes = new Uint8Array( len );
    for (var i = 0; i < len; i++)        {
        bytes[i] = binary_string.charCodeAt(i);
    }
    return bytes;
}

function stringToArrayBuffer(string){
    var len = string.length;
    var bytes = new Uint8Array( len );
    for (var i = 0; i < len; i++)        {
        bytes[i] = string.charCodeAt(i);
    }
    return bytes.buffer;
}

function arrayBufferToString(buffer){
    var bytes = new Uint8Array(buffer);
    var binary = '';
    var len = bytes.byteLength;
    for (let i = 0; i < len; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return binary;
}

function createRandomToken64(tokenSize)
{
    var token = new Uint32Array(10);
    window.crypto.getRandomValues(token);
    return btoa(token);
}

