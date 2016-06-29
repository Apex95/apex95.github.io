---
layout: post
title:  "C# Connect to MySql"
date:   2012-05-02 20:02:05 +0300
categories: miscellaneous
thumbnail: /imgs/thumbnails/connectMysql.jpg
---

**MsSql** or **MySql** ? What to use ?  
I prefer **MySql** because I work with it more often. Unfortunately **.NET** doesn't support by default this kind of database...

There's a solution!

It's a small library called **Connector/NET**, available [on MySql's official website](http://dev.mysql.com/downloads/connector/net/1.0.html#downloads). You just have to install it.

After installation, create a new project (console or form) and make sure you have a MySql server running (if you don't have one, just download and install Xampp).

Then go into **Solution Explorer**, right click on **References**->**Add reference**->**.NET**: from here, select **MySql.Data** then click Ok.

Before starting to code, add into your project:

{% highlight csharp linenos %}
using MySql.Data.MySqlClient;
{% endhighlight %}

In this tutorial I work with a table called **members**:

<table style="border-collapse:collapse;color: #444;" border="1" cellpadding="3" cellspacing="10">

<tbody>

<tr>

<td>**Name**</td>

<td>**Email**</td>

</tr>

<tr>

<td>User-1</td>

<td>user-1@mail.com</td>

</tr>

<tr>

<td>User-2</td>

<td>user-2@mail.com</td>

</tr>

</tbody>

</table>

&nbsp;

The connection to the database is made using a string which contains all the information required: host, database name, username and password.  
This string has the following structure:

{% highlight csharp linenos %}
string str_con = "Server=server_address;Database=database_name;Uid=username;Pwd=password";
{% endhighlight %}

Using this we get:

{% highlight csharp linenos %}
string str_con = "Server=localhost;Database=tutorial;Uid=root;Pwd=";  //my server has no password 

MySqlConnection connection = new MySqlConnection(str_con);  //we create a MySql connection

try  
{
      connection.Open();  //we try to open the connection
}
catch(Exception ex)
{
      Console.Writeline(ex.Message);  // if we got here => db is offline
}
{% endhighlight %}

Until now...we managed to establish a connection to the **MySql** server...  
To execute commands, like **INSERT, SELECT, DELETE.** use the following code:

{% highlight csharp linenos %}
MySqlCommand command = connection.CreateCommand(); //we create a command
command.CommandText = "SELECT * FROM memers"; // in CommandText, we write the Query
{% endhighlight %}

_One thing to note: the code must be adjusted depending on the command's type._

What does that mean? We use a different code snippet if we expect a result from our query: if we use **SELECT**, we expect the MySql server to return some data, but if we use **DELETE** we won't expect any result from the database - I think you got the point.

## SELECT Example

{% highlight csharp linenos %}
MySqlDataReader reader = command.ExecuteReader();  //execute the SELECT command, which returns the data into the reader

while (reader.Read())  //while there is data to read
{
        Console.WriteLine(reader["name"] + " " + reader["email"]);  //finally, displaying what we got from our server
}
{% endhighlight %}

We need the **reader** only for the commands that return something.

## INSERT Example

For a simple...**INSERT**, the following lines would be enough:

{% highlight csharp linenos %}
command.CommandText = "INSERT INTO members VALUES ('User-3', 'user-3@mail.com')";  //we add a new member in our table

command.ExecuteNonQuery();
{% endhighlight %}

This code goes for every MySql query that does not return a value, so, you can just modify the query and use everything you need.

Once the queries are executed, the connection must be closed using the following line:

{% highlight csharp linenos %}
connection.Close();
{% endhighlight %}