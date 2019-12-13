---
layout: post
title:  "C# Compile at Runtime"
date:   2012-08-05 20:02:05 +0300
categories: miscellaneous
thumbnail: /imgs/thumbnails/compileRuntime.png
---

To our luck, **.NET Framework** contains some classes that allow us to access the compiler and with it, we can **compile our code at runtime**.

Basically when our executable will run, it will compile a small piece of code stored in a string and saves the result as a new executable file.

## 1\. The code we want to compile at Runtime

First, write the code of a small valid C# application (preferable Console Project), that we'll compile at Runtime.

```csharpusing System;
using System.Text;
namespace Hello
{
  class Program
  {
    static void Main(string[] args)
     {
        Console.WriteLine("Hello World!");
        Console.ReadLine();
     }
  }
}```

## 2\. Writing the 'compiler'

Create a new application, and make sure you include these 2 lines:

```csharpusing Microsoft.CSharp;
using System.CodeDom.Compiler;```

Then, create a **CSharpCodeProvider** object - this will give us access to the .NET Compiler.

```csharpCSharpCodeProvider provider = new CSharpCodeProvider();  
ICodeCompiler compiler = provider.CreateCompiler();  //the compiler, created from CSharpCodeProvider```

It remains to adjust the compiler's settings, this can be done by providing some parameters:

```csharpCompilerParameters parameters = new CompilerParameters();

parameters.GenerateExecutable = true;  // we want to save it as an .exe
parameters.GenerateInMemory = false;  // it must be saved on the harddisk, not in memory
parameters.OutputAssembly = "hello.exe"; // the file's name
parameters.TreatWarningsAsErrors = false; // ignoring the warnings - my favourite one :)```

Now the compiler's done.

## 3\. Compiling the code

In the end, use a **string** to store the code you want to compile at Runtime, in this case, I'll compile the 'Hello World' code written at the beginning of the tutorial.

Be sure to escape any quotation mark from the code:

```csharpstring code = "using System; using System.Text; namespace Hello { class Program { static void Main(string[] args) { Console.WriteLine(\"Hello World\"); Console.ReadLine(); } } }";

CompilerResults result = compiler.CompileAssemblyFromSource(parameters, code);  
//compiling the code using the given parameters

if (result.Errors.Count > 0)   //if there are any compiling errors
{
    foreach (CompilerError er in result.Errors)
    {
          Console.WriteLine(er.ToString());  //we show them
    }
}```

## 4\. The whole program

This is how your compiler should look like, if you carefully followed the steps:

```csharpstatic void Main(string[] args)
{
    CSharpCodeProvider provider = new CSharpCodeProvider();
    ICodeCompiler compiler = provider.CreateCompiler();

    CompilerParameters parameters = new CompilerParameters();

    parameters.GenerateExecutable = true;
    parameters.GenerateInMemory = false;
    parameters.OutputAssembly = "hello.exe";
    parameters.TreatWarningsAsErrors = false;

    string code = "using System; using System.Text; namespace Hello { class Program { static void Main(string[] args) { Console.WriteLine(\"Hello World\"); Console.ReadLine(); } } }";

    CompilerResults result = compiler.CompileAssemblyFromSource(parameters, code);

    if (result.Errors.Count != 0)
    {
        foreach (CompilerError er in result.Errors)
        {
            Console.WriteLine(er.ToString());
        }
    }
}```