---
layout: post
title:  "C# Simple Form with Rounded Corners"
date:   2012-08-13 20:02:05 +0300
categories: interface
thumbnail: /imgs/thumbnails/formround.png
---

This tutorial aims to show how to make a **C# Form** with **rounded corners**, using a very simple method. It's not actually our policy as we won't use code here...

**1.** Select a background image for the Form(window) - it must have the Form's size (if the Form is 300x200, the image must be 300x200 too).

In the tutorial, I'll use something like this:

{% include image.html url="/imgs/posts/c-simple-form-with-rounded-corners/1.png" description="The initial background image" %}

**2.** Use a 'specific' color to cover the corners of the image - so it appears with rounded corners - it can be easily done by drawing a rectangle over the original image. This color will be set as transparent, so it will not show up with the window. For this it's usually used the **Magenta** (R: 255, G: 0, B: 255) color. I recommend using it for the first time.

You'll get something like this:

{% include image.html url="/imgs/posts/c-simple-form-with-rounded-corners/2.png" description="Rounding the corners by adding a border" %}

**3.** Open **Visual Studio** or any **IDE** and create a **Form Project**.  
On the right side, in the **Properties Window** look for **BackgroundImage**. option. Click **Import** and choose the image you made before.  
Also in the properties, set the **TransparencyKey** to **Magenta** - so it won't show the pink border around the Form.

**4\.** Finally, set **FormBorderStyle** to none in order to hide the original borders/title bar and you're done.

Now when you'll open the window it will show the background image with nice, rounded corners:

{% include image.html url="/imgs/posts/c-simple-form-with-rounded-corners/3.png" description="A Form with Rounded Corners" %}

You've probably noticed that the form isn't moving - that's because it has no title bar and border. No need to worry about that, you can find [here](http://www.codingvision.net/interface/c-moving-form-without-title-bar/) a solution.