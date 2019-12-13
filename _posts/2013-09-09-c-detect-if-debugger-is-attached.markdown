---
layout: post
title:  "C# Detect if Debugger is Attached"
date:   2013-09-09 20:02:05 +0300
categories: security
thumbnail: /imgs/thumbnails/detectDebugger.png
---

This method is used to detect if a running process has a **debugger** attached to it. It involves using **CheckRemoteDebuggerPresent**, imported from **kernel32.dll** via PInvoke.

It's a neat way to add a little bit of protection to your program, but don't expect too much since .NET is far from being safe.

* tested on <u>Visual Studio's Debugger</u> & <u>OllyDbg</u>

## How to...

First, include the following lines in your program:

```csharp
[DllImport("kernel32.dll", SetLastError = true, ExactSpelling = true)]
static extern bool CheckRemoteDebuggerPresent(IntPtr hProcess, ref bool isDebuggerPresent);
```

Now, this method is pretty simple to use since it takes only 2 arguments:

1.  **IntPtr hProcess** = the target process' handle
2.  **ref bool isDebuggerPresent** = pointer that indicates the result

Since it's pretty straightforward, I guess there's no need for additional details - in any case you can find the complete source code below:

```csharp
using System;
using System.Diagnostics;
using System.Runtime.InteropServices;

public class DetectDebugger
{
    [DllImport("kernel32.dll", SetLastError = true, ExactSpelling = true)]
    static extern bool CheckRemoteDebuggerPresent(IntPtr hProcess, ref bool isDebuggerPresent);

    public static void Main()
    {
        bool isDebuggerPresent = false;
        CheckRemoteDebuggerPresent(Process.GetCurrentProcess().Handle, ref isDebuggerPresent);

        Console.WriteLine("Debugger Attached: " + isDebuggerPresent);
        Console.ReadLine();
    }
}
```

## Debugger.IsAttached ?

In order to avoid any confusion about **Debugger.IsAttached** and **CheckRemoteDebuggerPresent** - sorry I didn't mention this earlier in the article:

*   **IsDebuggerPresent** = works for any running process and detects native debuggers too.
*   **Debugger.IsAttached** = works only for the current process and detects only managed debuggers. As an example, OllyDbg **won't** be detected by this.