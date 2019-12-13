---
layout: post
title:  "C# Form Fade In/Fade Out"
date:   2013-02-18 20:02:05 +0300
categories: interface
thumbnail: /imgs/thumbnails/fadeinout.png
---

This short tutorial is made to show you how to create a **fade in** / **fade out** effect for a form. Since basic Windows Forms doesn't provide such an option, it must be done manually.

_Note: we'll use timers instead of general repetitive structures to avoid thread blocking_

## Fade in Effect

To do this, all we have to do is to set the Form's **Opacity** to **0**. Then, using a **Timer** we'll slowly increase opacity. All this code should go in a event handler that is executed when the form loads.

As an example:

{% highlight csharp linenos %}Timer t1 = new Timer();

private void Form1_Load(object sender, EventArgs e)
{
            Opacity = 0;      //first the opacity is 0

            t1.Interval = 10;  //we'll increase the opacity every 10ms
            t1.Tick += new EventHandler(fadeIn);  //this calls the function that changes opacity 
            t1.Start(); 
}

void fadeIn(object sender, EventArgs e)
{
            if (Opacity >= 1)  
                t1.Stop();   //this stops the timer if the form is completely displayed
            else
                Opacity += 0.05;
}{% endhighlight %}

## Fade Out Effect

This works the same way as the fade in effect: we'll use a **Timer** that lowers the Opacity, that is started when the form is closing. The code should be added in the form-closing event handler.

{% highlight csharp linenos %}private void main_FormClosing(object sender, FormClosingEventArgs e)
{
      e.Cancel = true;    //cancel the event so the form won't be closed

      t1.Tick += new EventHandler(fadeOut);  //this calls the fade out function
      t1.Start();

      if (Opacity == 0)  //if the form is completly transparent
          e.Cancel = false;   //resume the event - the program can be closed

}

void fadeOut(object sender, EventArgs e)
{
      if (Opacity <= 0)     //check if opacity is 0
      {
          t1.Stop();    //if it is, we stop the timer
          Close();   //and we try to close the form
      }
      else
          Opacity -= 0.05;
}{% endhighlight %}

Believe it or not, that's all, however pay attention to the events so you won't assign 2 event handlers to the same event.