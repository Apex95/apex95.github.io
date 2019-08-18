---
layout: post
title:  "C# Perceptron Tutorial"
date:   2012-09-16 20:02:05 +0300
categories: miscellaneous
thumbnail: /imgs/thumbnails/perceptron.png
---

## Intro

The **Perceptron** is basically the simplest learning algorithm, that uses only one neuron.  
An usual representation of a perceptron (neuron) that has **2 inputs** looks like this:

{% include image.html url="/imgs/posts/c-perceptron-tutorial/1.png" description="A 2 Inputs + Bias Perceptron" %}

Now for a better understanding:

**Input 1** and **Input 2** are the values we provide and **Output** is the result.

**Weight 1** and **Weight 2** are random values - they're used to adjust the input values so the error is minimum. By modifying them, the perceptron is able to learn.

The **Bias** shoult be treated as another input value, that always has the value of **1** (bias = 1). It must have it's own weight -> **weight 3**.

To learn, a perceptron uses **supervised learning**: that means, we need to provide multiple inputs and correct outputs so the weights can be adjusted correctly. Repeating this process will constantly lower the error until the generated output is almost equal with the desired output. When the weights are adjusted, the perceptron will be able to 'guess' the output for new inputs.

## How the perceptron works

One thing that you must understand about the perceptron is that it can only handle **linear separable** outputs, as its 'backend' function can be written as a polynomial (weights multiplied by inputs).
  
Let's take a look at the following image:

{% include image.html url="/imgs/posts/c-perceptron-tutorial/2.png" description="Linear separability of 2 classes is required in order to perform classification using only 1 Perceptron" %}

Each dot from the graphic above represents an output value:  
<font color="red">red dots</font> shall return **0**  
<font color="green">green dots</font> shall return **1**

As you can see, the outputs can be separated by a line, so the perceptron will know, using that line, if he has to return 0 or 1.

However that line must be positioned correctly so it separates the 2 outputs, here is where **weights** and **bias** are used:

*   **input weights** will rotate that line
*   **bias** will move the line to its position

## Formulas

**Output** = input[0] * weight[0] + input[1] * weight[1] + bias * weights[2]               
_If the output is greater than (or equal to) **0** it returns **1**, else it returns **0**._


**LocalError** = desiredOutput - calculatedOutput   
_For 2 input values, we get one output, but that output is not always correct, so he have to calculate the error._

**Weight[i]** = weight[i] + learningRate * localError * input[i]      
_Adjusting weights for Inputs._

**Weight[i]** = weight[i] + learningRate * localError * bias     
_Adjusting weight for bias (which is 1)_


**totalError** = totalError + Math.Abs(localError)

## Coding part

Coding time! I wrote for this tutorial a simple perceptron that learns the **AND gate**, using the formulas above. Take a look:

{% highlight csharp linenos %}using System;

namespace test
{

    class Program
    {
        static void Main(string[] args)
        {
            int[,] input = new int[,] { {1,0}, {1,1}, {0,1}, {0,0} };
            int[] outputs = { 0, 1, 0, 0 };

            Random r = new Random();

            double[] weights = { r.NextDouble(), r.NextDouble(), r.NextDouble() };

            double learningRate = 1;
            double totalError = 1;

            while (totalError > 0.2)
            {
                totalError = 0;
                for (int i = 0; i < 4; i++)
                {
                    int output = calculateOutput(input[i, 0], input[i, 1], weights);

                    int error = outputs[i] - output;

                    weights[0] += learningRate * error * input[i, 0];
                    weights[1] += learningRate * error * input[i, 1];
                    weights[2] += learningRate * error * 1;

                    totalError += Math.Abs(error);
                }

            } 

            Console.WriteLine("Results:");
            for (int i = 0; i < 4; i++)
                Console.WriteLine(calculateOutput(input[i, 0], input[i, 1], weights));

            Console.ReadLine();

        }

        private static int calculateOutput(double input1, double input2, double[] weights)
        {
            double sum = input1 * weights[0] + input2 * weights[1] + 1 * weights[2];
            return (sum >= 0) ? 1 : 0;
        }
    }

}

{% endhighlight %}