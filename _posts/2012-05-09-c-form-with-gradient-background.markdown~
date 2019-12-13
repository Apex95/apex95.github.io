---
layout: post
title:  "C# Form with Gradient Background"
date:   2012-05-09 20:02:05 +0300
categories: interface
thumbnail: /imgs/thumbnails/formGradient.png
---

**Gradient** is a method which consists in slowly switching from one color to another - it's used very often in application's design.

In this tutorial I'll show you how to create this effect using only code:

First, create a **Forms Project**, then add the following line:

{% highlight csharp linenos %}using System.Drawing.Drawing2D;{% endhighlight %}

Now, we'll create a **Rectangle** as big as our window and add the gradient effect to it.

{% highlight csharp linenos %}Rectangle gradient_rectangle = new Rectangle(0, 0, Width, Height); {% endhighlight %}

Then using the **LinearGradientBrush** we add the two main colors. Everything else is done by .NET. Really simple, isn't it?  
To assign the gradient effect to the **Rectangle**, use the following code:

{% highlight csharp linenos %}Brush brush = new LinearGradientBrush(gradient_rectangle, Color.Red, Color.Black, 45f);
graphics.FillRectangle(brush, gradient_rectangle);  //graphics comes from a PaintEventArgs argument(event){% endhighlight %}

As you can see, the **LinearGradientBrush** takes 4 arguments:  
- the first is the rectangle we made before  
- the second and the third are the Colors that will create the gradient - we start from Black and we get to Blue  
- the fourth is the gradient's angle (float), I set it to 45 degrees here.

Finally, we can create a simple function to do everything needed:

{% highlight csharp linenos %}private void set_background(Object sender, PaintEventArgs e)
{
            Graphics graphics = e.Graphics;

            //the rectangle, the same size as our Form
            Rectangle gradient_rectangle = new Rectangle(0, 0, Width, Height);  

            //define gradient's properties
            Brush b = new LinearGradientBrush(gradient_rectangle, Color.FromArgb(0, 0, 0), Color.FromArgb(57, 128, 227), 65f);  

            //apply gradient         
            graphics.FillRectangle(b, gradient_rectangle);
}{% endhighlight %}

This method (**set_background**) must be called by a **Paint event** so we'll create a **PaintEventHandler** in our **Form's Constructor**  
* the form's constructor is the area which contains InitializeComponent()

{% highlight csharp linenos %}this.Paint += new PaintEventHandler(set_background);{% endhighlight %}

If you followed all the steps correctly, your form should look like this - maybe with different colors:

{% include image.html url="/imgs/posts/c-form-with-gradient-background/1.png" description="Result: Form with code-generated Gradient Background" %}
