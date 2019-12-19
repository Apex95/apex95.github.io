---
layout: post
title:  "C# Synchronize 2 RichTextBoxes' Scroll"
date:   2013-03-17 20:02:05 +0300
categories: interface
thumbnail: /imgs/thumbnails/rtbcontrol.webp
---

I recently had a problem when I tried to synchronize the scrolling between 2 **RichTextBoxes** - that was because these controls behave different than normal TextBoxes. However I managed to solve this...after some time, and I decided to post the solution. The idea is based on overriding one RichTextBox's **WndProc()** and then sending its scroll position to the other one.

The advantage of this method is that the synchronization is based on the RichTextBox's real position - not on the thumb/scrollbar position.

## 1.Fixed problems

These 2 problems are **fixed** if you use this method:

1.  If you press enter, while the caret is on the last line, the RichTextBox scrolls a little bit more than it should while the other one scrolls normally.
2.  If you delete the last lines in a RichTextBox, it doesn't scroll down - but the other one will keep scrolling.


## 2\. How to

As I said before, you need to create a **custom RichTextBox**, based on the original one, so you can override **WndProc()**.

A short schema:

**syncRichTextBox** (object)  
1) scroll  
2) tell **anotherRichTextBox** to scroll to my position

**anotherRichTextBox**  
1) idle - doing nothing but waiting for messages from **syncRichTextBox**

First, include this function, from **user32.dll**

```csharp
[DllImport("user32.dll", CharSet = CharSet.Auto)]
private static extern int SendMessage(IntPtr hWnd, int wMsg, IntPtr wParam, ref Point lParam);
```

* notice the **lParam** argument is a **Point** - this will store the scroll's position.

Then, add these **WM contants**, you'll need them when you synchronize the scrolling:

```csharp
private const int WM_VSCROLL = 0x115;  //tells the control to scroll

private const int WM_GETDLGCODE = 0x87;   //sent when the caret is going out of the 'visible area' (so scroll is needed)

private const int WM_MOUSEFIRST = 0x200;  //scrolls if the mouse leaves the 'visible area' (example when you select text)

private const int EM_GETSCROLLPOS = 0x4DD;  //you send this message and the control returns it's scroll position

private const int EM_SETSCROLLPOS = 0x4DE;//this is used to set the control's scroll position
```

Now, you only have to create the custom **RichTextBox** - if its scroll position is changed, it will send a message containing its new position to the other RichTextBox (**anotherRichTextBox**) - the 2nd one doesn't require overriding.

The code would look like this:

```csharp
public class syncRichTextBox : RichTextBox
{
      public syncRichTextBox()
      {
              protected override void WndProc(ref Message m)
              {
                    base.WndProc(ref m);

                    if (m.Msg == WM_VSCROLL || m.Msg == WM_GETDLGCODE || m.Msg == WM_MOUSEFIRST)
                    {
                          Point p = new Point();

                          //the scroll position is returned in the variable p (point)
                          SendMessage(this.Handle, EM_GETSCROLLPOS, IntPtr.Zero, ref p);  

                          //sends the position to the other richtextbox (remember to replace its name)
                          SendMessage(anotherRichTextBox.Handle, EM_SETSCROLLPOS, IntPtr.Zero, ref p);  

                    }

              }
      }
}
```