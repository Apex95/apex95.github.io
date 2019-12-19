---
layout: post
title:  "C# Moving form without border/title bar"
date:   2012-05-25 20:02:05 +0300
categories: interface
image: /imgs/thumbnails/formTitleBar.webp
---

## 1\. Removing the title bar and border

In this tutorial I will show you how you can make a draggable window (**Form**) with no **title bar** or **border**. By default, when you remove the border of a Form, you can't move or drag it anymore and this behavior must be implemented separately.

I assume you already have the program ready - at least the design part, so I'll skip to what interests you. :D

Initially, set in the **Properties Window**:  
**FormBorderStyle** : **None**

## 2\. Getting a movable window

This will hide the title bar and window's border. But if we remove that **title bar**, we can not move the window on the screen anymore - just because the title bar handles the window's movement.

To move the window, we have to use some **WinAPI** . Don't worry if you don't know WinAPI very well, it's not a long code - so no special knowledge is required .

We'll include in the program:

```csharp
using System.Runtime.InteropServices
```

After that, two methods must be imported from **user32.dll** :  
**SendMessage()**  
**ReleaseCapture();**

To do this, we'll add the following code to the program

```csharp
[DllImportAttribute("user32.dll")]
public static extern int SendMessage(IntPtr hWnd, int Msg, int wParam, int LPAR);
[DllImportAttribute ("user32.dll")]
public static extern bool ReleaseCapture();
```

What is this doing? It imports 2 methods from **user32.dll**:  
- the first one (**SendMessage()**) checks if the mouse button is clicked, and then sends a message to our program, notifying the window to change it's position acording to our cursor  
- the second method (**ReleaseCapture()**) releases the mouse capture from our window.

Using them both, we can make a method that when called, moves the window to our cursor position - acts exactly like a title bar. However we'll have to bind this method to the **MouseDown** event of the **Form**.

```csharp
const int WM_NCLBUTTONDOWN = 0xA1; 
const int HT_CAPTION = 0x2;  //this indicates that the action takes place on the title bar

private void move_window(object sender, MouseEventArgs e)
{
        if (e.Button == MouseButtons.Left)
        {
               ReleaseCapture();
               SendMessage(this.Handle, WM_NCLBUTTONDOWN, HT_CAPTION, 0);
        }
}
```

Now you just have to attach this method to the **MouseDown** event of the Form. You can do this from the Properties Window or, using the following code:

```csharp
this.MouseDown += new MouseEventHandler(move_window);
//any form has a MouseDown event, we use it to call the function
```

In the end, you get (or should get) something like this:

```csharp
public partial class Form1: Form
{
    [DllImportAttribute("user32.dll")]
    public static extern int SendMessage(IntPtr hWnd, int Msg, int wParam, int LPAR);
    [DllImportAttribute ("user32.dll")]
    public static extern bool ReleaseCapture();

    const int WM_NCLBUTTONDOWN = 0xA1;
    const int HT_CAPTION = 0x2;

    private void move_window(object sender, MouseEventArgs e)
    {
        if (e.Button == MouseButtons.Left)
        {
            ReleaseCapture();
            SendMessage(this.Handle, WM_NCLBUTTONDOWN, HT_CAPTION, 0);
        }
    }

    public Form1()
    {
        // If you haven't set FormBorderStyle = none from the properties window, just uncomment the line below           
        // FormBorderStyle = FormBorderStyle.None;

        this.MouseDown += new MouseEventHandler(move_window); // binding the method to the event

        InitializeComponent();
    }
}
```