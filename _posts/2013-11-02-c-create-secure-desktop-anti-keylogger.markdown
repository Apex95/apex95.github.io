---
layout: post
title:  "C# Create Secure Desktop (Anti-Keylogger)"
date:   2013-11-02 20:02:05 +0300
tags: c-sharp keylogging
redirect_from: /security/c-create-secure-desktop-anti-keylogger
image: /imgs/thumbnails/secureDesktop.webp
---

Since the number of **Keyloggers** keeps growing, I decided to publish this little trick hoping that it might be useful for someone. I discovered it when I was looking on how User Account Control/UAC from Windows 7 protects the data - I was 'amazed' by this idea so I tried to make this accessible for any program.

This tutorial will show you how to create a form that can't be tracked by keyloggers.

## 1\. Details

As you probably know, some keyloggers (not all) place hooks like **WH_KEYBOARD_LL** in order to intercept window's messages. Now...why don't we move the applications we want to protect from keyloggers to a new, safe environment?

This is where <u>Secure Desktop</u> becomes useful: it's actually a 2nd desktop, but whatever runs on this desktop can not be 'influenced' by what runs on the original desktop. Basically, the 2 desktops are separated by the kernel, so the applications can't interact: the keylogger that is running on the original desktop will not intercept the messages received by a program which is found on the other desktop.

{% include image.html url="/imgs/posts/c-create-secure-desktop-anti-keylogger/1.png" description="The application will intermediate the communication between the normal desktop and the newly created one" %}

## 2\. Creating a new Desktop

Before we start, here's a _short_ list of the methods we'll need:

*   **CreateDesktop()** - used to actually create the desktop

    ```csharp
    [DllImport("user32.dll")]
    public static extern IntPtr CreateDesktop(string lpszDesktop, IntPtr lpszDevice, IntPtr pDevmode, int dwFlags, uint dwDesiredAccess, IntPtr lpsa);
    ```

*   **SwitchDesktop()** - for switching between the original and the new desktop

    ```csharp
    [DllImport("user32.dll")]
    private static extern bool SwitchDesktop(IntPtr hDesktop);
    ```

*   **CloseDesktop()** - closes the desktop handle

	```csharp
	[DllImport("user32.dll")]
	public static extern bool CloseDesktop(IntPtr handle);
	```

*   **SetThreadDesktop()** - sets the desktop for the calling thread

	```csharp
	[DllImport("user32.dll")]
	public static extern bool SetThreadDesktop(IntPtr hDesktop);
	```

*   **GetThreadDesktop** - gets the desktop defined for the specified thread

	```csharp
	[DllImport("user32.dll")]
	public static extern IntPtr GetThreadDesktop(int dwThreadId);
	```

*   **GetCurrentThreadId()** - gets the current thread's id

	```csharp
	[DllImport("kernel32.dll")]
	public static extern int GetCurrentThreadId();
	```

Basically there will be 2 desktop handles:

*   <u>original desktop's handle</u> = **GetThreadDesktop(GetCurrentThreadId())**
*   <u>new desktop's handle</u> = **CreateDesktop(...)**

Then, you can easily switch between them using **SwitchDesktop(desktopHandle)**.

<u>Important</u>: **SetThreadDesktop()** will **fail** if a window/form was already created on its thread. If on this thread you create a window and then call **SetThreadDesktop()**, it will not run, even if that window was closed. This was quite a setback, I found no way around this so I decided to use an <u>additional thread</u> - this thread will be running on the new desktop and will host the window. The thread will be compromised anyway, we won't be able to change its assigned desktop once that form is created.

We also need to define the desired <u>desktop access</u>, which will be an **enum**:

```csharp
enum DESKTOP_ACCESS : uint
{
    DESKTOP_NONE = 0,
    DESKTOP_READOBJECTS = 0x0001,
    DESKTOP_CREATEWINDOW = 0x0002,
    DESKTOP_CREATEMENU = 0x0004,
    DESKTOP_HOOKCONTROL = 0x0008,
    DESKTOP_JOURNALRECORD = 0x0010,
    DESKTOP_JOURNALPLAYBACK = 0x0020,
    DESKTOP_ENUMERATE = 0x0040,
    DESKTOP_WRITEOBJECTS = 0x0080,
    DESKTOP_SWITCHDESKTOP = 0x0100,

    GENERIC_ALL = (DESKTOP_READOBJECTS | DESKTOP_CREATEWINDOW | DESKTOP_CREATEMENU |
                    DESKTOP_HOOKCONTROL | DESKTOP_JOURNALRECORD | DESKTOP_JOURNALPLAYBACK |
                    DESKTOP_ENUMERATE | DESKTOP_WRITEOBJECTS | DESKTOP_SWITCHDESKTOP),
}
```

However, here we'll use **GENERIC_ALL**.

Ok, this was the 'hardest' part, now we only need to create the program by putting the methods above to good use.

