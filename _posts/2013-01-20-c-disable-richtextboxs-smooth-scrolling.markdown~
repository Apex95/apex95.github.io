---
layout: post
title:  "C# Disable RichTextBox's Smooth Scrolling"
date:   2013-01-20 20:02:05 +0300
categories: interface
thumbnail: /imgs/thumbnails/smoothscrolling.png
---

In this article I'll show you how to disable **RichTextBox**'s **Smooth Scrolling** - aka make RichTextBox scroll **line by line**. I know this is a problem for many developers, it was a problem for me too, so that's why I decided to post this code snippet.

## Removing Smooth Scrolling

Well, there's no easy way to fix it and since there's no other option, you'll have to make a custom RichTextBox and override the **WndProc()** function.

Basically you need to handle all the vertical scrolling: this means check if user scrolls (**WM_MOUSEWHEEL**), if so, use **SendMessage()** to send **WM_VSCROLL** to the control.

Before starting, you'll need to include this namespace:

```csharpusing System.Runtime.InteropServices;
```

The following line sends a message to the RichTextBox which will tell it to scroll up or down:

```csharpSendMessage(this.Handle, WM_VSCROLL, (IntPtr)wParam, IntPtr.Zero);

//wParam (3rd parameter) can be 0 or 1
// 0 to scroll up
// 1 to scroll down 
```

Now, you must create your own control, which inherits from **RichTextBox** and that handles the **WM_MOUSEWHEEL** messages separately - it will send a **WM_VSCOLL** each time we scroll.

It should look like this one (thanks to <font color="darkred">Mark</font> for improvements):

```csharpclass editedRichTextBox : RichTextBox
{
    [DllImport("user32.dll", CharSet = CharSet.Auto)]
    private static extern int SendMessage(IntPtr hWnd, int wMsg, IntPtr wParam, IntPtr lParam);

    //this message is sent to the control when we scroll using the mouse
    private const int WM_MOUSEWHEEL = 0x20A;

    //and this one issues the control to perform scrolling
    private const int WM_VSCROLL = 0x115;

    protected override void WndProc(ref Message m)
    {
        if (m.Msg == WM_MOUSEWHEEL)
        {
            int scrollLines = SystemInformation.MouseWheelScrollLines;
            for (int i = 0; i < scrollLines; i++)
            {
                if ((int)m.WParam > 0) // when wParam is greater than 0
                    SendMessage(this.Handle, WM_VSCROLL, (IntPtr)0, IntPtr.Zero); // scroll up 
                else  
                    SendMessage(this.Handle, WM_VSCROLL, (IntPtr)1, IntPtr.Zero); // else scroll down
            }
            return;
        }
        base.WndProc(ref m);
    }
} ```