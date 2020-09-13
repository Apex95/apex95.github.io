---
layout: post
title:  "C# Get Desktop Screenshot"
date:   2013-05-21 20:02:05 +0300
tags: c-sharp screenshot
redirect_from: /miscellaneous/c-get-desktop-screenshot
image: /imgs/thumbnails/desktopSS.webp
---

I found this feature while looking inside **Graphics** class and since it was so simple to use, I decided to post it here. It basically allows you to take print screens programmatically and save them as local images or forward them through the network, etc.

As I said, it doesn't require more than 15 lines of code - this function: **Graphics.CopyFromScreen** does all the 'hard work' so we only need to put this into a **Bitmap** and save/display it.

## To the code!

There are 3 steps that you need to follow:

*   create a **Bitmap** that's exactly the screen's size
*   using that Bitmap, create a **Graphics** object (**Graphics.FromImage**)
*   use **CopyFromScreen()** and save the **Bitmap**

The code looks like this:

```csharp
private void takeScreenShot()
{
    Bitmap bmp = new Bitmap(Screen.PrimaryScreen.Bounds.Width, Screen.PrimaryScreen.Bounds.Height);
    using (Graphics g = Graphics.FromImage(bmp))
    {
        g.CopyFromScreen(0, 0, 0, 0, Screen.PrimaryScreen.Bounds.Size);
        bmp.Save("screenshot.png");  // saves the image
    }                 
}
```