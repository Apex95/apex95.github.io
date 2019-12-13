---
layout: post
title:  "C# Send email using Gmail"
date:   2012-06-19 20:02:05 +0300
categories: networking
thumbnail: /imgs/thumbnails/smtpConnect.png
---

In this tutorial ... we'll send emails :) using C# of course.

## 1\. Required:

- SMTP server | I use: **smtp.google.com** , you must have a Gmail account  
- Little attention / some basic knowledge of C#

## 2\. Creating the client

We start by including **System.Net** and **System.Net.Mail** in our program.

```csharp
using System.Net.Mail;
using System.Net;
```

Then, set the two addresses:

```csharp
MailAddress myemail = new MailAddress("me@gmail.com", "Name");  //used for authentication
MailAddress mail_to = new MailAddress("receiver@yahoo.com", "Receiver");  //the email address of the receiver

string password = "email password here";  //used for authentication
```

We will create a **SMTP client** that connects to the **Gmail** server:

```csharp
SmtpClient client_smtp = new SmtpClient("smtp.gmail.com", 587);   //address and port

client_smtp.EnableSsl = true;   //Gmail requires a ssl connection
client_smtp.DeliveryMethod = SmtpDeliveryMethod.Network;
client_smtp.UseDefaultCredentials = false;
client_smtp.Credentials = new NetworkCredential(myemail.Address, password); //authentication data
```

That's the SMTP client, now we have to write the message:

```csharp
MailMessage message = new MailMessage (myemail, mail_to);
message.Subject = "Test";  //subject
message.Body = "just a test email";  //content

client_smtp.Send(message);
```

Finally you get this:

```csharp
using System;
using System.Collections.Generic;  
using System.Linq;  
using System.Text;  
using System.Net.Mail;  
using System.Net;

namespace smtp_client  

{
    class Program  
    {
        static void Main (string[] args)  
        {

            MailAddress myemail = new MailAddress("me@gmail.com", "Name");
            MailAddress mail_to = new MailAddress("receiver@yahoo.com", "Receiver");  

            string password = "email_password";

            SmtpClient client_smtp = new SmtpClient("smtp.gmail.com", 587);  
            client_smtp.EnableSsl = true;  
            client_smtp.DeliveryMethod = SmtpDeliveryMethod.Network;  
            client_smtp.UseDefaultCredentials = false;  
            client_smtp.Credentials = new NetworkCredential (myemail.Address, password);

            MailMessage message = new MailMessage (myemail, mail_to);  
            message.Subject = "Hello from sharpcode";  
            message.Body = "just a test";
            
            client_smtp.Send(message);

        }
    }  
}
```

If the message isn't showing up in about 5 minutes, it might be an error with your application, if so check the code again.