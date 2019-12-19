---
layout: post
title:  "C# Fix SimpleWorkerRequest Path Issue"
date:   2012-09-21 20:02:05 +0300
categories: tips-and-tricks
image: /imgs/thumbnails/aspnet404.webp
---

## The problem

If you ever tried to create an http server that can run **ASP.NET** code, you may know that you can only open pages from the root directory. If you try to open a page, that is in a folder (root/randomFolder/mypage.aspx) - it won't work. It will just give you a **404 Not Found**, even if your page is in the right place.

## Fixing it

It can be easily fixed by modifying the path to your file from **SimpleWorkerRequest**.  
The problem is that the **GetFilePath()** function returns only the path to the page's directory, but it doesn't include the page. We must do this manually, by overriding the function and setting the correct path.

If you don't know how to do this, I wrote the code below - just add it to your source:

```csharp
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
```

Now, instead of using **SimpleWorkerRequest**, you must use **WorkerRequest** (the fixed version) to parse your pages.

You can find the patched server [here](http://www.codingvision.net/networking/c-http-server-with-aspnet/).