---
layout: post
title:  "XNA Disable Profile check"
date:   2012-05-17 20:02:05 +0300
categories: xna
thumbnail: /imgs/thumbnails/fbdeprofiler.png
---

**HiDef** is one of the 2 profiles available for developing games in XNA. But...this profile requires a **direct3d/D3D** compatible video card. It apparently checks for **DirectX10** compatibility.  
XNA will check this before compiling/running the project and will throw an error if the video card doesn't meet the requirements

{% include image.html url="/imgs/posts/xna-disable-profile-check/1.png" description="Error thrown whenever a HiDef profile is used with an incompatible video card" %}


## How to solve this ?

The solution is this library **fbDeprofiler.dll** - or another video card. (both work :D).

**fbDeprofiler** is a small application which allows us to bypass the profile checking. So, even if the video card doesn't accept **direct3d/D3D**, the game will run, but unexpected errors may appear anytime - this is not an official fix.

## Adding fbDeprofiler to your project

**1.** You can download it from here: [fbDeprofiler](http://www.2shared.com/file/Ytbepnqt/fbDeprofiler.html "Download fbdeprofiler")

**2.** After downloading, unrar the file and copy **fbDeprofiler.dll** in the directory where the game's source code is found.

**3.** Open your project in Visual Studio, go to **Solution Explorer**, right click on the project's name -> **Add Reference** -> **Browse** and select **fbDeprofiler.dll**.

**4.** Finally, add in the game's contructor (**public Game1()**) the following line:

{% highlight csharp linenos %}fbDeprofiler.DeProfiler.Run();{% endhighlight %}

Now your game will run in **Hidef profile** on any computer with any video card so you don't have to worry anymore about the requirements.

## Update (for Steam users):

I noticed this thread gets a lot of attention from SteamPowered forums. If you get this error it means your video card doesn't meet the requirements for HiDef profile - check for DirectX10 compatibility. Not really a problem with the game, it's just the framework that asks for special stuff.