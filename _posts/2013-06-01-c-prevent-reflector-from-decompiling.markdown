---
layout: post
title:  "C# Prevent Reflector from Decompiling"
date:   2013-06-01 20:02:05 +0300
categories: security
thumbnail: /imgs/thumbnails/reflectorIcon.gif
---

This is a simple way to protect your application from any so-called "cracker", without involving obfuscation. Remember that this works only against **Reflector** (tested on: **v7.5.2.1**), any other decompilers are "immune".

## Technical stuff...

The main idea is this: you change the value of **NumberOfRvaAndSizes** from the optional header of your application (**IMAGE_OPTIONAL_HEADER**).

Note that **NumberOfRvaAndSizes** is usually **16** (**0x10**) in any PE, however we can change that value to any number between: **0x6** and **0x9**. Values outside this range will crash the application.

This value holds the number of data directories (**IMAGE_DATA_DIRECTORY**) - Reflector's problem is that it always expects the value to be **16** even though the application doesn't require that.

## Modifying the optional header

On 32-bit systems, the value of **NumberOfRvaAndSizes** is always stored on the **244th byte** (**0x00000F4**), so you can change that value with a simple Hex Editor.

It will look like this:  
![Hex Editor View](http://oi40.tinypic.com/1sgsr7.jpg)

After you change that value with one between **6** and **9**, save the application and you're done.  
If you try to open this in **Reflector** it should return an error message:

"<font color="red" size="3">Invalid number of data directories in NT header.</font>"

## Cons

- might not work on 64 bit systems.  
- not a "global" fix, other decompilers can still get the source code.  
- still a weak method, any skilled cracker would notice that.