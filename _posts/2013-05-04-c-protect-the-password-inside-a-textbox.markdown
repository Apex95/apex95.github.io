---
layout: post
title:  "C# Protect the Password inside a TextBox"
date:   2013-05-04 20:02:05 +0300
categories: security
image: /imgs/thumbnails/passwordTextBox.webp
---

First of all, the **TextBox** Control is not a secure way to hold passwords - so don't use it as it is by default. Even with a **PasswordChar**, the real password is still visible if you use a tool like **Spy++**.  

## The Flaw (Explained)

As an example, take a simple **TextBox** with **PasswordChar = '*'**.  
Now, if you use Spy++ and inspect this application, you can get the password.

{% include image.html url="/imgs/posts/c-protect-the-password-inside-a-textbox/1.jpg" description="Recovering values from Password Textboxes with Spy++" %})


_But...why is this happening?_

Spy++ sends the message **WM_GETTEXT (0x000D)** to the TextBox, and the control just returns its value. It's actually working as intended and it reacts just like any other control, that obeys any message received.

## Fixing this issue...

I found a way to solve this by not allowing the **TextBox** to process the 'malicious' messages. So the solution consists in blocking any **WM_GETTEXT** message **unless** it was sent by the **Text property**.

_If the Text property is called, it will send an **WM_GETTEXT** message, so it will surely be an internal (safe) call. But if that message is received and the Text property wasn't called, then it might be risky to return the password, so we'll not process that message._

I wrote a "safer" **TextBox** here, just to show you the idea, feel free to write your own or simply improve this one.

```csharp
class ProtectedTextBox : TextBox
{
    // the malicious message, that needs to be handled
    private const int WM_GETTEXT = 0x000D;

    // 'true' if the messages are sent from our program (from Text property)
    // 'false' if they're sent by anything else 
    bool allowAccess { get; set; }

    public override string Text   // overriding Text property
    {
        get
        {
            allowAccess = true;    // allow WM_GETTEXT (because it's an internal call)
            return base.Text;  //this sends the message above in order to retrieve the TextBox's value
        }
        set
        {
            base.Text = value;
        }
    }

    protected override void WndProc(ref Message m)
    {
        if (m.Msg == WM_GETTEXT)  // if the message is WM_GETTEXT 
        { 
            if (allowAccess)  // and it comes from the Text property
            {
                allowAccess = false;   //we temporary remove the access
                base.WndProc(ref m);  //and finally, process the message
            }
        }
        else
            base.WndProc(ref m);
    }
}
```