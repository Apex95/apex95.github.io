---
layout: post
title:  "C# Password Protected File"
date:   2013-12-08 20:02:05 +0300
categories: file
thumbnail: /imgs/thumbnails/filePassword.png
---

In this article...I'll talk about how to <u>protect a file with a password</u> (any file type) - without using **ZIP** or any other archivers. The file will be encrypted and then 'attached' to an executable, which will be later used to decrypt it using the password provided.

## Starting information

Initially there'll be 2 files: the file we want to encrypt, and the decryptor (which is a C# executable). These files will be 'merged' together, and when needed, the decryptor will retrieve from its own file the content of the original file.

<u>How to 'pack' the file (steps):</u>

1.  get the content (bytes) of the file we want to protect by password
2.  encrypt it using a good algorithm (I'm using **AES**)
3.  put everything at the end of the generic decryptor *

_* the executable file won't be affected by what we add._

<u>How to decrypt the file</u>:

1.  the file is appended at the end of the decryptor, so we need to skip as many bytes as the <u>original decryptor's size</u> (when it has no file attached)
2.  load the file's content into memory -> decrypt it with the password provided
3.  save the content as a new file

![](http://oi40.tinypic.com/16hrqt5.jpg)

## 1\. Creating the decryptor

This part explains how to write the decryptor application: the resulting executable is, what I like to call, the 'original decryptor'. Its size is exactly **10240 bytes**, so after we attach the encrypted file, we need to skip those bytes when we want to decrypt the content.

I made it as a **Forms** project only for the sake of design - anyway there's only 1 method that does all the work so it can be easily modified.

{% highlight csharp linenos %}using System;
using System.Diagnostics;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using System.Windows.Forms;

namespace decryptor
{
    public partial class DecryptorWnd : Form
    {
        public DecryptorWnd()
        {
            InitializeComponent();
        }

        // hardcoded size of the original decryptor...lazy coder...
        int decryptorSize = 10240;  

        private void decryptButton_Click(object sender, EventArgs e)
        {
            // sending the current process' name and the password provided by the user
            decrypt(Process.GetCurrentProcess().ProcessName, passwordTextBox.Text);
        }

        private void decrypt(string file, string password)
        {
            byte[] key = new byte[32]; // 256 bits key
            Encoding.Default.GetBytes(password).CopyTo(key, 0); // padding with 0

            RijndaelManaged aes = new RijndaelManaged();
            aes.Mode = CipherMode.CBC;
            aes.KeySize = 256;
            aes.BlockSize = 256;
            aes.Padding = PaddingMode.Zeros;

            using (FileStream outputStream = new FileStream("decrypted_" + file, FileMode.Create))
            {
                using (CryptoStream cryptoStream = new CryptoStream(outputStream, aes.CreateDecryptor(key, key), CryptoStreamMode.Write))
                {
                    // reading the content of the current process
                    byte[] buffer = File.ReadAllBytes(file + ".exe");  

                    // skip the original decryptor's size (we don't want to decrypt that!)
                    cryptoStream.Write(buffer, decryptorSize, buffer.Length - decryptorSize);  
                }
            }
        }
    }
}{% endhighlight %}

## 2\. Attaching the file to the decryptor

This requires another executable file that will handle encryption and file attachment. I used a **Console Application** for this - to be honest I never intended to publish this as a program, I was just testing - and for testing, the console was enough.

{% highlight csharp linenos %}using System.IO;
using System.Security.Cryptography;
using System.Text;

namespace FileAppender
{
    class Program
    {
        static MemoryStream mStream = new MemoryStream();

        public static void Main()
        {
            encrypt("SomeFile.txt", "myPassword");
        }

        private static void encrypt(string fileName, string password)
        {
            byte[] key = new byte[32];  // same key (256 bits)
            Encoding.Default.GetBytes(password).CopyTo(key, 0);  // padding with 0 once again

            RijndaelManaged aes = new RijndaelManaged();
            aes.Mode = CipherMode.CBC;
            aes.KeySize = 256;
            aes.BlockSize = 256;
            aes.Padding = PaddingMode.Zeros;

            using (CryptoStream cStream = new CryptoStream(mStream, aes.CreateEncryptor(key, key), CryptoStreamMode.Write))
            {
                // reading the content of the file that requires password protection
                byte[] buffer = File.ReadAllBytes(fileName);

                // encrypting & storing everything in a MemoryStream
                cStream.Write(buffer, 0, buffer.Length);
            }
            append(fileName); // time to append
        }

        private static void append(string file)
        {
            // reading the content of the original decryptor
            byte[] exeBuffer = File.ReadAllBytes("decryptor.exe");  

            // extracting the encrypted content from the MemoryStream
            byte[] appendBuffer = mStream.ToArray() ;

            // this buffer is the 'new' decryptor, that contains the new file
            byte[] finalBuffer = new byte[exeBuffer.Length + appendBuffer.Length];
            exeBuffer.CopyTo(finalBuffer, 0);
            appendBuffer.CopyTo(finalBuffer, exeBuffer.Length);

            // creating 'SomeFile.txt.exe'
            File.WriteAllBytes(file + ".exe", finalBuffer);
        }
    }
}{% endhighlight %}

## Note

This code is provided to give you an idea on how to write such a program. This means it's <u>not optimized</u>, so it can be improved.HF.