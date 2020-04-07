---
layout: post
title:  "RSA: Encrypt in .NET & Decrypt in Python"
date:   2020-04-07 00:45:05 +0300
categories: tips-and-tricks
image: /imgs/thumbnails/rsa-python-net.png
---

So... one of my current projects required the following actions: asymmetrically **encrypt** a string in **.NET** using a **public key** and **decrypt** it in a **python** script using a **private key**.

The problem that I've encountered was that, apparently, I couldn't achieve compatibility between the two exposed classes: `RSACryptoServiceProvider`[1](https://docs.microsoft.com/en-us/dotnet/api/system.security.cryptography.rsacryptoserviceprovider?view=netframework-4.8) and `PKCS1_v1_5`[2](https://pycryptodome.readthedocs.io/en/latest/src/cipher/pkcs1_v1_5.html). To be more specific, the python script couldn't decrypt the ciphertext even though proper configurations were made and the provided keys were compatible. Additionally, separate encryption-decryption actions worked inside .NET and python but not in-between them.

I wasn't able to find too much information about this specific problem in the `RSAParameters` documentation[3](https://docs.microsoft.com/en-us/dotnet/api/system.security.cryptography.rsaparameters?view=netframework-4.8), hence this post.


## Solution

Alright, the issue seems to be caused by a difference in **endianness** between the two classes, when the RSA parameters are provided. `PKCS1_v1_5` (**python**) uses **little endian** and `RSACryptoServiceProvider` (**.NET**) prefers **big endian**. In my case, this made the encryption method use a different key than the one I though I specified. Nevertheless, it was more fun to debug because of PKCS which always ensured different ciphertexts.

I fixed this by **base64**-encoding the **exponent** and **modulus** in **big-endian** format (in python) and then loading them with `RSACryptoServiceProvider.FromXmlString()`[4](https://docs.microsoft.com/en-us/dotnet/api/system.security.cryptography.rsa.fromxmlstring?view=netframework-4.8) (in .NET). 

## Working Example

I hardcode the `(N, E, D)` parameters for a private key in **python** and export the **exponent** and **modulus** to be used later for encryption.

```python
# custom base64 encoding
def b64_enc(n, l):
    n = n.to_bytes(l, 'big')
    return base64.b64encode(n)

# fixed a set of keys for testing purposes (trimmed to avoid cluttering)
N = 26004126751443262055682011081007404548850063543219588539086190001742195632834884763548378850634989264309169823030784372770378521274048211537270851954737597964394738860810397764157069391719551179298507244962912383723776384386127059976543327113777072990654810746825378287761304202032439750301912045623786736128233730798303406858144431081065384988539277630625160727011582345942687126935423502995613920211095965452425548919926951203151483590222152446516520421379279591807660810550784744188433550335950652666201439521115515355539373928576162221297645781251953236644092963307595988040539993067709240004782161131243282208593
E = 65537
D =  844954574014654722486150458473919587206863455991060222377955072839922571984098861772377020041002939383041291761051853484512886782322743892284027026528735139923685801975918062144627908962369108081178131103781404720078456605432924519279933702927938064507063482999903002331319671303661755165294744970869186178561527578261522199503340027952798084625109041630166309505066404215223685733585467434168146932177924040219720383860880583466676764286302300281603021045351842170755190359364339936360197909582974922675680101321863304283607829144759777189360340512230537108705852116021758740440195445732631657876008160876867027543

# construct pair of keys
private_key = RSA.construct((N, E, D))
public_key = private_key.publickey()

# base64-encode parameters in big-endian format
EXP = b64_enc(public_key.e, 3)
MODULUS = b64_enc(public_key.n, 256)

print('EXP:', EXP, 'MODULUS:', MODULUS)

# Output:
# EXP: b'AQAB' MODULUS: b'zf4LgceVPvjMLz/pp8exH58AeBrhjLe0k4FRmd59I0k4sH6oug6Z9RfY4FvEFcssBwH1cmWF5/Zen8xbRVRyUnzer6b6cKmlzHFYf0LlbovvYMkW5pdhRcTHK2ijByGtmVgU/CEKEQTy3elpU7ZsHE8D6T1M7L2gmGAxvgldUMRu4l8BPuRyht1a9dA9b6005atpdlkCSc3emXSfyBOBwNE0UicVTVncn9SBjP7bTBGgOKshYnYsqh4BD0I7AU3xdoAsZVWudECX/zVa7uUOk1ooVYjMEyfBngrEDXrmIkAlVruUuj/eWiYwT2vXqByQgDfDvat5IS4i3ywiHAWXUQ=='
```

In **.NET** (I used **C#**), there will be something like this:
```csharp
using System;
using System.Security.Cryptography;
using System.Text;

public class RSACryptoApp
{
    // parameters from the python script (public key)
    private static readonly String EXP = "AQAB";
    private static readonly String MODULUS = "zf4LgceVPvjMLz/pp8exH58AeBrhjLe0k4FRmd59I0k4sH6oug6Z9RfY4FvEFcssBwH1cmWF5/Zen8xbRVRyUnzer6b6cKmlzHFYf0LlbovvYMkW5pdhRcTHK2ijByGtmVgU/CEKEQTy3elpU7ZsHE8D6T1M7L2gmGAxvgldUMRu4l8BPuRyht1a9dA9b6005atpdlkCSc3emXSfyBOBwNE0UicVTVncn9SBjP7bTBGgOKshYnYsqh4BD0I7AU3xdoAsZVWudECX/zVa7uUOk1ooVYjMEyfBngrEDXrmIkAlVruUuj/eWiYwT2vXqByQgDfDvat5IS4i3ywiHAWXUQ==";

    public static void Main(string[] args)
    {
       RSACryptoServiceProvider csp = new RSACryptoServiceProvider(2048);
       csp.FromXmlString("<RSAKeyValue><Exponent>" + EXP + "</Exponent><Modulus>" + MODULUS + "</Modulus></RSAKeyValue>");

       // encrypting a string for testing purposes
       byte[] plainText = Encoding.ASCII.GetBytes("Hello from .NET");
       byte[] cipherText = csp.Encrypt(plainText, false);

       Console.WriteLine("Encrypted: " + Convert.ToBase64String(cipherText));

       // Output:
       // Encrypted: F/agXpfSrs7HSXZz+jVq5no/xyQDXuOiVAG/MOY7WzSlp14vMOTM8TshFiWtegB3+2BZCMOEPLQFFFbxusuCFOYGGJ8yRaV7q985z/UDJVXvbX5ANYqrirobR+c868mY4V33loAt2ZFNXwr+Ubk11my1aJgHmoBem/6yPfoRd9GrZaSQnbJRSa3EDtP+8pXETkF9B98E7KvElrsRTLXEXSBygmeKsyENo5DDcARW+lVVsQuP8wUEGnth9SX4oG8i++gmQKkrv0ep6yFrn05xZJKgpOfRiTTo/Bkh7FxNP2wo7utzhtYkNnvtXaJPWAvqXg93KmNPqg1IsN4P1Swb8w==
    }
}
```


Back to the **python** script: 
```python
cipher = PKCS1_v1_5.new(private_key)

random_generator = Random.new().read
sentinel = random_generator(20)

cipher_text = 'F/agXpfSrs7HSXZz+jVq5no/xyQDXuOiVAG/MOY7WzSlp14vMOTM8TshFiWtegB3+2BZCMOEPLQFFFbxusuCFOYGGJ8yRaV7q985z/UDJVXvbX5ANYqrirobR+c868mY4V33loAt2ZFNXwr+Ubk11my1aJgHmoBem/6yPfoRd9GrZaSQnbJRSa3EDtP+8pXETkF9B98E7KvElrsRTLXEXSBygmeKsyENo5DDcARW+lVVsQuP8wUEGnth9SX4oG8i++gmQKkrv0ep6yFrn05xZJKgpOfRiTTo/Bkh7FxNP2wo7utzhtYkNnvtXaJPWAvqXg93KmNPqg1IsN4P1Swb8w=='

plain_text = cipher.decrypt(base64.b64decode(cipher_text.encode('ASCII')), sentinel)
print('Decrypted:', plain_text.decode('ASCII'))

# Output:
# Decrypted: Hello from .NET
```









