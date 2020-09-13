---
layout: post
title:  "C# Simple Http Server"
date:   2012-09-09 20:02:05 +0300
tags: c-sharp http
redirect_from: /networking/c-simple-http-server
image: /imgs/thumbnails/httpserver.webp
---

In this short tutorial I'll explain how to make a simple **Http Server** using only C#. The server will be able to serve any page that contains **client-side** code (html and javascript).

## Basic stuff

When a client requests a page of a website (let's say index.html), the **Http Server** will start looking for that file. If the file is found, the server will read all the content and send it back to the client as a **byte array**. After this, the connection is closed.

## The coding part

Before starting, you need to change your project's profile to **.NET Framework 4** (not .NET Framework 4 client profile). This can be done by going to _Project->Project properties->Application_.

Now, go to _Solution Explorer->References->Add Reference->.NET_ and import **System.Web** .  
Also make sure you have the following lines included in your project's header:

```csharp
using System;
using System.Net;
using System.IO;
using System.Text;
```

Creating the server is quite simple - we'll use .NET's **HttpListener**:

```csharp
HttpListener server = new HttpListener();  // this is the http server
server.Prefixes.Add("http://127.0.0.1/");  //we set a listening address here (localhost)
server.Prefixes.Add("http://localhost/");

server.Start();   // and start the server
```

The server is made, now we need to identify incoming connections and serve the requested files. For each connection, we send only one file and because we might have multiple connections, we'll need an endless loop to handle them one by one.

```csharp
while (true)
{
          HttpListenerContext context = server.GetContext();  
          //context: provides access to httplistener's response

          HttpListenerResponse response = context.Response; 
         //the response tells the server where to send the datas

          string page = Directory.GetCurrentDirectory() + context.Request.Url.LocalPath;
          //this will get the page requested by the browser 

          if (page == string.Empty)  //if there's no page, we'll say it's index.html
              page = "index.html"; 

          TextReader tr = new StreamReader(page);  
          string msg = tr.ReadToEnd();  //getting the page's content

          byte[] buffer = Encoding.UTF8.GetBytes(msg);   
          //then we transform it into a byte array

          response.ContentLength64 = buffer.Length;  // set up the messasge's length
          Stream st = response.OutputStream;  // here we create a stream to send the message
          st.Write(buffer, 0, buffer.Length); // and this will send all the content to the browser

          context.Response.Close();  // here we close the connection
}
```

Well, this is all, now all you need to do is to create some html pages and place them into your executable's directory.  
Then run the application and access  
**http://127.0.0.1/anyfile.html**.

You should be able to see your file in the browser's window.

## The complete code

```csharp
using System;
using System.Net;
using System.IO;
using System.Text;

namespace test
{

    class Program
    {
        static void Main(string[] args)
        {
            HttpListener server = new HttpListener();
            server.Prefixes.Add("http://127.0.0.1/");
            server.Prefixes.Add("http://localhost/");

            server.Start();

            Console.WriteLine("Listening...");

            while (true)
            {
                HttpListenerContext context = server.GetContext();
                HttpListenerResponse response = context.Response;

                string page = Directory.GetCurrentDirectory() + context.Request.Url.LocalPath;

                if (page == string.Empty)
                    page = "index.html";

                TextReader tr = new StreamReader(page);
                string msg = tr.ReadToEnd();

                byte[] buffer = Encoding.UTF8.GetBytes(msg);

                response.ContentLength64 = buffer.Length;
                Stream st = response.OutputStream;
                st.Write(buffer, 0, buffer.Length);

                context.Response.Close();
            }

        }
    }

}
```

Remember that this server isn't able to parse server-side languages like PHP or ASP.NET, it just sends the file's content to the browser. If you're interested in embedding ASP.NET into a http server [see this tutorial](http://www.codingvision.net/networking/c-http-server-with-aspnet).