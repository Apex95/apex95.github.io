---
layout: post
title:  "C# Make a Critical Process (BSoD if Killed)"
date:   2013-10-07 20:02:05 +0300
categories: tips-and-tricks
thumbnail: /imgs/thumbnails/bsod.png
---

A **critical** process is a type of process that Windows requires to be running - **csrss.exe** is an example of such process. Whenever a process like this finishes its execution (or it's terminated) Windows will respond with an authentic **Blue Screen of Death**.

Theoretically, you can BSoD yourself whenever you want :)

##### The complete code is available at the bottom of the page.

{% include image.html url="/imgs/posts/c-make-a-critical-process-bsod-if-killed/1.png" description="We all love it" %}

## Technical Details

Setting a process as a critical process is done by PInvoking **NtSetInformationProcess**, from **ntdll.dll** (it requires _Debug Privileges_). More information about this method can be found below, in the coding section.

Now, whenever a critical process is terminated, the Kernel will throw up a **BSoD**, with the following bug check:

_*** STOP: 0x000000F4_

**0x000000F4** is the value for **CRITICAL_OBJECT_TERMINATION**. From now, I think it starts making sense, isn't it?

## Coding Part

First things first, import **NtSetInformationProcess** via PInvoke, with the following code:

{% highlight csharp linenos %}[DllImport("ntdll.dll", SetLastError = true)]
private static extern int NtSetInformationProcess(IntPtr hProcess, int processInformationClass, ref int processInformation, int processInformationLength);
{% endhighlight %}

<u>Method Details</u>:

*   **IntPtr** hProcess = the process' handle
*   **int processInformationClass** = it's like a 'flag' - we supply this value **0x1D (BreakOnTermination)**
*   **ref int processInformation** = value for that flag (1 = enabled / 0 = disabled), in this case, 1 means that it's a critical process
*   **int processInformationLength** = is the value supplied for the flag, which in our case is the size of an integer

Before calling this method, you also need _Debug Privileges_ - these privileges also require _Administrator Privileges_.

In order to obtain them, you must call this method:

{% highlight csharp linenos %}Process.EnterDebugMode();{% endhighlight %}

Now you can safely call **NtSetInformationProcess()** and since that wouldn't require additional explanation, I'll provide the complete code:

{% highlight csharp linenos %}using System;
using System.Diagnostics;
using System.Runtime.InteropServices;

public class CriticalProcess
{
    [DllImport("ntdll.dll", SetLastError = true)]
    private static extern int NtSetInformationProcess(IntPtr hProcess, int processInformationClass, ref int processInformation, int processInformationLength);

    static void Main(string[] args)
    {
        int isCritical = 1;  // we want this to be a Critical Process
        int BreakOnTermination = 0x1D;  // value for BreakOnTermination (flag)

        Process.EnterDebugMode();  //acquire Debug Privileges

        // setting the BreakOnTermination = 1 for the current process
        NtSetInformationProcess(Process.GetCurrentProcess().Handle, BreakOnTermination, ref isCritical, sizeof(int));
    }
}{% endhighlight %}
