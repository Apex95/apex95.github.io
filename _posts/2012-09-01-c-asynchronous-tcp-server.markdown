---
layout: post
title:  "C# Asynchronous Tcp Server"
date:   2012-09-01 20:02:05 +0300
categories: networking
thumbnail: /imgs/thumbnails/asynctcplistener.bmp
---

This is the model of an **Asynchronous TCP server**, that can have multiple clients connected, each one on it's own **thread** - all of this is done using a relatively short and easy-to-remember code.

If you don't have basic knowledge of how a Tcp server works, it is highly recommended to read first: [how to make a simple tcp server](https://www.codingvision.net/networking/c-simple-tcp-server "C# simple tcp server").

## The code

As always, the code first and after, the comments:  
* functions used for sending/receiving data are not included - you should know these, from the basic server stuff.

{% highlight csharp linenos %}using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net;      
using System.Net.Sockets;  

using System.Threading;

namespace ServerTest
{
    class Program
    {

        static void Main(string[] args)
        {
            Program main = new Program();
            main.server_start();  //starting the server

            Console.ReadLine();  
        }

        TcpListener server = new TcpListener(IPAddress.Any, 9999);   

        private void server_start()
        {
            server.Start();    
            accept_connection();  //accepts incoming connections
        }

        private void accept_connection()
        {
            server.BeginAcceptTcpClient(handle_connection, server);  //this is called asynchronously and will run in a different thread
        }

        private void handle_connection(IAsyncResult result)  //the parameter is a delegate, used to communicate between threads
        {
            accept_connection();  //once again, checking for any other incoming connections
            TcpClient client = server.EndAcceptTcpClient(result);  //creates the TcpClient

            NetworkStream ns = client.GetStream();

            /* here you can add the code to send/receive data */

        }

    }
}{% endhighlight %}

## Comments

This is the server, containing almost anything required to work properly.

Now, to understand how it works, take a look at the methods below:

{% highlight csharp linenos %}        private void server_start()
        {
            ...  
            accept_connection();  
        }

        private void accept_connection()
        {
            server.BeginAcceptTcpClient(handle_connection, server);  
        }

        private void handle_connection(IAsyncResult result)
        {
            accept_connection();
            TcpClient client = server.EndAcceptTcpClient(result);
            ...
        }

{% endhighlight %}

- first, the program calls the function **accept_connection()** - used to accept a client's connection to the server. This function will invoke through **BeginAcceptTcpClient** another function called **handle_connection()** which will run on a **different thread** chosen from the **threadpool** - so you don't have to manually create/release threads.

- when **handle_connection()** is called, it also receives an **IAsyncResult** argument - this argument maintains the connection between the 2 threads. This method will then call again **accept_connection()** - so the program will constantly change the threads.

- if the connection is closed, the thread used is released automatically and can later be used for a new client; however this threadpool is limited.

## In the end...

This is basically everything you _might_ need to know about the **asynchronous tcp servers** - without involving any unnecessary code. If there are any questions, feel free to leave a comment :)
