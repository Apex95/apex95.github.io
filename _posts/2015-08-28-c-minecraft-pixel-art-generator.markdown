---
layout: post
title:  "C# Minecraft Pixel Art Generator"
date:   2015-08-28 20:02:05 +0300
categories: miscellaneous
thumbnail: /imgs/thumbnails/minecraft.jpg
---

_Good morning **class**, (see what I did there:P ?)_
_Today we will discuss a very important subject: creating **pixel art** in **Minecraft** from a given image._  

&nbsp;

&nbsp;


Ok guys, so I saw people creating **pixel art** in **Minecraft** (trying to render images in the game using blocks) and I really liked the idea. Unfortunately I'm not good at drawing but I'm a coder and this will suffice, for now - hopefully this will prove its usefulness for those of you who want to "decorate" their servers.

<u>The program's idea is quite simple:</u> it scans the image pixel by pixel and for each pixel places a block with a similar color in the game, by sending a command (**/setblock X Y Z &lt;block name&gt;**) to the server's **InputStream** (no networking stuff, no delay, no headache).

## Results

This is what I managed to obtain with this program using a palette of **16 colors**. The coloring is not very accurate since I can't produce all the colors in the photos with only 16 types of blocks - however this can be fixed by using more types of blocks.

![](http://i57.tinypic.com/35lyxeb.png)

![](http://i59.tinypic.com/2q33wpk.png)

![](http://i59.tinypic.com/k05aas.png)

![](http://i59.tinypic.com/jsnll3.png)

![](http://i61.tinypic.com/34j50gl.png)

![](http://i57.tinypic.com/fdgaaa.png)

![](http://i59.tinypic.com/11j0hth.png)

## 1\. Starting the server

In order to send commands to your server's **InputStream** you need to tweak a few settings at process level. This means you'll have to start the server from this program, using the **Process** class. Our goal is to make this process read inputs from a custom stream (**Process.StandardInput**) - this stream will be used by our console application to send the set of **/setblock** commands.

{% highlight csharp linenos %}// Process mcServerProc = new Process();

// this must be set to false or the application will throw an exception
mcServerProc.StartInfo.UseShellExecute = false; 

// forcing cmd.exe to use Process.StandardInput as input stream 
mcServerProc.StartInfo.RedirectStandardInput = true; 

// same for these 2 lines - so we can see the server's output
mcServerProc.StartInfo.RedirectStandardOutput = true; 
mcServerProc.StartInfo.RedirectStandardError = true;
{% endhighlight %}

After the input stream was changed, this method can be used to supply information to the process:

{% highlight csharp linenos %}mcServerProc.StandardInput.WriteLine("command goes here");
{% endhighlight %}

If you want to display, in your console, any messages that the server sends, you'll need 2 event handlers (1 for the outputstream and 1 for the errorstream). I wrote them as anonymous functions to keep this sourcecode as short as possible:

{% highlight csharp linenos %}mcServerProc.OutputDataReceived += (sender, e) => { Console.WriteLine(e.Data); };
mcServerProc.ErrorDataReceived += (sender, e) => { Console.WriteLine(e.Data); };
{% endhighlight %}

After this, you'll need to call these 2 functions:

{% highlight csharp linenos %}mcServerProc.BeginOutputReadLine();
mcServerProc.BeginErrorReadLine();{% endhighlight %}

Basically you'll start **cmd.exe** from the C# application and from there launch the server by loading the jar file with a line like this:  
**java -Xmx1024M -Xms1024M -jar minecraft_server.1.8.8.jar nogui**

What you need to be careful about is that once you start the server, your only way to communicate with it is the console - if you close the console, the server will keep running in the background (**java.exe**) and you'll have to kill the process in order to stop it.

To avoid this make sure you send the command: **stop** before the console closes.

Until now we have something that looks like a primitive wrapper:

{% highlight csharp linenos %}using (Process mcServerProc = new Process())
{
    // path to cmd.exe
    mcServerProc.StartInfo.FileName = Path.Combine(Environment.SystemDirectory, "cmd.exe");

    // path to your minecraft server
    mcServerProc.StartInfo.WorkingDirectory = "D:\\mc server"; 

    // bunch of settings, to allow redirection of stdin / stdout / stderr
    mcServerProc.StartInfo.UseShellExecute = false; // don't use windows's shell to start this
    mcServerProc.StartInfo.RedirectStandardInput = true;
    mcServerProc.StartInfo.RedirectStandardOutput = true;
    mcServerProc.StartInfo.RedirectStandardError = true;
    mcServerProc.StartInfo.CreateNoWindow = true;

    // events used to display stderr and stdout in our console
    mcServerProc.OutputDataReceived += (sender, e) => { Console.WriteLine(e.Data); };
    mcServerProc.ErrorDataReceived += (sender, e) => { Console.WriteLine(e.Data); };

    // starting cmd.exe
    mcServerProc.Start();

    // starts reading form stdout & stderr
    mcServerProc.BeginOutputReadLine();
    mcServerProc.BeginErrorReadLine();

    // launches the server by sending the line between quotes to cmd.exe
    mcServerProc.StandardInput.WriteLine("java -Xmx1024M -Xms1024M -jar minecraft_server.1.8.8.jar nogui");

    // keeps the command prompt alive until you type 'stop'
    // otherwise your program will close but the server will keep running
    // and can only be closed from task manager
    while (true)
    {
        if (Console.ReadLine().Contains("stop"))
            break;
    }

    mcServerProc.StandardInput.WriteLine("stop"); // stops the server

    Thread.Sleep(3000);
}{% endhighlight %}

## 2\. Choosing the right block

Ok, that was the easy part, believe it or not. We'll now have to create a list (it's actually a **Dictionary**) that contains the name of the available blocks and their colors.

{% highlight csharp linenos %}static Dictionary<Color, string> colorsDictionary = new Dictionary<Color, string>();

static void populateDictionary()
{
    colorsDictionary.Add(Color.FromArgb(238, 238, 238), "wool");
    colorsDictionary.Add(Color.FromArgb(235, 131, 60), "wool 1");
    colorsDictionary.Add(Color.FromArgb(184, 56, 195), "wool 2");
    colorsDictionary.Add(Color.FromArgb(111, 144, 214), "wool 3");
    colorsDictionary.Add(Color.FromArgb(222, 207, 42), "wool 4");
    colorsDictionary.Add(Color.FromArgb(60, 195, 48), "wool 5");
    colorsDictionary.Add(Color.FromArgb(219, 138, 160), "wool 6");
    colorsDictionary.Add(Color.FromArgb(76, 76, 76), "wool 7");
    colorsDictionary.Add(Color.FromArgb(163, 170, 170), "wool 8");
    colorsDictionary.Add(Color.FromArgb(45, 134, 172), "wool 9");
    colorsDictionary.Add(Color.FromArgb(148, 77, 210), "wool 10");
    colorsDictionary.Add(Color.FromArgb(45, 59, 178), "wool 11");
    colorsDictionary.Add(Color.FromArgb(90, 54, 29), "wool 12");
    colorsDictionary.Add(Color.FromArgb(64, 89, 28), "wool 13");
    colorsDictionary.Add(Color.FromArgb(171, 47, 42), "wool 14");
    colorsDictionary.Add(Color.FromArgb(14, 14, 14), "wool 15");
}
{% endhighlight %}

The next step is to realize that these images contain more than 16 colors so we need a function that takes a pixel's color and tells us which color (block) from the list above is the best match.

Our function is based on a method called **k nearest neighbor**: which compares 2 colors and returns an error. The lower the error is the closer the block's color is to the original. In our case the formula looks like the euclidean distance between **2 points** in a **3d** space - but instead of coordinates **(X, Y, Z)** we use **(R, G, B)** and the points are actually the colors.

<u>For example:</u>

if we have a pixel of this color: **P****(R:100 G:100 B:100)** and we have only 2 available blocks: **BlackBlock****(R:0 G:0 B:0)** and **WhiteBlock****(R:255 G:255 B:255)** we compute the errors for each one

*   Comparing the pixel's color to the **BlackBlock**:  
    error = sqrt((100-0)^2 + (100-0)^2 + (100-0)^2) = <u>173.2</u>
*   Now comparing it to the **WhiteBlock**:  
    error = sqrt((100-255)^2 + (100-255)^2 + (100-255)^2) = <u>268.46</u>

This means the **BlackBlock** is a better choice as it matches the pixel's color better.

The function will look like this (it returns the index of the block):

{% highlight csharp linenos %}static int approximateColor(Color pixelColor)
{
    double minError = 99999; double currentError = 0;
    int bestColorIndex = 0;

    for (int i = 0; i < colorsDictionary.Count; i++)
    {
        // gets the color of the block found at index 'i'
        Color blockColor = colorsDictionary.ElementAt(i).Key;

        // k nearest neighbor
        currentError = Math.Sqrt(Math.Pow(pixelColor.R - blockColor.R, 2) + Math.Pow(pixelColor.G - blockColor.G, 2) + Math.Pow(pixelColor.B - blockColor.B, 2));

        if (currentError < minError)
        {
            minError = currentError;
            bestColorIndex = i;
        }            
    }

    return bestColorIndex;
}
{% endhighlight %}

## 3\. Rendering the image in game

The last step is constructing the image using blocks; take each pixel of the image, get its color using **GetPixel(x, y)** and run it through the function above to obtain the block that matches the color.

Make sure you include this reference: **System.Drowing.dll**.

Once you have the index of the block, you'll have to construct a **/setblock** command and send it to the server.

<u>small note:</u> you can use **LockBits()** and **UnlockBits()** for efficiency reasons but the server will still limit your speed. In my opinion, it's not worth it here.

{% highlight csharp linenos %}static void renderImage(StreamWriter stdin, Image img)
{
    Bitmap bmp = (Bitmap)img;

    // coordinates - from where to start rendering the image (F3 in game)
    int X = 335;
    int Y = 4;
    int Z = -567;

    // rendering the image from the last row of pixels to the first
    for (int i = bmp.Height-1; i > 0; i--)
    {
        for (int j = 0; j < bmp.Width; j++)
        {
            string cmdTemplate = String.Format("/setblock {0} {1} {2} ", X, Y, Z);

            int bestColorIndex = approximateColor(bmp.GetPixel(j, i));
            stdin.WriteLine(cmdTemplate + colorsDictionary.ElementAt(bestColorIndex).Value);
            X++;

        }
    Y++;
    X -= bmp.Width; 

    }
}
{% endhighlight %}

## 4\. Complete Sourcecode

This is the complete sourcecode - it was made for fun, so don't expect it to be really optimized.

Feel free to use / modify it and if you find it interesting or useful, consider sharing this page or dropping a backlink - it <u>helps a lot</u> xD

{% highlight csharp linenos %}using System;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Threading;

namespace Minecraft_Drawer
{
    class Program
    {
        static Dictionary<Color, string> colorsDictionary = new Dictionary<Color, string>();

        static void populateDictionary()
        {
            colorsDictionary.Add(Color.FromArgb(238, 238, 238), "wool");
            colorsDictionary.Add(Color.FromArgb(235, 131, 60), "wool 1");
            colorsDictionary.Add(Color.FromArgb(184, 56, 195), "wool 2");
            colorsDictionary.Add(Color.FromArgb(111, 144, 214), "wool 3");
            colorsDictionary.Add(Color.FromArgb(222, 207, 42), "wool 4");
            colorsDictionary.Add(Color.FromArgb(60, 195, 48), "wool 5");
            colorsDictionary.Add(Color.FromArgb(219, 138, 160), "wool 6");
            colorsDictionary.Add(Color.FromArgb(76, 76, 76), "wool 7");
            colorsDictionary.Add(Color.FromArgb(163, 170, 170), "wool 8");
            colorsDictionary.Add(Color.FromArgb(45, 134, 172), "wool 9");
            colorsDictionary.Add(Color.FromArgb(148, 77, 210), "wool 10");
            colorsDictionary.Add(Color.FromArgb(45, 59, 178), "wool 11");
            colorsDictionary.Add(Color.FromArgb(90, 54, 29), "wool 12");
            colorsDictionary.Add(Color.FromArgb(64, 89, 28), "wool 13");
            colorsDictionary.Add(Color.FromArgb(171, 47, 42), "wool 14");
            colorsDictionary.Add(Color.FromArgb(14, 14, 14), "wool 15");
        }

        // gets the closest available color (decides what block color should be used for a pixel)
        static int approximateColor(Color pixelColor)
        {
            double minError = 99999; double currentError = 0;
            int bestColorIndex = 0;

            for (int i = 0; i < colorsDictionary.Count; i++)
            {
                Color blockColor = colorsDictionary.ElementAt(i).Key;

                // k nearest neighbor
                currentError = Math.Sqrt(Math.Pow(pixelColor.R - blockColor.R, 2) + Math.Pow(pixelColor.G - blockColor.G, 2) + Math.Pow(pixelColor.B - blockColor.B, 2));

                if (currentError < minError)
                {
                    minError = currentError;
                    bestColorIndex = i;
                }

            }

            return bestColorIndex;
        }

        static void renderImage(StreamWriter stdin, Image img)
        {
            Bitmap bmp = (Bitmap)img;

            // coordinates - from where to start rendering the image
            int X = 335;
            int Y = 4;
            int Z = -567;

            for (int i = bmp.Height-1; i > 0; i--)
            {
                for (int j = 0; j < bmp.Width; j++)
                {
                    string cmdTemplate = String.Format("/setblock {0} {1} {2} ", X, Y, Z);

                    int bestColorIndex = approximateColor(bmp.GetPixel(j, i));
                    stdin.WriteLine(cmdTemplate + colorsDictionary.ElementAt(bestColorIndex).Value);
                    X++;

                }
                Y++;
                X -= bmp.Width; 

            }
        }

        static void Main(string[] args)
        {
            using (Process mcServerProc = new Process())
            {
                // path to cmd.exe
                mcServerProc.StartInfo.FileName = Path.Combine(Environment.SystemDirectory, "cmd.exe");

                // path to your minecraft server
                mcServerProc.StartInfo.WorkingDirectory = "D:\\mc server"; 

                // bunch of settings, to allow redirection of stdin / stdout / stderr
                mcServerProc.StartInfo.UseShellExecute = false;
                mcServerProc.StartInfo.RedirectStandardInput = true;
                mcServerProc.StartInfo.RedirectStandardOutput = true;
                mcServerProc.StartInfo.RedirectStandardError = true;
                mcServerProc.StartInfo.CreateNoWindow = true;

                // displaying stderr and stdout in our console
                mcServerProc.OutputDataReceived += (sender, e) => { Console.WriteLine(e.Data); };
                mcServerProc.ErrorDataReceived += (sender, e) => { Console.WriteLine(e.Data); };

                mcServerProc.Start();

                // starts reading form stdout & stderr
                mcServerProc.BeginOutputReadLine();
                mcServerProc.BeginErrorReadLine();

                // writes to the command prompt (cm d.exe) the line to execute the jar file (start the server)
                mcServerProc.StandardInput.WriteLine("java -Xmx1024M -Xms1024M -jar minecraft_server.1.8.8.jar nogui");

                Thread.Sleep(15000); // waiting for server to start

                // adds available blocks and their colors to the dictionary
                populateDictionary();

                // renders an image in the game
                renderImage(mcServerProc.StandardInput, Image.FromFile("randomPhoto.png"));

                // keeps the command prompt alive until you type 'stop'
                // otherwise this will close and the server keeps running
                while (true)
                {
                    if (Console.ReadLine().Contains("stop"))
                        break;
                }

                mcServerProc.StandardInput.WriteLine("stop"); // stops the server

                Thread.Sleep(3000);
            }
        }
    }
}
{% endhighlight %}