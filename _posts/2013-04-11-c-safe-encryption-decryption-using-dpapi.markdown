---
layout: post
title:  "C# Safe Encryption/Decryption using DPAPI"
date:   2013-04-11 20:02:05 +0300
tags: c-sharp encryption
redirect_from: /security/c-safe-encryption-decryption-using-dpapi
image: /imgs/thumbnails/dpapi.webp
---

**Data Protection API** aka **DPAPI** is a neat service provided by Windows Operating Systems (newer than Windows 2000) that safely encrypts and decrypts user credentials, using the **Triple-DES** algorithm.

You have to supply the data as **byte array** in order to be encrypted / decrypted.

##### DPAPI uses the user's key to encrypt / decrypt so anyone who has access to your account can see the original data unless you define an **Entropy** - see below what that is.

## 1.What is needed

Before starting, **add a reference** to **System.Security.dll**, and include this line in your project:

```csharp
using System.Security.Cryptography;
```

For increased security, you can choose an **Entropy** (which is an additional byte array) to make the encryption safer - this way, users that have access to your Windows account must also know the Entropy used.

```csharp
readonly byte[] entropy = { 1, 2, 3, 4, 5, 6 }; //the entropy
```

## 2.Encryption

One of the functions that come with DPAPI is **Protect()**, that has 3 arguments. It returns an encrypted version of the message you provide.

```csharp
private string Encrypt(string text) 
{ 
    // first, convert the text to byte array 
    byte[] originalText = Encoding.Unicode.GetBytes(text); 
    
    // then use Protect() to encrypt your data 
    byte[] encryptedText = ProtectedData.Protect(originalText, entropy, DataProtectionScope.CurrentUser); 
    
    //and return the encrypted message 
    return Convert.ToBase64String(encryptedText); 
}
```

## 3.Decryption

Another function that comes with DPAPI is **Unprotect()**, has 3 parameters and returns the original message, when you supply the encrypted one.

```csharp
private string Decrypt(string text) 
{ 
    // the encrypted text, converted to byte array 
    byte[] encryptedText = Convert.FromBase64String(text); 
    
    // calling Unprotect() that returns the original text 
    byte[] originalText = ProtectedData.Unprotect(encryptedText, entropy, DataProtectionScope.CurrentUser); 
    
    // finally, returning the result 
    return Encoding.Unicode.GetString(originalText); 
}
```

## 4.Errors?

These methods may throw up errors if you try to decrypt a text using a different user than the one you used for encryption.

You can solve this by using **DataProtectionScope.LocalMachine** instead of **DataProtectionScope.CurrentUser**, this way any user has the possibility to decrypt the message if he knows the Entropy.
