---
layout: post
title:  "C# Working with Xml Documents"
date:   2012-05-01 20:02:05 +0300
categories: files
thumbnail: /imgs/thumbnails/xmlFiles.jpg
---

**XML** is the main file type used to save our program's data. In this tutorial, I'll show you how to work with XML files in C#.

I'll be working with the following file:

{% highlight xml linenos %}
<products>

         <product>
                <name>Book</name>
                <price>15$</price>
         </product>

         <product>
                <name>Crayon</name>
                <price>5$</price>
         </product>

</products>
{% endhighlight %}

## Basics

**&lt;products&gt;** is the main node.  
**&lt;product&gt;** is a smaller node, found in the main node, each one contains information about a product (its parent is 'product')  
**&lt;name&gt;** and **&lt;price&gt;** are nodes which correspond to **product** node (parent node: 'product').

Ok, now for the coding part, include in the project: **using System.Xml**;  
After this, we create an **XmlDocument** object - used for opening the xml file:

{% highlight csharp linenos %}
XmlDocument xmldoc = new XmlDocument();
xmldoc.Load("file.xml");  //open the file
{% endhighlight %}

## Reading from a node

Before reading the values form our file, we must select the nodes.

If we need to select **only one node** corresponding to a certain product, the following code must be used:

{% highlight csharp linenos %}
XmlNode book_node = xmldoc.SelectSingleNode("/products/product[name='Book']"); //selects the node where name is 'Book'
{% endhighlight %}

If we need to know the price of the product selected before:

{% highlight csharp linenos %}
string book_price = book_node["price"].InnerText;
{% endhighlight %}

However, it is also possible to select multiple nodes from the file - not just one:

{% highlight csharp linenos %}
XmlNodeList nodelist = xmldoc.SelectNodes("/products/product");
{% endhighlight %}

The code above returns an array containing all the nodes found in **products**.

Now, we get the values of every node in the list:

{% highlight csharp linenos %}
foreach (XmlNode node in nodelist)
{
         string name = node["name"].InnerText;
         string price = node["price"].InnerText;
}
{% endhighlight %}

## Adding a new node

Let's say we want to add to our file another product, with a custom name & price.  
We start by creating the **product**'s node and attach it to the main node (products):

{% highlight csharp linenos %}
XmlNode product_node = xmldoc.CreateElement("product");
xmldoc.DocumentElement.AppendChild(product_node);
{% endhighlight %}

Having the node, we have to add the other 2 elements (name & price)

{% highlight csharp linenos %}
XmlNode product_name = xmldoc.CreateElement("name");     
product_node.InnerText = "Pencil"; //set the product's name
product_node.AppendChild(product_name);  //and attach it to the product node

XmlNode product_price = xmldoc.CreateElement("price");     
product_price.InnerText = "9$"; 
nod_produs.AppendChild(product_name);
{% endhighlight %}

## Deleting a node

A node is 'deleted' when it's removed from it's parent node, so if we want to delete the last node from the list - the one that we created before, we use this:

{% highlight csharp linenos %}
XmlNode node = xmldoc.SelectSingleNode("/products/product[name='Pencil']");  //select node where name is 'Pencil'
node.ParentNode.RemoveChild(node);
{% endhighlight %}

## Saving the file

Don't forget to save any changes you made in the xml document:

{% highlight csharp linenos %}
xmldoc.Save("file.xml");
{% endhighlight %}

The end :)