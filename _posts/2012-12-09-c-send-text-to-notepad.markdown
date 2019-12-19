---
layout: post
title:  "C# Send Text to Notepad"
date:   2012-12-09 20:02:05 +0300
categories: miscellaneous
image: /imgs/thumbnails/sendtext.webp
---

This tutorial focuses on **sending text** from a C# program to any other window by using 2 functions provided by **user32.dll**. The big advantage of this method is that the window you're sending the text to **doesn't require focus**.

Don't forget to include these namespaces:

```csharp
using System.Diagnostics;
using System.Runtime.InteropServices;
```

## 1\. FindWindowEx

This method gets all the child elements from a parent element: for example it can get the handle of a textbox(child) from the window(parent).

```csharp
[DllImport("user32.dll")]
public static extern IntPtr FindWindowEx(IntPtr hwndParent, IntPtr hwndChildAfter, string lpszClass, string lpszWindow);
```

## 2\. SendMessage

This one simply sends a message to the specified handle (it might be a window, a textbox, anything...).  
We'll use this to send the data we want.

```csharp
[DllImport("User32.dll")]
public static extern int SendMessage(IntPtr hWnd, int uMsg, int wParam, string lParam);
```

## How it works

In this tutorial I'll send some text to **Notepad** - it's just an example, but this method works for any program. Basically you get the window's handle from the process and then, by using **FindWindowEx** you get the children's handle (that's the textbox). Finally, you send the text to that child.

* you need to know the child element's name - you can find it with Spy++.

I'll post below a C# application that changes the text from **notepad**'s window.

```csharp
using System;
using System.Diagnostics;
using System.Runtime.InteropServices;

namespace Test
{
    class progam
    {
        //include FindWindowEx
        [DllImport("user32.dll")]
        public static extern IntPtr FindWindowEx(IntPtr hwndParent, IntPtr hwndChildAfter, string lpszClass, string lpszWindow);

        //include SendMessage
        [DllImport("user32.dll")]
        public static extern int SendMessage(IntPtr hWnd, int uMsg, int wParam, string lParam);

        //this is a constant indicating the window that we want to send a text message
        const int WM_SETTEXT = 0X000C;

        static void Main(string[] args)
        {
            //getting notepad's process | at least one instance of notepad must be running
            Process notepadProccess = Process.GetProcessesByName("notepad")[0]; 

            //getting notepad's textbox handle from the main window's handle
            //the textbox is called 'Edit'
            IntPtr notepadTextbox = FindWindowEx(notepadProccess.MainWindowHandle, IntPtr.Zero, "Edit", null);  
            //sending the message to the textbox
            SendMessage(notepadTextbox, WM_SETTEXT, 0, "This is the new Text!!!");  
        }
    }
}
```

Using this method, you won't need to actually give focus to the window - but you'll have to know some additional information about the **program's structure** - that's because you need to know what child to select, where is that child located, etc..

But as I said before, you can find this out by using **Spy++** (from Visual Studio).