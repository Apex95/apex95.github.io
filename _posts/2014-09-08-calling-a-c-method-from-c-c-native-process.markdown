---
layout: post
title:  "Call a C# Method from C/C++ (native process)"
date:   2014-09-08 20:02:05 +0300
categories: tips-and-tricks
thumbnail: /imgs/thumbnails/runtime-host.png
---

So...I received a challenge from a _friend_ (lost a bet...) regarding how to load a **managed (C#) dll** in a **native (C++) process** by using the **Common Language Runtime (CLR)**. After a few tries, I came up with this...it seems to work with **.Net Framework 4.0**.

The trick was to host the **CLR** in the C++ **process** and then using it to load the managed dll.

_// This tutorial contains C/C++; you have been warned._

## 1) Making a C# Dll...

This is the only part where we'll be using C# - so enjoy it as much as you can! We'll make a dummy dll, that will be later loaded into a native application.

I came up with this _sophisticated_ code (feel free to improvise), but the function that you want to call must **return** something (preferably **int**).

{% highlight csharp linenos %}using System.Windows.Forms;

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
}{% endhighlight %}

## 2) Hosting the CLR in a native process

First things first, you'll need to include these 2 lines:

{% highlight csharp linenos %}#include <metahost.h>
#pragma comment(lib, "mscoree.lib")
{% endhighlight %}

We have to call **CLRCreateInstance()** in order to gain access to **ICLRMetaHost**. This interface contains various methods that will provide general information about .NET Framework.

From there, it is required to focus on one version of the framework (in this tutorial I'm working with **v4.0.30319**) - calling **ICLRMetaHost::GetRuntime()** will return a pointer to another interface (**ICLRRuntimeInfo**), which contains...more methods. (this is the upgraded version of **ICorRuntimeHost**).

The next step is calling **ICLRRuntimeInfo::GetInterface** which loads the **CLR** into the current process and allows us to use some runtime pointers.

Finally, start the runtime host (if it's not running already) using **ICLRRuntimeHost::Start()**.

## 3) Calling a method from the Managed Dll

This is done via the runtime host that we struggled to load earlier.  
Using **ICLRRuntimeHost::ExecuteInDefaultAppDomain()** with a bunch of arguments does the job pretty well.

The method looks like this:

{% highlight c linenos %}HRESULT ExecuteInDefaultAppDomain (
    [in] LPCWSTR pwzAssemblyPath,  // absolute path to the managed dll (not relative!)
    [in] LPCWSTR pwzTypeName,  // name of the class for example: dllNamespace.dllClass
    [in] LPCWSTR pwzMethodName,  // name of the method 
    [in] LPCWSTR pwzArgument,   // argument(s)
    [out] DWORD *pReturnValue   // this is what the method returns
);{% endhighlight %}

## SourceCode

This is the whole sourcecode:

{% highlight c linenos %}#include <metahost.h>
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
{% endhighlight %}

<u>Short advice:</u> always check that each **HRESULT** returned is equivalent to **S_OK**.

**P.S.:** due to some problems with my compiler, I couldn't test this code properly - last time, it worked pretty well...hope it still does so.