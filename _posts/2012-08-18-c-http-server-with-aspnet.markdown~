---
layout: post
title:  "C# Http Server With ASP.NET"
date:   2012-08-18 20:02:05 +0300
categories: networking
thumbnail: /imgs/thumbnails/aspnet.png
redirect_from: "/networking/c-http-server-with-asp-net/"
---

This tutorial will show you how to create a **HTTP server** that can parse **ASP.NET files**. It will be able to serve pages containing **html**,**css** and **server-side code**. As always I'll try to keep the code simple - luckily .NET does all the work for us.

## 1\. Preparing the project

Start by creating a **Console Project**. Once the project is created, go to _Project->Project properties->Application_ and make sure that **Target Framework** isn't set to a client profile framework:

Example: if it is **.NET Framework 4 Client Profile** change it to **.NET Framework 4**.

Now go to the Solution Explorer, right click on _References->Add Reference->.NET->**System.Web**_

Also, include the following namespaces:

```csharpusing System.Net;
using System.IO;
using System.Web.Hosting;
using System.Web;```

## 2\. Creating a simple server

Define a **HttpListener** object (that's the server actually) and set it's listening address to **localhost**.

```csharpHttpListener server = new HttpListener();
server.Prefixes.Add("http://localhost/");
server.Start();  //also start the server```

Using an endless loop, this server will check for any incoming connections, if any connection is made, it will serve the page to the client, using a **StreamWriter**.

```csharphost asphost = (host)ApplicationHost.CreateApplicationHost(typeof(host), "/", Directory.GetCurrentDirectory());
//the code above will be explained later

while (true)
{
      HttpListenerContext context = server.GetContext(); //the context
      HttpListenerResponse response = context.Response; //this will specify where to send the data

      StreamWriter sw = new StreamWriter(response.OutputStream); //data is sent using a streamwriter

      string page = context.Request.Url.LocalPath.Replace("/", ""); 
      //this gets the file requested by the client

      string query = context.Request.Url.Query.Replace("?", "");
      //and this will store any GET parameters -- not very important

      asphost.parse_code(page, query, ref sw); //parses the page and sends it

      sw.Flush();
      context.Response.Close(); //closes the connection, once the page was sent
}```

## 3\. Embedding the ASP.NET Runtime

The lines above, which I said I'll explain later are used for parsing the ASP.NET file: we can't just send the file to the client, because it might contain server-side code, that can't be interpreted by the browser.

Parsing the file is done using the following snippet:

```csharpclass host : MarshalByRefObject 
{
     public void parse_code(string page, string query, ref StreamWriter sw)
     {
         SimpleWorkerRequest swr = new SimpleWorkerRequest(page, query, sw);
         HttpRuntime.ProcessRequest(swr);
     }
}```

This class called **host**, embeds the **ASP.NET Runtime** service. However this requires a custom AppDomain - otherwise it won't work - so that's the role of the line below:

```csharphost asphost = (host)ApplicationHost.CreateApplicationHost(typeof(host), "/", Directory.GetCurrentDirectory());```

3 arguments are required here, first is the type, the second is the virtual path and the third the physical path.

Ok, this is what you need to know before creating your ASP.NET server.

## 4\. The complete code + bug fix

What you might not know is that there is a **bug** in .NET's **SimpleWorkerRequest** - because of this bug, you can't access pages that are in directories. If you have your asp file in a directory, you'll get an 404 error - more information about this can be found [here](http://www.codingvision.net/tips-and-tricks/c-fix-simpleworkerrequest-path-issue/ "C# Fix SimpleWorkerRequest Path Issue")

This is the complete code of the server, that also **fixes the problem**:

```csharpusing System;
using System.Net;
using System.IO;
using System.Web;
using System.Web.Hosting;

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

            host asphost = (host)ApplicationHost.CreateApplicationHost(typeof(host), "/", Directory.GetCurrentDirectory());

            while (true)
            {
                HttpListenerContext context = server.GetContext();
                HttpListenerResponse response = context.Response;
                StreamWriter sw = new StreamWriter(response.OutputStream);

                string page = context.Request.Url.LocalPath;
                string query = context.Request.Url.Query.Replace("?", "");
                asphost.parse_code(page, query, ref sw);
                sw.Flush();
                context.Response.Close();
            }
        }
    }

    class WorkerRequest : SimpleWorkerRequest   //the fix, use this instead of SimpleWorkerRequest
    {
        string page = string.Empty;
        public WorkerRequest(string page, string query, TextWriter output) : base(page, query, output)
        {
            this.page = page;   
        }

        public override string GetFilePath()
        {
            return base.GetFilePath() + page;
        }
    }

    class host : MarshalByRefObject
    {
        public void parse_code(string page, string query, ref StreamWriter sw)
        {
            WorkerRequest swr = new WorkerRequest(page, query, sw);  //replacing SimpleWorkerRequest
            HttpRuntime.ProcessRequest(swr);
        }
    }

}

```

## 5\. Fixing the NotFoundException (error)

Yes, even if the code is correct, this error might appear:  
_"Could not load file or assembly 'projectnamehere, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null' or one of its dependencies. The system cannot find the file specified."_

This is caused by **ASP.NET Runtime** - but it can be easily solved by creating a directory named **bin** and copying the executable there.

If you have your executable in the Debug folder:  
_"project_name/bin/Debug/asp_server.exe"_ <- original path

You have to create the **Bin** folder here (you'll also have to copy the application in the new directory):  
_"project_name/bin/Debug/**bin**/asp_server.exe"_ <- new path

Now you can safely run your ASP.NET server, from the default location (not from the bin folder).

Note: if you change anything in the server's source and recompile it, you have to do the copy-paste thing again.

**_Later Edit:_** there seems to be a problem with the extensions - the server is only serving .aspx files (apparently files with other extensions can not be "seen"). Don't know sure what can cause this...
