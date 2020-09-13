---
layout: post
title:  "Call a C# Method from C/C++ (native process)"
date:   2014-09-08 20:02:05 +0300
tags: c c-sharp clr
redirect_from: /tips-and-tricks/calling-a-c-method-from-c-c-native-process
image: /imgs/thumbnails/runtime-host.webp
---

This article presents a method of loading a **managed (C#) dll** in a **native (C++) process** by using the **Common Language Runtime (CLR)**. Basically, it refers to calling a **C# method** from **C/C++** and enables calling managed code from native applications. This method was tested on the **.Net Framework 4.0**.

The trick consists in creating and hosting a **CLR** instance in the C++ process and then using it to load a managed dll.


## Hosting the CLR in a Native Process

The following dependencies will be required

```c
#include <metahost.h>
#pragma comment(lib, "mscoree.lib")
```

`CLRCreateInstance()` needs to be called in order to gain access to the `ICLRMetaHost` interface. This interface contains various methods that will provide general information about the current .NET Framework runtime.

From there, it is required to focus on one version of the framework (I'm working with **v4.0.30319**) - calling `ICLRMetaHost::GetRuntime()` will return a pointer to another interface (`ICLRRuntimeInfo`), which contains... more methods. (this is the upgraded version of `ICorRuntimeHost`).

The next step is calling `ICLRRuntimeInfo::GetInterface()` which returns an instance of the `ICLRRuntimeHost`. The `ICLRRuntimeHost` needs to be started (`ICLRRuntimeHost::Start()`) in the current native process and can be used to execute managed code through `ICLRRuntimeHost::ExecuteInDefaultAppDomain()`. The aforementioned method has the following prototype:

```c
HRESULT ExecuteInDefaultAppDomain (
    [in] LPCWSTR pwzAssemblyPath,  // absolute path to the managed dll (not relative!)
    [in] LPCWSTR pwzTypeName,  // name of the class for example: dllNamespace.dllClass
    [in] LPCWSTR pwzMethodName,  // name of the method 
    [in] LPCWSTR pwzArgument,   // argument(s)
    [out] DWORD *pReturnValue   // this is what the method returns
);
```

It is advised to always check if each call of the above methods returns a `S_OK`.

## Example: Dummy Managed DLL

This part implements a dummy managed DLL that will be attached to the native application. In this version, I'm implementing a method which displays a `MessageBox` that contains a message (`string`) given as parameter; the returned `int` will also be available in the native code. This method will be called by the C process. 


```csharp
using System.Windows.Forms;

namespace dllNamespace
{
    public class dllClass
    {
        public static int ShowMsg(string msg)
        {
            MessageBox.Show(msg);
            return 0;
        }
    }
}
```

## Example: Native Application

I've implemented a loader for the previously presented DLL.

```c
#include <metahost.h>
#pragma comment(lib, "mscoree.lib")

int main()
{
    ICLRMetaHost* metaHost = NULL;
    ICLRRuntimeInfo* runtimeInfo = NULL;
    ICLRRuntimeHost* runtimeHost = NULL;

    if (CLRCreateInstance(CLSID_CLRMetaHost, IID_ICLRMetaHost, (LPVOID*)&metaHost) == S_OK)
        if (metaHost->GetRuntime(L"v4.0.30319", IID_ICLRRuntimeInfo, (LPVOID*)&runtimeInfo) == S_OK)
            if (runtimeInfo->GetInterface(CLSID_CLRRuntimeHost, IID_ICLRRuntimeHost, (LPVOID*)&runtimeHost) == S_OK)
                if (runtimeHost->Start() == S_OK)
	            {		
                    DWORD pReturnValue;
                    runtimeHost->ExecuteInDefaultAppDomain(L"C:\\random.dll", L"dllNamespace.dllClass", L"ShowMsg", L"It works!!", &pReturnValue);

                    runtimeInfo->Release();
                    metaHost->Release();
                    runtimeHost->Release();
                }
    return 0;
} 
```



**P.S.:** due to some problems with my compiler, I couldn't test this code properly - last time, it worked pretty well...hope it still does so.