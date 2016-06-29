---
layout: post
title:  "C# How to Scan a Process' Memory"
date:   2014-01-26 20:02:05 +0300
categories: security
thumbnail: /imgs/thumbnails/memorydump.png
---

## Intro

This article is about how to <u>get the memory dump of a process</u>, by checking _almost_ all memory addresses that can store data. Since C# is quite a high level programming language, I think this is the only method available to do this.

And since someone asked how to <u>search a string in a process' memory</u> - well the easiest way would be to search in this generated memory dump. There are also other methods that imply pointers, offsets and Assembly or injecting some dll in the target application, but...this is C#.

In this tutorial I'll try to output all memory allocated by **Notepad**, I _recommend_ you target processes that don't take too much RAM memory. Notepad allocates about **1-2MB** of memory and the generated dump file has about **38MB** (however, I also include the memory address for each byte and newlines).

Here's a small image that shows the outcome:  
* spaces between chars (empty bytes) are caused by Notepad's usage of Unicode Encoding.

![](http://i43.tinypic.com/yjx2q.png)

## Required Methods

Whenever a process starts, the system allocates enough memory for its heap, stack and regions - however Windows won't allocate an 'entire block' of memory. It tries to allocate any free memory available for the User-Mode - so the allocated memory won't be contiguous. Basically, Windows won't tell us a range of addresses where we can find the program's data.

![](http://i40.tinypic.com/nybn28.png)

So, the remaining solution is to scan almost every possible address (we get this using **GetSystemInfo()**) and check if it belongs to the target process (with **VirtualQueryEx()**): if it does, we read the values from there (**ReadProcessMemory()**).

Methods that will be required (including the ones above):

**GetSystemInfo()**

{% highlight csharp linenos %}
[DllImport("kernel32.dll")]
static extern void GetSystemInfo(out SYSTEM_INFO lpSystemInfo);{% endhighlight %}

Retrieves random information about the system in a structure called **SYSTEM_INFO**. This structure also contains 2 variables: **minimumApplicationAddress** & **maximumApplicationAddress** which store the minimum and the maximum address where the system can allocate memory for User-Mode applications.

**SYSTEM_INFO** looks like this:

{% highlight csharp linenos %}public struct SYSTEM_INFO
{
    public ushort processorArchitecture;
    ushort reserved;
    public uint pageSize;
    public IntPtr minimumApplicationAddress;  // minimum address
    public IntPtr maximumApplicationAddress;  // maximum address
    public IntPtr activeProcessorMask;
    public uint numberOfProcessors;
    public uint processorType;
    public uint allocationGranularity;
    public ushort processorLevel;
    public ushort processorRevision;
}
{% endhighlight %}

&nbsp;

**VirtualQueryEx()**

{% highlight csharp linenos %}
[DllImport("kernel32.dll", SetLastError=true)]
static extern int VirtualQueryEx(IntPtr hProcess, IntPtr lpAddress, out MEMORY_BASIC_INFORMATION lpBuffer, uint dwLength);{% endhighlight %}

    
  This method gets information about a range of memory addresses and returns it into a structure named **MEMORY_BASIC_INFORMATION**. Given a minimum address, we use this to find out if there's a region of memory that's allocated by that program (this way we reduce the search range by directly jumping over memory chunks). Basically this method tells us the range of a memory chunk that starts from the specified address: in order to get to the next memory chunk, we add the length of this region to the current memory address (sum).  
  Requires **PROCESS_QUERY_INFORMATION**.

![](http://i43.tinypic.com/212zarp.png)

**MEMORY_BASIC_INFORMATION** must be defined this way:

{% highlight csharp linenos %}public struct MEMORY_BASIC_INFORMATION
{
    public int BaseAddress;
    public int AllocationBase;
    public int AllocationProtect;
    public int RegionSize;   // size of the region allocated by the program
    public int State;   // check if allocated (MEM_COMMIT)
    public int Protect; // page protection (must be PAGE_READWRITE)
    public int lType;
}
{% endhighlight %}

&nbsp;

**ReadProcessMemory()**

{% highlight csharp linenos %}[DllImport("kernel32.dll")]
public static extern bool ReadProcessMemory(int hProcess, int lpBaseAddress, byte[] lpBuffer, int dwSize, ref int lpNumberOfBytesRead);{% endhighlight %}

Used to read a number of bytes starting from a specific memory address.  
Requires **PROCESS_WM_READ**.

&nbsp;

**OpenProcess()**

{% highlight csharp linenos %}[DllImport("kernel32.dll")]
public static extern IntPtr OpenProcess(int dwDesiredAccess, bool bInheritHandle, int dwProcessId);{% endhighlight %}

Returns a handle to a specific process - the process must be opened with **PROCESS_QUERY_INFORMATION** and **PROCESS_WM_READ**.

## Source Code

Once you understand what happens above, we can move to some code - but since there isn't much more to explain, I'll provide the whole source and cover what's left using comments.

{% highlight csharp linenos %}using System;
using System.Diagnostics;
using System.IO;
using System.Runtime.InteropServices;

namespace MemoryScanner
{
    class Program
    {
        // REQUIRED CONSTS
        const int PROCESS_QUERY_INFORMATION = 0x0400;
        const int MEM_COMMIT = 0x00001000;
        const int PAGE_READWRITE = 0x04;
        const int PROCESS_WM_READ = 0x0010;

        // REQUIRED METHODS
        [DllImport("kernel32.dll")]
        public static extern IntPtr OpenProcess(int dwDesiredAccess, bool bInheritHandle, int dwProcessId);

        [DllImport("kernel32.dll")]
        public static extern bool ReadProcessMemory(int hProcess, int lpBaseAddress, byte[] lpBuffer, int dwSize, ref int lpNumberOfBytesRead);

        [DllImport("kernel32.dll")]
        static extern void GetSystemInfo(out SYSTEM_INFO lpSystemInfo);

        [DllImport("kernel32.dll", SetLastError=true)]
        static extern int VirtualQueryEx(IntPtr hProcess, IntPtr lpAddress, out MEMORY_BASIC_INFORMATION lpBuffer, uint dwLength);

        // REQUIRED STRUCTS
        public struct MEMORY_BASIC_INFORMATION
        {
            public int BaseAddress;
            public int AllocationBase;
            public int AllocationProtect;
            public int RegionSize;
            public int State;
            public int Protect;
            public int lType;
        }

        public struct SYSTEM_INFO
        {
            public ushort processorArchitecture;
            ushort reserved;
            public uint pageSize;
            public IntPtr minimumApplicationAddress;
            public IntPtr maximumApplicationAddress;
            public IntPtr activeProcessorMask;
            public uint numberOfProcessors;
            public uint processorType;
            public uint allocationGranularity;
            public ushort processorLevel;
            public ushort processorRevision;
        }

        // finally...
        public static void Main()
        {
            // getting minimum & maximum address
            SYSTEM_INFO sys_info = new SYSTEM_INFO();
            GetSystemInfo(out sys_info);  

            IntPtr proc_min_address = sys_info.minimumApplicationAddress;
            IntPtr proc_max_address = sys_info.maximumApplicationAddress;

            // saving the values as long ints so I won't have to do a lot of casts later
            long proc_min_address_l = (long)proc_min_address;
            long proc_max_address_l = (long)proc_max_address;

            // notepad better be runnin'
            Process process = Process.GetProcessesByName("notepad")[0];

            // opening the process with desired access level
            IntPtr processHandle = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_WM_READ, false, process.Id);

            StreamWriter sw = new StreamWriter("dump.txt");

            // this will store any information we get from VirtualQueryEx()
            MEMORY_BASIC_INFORMATION mem_basic_info = new MEMORY_BASIC_INFORMATION();

            int bytesRead = 0;  // number of bytes read with ReadProcessMemory

            while (proc_min_address_l < proc_max_address_l)
            {
                // 28 = sizeof(MEMORY_BASIC_INFORMATION)
                VirtualQueryEx(processHandle, proc_min_address, out mem_basic_info, 28);

                // if this memory chunk is accessible
                if (mem_basic_info.Protect == PAGE_READWRITE && mem_basic_info.State == MEM_COMMIT)
                {
                    byte[] buffer = new byte[mem_basic_info.RegionSize];

                    // read everything in the buffer above
                    ReadProcessMemory((int)processHandle, mem_basic_info.BaseAddress, buffer, mem_basic_info.RegionSize, ref bytesRead);

                    // then output this in the file
                    for (int i = 0; i < mem_basic_info.RegionSize; i++)
                        sw.WriteLine("0x{0} : {1}", (mem_basic_info.BaseAddress+i).ToString("X"), (char)buffer[i]);
                }

                // move to the next memory chunk
                proc_min_address_l += mem_basic_info.RegionSize;
                proc_min_address = new IntPtr(proc_min_address_l);
            }
            sw.Close();

            Console.ReadLine();
        }
    }
}
{% endhighlight %}