<u>Note:</u> you need to <u>store the original desktop's handle</u>, so you'll be able to switch back to it - otherwise you'll have to log off.

## 3\. Source Code

This is the code I came up with, tried to keep it as simple as possible, so you can freely take what you need or modify it as you want. Anyway, there are some comments that will explain what the code is doing.

// The source code was tested on Windows 7, if you get compilation errors, check if you included these references  
**System.Windows.Forms.dll  
System.Drawing.dll**

```csharp
using System;
using System.Drawing;
using System.Runtime.InteropServices;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace AntiKeylogger
{
    class Program
    {
        [DllImport("user32.dll")]
        public static extern IntPtr CreateDesktop(string lpszDesktop, IntPtr lpszDevice, IntPtr pDevmode, int dwFlags, uint dwDesiredAccess, IntPtr lpsa);

        [DllImport("user32.dll")]
        private static extern bool SwitchDesktop(IntPtr hDesktop);

        [DllImport("user32.dll")]
        public static extern bool CloseDesktop(IntPtr handle);

        [DllImport("user32.dll")]
        public static extern bool SetThreadDesktop(IntPtr hDesktop);

        [DllImport("user32.dll")]
        public static extern IntPtr GetThreadDesktop(int dwThreadId);

        [DllImport("kernel32.dll")]
        public static extern int GetCurrentThreadId();

        enum DESKTOP_ACCESS : uint
        {
            DESKTOP_NONE = 0,
            DESKTOP_READOBJECTS = 0x0001,
            DESKTOP_CREATEWINDOW = 0x0002,
            DESKTOP_CREATEMENU = 0x0004,
            DESKTOP_HOOKCONTROL = 0x0008,
            DESKTOP_JOURNALRECORD = 0x0010,
            DESKTOP_JOURNALPLAYBACK = 0x0020,
            DESKTOP_ENUMERATE = 0x0040,
            DESKTOP_WRITEOBJECTS = 0x0080,
            DESKTOP_SWITCHDESKTOP = 0x0100,

            GENERIC_ALL = (DESKTOP_READOBJECTS | DESKTOP_CREATEWINDOW | DESKTOP_CREATEMENU |
                            DESKTOP_HOOKCONTROL | DESKTOP_JOURNALRECORD | DESKTOP_JOURNALPLAYBACK |
                            DESKTOP_ENUMERATE | DESKTOP_WRITEOBJECTS | DESKTOP_SWITCHDESKTOP),
        }

        static void Main(string[] args)
        {

            // old desktop's handle, obtained by getting the current desktop assigned for this thread
            IntPtr hOldDesktop = GetThreadDesktop(GetCurrentThreadId());

            // new desktop's handle, assigned automatically by CreateDesktop
            IntPtr hNewDesktop = CreateDesktop("RandomDesktopName", IntPtr.Zero, IntPtr.Zero, 0, (uint)DESKTOP_ACCESS.GENERIC_ALL, IntPtr.Zero);

            // switching to the new desktop
            SwitchDesktop(hNewDesktop);     

            // Random login form: used for testing / not required
            string passwd= "";

            // running on a different thread, this way SetThreadDesktop won't fail
            Task.Factory.StartNew(() =>
            {
                // assigning the new desktop to this thread - so the Form will be shown in the new desktop)
                SetThreadDesktop(hNewDesktop);  

                Form loginWnd = new Form();
                TextBox passwordTextBox = new TextBox();

                passwordTextBox.Location = new Point(10, 30);
                passwordTextBox.Width = 250;
                passwordTextBox.Font = new Font("Arial", 20, FontStyle.Regular);

                loginWnd.Controls.Add(passwordTextBox);
                loginWnd.FormClosing += (sender, e) => { passwd = passwordTextBox.Text; };

                Application.Run(loginWnd);

            }).Wait();  // waits for the task to finish
            // end of login form

            // if got here, the form is closed => switch back to the old desktop
            SwitchDesktop(hOldDesktop);    

            // disposing the secure desktop since it's no longer needed
            CloseDesktop(hNewDesktop);

            Console.WriteLine("Password, typed inside secure desktop: " + passwd);
            Console.ReadLine();
        }
    }
}
```

## 4\. Additional notes

**AVG** (and others probably?) may detect this as **Luhe.MalMSIL.A** - it's obviously a <u>false positive</u> since this program causes no harm (check the source code, I'm not coding viruses here!).

## 5\. Proof of concept

I haven't wrote a complete demo for this, since that would require some parts from a keylogger...which I'm not supposed to share.

Anyway, I made a video (watch in HD):

<object height="315" width="420"><param name="movie" value="//www.youtube.com/v/BXjZWiDtlRY?version=3&amp;hl=ro_RO"><param name="allowFullScreen" value="true"><param name="allowscriptaccess" value="always"><embed src="//www.youtube.com/v/BXjZWiDtlRY?version=3&amp;hl=ro_RO" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" height="315" width="420"></object>