---
layout: post
title:  "C# Prevent Decompilation by Decrypting Source at Runtime"
date:   2016-09-19 20:02:05 +0300
categories: security
thumbnail: /imgs/thumbnails/reflector-runtime-decryption.png
---

*Hello world!* 

Today we continue the *"Trolling the Decompiler"* series (first part here: [Prevent Reflector from Decompiling](http://www.codingvision.net/security/c-prevent-reflector-from-decompiling))
but now with a more serious approach - this one should work on **any decompiler**.

<u>The point is:</u> it is rather difficult to make **.NET** programs run with a key or license; since these can be reverted back
to their sourcecode, anyone can alter it or just learn to create fake keys that will be seen as valid.

{% include image.html url="/imgs/posts/c-prevent-decompilation-by-decrypting-source-at-runtime/1.png" description="Data placed as plain text in a .NET application can be easily discovered" %}


## Possible Solution

One way to make an application a little bit more difficult to crack would be to deliver it as a program
that **decrypts** instructions, **compiles** and **runs** them only when needed. This way, if someone finds out where
the sourcecode is stored, it will still be encrypted and without a **key** (or license) it is unusable.

We're kinda writing polymorphic stuff here - AVs won't be happy; actually...only 2/57 don't like it, we're good.


## 1. Making the Compiler

We're not really going to reinvent the wheel here - .NET seems to allow us to use the original compiler to produce
an `Assembly`. Just as always, we start with a `CodeDomProvider`, add a bunch of settings using `CompilerParameters` and
a few sourcecodes.

{% highlight csharp linenos %}
CodeDomProvider provider = CodeDomProvider.CreateProvider("CSharp");

CompilerParameters parameters = new CompilerParameters();

parameters.GenerateExecutable = true;
parameters.GenerateInMemory = true; // it's still going to generate a file somewhere in AppData (temp)
parameters.TreatWarningsAsErrors = false;
            
// I need these references because the program that I will 'secure'
// is that Form from the photo above that requires a password
parameters.ReferencedAssemblies.Add("System.Windows.Forms.dll");
parameters.ReferencedAssemblies.Add("System.dll");
parameters.ReferencedAssemblies.Add("System.Drawing.dll");

// getContents() is a method that extracts & decrypts the sourcecodes 
// of the 'secured' application and returns everything as an array of Strings
// in order to be compiled

CompilerResults result = provider.CompileAssemblyFromSource(parameters, getContents());
{% endhighlight %}


If you look around, there's also an article that provides a little bit more detail about how to compile code at runtime
using `CSharpCodeProvider` and `ICodeCompiler` which are now considered obsolete, but the code is similar.


## 2. Running the Compiled Assembly

What we're interested in is `result.CompiledAssembly` - in order to run it we have to create an **instance** of the 
method that serves as **entrypoint** and then **invoking** it.

<u>Short note:</u> if the assembly that you're trying to run belongs to a **Console Application** and this program has the same
project type, you might need to call `FreeConsole()` and then `AllocConsole()`. Without recreating the **Console** there seems 
to be no output from the compiled assembly.

This is how we can run the compiled code:

{% highlight csharp linenos %}
Assembly assembly = result.CompiledAssembly;

//taking the entrypoint
MethodInfo methodInfo = assembly.EntryPoint;

// creating an instance
object entryPointInstance = assembly.CreateInstance(methodInfo.Name);

// then invoking it with no arguments (hence the 'null')
methodInfo.Invoke(entryPointInstance, null);
{% endhighlight %}


## 3. Encrypting & Attaching Sourcecodes

This is one of the tough parts - we take the sourcecodes of the files that we want to secure and 
encrypt them (I use **AES** with **Rijndael**'s algorithm) then attach the results at the end of the executable that we've
been working on at the previous steps.

Here, the content of the executable and each sourcecode are separated by a sequence of **3** **FS** (File Separator Character).
It's not the clean way to handle this...don't use it in serious projects; but for this tutorial it should be fine.

**FS** = **28**(dec) = **1C**(hex);

{% include image.html url="/imgs/posts/c-prevent-decompilation-by-decrypting-source-at-runtime/2.png" description="Hex editor view: the format of the encrypter with 2 attached files." %}

The method that I use looks like this:

{% highlight csharp linenos %}
static void appendContents(String fileName)
{
    // fileName contains the name of the decrypter 
    FileStream fstream = new FileStream(fileName, FileMode.Append);
    
    // attaching the first 3 FS chars
    fstream.WriteByte(CHAR_FS);
    fstream.WriteByte(CHAR_FS);
    fstream.WriteByte(CHAR_FS);

    // grabbing any .cs file (anything that needs to be encrypted and attached)
    string[] sourceFiles = Directory.GetFiles(Path.GetDirectoryName(Assembly.GetEntryAssembly().Location), "*.cs", SearchOption.AllDirectories);

    // taking each source file
    for (int i = 0; i < sourceFiles.Length; i++)
    {
        byte[] buffer = File.ReadAllBytes(sourceFiles[i]);
                

        // removing UTF8's byte order mark, if needed
        if (buffer.Length > 2 && buffer[0] == 0xEF && buffer[1] == 0xBB && buffer[2] == 0XBF)
        {
            // skipping the first 3 bytes
            byte[] newBuffer = new byte[buffer.Length - 3];
            Array.Copy(buffer, 3, newBuffer, 0, buffer.Length - 3);

            // encrypting with a test key
            newBuffer = EncryptMessage(newBuffer, "abcdabcdabcdabcdabcdabcdabcdabcd");

            // writing...
            fstream.Write(newBuffer, 0, newBuffer.Length);
        }
        else
        {
            // same thing as above, but for texts without BOM
            buffer = EncryptMessage(buffer, "abcdabcdabcdabcdabcdabcdabcdabcd");
            fstream.Write(buffer, 0, buffer.Length);
        }

        // more separators!
        fstream.WriteByte(CHAR_FS);
        fstream.WriteByte(CHAR_FS);
        fstream.WriteByte(CHAR_FS);
    }
}
{% endhighlight %}

I'll not add `EncryptMessage()`'s code here since it's not related to the actual subject - you can find it below,
in the complete sourcecode.


## 4. Extracting & Decrypting Sourcecodes

Procedure that runs before the whole compile & run thingy - we look for any sequence of **3** **FS** characters,
skip the executable's content, take the encrypted sourcecode and run it through the decryption method - the result
is pure C# code that will be given to the compiler.

Remember to replace the `"abcdabcdabc..."` decryption key with what the user inputs in order to use the program
(like a license) - **line 31**.

{%highlight csharp linenos %}
static String[] getContents()
{
    // reads all the bytes found in the running executable's file
    byte[] bytes = File.ReadAllBytes(Assembly.GetEntryAssembly().Location);

    int i = 0;
            
    List<String> sourceFiles = new List<String>();

    // skipping the original executable's data
    for (i = 0; i < bytes.Length - 2; i++)
    {
        // if there are 3 FS characters in a row
        // then there's a source file
        if (bytes[i] == bytes[i + 1] && bytes[i + 1] == bytes[i + 2] && bytes[i + 2] == 28)
        {
            i += 3;
            break;
        }
    }

    // here I should keep one sourcefile at a time
    List<Byte> sourceFileBuffer = new List<Byte>(4000);

    for (; i < bytes.Length - 2; i++)
    {
        // checking if I reached the end of a sourcefile
        if (bytes[i] == bytes[i + 1] && bytes[i + 1] == bytes[i + 2] && bytes[i + 2] == 28)
        {
            // TO DO: decrypt with the key given by the user of the program
            sourceFiles.Add(Encoding.Default.GetString(DecryptMessage(sourceFileBuffer.ToArray(), "abcdabcdabcdabcdabcdabcdabcdabcd")));
            sourceFileBuffer.Clear();
            i += 2;
        }
        else
            sourceFileBuffer.Add(bytes[i]);
    }

    // returning the array of sourcecodes
    return sourceFiles.ToArray();
}
{% endhighlight %} 


## Final Notes & Complete Sourcecode

Below you'll find the sourcecode I ended up with while writing this article. It's more like a fast way to explain an idea - it needs some "patching".

In order to actually use it you should split this into **2** programs - one for encrypting and attaching and the other to do the decryption, compilation & execution.
You send **only** the latter one to the user - so he won't get the **encryption key** - this or switch to an **asymmetric** algorithm. Also don't forget to remove 
the hardcoded **decryption key** and ask the user for his own.

{%highlight csharp linenos %}
using System;
using System.CodeDom.Compiler;
using System.Collections.Generic;
using System.IO;
using System.Reflection;
using System.Security.Cryptography;
using System.Text;

namespace ConsoleApplication1
{
    class Program
    {
        const int CHAR_FS = 28;

        public static byte[] EncryptMessage(byte[] text, string key)
        {
            RijndaelManaged aes = new RijndaelManaged();
            aes.KeySize = 256;
            aes.BlockSize = 256;
            aes.Padding = PaddingMode.Zeros;
            aes.Mode = CipherMode.CBC;

            aes.Key = Encoding.Default.GetBytes(key);
            aes.GenerateIV();

            string IV = Encoding.Default.GetString(aes.IV);

            ICryptoTransform AESEncrypt = aes.CreateEncryptor(aes.Key, aes.IV);
            byte[] buffer = text;

            return Encoding.Default.GetBytes(Encoding.Default.GetString(AESEncrypt.TransformFinalBlock(buffer, 0, buffer.Length)) + IV);
        }

        public static byte[] DecryptMessage(byte[] text, string key)
        {
            RijndaelManaged aes = new RijndaelManaged();
            aes.KeySize = 256;
            aes.BlockSize = 256;
            aes.Padding = PaddingMode.Zeros;
            aes.Mode = CipherMode.CBC;

            aes.Key = Encoding.Default.GetBytes(key);

            byte[] IV = new byte[32];
            Array.Copy(text, text.Length - 32, IV, 0, 32);

            byte[] text2 = new byte[text.Length - 32];
            Array.Copy(text, text2, text2.Length);

            aes.IV = IV;

            ICryptoTransform AESDecrypt = aes.CreateDecryptor(aes.Key, aes.IV);

            return AESDecrypt.TransformFinalBlock(text2, 0, text2.Length);
        }

        static void appendContents(String fileName)
        {
            FileStream fstream = new FileStream(fileName, FileMode.Append);
            fstream.WriteByte(CHAR_FS);
            fstream.WriteByte(CHAR_FS);
            fstream.WriteByte(CHAR_FS);


            string[] sourceFiles = Directory.GetFiles(Path.GetDirectoryName(Assembly.GetEntryAssembly().Location), "*.cs", SearchOption.AllDirectories);


            for (int i = 0; i < sourceFiles.Length; i++)
            {
                byte[] buffer = File.ReadAllBytes(sourceFiles[i]);
                

                // removing UTF8's byte order mark...
                if (buffer.Length > 2 && buffer[0] == 0xEF && buffer[1] == 0xBB && buffer[2] == 0XBF)
                {
                    byte[] newBuffer = new byte[buffer.Length - 3];
                    Array.Copy(buffer, 3, newBuffer, 0, buffer.Length - 3);

                    newBuffer = EncryptMessage(newBuffer, "abcdabcdabcdabcdabcdabcdabcdabcd");

                    fstream.Write(newBuffer, 0, newBuffer.Length);
                }
                else
                {
                    buffer = EncryptMessage(buffer, "abcdabcdabcdabcdabcdabcdabcdabcd");

                    fstream.Write(buffer, 0, buffer.Length);
                }

                fstream.WriteByte(CHAR_FS);
                fstream.WriteByte(CHAR_FS);
                fstream.WriteByte(CHAR_FS);
            }
        }
        static String[] getContents()
        {
            byte[] bytes = File.ReadAllBytes(Assembly.GetEntryAssembly().Location);

            int i = 0;
            
            List<String> sourceFiles = new List<String>();

            for (i = 0; i < bytes.Length - 2; i++)
            {
                if (bytes[i] == bytes[i + 1] && bytes[i + 1] == bytes[i + 2] && bytes[i + 2] == 28)
                {
                    i += 3;
                    break;
                }
            }

            List<Byte> sourceFileBuffer = new List<Byte>(4000);

            for (; i < bytes.Length - 2; i++)
            {
                if (bytes[i] == bytes[i + 1] && bytes[i + 1] == bytes[i + 2] && bytes[i + 2] == 28)
                {
                    sourceFiles.Add(Encoding.Default.GetString(DecryptMessage(sourceFileBuffer.ToArray(), "abcdabcdabcdabcdabcdabcdabcdabcd")));
                    sourceFileBuffer.Clear();
                    i += 2;
                }
                else
                    sourceFileBuffer.Add(bytes[i]);

            }
            return sourceFiles.ToArray();
        }

        static void Main(string[] args)
        {
            CodeDomProvider provider = CodeDomProvider.CreateProvider("CSharp");

            CompilerParameters parameters = new CompilerParameters();

            parameters.GenerateExecutable = true;
            parameters.GenerateInMemory = true;
            parameters.TreatWarningsAsErrors = false;
            

            parameters.ReferencedAssemblies.Add("System.Windows.Forms.dll");
            parameters.ReferencedAssemblies.Add("System.dll");
            parameters.ReferencedAssemblies.Add("System.Drawing.dll");

            if (args.Length > 0)
            {
                appendContents(args[0]);
                return;
            }

            // source-files
            CompilerResults result = provider.CompileAssemblyFromSource(parameters, getContents());


            if (result.Errors.Count > 0)
            {
                foreach (CompilerError er in result.Errors)
                    Console.WriteLine(er.ToString());

                Console.ReadLine();
                return;
            }

            Assembly assembly = result.CompiledAssembly;
            MethodInfo methodInfo = assembly.EntryPoint;

            object entryPointInstance = assembly.CreateInstance(methodInfo.Name);
            methodInfo.Invoke(entryPointInstance, null);
        }
    }
}
{% endhighlight %}


## Proof of concept

Short video, before people start saying *it's not working!!!*.

<iframe width="560" height="315" src="https://www.youtube.com/embed/q2Ip8A-8wu8" frameborder="0" allowfullscreen></iframe>

<a href="http://www.codeproject.com" rel="tag" style="display:none;">CodeProject</a>

