---
layout: post
title:  "Hot Patching C/C++ Functions with Intel Pin"
date:   2019-08-21 00:45:05 +0300
categories: security
thumbnail: /imgs/thumbnails/patch.png
---

5 years ago, I said in one of my articles that I shall return, one day, with a method of **hot patching** functions inside live processes; So... I guess this is that day.

What we'll try to achieve here is to **replace**, from outside, a **function** inside a **running executable**, without stopping/freezing the process (or crashing it...).

In my opinion, applying **hot patches** is quite a daunting task, if implemented **from scratch**, since:

* it requires access to a different process' memory (most operating systems are fans of **process isolation**)
* has software compatibility constraints (**Windows** binaries vs **Linux** binaries)
* has architecture compatibility contrains (**32bit** vs **64bit**)
* it implies working with machine code and brings certain issues to the table
* it has only a didactic purpose - probably no one would actually use a 'from-scratch' method since there are tools that do this better

Considering these, I guess it is better to use something that was actually written for this task and not coding something manually.
Therefore, we'll be looking at a way to do this with [Intel Pin](https://software.intel.com/en-us/articles/pin-a-dynamic-binary-instrumentation-tool). I stumbled upon this tool while working at a completely different project but it seems to be quite versatile. Basically, it is described as a **Dynamic Binary Instrumentation Tool**, however we'll be using it to facilitate the procedure of writing code to another's process memory.





## Initial Preparations


