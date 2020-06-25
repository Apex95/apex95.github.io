---
layout: post
title:  "C# Ascii Art Tutorial"
date:   2013-04-18 20:02:05 +0300
categories: files
image: /imgs/thumbnails/asciiArt.webp
---

If you got here, you probably want to know how **Ascii Art** works and how to use C# to **transform images into text**. We'll do this by making good use of **LockBits()** and **UnlockBits()**, and also, a **pointer** - going unsafe !

I know those make everything more complicated, but they're more efficient.

## How does an Ascii Art generator work?

*   first, it opens the Image and resizes it to a custom size (about 100x100)
*   using 2 loops and a **pointer**, it gets the color of each pixel in the image (the image, stored in memory, looks like a two-dimensional array of pixels)
*   for each pixel, it adds a character into a text file, depending on the **alpha** (transparency)

Now if you got a basic idea about how this works, you can build your own program - no need to worry about the source code, you'll find everything here, including the necessary explanations.

Start by creating a **Forms Project**, make sure you have checked **Allow unsafe code** from _Project->Properties->Build_.

In **form1_load** add the following line to load the image from the executable's directory:

```csharp
Image img = Image.FromFile("image.png");
```

Then, we transform this image into a **Bitmap**, and resize it to **100x100** pixels - don't use HD images there, because it will take some time to check every pixel:

```csharp
Bitmap bmp = new Bitmap(img, 100, 100);
// you can increase the Ascii Art's quality by increasing the bitmap's dimensions
// this also increases the time taken by the conversion process...
```

Now we need a **StringBuilder** in which we store the characters corresponding to the image's pixels.

_Update: it is more efficient to use a **StringBuilder** instead of a **string** ([see here why](http://www.codingvision.net/tips-and-tricks/c-string-vs-stringbuilder/ "String vs StringBuilder"))._

## 1.From Pixel to Char

As I said, we'll use those 2 functions :

**LockBits()** - locks the image in the system's memory so we can directly get pixel's attributes by using a pointer  
**UnlockBits()** - releases the memory used

As you know, an image is created by a group of pixels and each **pixel** takes **4 bytes** of memory, that means it has 4 properties: Red, Green, Blue and Alpha/transparency. From the memory we can read each pixel's property.

Each pixel must be transformed into a character with the same color and all the characters must be the same width and height (**monospaced**) so we maintain the aspect ratio.

```csharp
private unsafe StringBuilder convert_image(Bitmap bmp)
{
            StringBuilder asciiResult = new StringBuilder();   //here we store the ascii-art string

            //setting the font's size & type (Courier new is monospace)
            asciiResult.Append(""); 

            //storing the image's height & width
            int bmpHeight = bmp.Height;  
            int bmpWidth = bmp.Width;

            //here we lock the image in the memory by using LockBits
            BitmapData bmpData = bmp.LockBits(new Rectangle(0, 0, bmpWidth, bmpHeight), ImageLockMode.ReadOnly, bmp.PixelFormat);

            // bmpStride tells us how many pixels are on a line
            // because images have multiple lines of pixels (like 2D arrays)
            int bmpStride = bmpData.Stride;  

            // this gets the memory address of the first pixel in the image
            // currentPixel is the pointer we'll use
            byte* currentPixel = (byte*)bmpData.Scan0;

            for (int y = 0; y < bmpHeight; y++)
            {
                for (int x = 0; x < bmpWidth; x++)
                {
                    // as I said a pixel takes 4 bytes of memory so it has 4 attributes
                    int r = currentPixel[x*4]; 
                    int g = currentPixel[x*4 + 1];
                    int b = currentPixel[x*4 + 2];
                    int alpha = currentPixel[x * 4 + 3];

                    // appending the character to the ascii-art stringbuilder
                    // note there's a custom function 'getAsciiChar()' - I'll explain it soon
                    asciiResult.Append(String.Format("<span style="color:rgb({0},{1},{2});">{3}</span>", r, g, b, getAsciiChar(alpha)));

                }

                // reached end of this line, by adding bmpStride (number of pixels on each line)
                // to the memory address, it gives us the address of the first pixel on the next line
                currentPixel += bmpStride;  
                asciiResult.Append("  
");

            }
            asciiResult.Append(""); // closing the body tag we opened at the beginning

            bmp.UnlockBits(bmpData);  //removing the image from the memory

            return asciiResult;  // returning the ascii-art stringbuilder
}
```

## 2.Choosing the right character

There's a function in the code above that I'll explain here: **getAsciiChar()**. What it does? It returns a character depending on the transparency of the current pixel (so it looks like true ascii art).

```csharp
private char getAsciiChar(int alpha)
{
    if (alpha >= 240)
        return '@';
    if (alpha >= 200)
        return '#';
    if (alpha >= 160)
        return '/pre>;
    if (alpha >= 120)
        return '%';
    if (alpha >= 80)
        return '8';
    if (alpha >= 40)
        return '|';

    return '.';
}
```

## 3.Displaying the Ascii-Art

Now we just have to display our image, which is easily done using this:

```csharp
private void show_image(StringBuilder asciiResult)
{
    StreamWriter sw = new StreamWriter("image.html");
    sw.Write(asciiResult.ToString());
    sw.Close();
}
```

Finally, we get this:

```csharp
using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Text;
using System.Windows.Forms;

namespace WindowsFormsApplication1
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();

            Image img = Image.FromFile("image.png");
            Bitmap bmp = new Bitmap(img, 100, 100);
            show_image(convert_image(bmp));
        }

        private unsafe StringBuilder convert_image(Bitmap bmp)
        {
            StringBuilder asciiResult = new StringBuilder();
            asciiResult.Append("");

            int bmpHeight = bmp.Height;
            int bmpWidth = bmp.Width;

            BitmapData bmpData = bmp.LockBits(new Rectangle(0, 0, bmpWidth, bmpHeight), ImageLockMode.ReadOnly, bmp.PixelFormat);

            int bmpStride = bmpData.Stride;
            byte* currentPixel = (byte*)bmpData.Scan0;

            for (int y = 0; y < bmpHeight; y++)
            {
                for (int x = 0; x < bmpWidth; x++)
                {
                    int r = currentPixel[x * 4];
                    int g = currentPixel[x * 4 + 1];
                    int b = currentPixel[x * 4 + 2];
                    int alpha = currentPixel[x * 4 + 3];
                    asciiResult.Append(String.Format("<span style="color:rgb({0},{1},{2});">{3}</span>", r, g, b, getAsciiChar(alpha)));

                }
                currentPixel += bmpStride;
                asciiResult.Append("  
");

            }
            asciiResult.Append("");

            bmp.UnlockBits(bmpData);
            return asciiResult;
        }

        private char getAsciiChar(int alpha)
        {
            if (alpha >= 240)
                return '@';
            if (alpha >= 200)
                return '#';
            if (alpha >= 160)
                return '/pre>;
            if (alpha >= 120)
                return '%';
            if (alpha >= 80)
                return '8';
            if (alpha >= 40)
                return '|';

            return '.';
        }
        private void show_image(StringBuilder asciiResult)
        {
            StreamWriter sw = new StreamWriter("image.html");
            sw.Write(asciiResult.ToString());
            sw.Close();
        }
    }
}
```

When you run the application, wait until the Form shows up - that's when the image conversion is done, then simply open "image.html".

Here's a small screenshot of an Ascii Art made with this program - this is how the result will look like:

{% include image.html url="/imgs/posts/c-ascii-art-tutorial/1.png" description="Ascii Art Sample generated with this program" %}

Well, that's all, if you have problems, you can always leave a comment :).