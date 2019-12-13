---
layout: post
title:  "C# Text to Speech"
date:   2012-05-15 20:02:05 +0300
categories: tips-and-tricks
thumbnail: /imgs/thumbnails/pcSpeak.jpg
---

**Windows SAPI** is a nice tool that comes with Windows that allows us to transform an input **text into a speech**.

Ok, this is quite simple...takes only 3 lines of code, so not much explanation is needed.

## How to?

Right click on the project's name (in Solution Explorer)->**Add Reference**->**COM** and look for **Microsoft Speech Object Library**, select it then click Ok.

Now include the following line, near the first lines of code (where the namespaces are included):

```csharpusing SpeechLib;```

Double click on the button we created before - this will create a new method, in which we'll add the code that converts text to speech:

```csharpstring helloString = "Hello World";

SpVoice voice = new SpVoice();
voice.Speak(helloString, SpeechVoiceSpeakFlags.SVSFDefault); // tries to spell "Hello World"```