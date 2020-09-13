---
layout: post
title:  "C# Countdown Timer"
date:   2012-06-15 20:02:05 +0300
tags: c-sharp
redirect_from: /miscellaneous/c-countdown-timer
image: /imgs/thumbnails/timer1.webp
---

A **timer** in C # is an object that executes an action after a specified time interval - for example, it can call a method every 5 seconds.  
The best way to understand how it works is to use it in a program.

{% include image.html url="/imgs/posts/c-countdown-timer/1.png" description="Basic .NET Timer Properties" %}

## Creating a timer

Go **File** -> **New** -> **Project** and select **Windows Forms Application**. From **ToolBox** choose **Timer** and add it in the program (with drag & drop).

Now, add a **label** - its value will be modified by the **timer**.

Click on the **timer1** and look on the properties window for an option:  
  **Interval** - here we set the time interval, in milliseconds. For a countdown timer, set 1000ms (= 1 second).

## Making the timer do something

Double-click on the **timer**, which we inserted near the form - in the code window, you'll have a new method: **timer1_Tick** . This function will be called **every second**. Here, we'll add the code to subtract 1 from our label value - so it'll look like the label value lowers every second.

I tried to write this code as short as possible, so it might look complicated but all it does is to convert the last value of the label into an int, subtracts 1 from that value, converts it back to string and adds it back to the label.

```csharp
private void timer1_Tick (object sender, EventArgs e)
{
      label1.Text = (int.Parse(label1.Text) - 1).ToString();     
}
```

If you don't understand the version above, here something easier (both versions do the same thing):

```csharp
private void timer1_Tick (object sender, EventArgs e)
{
      int timeLeft = int.Parse(label1.Text);  //getting the last value (the one from the label)
      timeLeft -= 1; //subtracting 1
      label1.Text = timeLeft.ToString();  //adding it back to the label.      
}
```

## Starting/stopping it

That's all, it remains to start our timer using **timer1.Start()** and provide an initial value for the label.

```csharp
public Form1()
{
      InitializeComponent();
      label1.Text = "90"; //start from 90 seconds
      timer1.Start();  
}
```

To stop it, use: **timer1.Stop()**

## Complete code

In the end, you should have something like this:

```csharp
using System;
using System.Windows.Forms;

namespace timer_tutorial
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            label1.Text = "90";
            timer1.Start();
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            label1.Text = (int.Parse(label1.Text) - 1).ToString(); //lowering the value - explained above
            if (int.Parse(label1.Text) == 0)  //if the countdown reaches '0', we stop it
                timer1.Stop();
        }
    }
}
```