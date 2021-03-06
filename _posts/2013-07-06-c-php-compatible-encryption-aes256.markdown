---
layout: post
title:  "C#/PHP Compatible Encryption (AES256)"
date:   2013-07-06 20:02:05 +0300
tags: c-sharp php encryption aes
redirect_from: 
    - /security/c-php-compatible-encryption-aes256
    - /tips-and-tricks/c-php-compatible-encryption-aes256
image: /imgs/thumbnails/sharedEncryption.webp
---

Finding a way to encrypt messages in **C#** and decrypting them in **PHP** or vice versa seems to be a "challenge" for many users. I wrote this tutorial to provide some help with this: below, you can find how to **encrypt / decrypt** messages in **C# / PHP** using **AES256** with **CBC mode**.

## 1.Basic Information

**AES 256** with **CBC mode** requires 3 values: the **message**, a **key (32 bytes long)** and an **initialization vector (IV)**. Note that you must use the **same IV** when encrypting / decrypting a message: otherwise the message is lost. Sending the **IV** with the message is perfectly safe but it always **has to be a random value**. Since it has a fixed size, I always place the IV at the end of the encrypted text.

The encrypted messages _should_ be encoded using **base64** before being sent.

<span style="color:green">base64</span>(<span style="color:gray">[</span>ENCRYPTED_TEXT<span style="color:gray">][<span style="color:darkred">-[--IV-[-</span><span style="color:gray">][<span style="color:darkred">INITIALIZATION_VECTOR</span><span style="color:gray">]</span>)

<font color="darkred">Encryption steps:</font>

*   encrypt the text
*   add the IV at the end
*   encode everything (base64)

<font color="darkred">Decryption steps:</font>

*   decode the message
*   get & remove the IV
*   proceed to decrypt

Ok, enough talking, let's see some code...

## 2.PHP Encryption/Decryption Code

PHP accepts keys that are not **32 bytes** long and simply extends them to the correct length. Well...C# doesn't, so you'll have to **use a key that is 32 bytes long**.

<font size="4">Encryption</font>

```php
function encrypt($text, $pkey)
{
	$key = $pkey;  
	$IV = mcrypt_create_iv(mcrypt_get_iv_size(MCRYPT_RIJNDAEL_256, MCRYPT_MODE_CBC), MCRYPT_RAND); 

	return base64_encode(mcrypt_encrypt(MCRYPT_RIJNDAEL_256, $key, $text, MCRYPT_MODE_CBC, $IV)."-[--IV-[-".$IV); 
}```

<font size="4">Decryption</font>

```php
function decrypt($text, $pkey)
{
	$key = $pkey;   
	$text = base64_decode($text); 
	$IV = substr($text, strrpos($text, "-[--IV-[-") + 9);
	$text = str_replace("-[--IV-[-".$IV, "", $text);

	return rtrim(mcrypt_decrypt(MCRYPT_RIJNDAEL_256, $key, $text, MCRYPT_MODE_CBC, $IV), "\0");
}```

## 3.C# Encryption/Decryption Code

As I said before, C# doesn't accept keys that aren't **32 bytes long** - it will throw an error. Also, many people get tricked here because of the **encoding** (most of the times you have to use **Encoding.Default**).

<font size="4">Encryption</font>

```csharp
public static string EncryptMessage(byte[] text, string key)
{
    RijndaelManaged aes = new RijndaelManaged();
    aes.KeySize = 256;  
    aes.BlockSize = 256;
    aes.Padding = PaddingMode.Zeros;
    aes.Mode = CipherMode.CBC;

    aes.Key = Encoding.Default.GetBytes(key);
    aes.GenerateIV();  

    string IV = ("-[--IV-[-" + Encoding.Default.GetString(aes.IV));

    ICryptoTransform AESEncrypt = aes.CreateEncryptor(aes.Key, aes.IV);
    byte[] buffer = text;

    return
Convert.ToBase64String(Encoding.Default.GetBytes(Encoding.Default.GetString(AESEncrypt.TransformFinalBlock(buffer, 0, buffer.Length)) + IV));

}
```


<font size="4">Decryption</font>

```csharp
public static string DecryptMessage(string text, string key)
{
    RijndaelManaged aes = new RijndaelManaged();
    aes.KeySize = 256;
    aes.BlockSize = 256;
    aes.Padding = PaddingMode.Zeros;
    aes.Mode = CipherMode.CBC;

    aes.Key = Encoding.Default.GetBytes(key);

    text = Encoding.Default.GetString(Convert.FromBase64String(text));

    string IV = text;
    IV = IV.Substring(IV.IndexOf("-[--IV-[-") + 9);
    text = text.Replace("-[--IV-[-" + IV, "");

    text = Convert.ToBase64String(Encoding.Default.GetBytes(text));
    aes.IV = Encoding.Default.GetBytes(IV);

    ICryptoTransform AESDecrypt = aes.CreateDecryptor(aes.Key, aes.IV);
    byte[] buffer = Convert.FromBase64String(text);

    return Encoding.Default.GetString(AESDecrypt.TransformFinalBlock(buffer, 0, buffer.Length));
}
```