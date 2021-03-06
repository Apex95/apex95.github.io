---
layout: post
title:  "C# EventHandler with Arguments"
date:   2012-06-25 20:02:05 +0300
tags: c-sharp
redirect_from: /tips-and-tricks/c-eventhandler-with-arguments
image: /imgs/thumbnails/eventhandlerArgs.webp
---

All the methods that are called by **events** require two arguments:  
**object** sender  
**EventArgs** e

The event calls a method using those 2 parameters, so we can't _directly_ add a custom argument.

If we have this code and we want to display the string '**s**' in a MessageBox...

```csharp
private void Form1_Load (object sender, EventArgs e)
{
      string s = "Hello!";
      button.Click += new EventHandler(show_msg);  // our string is not included in the call
}

private void show_msg(object sender, EventArgs e, string s) 
// this gives an error, because the function is called with only 2 arguments, but it expects 3
{
      MessageBox.Show(s);
}
```

Clearly this will not work because we are limited to those two parameters.

## The Solution

The easiest solution is to use a **delegate** to call our method.

We get the shortest code using the **lambda operator**, whose symbol is **=>**.  
* It is recommended for beginners because of its simplicity.

```csharp
private void Form1_Load (object sender, EventArgs e)
{
      string s = "Hello!";
      button.Click += (sender2, e2) => show_msg(sender2, e2, s);
}

private void show_msg (object sender, EventArgs e, string s)
{
      MessageBox.Show(s);
}
```

Without using the lambda operator, it can be rewritten using a **delegate**

```csharp
private void Form1_Load (object sender, EventArgs e)
{
       string s = "Hello!";

       button.Click += delegate(object sender2, EventArgs e2)
       {
             show_msg(sender2, e2, s);
       };
}

private void show_msg(object sender, EventArgs e, string s)
{
      MessageBox.Show(s);
} 
```

That's all :).