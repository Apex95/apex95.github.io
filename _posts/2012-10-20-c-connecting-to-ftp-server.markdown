---
layout: post
title:  "C# Connecting to FTP Server"
date:   2012-10-20 20:02:05 +0300
categories: networking
thumbnail: /imgs/thumbnails/ftpAddress.jpg
---

In this tutorial I will show you how to use **C#** to **connect to a FTP server** and perform basic operations:

- _uploading a file_  
- _downloading a file_  
- _deleting a file_

## 1.Connecting & Logging In

Before doing operations on files, you must learn how to connect to the FTP server. For every action, you have to use a **FtpWebRequest** - and with it, you tell the server what to do. When the **FtpWebRequest** is created, you have to provide the path to the file:

{% highlight csharp linenos %}FtpWebRequest ftpRequest = (FtpWebRequest)WebRequest.Create("ftp://myFtpAddress.tld/myFile.txt");
// 'ftp://myFtpAddress.tld/myFile.txt' is the path to the file
{% endhighlight %}

Now, we have to provide the authentication data (username & password). This data must be included into the FTP request:

{% highlight csharp linenos %}ftpRequest.Credentials = new NetworkCredential("username", "password");
{% endhighlight %}

This is how your code should look like:

{% highlight csharp linenos %}FtpWebRequest ftpRequest = (FtpWebRequest)WebRequest.Create("ftp://myFtpAddress.tld/myFile.txt");

ftpRequest.Credentials = new NetworkCredential("username", "password");
{% endhighlight %}

After this, you can start doing operations with files.

## 2.Uploading a file

You have to tell the **FTP Server** what you want to do - in this case, you want to **upload a file**. So, you'll set the **WebRequestMethod** to **UploadFile**:

{% highlight csharp linenos %}ftpRequest.Method = WebRequestMethods.Ftp.UploadFile;{% endhighlight %}

The line above tells the server that you want to upload a file - so it'll wait for **file's content**. The file's content must be sent as a byte array (**byte[]**):

{% highlight csharp linenos %}byte[] fileContent;  //in this array you'll store the file's content

using (StreamReader sr = new StreamReader("myFile.txt"))  //'myFile.txt' is the file we want to upload
{
       fileContent = Encoding.UTF8.GetBytes(sr.ReadToEnd()); //getting the file's content, already transformed into a byte array
}

using (Stream sw = ftpRequest.GetRequestStream())
{
       sw.Write(fileContent, 0, fileContent.Length);  //sending the content to the FTP Server
}
{% endhighlight %}

The complete code for file upload will look like this:

{% highlight csharp linenos %}using System;
using System.Net;
using System.IO;
using System.Text;

namespace testProj
{
    class Program
    {
        static void Main(string[] args)
        {
            FtpWebRequest ftpRequest = (FtpWebRequest)WebRequest.Create("ftp://myFtpAddress.tld/myFile.txt");

            ftpRequest.Credentials = new NetworkCredential("username", "password");
            ftpRequest.Method = WebRequestMethods.Ftp.UploadFile;

            byte[] fileContent;

            using (StreamReader sr = new StreamReader("myFile.txt"))
            {
                fileContent = Encoding.UTF8.GetBytes(sr.ReadToEnd()); 
            }

            using (Stream sw = ftpRequest.GetRequestStream())
            {
                sw.Write(fileContent, 0, fileContent.Length);
            }

            ftpRequest.GetResponse();
        }
    }
}
{% endhighlight %}

## 3.Downloading a file

This is easier, this time the server will send to our program the file's content. But first, we must tell the server that we want to download a file:

{% highlight csharp linenos %}ftpRequest.Method = WebRequestMethods.Ftp.DownloadFile;
{% endhighlight %}

Then, we'll get the **server's response** - that's the file we want. To do this, you can use a **StreamReader** to read from the main Stream.

{% highlight csharp linenos %}using (Stream sw = ftpRequest.GetResponse().GetResponseStream())  //getting the response stream
{
      StreamReader sr = new StreamReader(sw);   //reading from the stream
      Console.WriteLine(sr.ReadToEnd());   //showing the file's content
}
{% endhighlight %}

And the complete code:

{% highlight csharp linenos %}using System;
using System.Net;
using System.IO;
using System.Text;

namespace testProj
{
    class Program
    {
        static void Main(string[] args)
        {
            FtpWebRequest ftpRequest = (FtpWebRequest)WebRequest.Create("ftp://myFtpAddress.tld/myFile.txt");

            ftpRequest.Credentials = new NetworkCredential("username", "password");
            ftpRequest.Method = WebRequestMethods.Ftp.DownloadFile;

            using (Stream sw = ftpRequest.GetResponse().GetResponseStream())
            {
                StreamReader sr = new StreamReader(sw);
                Console.WriteLine(sr.ReadToEnd());
            }
        }
    }
}
{% endhighlight %}

## 4.Deleting a file

Once again, tell the server what you want to do (delete a file), using **WebRequestMethods**:

{% highlight csharp linenos %}ftpRequest.Method = WebRequestMethods.Ftp.DeleteFile;
{% endhighlight %}

And that's all ! - no additional code is required to do this.  
The complete source code:

{% highlight csharp linenos %}using System;
using System.Net;
using System.IO;
using System.Text;

namespace testProj
{
    class Program
    {
        static void Main(string[] args)
        {
            FtpWebRequest ftpRequest = (FtpWebRequest)WebRequest.Create("ftp://myFtpAddress.tld/myFile.txt");

            ftpRequest.Credentials = new NetworkCredential("username", "password");
            ftpRequest.Method = WebRequestMethods.Ftp.DeleteFile;

            ftpRequest.GetResponse();  
        }
    }
}
{% endhighlight %}