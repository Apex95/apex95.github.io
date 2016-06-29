---
layout: post
title:  "C# Edit Registry Keys or Values"
date:   2012-11-11 20:02:05 +0300
categories: miscellaneous
thumbnail: /imgs/thumbnails/registry.png
---

## First

Before starting to edit registry values/keys, include in your project's source this namespace **Microsoft.Win32**. It will give you access to the required **Registry** functions.

So, make sure you add this:

{% highlight csharp linenos %}using Microsoft.Win32;{% endhighlight %}

In order to edit anything, you must:

1.  open the key where you want to edit (set a path)
2.  add/delete/edit what you want
3.  close the key

**Note**: in this tutorial I used Windows' startup Key (path), but you can use anything you want.

So your snippet will look like this:

{% highlight csharp linenos %}//this is how your key will look like
//the 2nd argument (true) is indicating that the key is writable
RegistryKey key = Registry.CurrentUser.OpenSubKey(@"Software\Microsoft\Windows\CurrentVersion\Run", true);

//here you put the code to edit/delete values or subkeys
//which are found in: 'Software\Microsoft\Windows\CurrentVersion\Run'

//and finally, you close the key
key.Close();{% endhighlight %}

## Creating a Key

A key is a **subfolder**, in which you can add multiple **values**.  
To create a **key**:

{% highlight csharp linenos %}RegistryKey key = Registry.CurrentUser.OpenSubKey(@"Software\Microsoft\Windows\CurrentVersion\Run", true);

//create a new key 
key.CreateSubKey("someKey");

key.Close();

{% endhighlight %}

## Deleting a Key

In order to delete a key, you have to do the same thing: set the path then simply delete it.

{% highlight csharp linenos %}RegistryKey key = Registry.CurrentUser.OpenSubKey(@"Software\Microsoft\Windows\CurrentVersion\Run", true);

//deleting 'someKey'
key.DeleteSubKey("someKey");

key.Close();{% endhighlight %}

## Adding/Editing a value

Before doing this, you have to set the path to the **key** where you want to add that **value**. You can use the code below for adding or editing values.

{% highlight csharp linenos %}RegistryKey key = Registry.CurrentUser.OpenSubKey(@"Software\Microsoft\Windows\CurrentVersion\Run\someKey", true);

//adding/editing a value 
key.SetValue("someValue", "someData"); //sets 'someData' in 'someValue' 

key.Close();{% endhighlight %}

## Reading a value

You can get a value from a key by knowing its name:

{% highlight csharp linenos %}RegistryKey key = Registry.CurrentUser.OpenSubKey(@"Software\Microsoft\Windows\CurrentVersion\Run\someKey", true);

//getting the value
string data = key.GetValue("someValue").ToString();  //returns the text found in 'someValue'

key.Close();{% endhighlight %}

## Deleting a value

And finally, when we got bored of values, we can delete them:

{% highlight csharp linenos %}RegistryKey key = Registry.CurrentUser.OpenSubKey(@"Software\Microsoft\Windows\CurrentVersion\Run", true);

//deleting the value
key.DeleteValue("someValue");

key.Close();{% endhighlight %}