---
layout: post
title:  "C# Get Frames from a GIF"
date:   2014-08-01 20:02:05 +0300
categories: files
thumbnail: /imgs/thumbnails/9gag.png
---

This is a simple method to extract a certain frame (or all of them) from a **GIF**, using **C#**. As always, **.NET** provides all the functions we need, so it _shouldn't_ take more than **12 lines of code**.

## Basic Information

As you know, **GIFs** contain various images (frames) that are displayed one by one after a certain <u>time</u> interval (unlike **TIFFs**, that display all the frames simultaneously in one picture). However we'll be working with the **GIF** format (whose frames are entirely based on the **time dimension**).

In order to get the **number of frames** we'll use **GetFrameCount(FrameDimension.Time)**, which returns an **int**. Note that it requires an argument that specifies the **dimension**.

Next, we have to iterate through each **frame** and then select it using the same dimension and an index (**SelectActiveFrame(FrameDimension.Time, indexOfCurrentFrame)**).

<u>Important:</u> This method modifies the original image, so we'll need to call **Clone()** on this object and cast it as an **Image** before saving it (otherwise we'd just save the GIF - **not** the current frame).

## Example

This small function extracts & returns an **array of frames** (**Image**), from a given picture.

* Recommend executing this in a worker thread, especially when GIFs have many frames.

```csharp
Image[] getFrames(Image originalImg)
{
    int numberOfFrames = originalImg.GetFrameCount(FrameDimension.Time);
    Image[] frames = new Image[numberOfFrames];

    for (int i = 0; i < numberOfFrames; i++)
    {
        originalImg.SelectActiveFrame(FrameDimension.Time, i);
        frames[i] = ((Image)originalImg.Clone());
    }

    return frames;
}
```

It can be called like this:

```csharp
Image[] frames = getFrames(Image.FromFile("random.gif"));
```