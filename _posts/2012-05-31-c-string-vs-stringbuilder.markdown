---
layout: post
title:  "C# String vs StringBuilder"
date:   2012-05-31 20:02:05 +0300
categories: tips-and-tricks
thumbnail: /imgs/thumbnails/stringVstringBuilder.png
---

**StringBuilder** or **String**? Is there any difference?

It is - and not only the name, when we talk about our program's performance. I'll start by explaining how each one works so you'll understand why this and not that.

## String

{% highlight csharp linenos %}string a = "something";{% endhighlight %}

When we declare a string, there's allocated enough memory to store it's value, but that's all.  
The problem appears when we try to execute operations on that string.

Take a look at this code:

{% highlight csharp linenos %}string a = "some";
a += "string";{% endhighlight %}

The first time our string is declared, it's allocated memory to store its actual value. But when we modify/extend it, by concatenating the strings guess what happens? The memory used by our initial string is released and the program reallocates memory for the new string. So, if we **add to the string 10 characters**, one by one, the **memory gets reallocated 9 times** which makes our program lose performance.

## StringBuilder

{% highlight csharp linenos %}StringBuilder a = new StringBuilder("some", 1000);
a.Append("stringbuilder");{% endhighlight %}

The advantage offered by **StringBuilder** is that it stores the values in an internal buffer which can be **directly extended** without releasing and reallocationg memory. This buffer has its size specified in stringbuilder's declaration (in the example above, it's **1000**), if that limit is exceeded, the stringbuilder will create another internal buffer and will merge it with the first one. However is not a good idea to continously allocate memory for these buffers, so try to be precise when you specify the StringBuilder's size.

## So what to use?

**StringBuilder** - should be used when you want to execute many operations continuously to avoid creating a new string each time.

**String** - it should be used when you don't want to do heavy operations (like modifying its value very often/inside a loop).