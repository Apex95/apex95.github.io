---
layout: post
title:  "C# WebClient with Cookies"
date:   2012-10-26 20:02:05 +0300
categories: tips-and-tricks
thumbnail: /imgs/thumbnails/webclientcookie.png
---

Well, you're probably reading this because you noticed that .NET's **WebClient** doesn't support **cookies**. Basically, the cookies which are received through the **WebRequest** are NOT stored and also NOT sent - this is how it works by default.

## How to fix this?

Here, I'll show you how to make **WebClient** handle **cookies**. All you have to do is to add a **CookieContainer**, this is where the cookies will be stored. Then you'll just include this CookieContainer in your original request, by overriding **GetWebRequest**.

I'll post the code and I'll explain it using comments:

```csharp
public class ImprovedWebClient : WebClient
{
            CookieContainer cookies = new CookieContainer();
            //^here are automatically stored the cookies

            protected override WebRequest GetWebRequest(Uri address)
            {
                WebRequest request = base.GetWebRequest(address); 

                if (request is HttpWebRequest)  //if it is a Http request
                    ((HttpWebRequest)request).CookieContainer = cookies;  
                    //^we bind that cookie container to the request

                return request; // return the modified request (the one with cookies)
            }
}
```

That's all, now you don't have to use WebClient anymore, so just use derived class - **ImprovedWebClient**:

```csharp
ImprovedWebClient client = new ImprovedWebClient();
```