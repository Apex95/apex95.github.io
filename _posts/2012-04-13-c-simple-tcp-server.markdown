---
layout: post
title:  "C# Simple Tcp Server"
date:   2012-04-13 20:02:05 +0300
tags: c-sharp tcp
redirect_from: /networking/c-simple-tcp-server
image: /imgs/thumbnails/tcpserver.webp
---

If you got here, you probably want to know how to make a simple server in C#, using the shortest possible code and the easiest method to understand.

For the sake of simplicity we'll make a **synchronous server** using a **Console Application** project, so we don't need to use multithreading or anything else.

##### It's recommended to use a Console Application with this code, because this code is considered 'thread-blocker' - if you use it in a Form project, you won't be able to move/close the form while the server is running.

I'll post now the code of the TCP server and I'll explain below how it works:

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using System.Net;      //required
using System.Net.Sockets;    //required

namespace ServerTest
{
    class Program
    {
        static void Main(string[] args)
        {
            TcpListener server = new TcpListener(IPAddress.Any, 9999);  
           // we set our IP address as server's address, and we also set the port: 9999

            server.Start();  // this will start the server

            while (true)   //we wait for a connection
            {
                TcpClient client = server.AcceptTcpClient();  //if a connection exists, the server will accept it

                NetworkStream ns = client.GetStream(); //networkstream is used to send/receive messages

                byte[] hello = new byte[100];   //any message must be serialized (converted to byte array)
                hello = Encoding.Default.GetBytes("hello world");  //conversion string => byte array

                ns.Write(hello, 0, hello.Length);     //sending the message

                while (client.Connected)  //while the client is connected, we look for incoming messages
                {
                    byte[] msg = new byte[1024];     //the messages arrive as byte array
                    ns.Read(msg, 0, msg.Length);   //the same networkstream reads the message sent by the client
                    Console.WriteLine(encoder.GetString(msg).Trim('')); //now , we write the message as string
                }
            }

        }
    }
}
```

&nbsp;


**How it works?**  
* it's a good idea to take a look on the code up there, while you read this

1\. We include the namespaces **System.Net** and **System.Net.Sockets** because we need some types/methods from there.

2\. Now, we create the server: the following line is used to create a **TcpListener** (which is our server), that will check for any incoming connection, on any IP address on the port **9999**.

```csharp
TcpListener server = new TcpListener(IPAddress.Any, 9999);
```

3\. Ok, we have the server but it's not doing anything. So, we'll make him accept connections from a Tcp Client:

```csharp
while (true)
{
       TcpClient client = server.AcceptTcpClient();
       ...
}
```

4\. After the client connects, the server will send using the **NetworkStream.** a 'hello' message. Because we can't directly send/receive strings, we have to transform our messange into a **byte array**.

```csharp
Encoding.Default.GetBytes("hello world");
```

After the message is converted, it can be sent:

```csharp
NetworkStream ns = client.GetStream();
ns.Write(hello, 0, hello.Length);
```

5\. The last part consists in reading the messages received from the client.  
Any incoming message is read using the same **NetworkStream**.

```csharp
NetworkStream ns = client.GetStream();  
ns.Read(msg, 0, msg.Length);
```

Finally we transform it into a string, using the same encoding.

```csharp
Encoding.Default.GetString(msg);
```

&nbsp;
&nbsp;

## This server accepts only one client...Why?

Well... if we take a closer look into the source we can easily see the problem, but I'll explain for a better understanding:

We have the **tcp client** which connects to our **server** and sends data. While **client.Connected** returns **true** the server will be 'blocked' waiting for new messages, and won't check/accept a new Tcp Client. This is usually solved using a different **thread** for every client connected or simply using an **asynchronous server** but those methods are not ideal for this kind of tutorial. 

Take a look at [how to code an asynchronous tcp server](https://codingvision.net/networking/c-asynchronous-tcp-server) if you're interested in a version which accepts **multiple clients**.

If you don't have a client to connect to the server, you can use Telnet, available on any Windows System: go to **Command Prompt** and type: **telnet 127.0.0.1 9999**.
