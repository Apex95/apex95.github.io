---
layout: post
title:  "C# Inject a Dll into a Process (w/ CreateRemoteThread)"
date:   2014-10-14 20:02:05 +0300
tags: exploit process dll-injection c-sharp
redirect_from: 
    - /miscellaneous/c-inject-a-dll-into-a-process-w-createremotethread
    - /miscellaneous/c-inject-a-dll-into-a-process-w--createremotethread
    - /security/c-inject-a-dll-into-a-process-w-createremotethread
image: /imgs/thumbnails/dllInject.webp
---

Since I've been asked if this is possible - well...you can do **DLL Injection** using **C#** but the injected DLL must be written in a language that doesn't depend on a CLR (**C/C++** would be a good option here, but it's ok to write the injector in **C#**).


##### almost all AV programs detect this as a possible malware simply because this behaviour is specific to some viruses/keygens/etc. - and they prefer to be rather paranoid than ineffective. Even if this technique has a _bad reputation_ it has <u>legit</u> uses like hotpatching & logging - and this is what I'm going to write about.

Fun fact: you can achieve similar results (e.g., memory access) by [hooking and patching a function](https://codingvision.net/security/hot-patching-functions-with-intel-pin) in the original binary (not in C# though).

## Some theory

**DLL Injection** is a technique used to make a running process (executable) load a DLL without requiring a restart (name makes it kind of obvious :p).

It is usually done using 2 programs:

*   an **Injector** (written in any language)
*   a **DLL** (compiled to a native language)

The purpose of the **injector** is to...inject the DLL into the target process.
In order to do so:

1.  get the **handle** of the process (**OpenProcess()**)
2.  obtain the address of this method: **LoadLibraryA()** (from **kernel32.dll**) by using **GetProcAddress()**; we're trying to make the target process call it in order to load our library; DON'T hardcode this address - since Windows Vista came out, it will be different every time.
3.  use **VirtualAllocEx** to allocate a few bytes of memory on the target process
4.  write there the name/path of our library (**WriteProcessMemory()**)
5.  with **CreateRemoteThread()** spawn the **thread** which will run **LoadLibraryA()** with the pointer to the allocated address as an argument (that pointer actually indicates the name of the DLL).

One more thing: when the DLL is loaded, its **DllMain()** method (entry point) will be called with `DLL_PROCESS_ATTACH` as **reason** (`fdwReason`).

## Writing the DLL

For this tutorial I used a dummy DLL which displays a **MessageBox** once it's successfully loaded.

_Note: always return **true** at the end - otherwise some processes will crash when injecting._

I'm using this DLL:

```c
#include<Windows.h>
extern "C" __declspec(dllexport) bool WINAPI DllMain(HINSTANCE hInstDll, DWORD fdwReason, LPVOID lpvReserved)
{
    switch (fdwReason)
    {
        case DLL_PROCESS_ATTACH:
        {
            MessageBox(NULL, "Hello World!", "Dll says:", MB_OK);
	    break;
        }

        case DLL_PROCESS_DETACH:
            break;

        case DLL_THREAD_ATTACH:
            break;

        case DLL_THREAD_DETACH:
            break;
    }
    return true;
}
```

## Writing the Injector

Ok, the fancy part. I kind of explained how all this works in the first part of the tutorial so just remember: get the handle, allocate some memory on the process, write there the name of the DLL and finally, create a thread that will call **LoadLibraryA** and load your DLL.

Also, check the comments in code and refer to the "theory" part of this article whenever you feel the need to.

Here be sourcecode!

```csharp
using System;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Text;

public class BasicInject
{
    [DllImport("kernel32.dll")]
    public static extern IntPtr OpenProcess(int dwDesiredAccess, bool bInheritHandle, int dwProcessId);

    [DllImport("kernel32.dll", CharSet = CharSet.Auto)]
    public static extern IntPtr GetModuleHandle(string lpModuleName);

    [DllImport("kernel32", CharSet = CharSet.Ansi, ExactSpelling = true, SetLastError = true)]
    static extern IntPtr GetProcAddress(IntPtr hModule, string procName);

    [DllImport("kernel32.dll", SetLastError = true, ExactSpelling = true)]
    static extern IntPtr VirtualAllocEx(IntPtr hProcess, IntPtr lpAddress,
        uint dwSize, uint flAllocationType, uint flProtect);

    [DllImport("kernel32.dll", SetLastError = true)]
    static extern bool WriteProcessMemory(IntPtr hProcess, IntPtr lpBaseAddress, byte[] lpBuffer, uint nSize, out UIntPtr lpNumberOfBytesWritten);

    [DllImport("kernel32.dll")]
    static extern IntPtr CreateRemoteThread(IntPtr hProcess,
        IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, IntPtr lpThreadId);

    // privileges
    const int PROCESS_CREATE_THREAD = 0x0002;
    const int PROCESS_QUERY_INFORMATION = 0x0400;
    const int PROCESS_VM_OPERATION = 0x0008;
    const int PROCESS_VM_WRITE = 0x0020;
    const int PROCESS_VM_READ = 0x0010;

    // used for memory allocation
    const uint MEM_COMMIT = 0x00001000;
    const uint MEM_RESERVE = 0x00002000;
    const uint PAGE_READWRITE = 4;

    public static int Main()
    {
        // the target process - I'm using a dummy process for this
        // if you don't have one, open Task Manager and choose wisely
        Process targetProcess = Process.GetProcessesByName("testApp")[0];

        // geting the handle of the process - with required privileges
        IntPtr procHandle = OpenProcess(PROCESS_CREATE_THREAD | PROCESS_QUERY_INFORMATION | PROCESS_VM_OPERATION | PROCESS_VM_WRITE | PROCESS_VM_READ, false, targetProcess.Id);

        // searching for the address of LoadLibraryA and storing it in a pointer
        IntPtr loadLibraryAddr = GetProcAddress(GetModuleHandle("kernel32.dll"), "LoadLibraryA");

        // name of the dll we want to inject
        string dllName = "test.dll";

        // alocating some memory on the target process - enough to store the name of the dll
        // and storing its address in a pointer
        IntPtr allocMemAddress = VirtualAllocEx(procHandle, IntPtr.Zero, (uint)((dllName.Length + 1) * Marshal.SizeOf(typeof(char))), MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);

        // writing the name of the dll there
        UIntPtr bytesWritten;
        WriteProcessMemory(procHandle, allocMemAddress, Encoding.Default.GetBytes(dllName), (uint)((dllName.Length + 1) * Marshal.SizeOf(typeof(char))), out bytesWritten);

        // creating a thread that will call LoadLibraryA with allocMemAddress as argument
        CreateRemoteThread(procHandle, IntPtr.Zero, 0, loadLibraryAddr, allocMemAddress, 0, IntPtr.Zero);

        return 0;
    }
}
```
