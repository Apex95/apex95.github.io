---
layout: post
title:  "C# Falling Snowflakes on Desktop"
date:   2012-12-29 20:02:05 +0300
tags: c-sharp
redirect_from: /miscellaneous/c-falling-snowflakes-on-desktop
image: /imgs/thumbnails/snowflake.webp
---

Since it's winter, I decided to write about how to create an application that makes **snowflakes fall on your desktop**. It's just like snowing on your desktop, but the application is pretty basic so there's space for improvements - I tried to write a short code so it's easier to understand.

{% include image.html url="/imgs/posts/c-falling-snowflakes-on-desktop/1.png" description="Snowflakes over the window of Visual Studio" %}

## 1.How to?

It's quite simple:

1.  create a **transparent** form the same size as your desktop (you can still use other programs while this form is running)
2.  on this form you add about 40-50 `PictureBox`es - each one will contain a snowflake image
3.  finally you'll have to use a timer to constantly change their position in the form, so the snowflakes will look like they're slowly falling

The program presented in this tutorial has 2 parts:

*   a class called snowflake
*   the main program

## 2.Creating a Snowflake (class/image)

First, try drawing a **white** snowflake on a **black background**. Why? We'll set the black background as **transparent** so only the true snowflake will be shown.

For my application I used the following image:

{% include image.html url="/imgs/posts/c-falling-snowflakes-on-desktop/2.jpg" description="Snowflake image used in this project" %}

Next is the coding part: I created a separate class called **snowflake** (inherits from **PictureBox** class).

It contains 3 methods:

`create()` - sets the PictureBox's image and also its position in the form

`move()` - creates a Timer that changes the snowflake's position 

`t_tick()` - changes the snowflake's position each 40ms 


_Note that using a class makes everything much easier._

The code for the class:

```csharp
class snowflake : PictureBox
{
        public snowflake()
        {
            create();
            move();
        }

        Random r = new Random();

        private void create()   
        {
            //the line below sets a random point to the newly created snowflake
            this.Location = new Point(r.Next(-Screen.PrimaryScreen.Bounds.Width, Screen.PrimaryScreen.Bounds.Width), r.Next(-Screen.PrimaryScreen.Bounds.Height, Screen.PrimaryScreen.Bounds.Height));

            //here we define the picturebox's size & the image
            this.MinimumSize = new Size(7, 7);
            this.Size = new Size(10, 10);
            this.BackgroundImage = Image.FromFile("snowflake.jpg");
        }

        private void move()
        {
            //a snowflake has a timer that moves it on the screen
            Timer t = new Timer();
            t.Interval = 40;

            t.Tick += new EventHandler(t_Tick); 

            t.Start();
        }

        void t_Tick(object sender, EventArgs e)
        {
            //moves the snowflake by constantly adding a values to its location
            this.Location += new Size(1, 3);   

            //checking if the snowflake isn't going out of the visible area
            //if it goes out we reset its location to a random one.
            if (this.Location.X > Screen.PrimaryScreen.Bounds.Width || this.Location.Y > Screen.PrimaryScreen.Bounds.Height)
                this.Location = new Point(r.Next(-Screen.PrimaryScreen.Bounds.Width, Screen.PrimaryScreen.Bounds.Width), r.Next(-Screen.PrimaryScreen.Bounds.Height, Screen.PrimaryScreen.Bounds.Height));

        }
}
```

## 3\. Creating the main program

We want the main program (the form) to be **transparent** so we'll make it **black** and setting its size equal to **Screen.PrimaryScreen.Bounds.Size**. After we must set the **TransparencyKey** to **black**.

Finally, we'll create an array of **snowflake**(class), that will contain all the snowflakes we want. When an element from that array is instantiated, a new snowflake will spawn and will start falling.

_Note:_ we must use a timer and not a repetitive structure when we create snowflakes - that's because our instructions run on the UI Thread.

The sourcecode of the main program:

```csharp
public partial class main : Form
{
        public main()
        {
            InitializeComponent();
        }

        int i = 0;
        Timer t; 
        snowflake[] snowflakes;

        private void Form1_Load(object sender, EventArgs e)
        {
            this.TopMost = true;  //makes snowflakes show over other programs

            this.Size = Screen.PrimaryScreen.Bounds.Size + (new Size(20, 20));
            this.Location = new Point(0, 0);
            this.FormBorderStyle = FormBorderStyle.None; //also necessary so no borders will be shown
            this.BackColor = Color.Black;  
            this.TransparencyKey = Color.Black; //mandatory, it makes black color transparent (won't be shown)

            snowflakes = new snowflake[40];   //we want 40 snowflakes

            t = new Timer();  //this timer creates a snowflake each second
            t.Interval = 1000;
            t.Tick += new EventHandler(t_Tick);
            t.Start();  
        }

        void t_Tick(object sender, EventArgs e)
        {
            if (i >= 40)  //if we go over 40 snowflakes 
            {
                t.Stop();  //we can stop creating new ones
                return;
            }
            snowflakes[i] = new snowflake();
            Controls.Add(snowflakes[i]);  //each picturebox (snowflake) created must be added to the form
            i++;    
        }
}
```

## The Complete Code

Here's the complete code:

```csharp
using System;
using System.Drawing;
using System.Windows.Forms;

namespace FallingSnowFlakes
{
    public partial class main : Form
    {
        public main()
        {
            InitializeComponent();
        }

        int i = 0;
        Timer t;
        snowflake[] snowflakes;

        private void Form1_Load(object sender, EventArgs e)
        {
            this.TopMost = true;

            this.Size = Screen.PrimaryScreen.Bounds.Size + (new Size(20, 20));
            this.Location = new Point(0, 0);
            this.FormBorderStyle = FormBorderStyle.None;
            this.BackColor = Color.Black;
            this.TransparencyKey = Color.Black;

            snowflakes = new snowflake[40];

            t = new Timer();
            t.Interval = 1000;
            t.Tick += new EventHandler(t_Tick);
            t.Start();

        }

        void t_Tick(object sender, EventArgs e)
        {
            if (i >= 40)
            {
                t.Stop();
                return;
            }
            snowflakes[i] = new snowflake();
            Controls.Add(snowflakes[i]);
            i++;    
        }
    }

    class snowflake : PictureBox
    {
        public snowflake()
        {
            create();
            move();
        }

        Random r = new Random();

        private void create()
        {
            this.Location = new Point(r.Next(-Screen.PrimaryScreen.Bounds.Width, Screen.PrimaryScreen.Bounds.Width), r.Next(-Screen.PrimaryScreen.Bounds.Height, Screen.PrimaryScreen.Bounds.Height));

            this.MinimumSize = new Size(7, 7);
            this.Size = new Size(10, 10);

            this.BackgroundImage = Image.FromFile("snowflake.jpg");

        }

        private void move()
        {
            //this.Location += new Size(1, 3);
            Timer t = new Timer();
            t.Interval = 40;
            t.Tick += new EventHandler(t_Tick);

            t.Start();

        }

        void t_Tick(object sender, EventArgs e)
        {
            this.Location += new Size(1, 3);
            if (this.Location.X > Screen.PrimaryScreen.Bounds.Width || this.Location.Y > Screen.PrimaryScreen.Bounds.Height)
                this.Location = new Point(r.Next(-Screen.PrimaryScreen.Bounds.Width, Screen.PrimaryScreen.Bounds.Width), r.Next(-Screen.PrimaryScreen.Bounds.Height, Screen.PrimaryScreen.Bounds.Height));

        }
    }
}
```