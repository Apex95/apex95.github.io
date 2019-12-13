---
layout: post
title:  "C# Sending data using GET or POST"
date:   2012-10-12 20:02:05 +0300
categories: networking
thumbnail: /imgs/thumbnails/getpost.png
---

In this short article, I'll show you how to send data to a website from a C# application using **GET** or **POST** method. The tutorial also includes how to receive data from a website, by getting the page's source - so it's a neat way to check if the everything is working as intended.

## 1\. GET Method

Using the **GET** method is the easiest way to send any text data since all you have to do is to open the Url address with already-defined parameters, with **WebClient**. Notice that WebClient is IDisposable you can use it this way:

{% highlight csharp linenos %}string username = "john";
string urlAddress = "http://www.yoursite.tld/somepage.php?username=" + username;  

using (WebClient client = new WebClient())
{
       // this string contains the webpage's source
       string pagesource = client.DownloadString(urlAddress);  
}
{% endhighlight %}

The code above opens a Url address, with 1 GET parameter: _/somepage.php?username=john_.

Now if you need to check what the program sent, use a PHP snippet like this one and look in the source of the page:

{% highlight php linenos %}<?php
    $username = $_GET["username"];  //make sure you filter these values, before showing them
    echo $username;  //$username == "john"
?>
{% endhighlight %}

## 2\. POST Method

Sending data using **POST**, even if it looks similar to GET, you'll need a different approach. Not very different, we're still using **WebClient**, but we must also include a new class: **NameValueCollection**. This dictionary-like container will store each parameter's name and value. Once all the data has been loaded, call **WebClient.UploadValues** to send the information to the webpage.

First, make sure you include this namespace:

{% highlight csharp linenos %}using System.Collections.Specialized;{% endhighlight %}

Then, you can jump to the code:

{% highlight csharp linenos %}string username = "john";
string referer = "myprogram";
string urlAddress = "http://www.yoursite.tld/somepage.php";

using (WebClient client = new WebClient())
{
       NameValueCollection postData = new NameValueCollection() 
       { 
              { "username", username },  //order: {"parameter name", "parameter value"}
              { "referer", referer }
       };

       // client.UploadValues returns page's source as byte array (byte[])
       // so it must be transformed into a string
       string pagesource = Encoding.UTF8.GetString(client.UploadValues(urlAddress, postData));
}
{% endhighlight %}

Once again, a short PHP snippet that can be used with the example above (the result is shown in the source code, downloaded by WebClient.UploadValues):

{% highlight php linenos %}<?php
    $username = $_POST["username"];  
    $referer = $_POST["referer"];
    echo $username." from ".$referer;  // $username == "john" and $referer == "myprogram"
?>
{% endhighlight %}