Start by [downloading Intel Pin](https://software.intel.com/en-us/articles/pin-a-binary-instrumentation-tool-downloads) and extract it somewhere in your workspace. 


_Disclaimer: I'm doing this tutorial on **Ubuntu x86_64**. You might see some bash._


I'll use the following **dummy** C program as a target for the **hot patch**:

{% highlight c linenos %}
#include<stdio.h>

// TODO: hot patch this method
void read_input()
{
    printf("Tell me your name:\n");
    
    char name[11];
    scanf("%s", name); // this looks bad
    
    printf("Hello, %s!\n\n", name);
}

int main()
{
    // not gonna end too soon
    while(1 == 1)
        read_input();
    
    return 0;
}
{% endhighlight %}


Some of you probably noticed that the `read_input()` function is not very well written since it's reading inputs using `scanf("%s", name);` and thus enabling an attacker to hijack the program's execution using **buffer overflow**.


{% include image.html url="/imgs/posts/hot-patching-functions-with-intel-pin/buffer_overflow.png" description="Scanf() reading exceeds the limits of the allocated buffer" %}



## Project's Structure

**Intel Pin** works by performing actions, indicated in **tools**, to targeted **binaries** or **processes**. As an example, you may have a tool that says _'increase a counter each time you find a RET instruction'_ that you can attach to an executable and get the value of the counter at a certain time.

It offers a directory with examples of **tools** which can be found at: **pin/source/tools/**. In order to avoid updating makefile dependencies, we'll work here so continue by creating a new directory (mine's named **Hotpatch**) - this is where the coding happens.

Also, copy a **makefile** to your new directory, if you don't feel like writing one:

{% highlight bash %}
cp ../SimpleExamples/makefile .
{% endhighlight %}

And use the following as your **makefile.rules** file:

{% highlight make linenos %}
TEST_TOOL_ROOTS := hotpatch # for hotpatch.cpp
SANITY_SUBSET := $(TEST_TOOL_ROOTS) $(TEST_ROOTS)
{% endhighlight %}

Finally, create a file named **hotpatch.cpp** with some dummy code and run the **make** command. If everything works fine, you should end up with something like this...

{% include image.html url="/imgs/posts/hot-patching-functions-with-intel-pin/directory_structure.png" description="Directory structure for the Hotpatch tool" %}


## Coding the Hot Patcher


The whole idea revolves around registering a **callback** which is called everytime the binary loads an image (see `IMG_AddInstrumentFunction()`). Since the method is defined in the running program, we're interested when the process loads its own image. In this callback, we look for the method that we want to **hot patch** (replace) - in my example, it's `read_input()`.

You can list the functions that are present in a binary using:
{% highlight bash %}
nm targeted_binary_name
{% endhighlight %}

The process of replacing a function (`RTN_ReplaceSignatureProbed()`) is based on **probes** - as you can tell by the name, which, according to **Intel**'s claims, ensure less overhead and are less intrusive. Under the hood, **Intel Pin** will overwrite the original function's instructions with a `JMP` that points to the replacement function. It is up to you to call the original function, if needed.

Without further ado, the code I ended up with:

{% highlight cpp linenos %}
#include "pin.H"
#include <iostream>
#include <stdio.h>


char target_routine_name[] = "read_input";


// replacement routine's code (i.e. patched read_input)
void read_input_patched(void *original_routine_ptr, int *return_address)
{
    printf("Tell me your name:\n");
    
    // 5 stars stdin reading method
    char name[12] = {0}, c;
    fgets(name, sizeof(name), stdin);
    name[strcspn(name, "\r\n")] = 0;

    // discard rest of the data from stdin
    while((c = getchar()) != '\n' && c != EOF);

    printf("Hello, %s!\n\n", name);
}


void loaded_image_callback(IMG current_image, void *v)
{
    // look for the routine in the loaded image
    RTN current_routine = RTN_FindByName(current_image, target_routine_name);
    

    // stop if the routine was not found in this image
    if (!RTN_Valid(current_routine))
        return;

    // skip routines which are unsafe for replacement
    if (!RTN_IsSafeForProbedReplacement(current_routine))
    {
        std::cerr << "Skipping unsafe routine " << target_routine_name << " in image " << IMG_Name(current_image) << std::endl;
        return;
    }

    // replacement routine's prototype: returns void, default calling standard, name, takes no arugments 
    PROTO replacement_prototype = PROTO_Allocate(PIN_PARG(void), CALLINGSTD_DEFAULT, target_routine_name, PIN_PARG_END());

    // replaces the original routine with a jump to the new one 
    RTN_ReplaceSignatureProbed(current_routine, 
                               AFUNPTR(read_input_patched), 
                               IARG_PROTOTYPE, 
                               replacement_prototype,
                               IARG_ORIG_FUNCPTR,
                               IARG_FUNCARG_ENTRYPOINT_VALUE, 0,
                               IARG_RETURN_IP,
                               IARG_END);

    PROTO_Free(replacement_prototype);

    std::cout << "Successfully replaced " << target_routine_name << " from image " << IMG_Name(current_image) << std::endl;
}


int main(int argc, char *argv[])
{
    PIN_InitSymbols();

    if (PIN_Init(argc, argv))
    {
        std::cerr << "Failed to initialize PIN." << std::endl; 
        exit(EXIT_FAILURE);
    }

    // registers a callback for the "load image" action
    IMG_AddInstrumentFunction(loaded_image_callback, 0);
    
    // runs the program in probe mode
    PIN_StartProgramProbed();
    
    return EXIT_SUCCESS;
}
{% endhighlight %}


After running **make**, use a command like the following one to attach **Intel Pin** to a running instance of the targeted process.

{% highlight bash %}
sudo ../../../pin -pid $(pidof targeted_binary_name) -t obj-intel64/hotpatch.so
{% endhighlight %}


## Results and Conclusions

Aaand it seems to be working:
{% include image.html url="/imgs/posts/hot-patching-functions-with-intel-pin/hot_patched_process.png" description="Testing the Hot Patched version against Buffer Overflow" %}


To conclude, I'm pretty sure **Intel Pin** is capable of more complex stuff than what I'm presenting here - which I believe is examples-level (actually it's inspired by an example). To me, it seems rather strange that it is not a more popular tool - and no, I'm not paid by Intel to endorse it.

However, I hope this article manages to provide support and solutions/ideas to those who are looking at **hot patching** methods and who, like me, never heard of **Intel Pin** before. 

<a href="https://www.codeproject.com" rel="tag" style="display:none">CodeProject</a>
