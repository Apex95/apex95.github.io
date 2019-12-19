---
layout: post
title:  "C# Register a Url Protocol"
date:   2013-03-22 20:02:05 +0300
categories: miscellaneous
thumbnail: /imgs/thumbnails/protocolArgument.webp
---

This tutorial will show you how to register a custom **Url Protocol** for your application. Basically, you can control your application by simply clicking an Url address like this one:

**myApp:doSomething**

##### In this tutorial, I'll name the custom protocol **myApp** - but you can use any name you want.

## 1.Editing the Registry

In order to create your custom url protocol, you must first add it to the computer's Registry so it will know which application is associated with that protocol.

Here's the structure of the subkey you should create:

{% include image.html url="/imgs/posts/c-register-a-url-protocol/1.png" description="Setting an Application for the 'myApp' url protocol" %}

The method below creates all the **subkeys** needed:

```csharp
static void RegisterMyProtocol(string myAppPath)  //myAppPath = full path to your application
{
      RegistryKey key = Registry.ClassesRoot.OpenSubKey("myApp");  //open myApp protocol's subkey

      if (key == null)  //if the protocol is not registered yet...we register it
      {
          key = Registry.ClassesRoot.CreateSubKey("myApp"); 
          key.SetValue(string.Empty, "URL: myApp Protocol");
          key.SetValue("URL Protocol", string.Empty);

          key = key.CreateSubKey(@"shell\open\command");
          key.SetValue(string.Empty, myAppPath + " " + "%1");  
         //%1 represents the argument - this tells windows to open this program with an argument / parameter
      }

      key.Close();
}
```

## 2.Get the arguments in the Application

Now when you access a url like this: **myApp:SomeValue** Windows will automatically open your program and send to it the argument's value (which is "SomeValue").

Finally get the arguments supplied, by using **Environment.GetCommandLineArgs()**.

```csharp
static void Main()
{
      string[] args = Environment.GetCommandLineArgs();

      //args[0] is always the path to the application
      RegisterMyProtocol(args[0]); 
      //^the method posted before, that edits registry      

      try
      {
          //if there's an argument passed, write it
          Console.WriteLine("Argument: " + args[1].Replace("myapp:", string.Empty));  
      }
      catch
      {
          Console.WriteLine("No argument(s)");  //if there's an exception, there's no argument
      }

      Console.ReadLine(); //pauses the program - so you can see the result
}
```
