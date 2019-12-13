---
layout: post
title:  "C# How To: Get External IP Address"
date:   2014-09-27 20:02:05 +0300
categories: networking
thumbnail: /imgs/thumbnails/getIpAddress.png
---

Okay, this is a really short article, but I felt the need to write this because too many people seem to take the wrong way.

## Problem

First: getting the **public IP** address of a machine shouldn't be done locally (**Dns.GetHostAddresses(Dns.GetHostName())** <- this is evil).

_Why?_

This method is good only if you need the local IP address. If you need the public one consider that not every machine is **directly** connected to the internet. Some might be sitting behind a **firewall** or a **router**, but the framework won't know it and will return an address which is valid only inside your network. In order to get the public IP address, which allows computers from the internet to communicate with you, you need to query some entity from outside your network.

## Solution

One reliable way to solve this is to ask a **website** what's your external IP address - there are many websites that can be used for this and some of them will even return your IP address as a plain text - which is nice.

Here's a short example of how you should do it (don't forget to include **System.Net**):

* this snippet should only give you the idea of how to do this, don't use it as it is.

```csharp
string getExternalIP()
{
    using (WebClient client = new WebClient())
    {
         return client.DownloadString("http://canihazip.com/s");
    }
}
```

_What if the website is **down**?_

Well, this is a risk that can be avoided by using...more websites :) and a bunch of **try-catch** blocks. If a website can't be reached, we query the next one. Simple as that.

A more reliable example here:

```csharp
string getExternalIP()
{
    using (WebClient client = new WebClient())
    {
        try
        {
            return client.DownloadString("http://canihazip.com/s");
        }
        catch (WebException e)
        {
            // this one is offline
        }

        try
        {
            return client.DownloadString("http://wtfismyip.com/text");
        }
        catch (WebException e) 
        {  
            // offline...
        }

        try
        {
            return client.DownloadString("http://ip.telize.com/");
        }
        catch (WebException e)
        {
            // offline too...
        }

        // if we got here, all the websites are down, which is unlikely
        return "Check internet connection?";
    }
}
```

It can still be improved by doing all the connections at the same time (putting each one in a different thread) - this will reduce the waiting time (if the first websites are down).

However these modifications would exceed the purpose of the article.