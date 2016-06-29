---
layout: post
title:  "C# Load dll at Runtime"
date:   2012-06-23 20:02:05 +0300
categories: miscellaneous
thumbnail: /imgs/thumbnails/libraryRuntime.png
---

This is a method used to import a **dll** during the program's execution (at the **runtime**) without adding the actual library as a reference.

Obviously, you will need:  
- A DLL made in C# - only a function and a class  
- An executable - preferably a **Console project**

In this tutorial I work with my own examples, I recommend using them too because it makes everything easier to understand.

## 1\. The Dll / library

Shall consist of a simple class that contains a function which performs the sum of two variables (a and b) passed as parameters.

{% highlight csharp linenos %}using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace testdll
{
    public class Class1
    {
        public int sum(int a, int b)
        {
            return a + b;
        }
    }
} {% endhighlight %}

What you should know:  
- the **Type** of the dll is written as this: **namespace.class**. Therefore our dll will have the following type: **testdll.Class1**.

## 2\. Main Program

Start by copying the library we just made in the main program's folder. (where the executable is found).  
Loading the DLL can be done using the following code:

{% highlight csharp linenos %}Assembly assembly = Assembly.LoadFrom ("testdll.dll");
Type type = assembly.GetType("testdll.Class1"); 
object instance= Activator.CreateInstance(type); //creates an instance of that class {% endhighlight %}

- **type** contains all the information about our program (variables, functions, and many others)  
- **instance** makes a connection between our library/class and the main program - we use this to call the method from the dll.

Next we import the method **sum** in a **MethodInfo Array**, and call it using **Invoke(instance, arguments_array)** and store the result.

{% highlight csharp linenos %}MethodInfo[] methods = type.GetMethods() //takes all methods found in the dll in this array

//Having only one method in the dll, we simply call  the first element
object result = methods[0].Invoke(instance, new object [] {5, 3}) 

//arguments passed to  'sum' are 5 and 3  -> sum(5, 3)
//'result' will store the value returned (8);
{% endhighlight %}

Finally, you get something like this:

{% highlight csharp linenos %}using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Reflection;

namespace test
{
    class Program
    {
        static void Main (string[] args)
        {
            Assembly myassembly = Assembly.LoadFrom("testdll.dll");
            Type type = myassembly.GetType("testdll.Class1");

            object instance = Activator.Createinstance(type);

            MethodInfo[] methods = type.GetMethods();
            object res = methods[0].Invoke(instance, new object[] {5, 3});

            Console.WriteLine(res.ToString());
            Console.ReadLine();
        }
    }
}
{% endhighlight %}