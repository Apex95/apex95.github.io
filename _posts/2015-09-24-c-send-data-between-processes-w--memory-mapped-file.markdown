---
layout: post
title:  "C# Send Data Between Processes (w/ Memory Mapped File)"
date:   2015-09-24 20:02:05 +0300
categories: tips-and-tricks
thumbnail: /imgs/thumbnails/mmf.jpeg
---

If you're reading this right now you're probably developing some application that has 2 or more processes and you want those processes to share some data with each other.

There are multiple ways to **pass data between processes** (**IPC**), each one being better in specific situations. This article will cover one method: using **Memory Mapped Files** (or **mmf**).

## Advantages of Memory Mapped Files

The main advantage of this method is that data doesn't need to be duplicated and sent to another process - it's just shared (so you're actually saving some memory and cpu cycles).

Basically, a **memory mapped file** is a space allocated on the **user-mode** portion of memory which is then made 'public' by the **kernel**, so other processes can access that region too - there's no actual file on your disk. Each process can read whatever it's stored in there; reading is fine, but when writing, try having a different **offset** for each process so you won't run into the problem of having 2 processes writing on the same address.

To conclude, it is a good idea to use **memory mapped files** when:

*   you need to pass large amounts of data
*   some processes need to access shared data repeatedly
*   your application has _a lot_ of processes

## Including non-nullable types

**1:**  
While trying to implement this, I noticed that you can't use **MemoryMappedViewAccessor** to read/write anything that isn't a **non-nullable type** (**string**, **class** etc.), you get this error:

<span style="color:red;">_The type must be a non-nullable value type in order to use it as parameter 'T' in the generic type or method 'System.IO.UnmanagedMemoryAccessor.Write<t>(long, ref T)'</t>_</span>

If you try to include something like a **string** (variable size) inside a **struct** and then pass that to the **MemoryMappedViewAccessor**, this error pops up:

<span style="color:red;">_The specified Type must be a struct containing no references._</span>

In order to avoid these, we'll use **MemoryMappedViewStream** which does the same thing, but this one takes as argument a **byte[]**. So we can take an **object** and **serialize** it to a byte array (w/ **BinaryFormatter**), write it in the memory, and when needed, read it again and **deserialize** it. Using this method you're no longer limited to **non-nullable** types.

**TL;DR:**  
goto 1;

## Implementing this

To make this implementation...different...let's also include an example: we have **2** processes (**Proc1** and **Proc2**) and we want to send a **Message** object that contains 2 **strings** from **Proc1** to **Proc2**.

Btw, the class **Message** looks like this:

{% highlight csharp linenos %}[Serializable]  // mandatory
class Message
{
    public string title; 
    public string content;
}
{% endhighlight %}

**Proc1** will create an instance of **Message** and write it in the shared memory:

{% highlight csharp linenos %}static void Main(string[] args)
{
    const int MMF_MAX_SIZE = 1024;  // allocated memory for this memory mapped file (bytes)
    const int MMF_VIEW_SIZE = 1024; // how many bytes of the allocated memory can this process access

    // creates the memory mapped file which allows 'Reading' and 'Writing'
    MemoryMappedFile mmf = MemoryMappedFile.CreateOrOpen("mmf1", MMF_MAX_SIZE, MemoryMappedFileAccess.ReadWrite);

    // creates a stream for this process, which allows it to write data from offset 0 to 1024 (whole memory)
    MemoryMappedViewStream mmvStream = mmf.CreateViewStream(0, MMF_VIEW_SIZE);

    // this is what we want to write to the memory mapped file
    Message message1 = new Message();
    message1.title = "test";
    message1.content = "hello world";

    // serialize the variable 'message1' and write it to the memory mapped file
    BinaryFormatter formatter = new BinaryFormatter();
    formatter.Serialize(mmvStream, message1);
    mmvStream.Seek(0, SeekOrigin.Begin); // sets the current position back to the beginning of the stream

    // the memory mapped file lives as long as this process is running
    while(true);
}{% endhighlight %}

**Proc2** will have to read the **Message** that **Proc1** wrote. So it will look like this:

{% highlight csharp linenos %}static void Main(string[] args)
{
    const int MMF_MAX_SIZE = 1024;  // allocated memory for this memory mapped file (bytes)
    const int MMF_VIEW_SIZE = 1024; // how many bytes of the allocated memory can this process access

    // creates the memory mapped file
    MemoryMappedFile mmf = MemoryMappedFile.OpenExisting("mmf1");
    MemoryMappedViewStream mmvStream = mmf.CreateViewStream(0, MMF_VIEW_SIZE); // stream used to read data

    BinaryFormatter formatter = new BinaryFormatter();

    // needed for deserialization
    byte[] buffer = new byte[MMF_VIEW_SIZE];

    Message message1;

    // reads every second what's in the shared memory
    while (mmvStream.CanRead)
    {
        // stores everything into this buffer
        mmvStream.Read(buffer, 0, MMF_VIEW_SIZE);

        // deserializes the buffer & prints the message
        message1 = (Message)formatter.Deserialize(new MemoryStream(buffer));
        Console.WriteLine(message1.title + "\n" + message1.content + "\n");

        System.Threading.Thread.Sleep(1000);
    }
}{% endhighlight %}

## The end

That's all...comments in the code should explain almost everything that needs to be explained. I know there are many tutorials related to this subject on the internet but most of them handle only the simple example with a structure containing ints - aka the example on msdn.