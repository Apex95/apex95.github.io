---
layout: post
title:  "C# Custom MSBuild Logger"
date:   2012-10-05 20:02:05 +0300
categories: tips-and-tricks
image: /imgs/thumbnails/buildlogger.webp
---

Here's a short trick about how to make a **custom MSBuild Logger**. It's always a good idea to use MSBuild with your own logger (and not the original one) because it provides easier access to the output log. So, I'll show here how to do it.

Make sure you have those namespaces included before starting:

```csharp
using Microsoft.Build.Framework;
using Microsoft.Build.Utilities;
```

First create a new class, that will be your **custom logger**, that class must inherit from the original **Logger**. Basically we create a new logger by modifying the one provided by .NET - so you won't have to create one from zero.

What you might need to know is the way it works: the logger is based on multiple events, and if an event is fired, the corresponding method (eventhandler) is called. In the **custom logger** we'll create our **own eventhandlers**.  

## Code for a custom logger

```csharp
class customLogger : Logger  //customLogger inherits from original Logger
{
        //here I override the Initialize method in order to change the eventhandlers
        public override void Initialize(IEventSource eventSource) 
        {
            eventSource.BuildStarted += new BuildStartedEventHandler(eventSource_BuildStarted);
            eventSource.WarningRaised += new BuildWarningEventHandler(eventSource_WarningRaised);
            eventSource.ErrorRaised += new BuildErrorEventHandler(eventSource_ErrorRaised);
            eventSource.BuildFinished += new BuildFinishedEventHandler(eventSource_BuildFinished);

            //^there are more eventhandlers available - I added only a few
        }

        //triggered when build started
        private void eventSource_BuildStarted(Object sender, BuildStartedEventArgs e)
        {
            Console.WriteLine(e.Message); 
        }

        //triggered when a warning is encountered
        private void eventSource_WarningRaised(object sender, BuildWarningEventArgs e)
        {
            Console.WriteLine("Warning at: " + e.LineNumber+ "," + e.ColumnNumber + " - " + e.Message);
        }

        //triggered when an error is encountered
        private void eventSource_ErrorRaised(Object sender, BuildErrorEventArgs e)
        {
            Console.WriteLine("Error at: " + e.LineNumber+ "," + e.ColumnNumber + " - " + e.Message);
        }

        //triggered when the compiling process is over
        private void eventSource_BuildFinished(object sender, BuildFinishedEventArgs e)
        {
            Console.WriteLine("Result: " + e.Message);
        }
}
```

## How to use it?

You can use it the same way you use the **original logger**:

```csharp
Engine buildEngine = new Engine();
customLogger myCustomLogger = new customLogger();
buildEngine.RegisterLogger(myCustomLogger); //attaching the custom logger to the Engine
```