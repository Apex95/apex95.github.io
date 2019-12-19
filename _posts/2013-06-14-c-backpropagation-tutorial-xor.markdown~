---
layout: post
title:  "C# Backpropagation Tutorial (XOR)"
date:   2013-06-14 20:02:05 +0300
categories: miscellaneous
thumbnail: /imgs/thumbnails/backpropagation.webp
---

I've been trying for some time to learn and actually understand how **Backpropagation** (aka **backward propagation of errors**) works and how it trains the neural networks. Since I encountered many problems while creating the program, I decided to write this tutorial and also add a completely functional code that is able to **learn** the **XOR** gate.

_Since it's a lot to explain, I will try to stay on subject and talk only about the backpropagation algorithm._

## 1\. What is Backpropagation?

**Backpropagation** is a supervised-learning method used to train **neural networks** by adjusting the **weights** and the **biases** of each neuron.

**Important**: do NOT train for only one example, until the error gets minimal then move to the next example - you have to take each example once, then start again from the beginning.

_Steps:_

1.  _**forward propagation** - calculates the output of the neural network_
2.  _**back propagation** - adjusts the weights and the biases according to the global error_

In this tutorial I'll use a **2-2-1** neural network (2 input neurons, 2 hidden and 1 output). Keep an eye on this picture, it might be easier to understand.

{% include image.html url="/imgs/posts/c-backpropagation-tutorial-xor/1.png" description="Cookie-cutter Neural Network Model for learning XOR" %}

## 2\. How it works?

1.  initialize all weights and biases with random values between 0 and 1
2.  calculate the output of the network
3.  calculate the global error
4.  adjust the weights of the output neuron using the global error
5.  calculate the hidden neurons' errors (split the global error)
6.  adjust the hidden neurons' weights using their errors
7.  go to step 2) and repeat this until the error gets minimal

## 3\. Some math...

Any **neural network** can be described as a mathematical function which takes an **input**, and computes an **output** using a set of **coefficients** (here, we call them **weights**). The only variables that we can change are the **weights** (think of it as some sort of interpolation). Usually, on the resulted output, an **activation function** is applied for various reasons: 1) it adds nonlinearity and 2) it properly limits the output to a known interval. Here, we use a **sigmoid** activator - more details below.

Its graph looks like this (note that the output values range from **0** to **1**)

{% include image.html url="/imgs/posts/c-backpropagation-tutorial-xor/2.png" description="Plot of the Sigmoid activation function" %}

**Sigmoid formulas** that we'll use (where **f(x)** is our sigmoid function)

_1) Basic sigmoid function:_  
$$ f(x) = \frac{1}{1+e^{-x}} $$

_2) Sigmoid Derivative (its value is used to adjust the weights using gradient descent):_  
$$ f'(x) = f(x)(1-f(x)) $$

Backpropagation always aims to reduce the error of each output. The algorithm knows the correct final output and will attempt to minimize the error function by tweaking the weights.

For a better understanding of this, take a look at the graph below which shows the error, based on the output:

{% include image.html url="/imgs/posts/c-backpropagation-tutorial-xor/5.png" description="Plotting the error function, considering the case of 1 dimension (1 variable)" %}

We intend to produce an **output value** which ensures a **minimal error** by adjusting only the **weights** of the neural network.  
I won't dive into the **gradient descent** method, as I wrote a [separate article](https://codingvision.net/numerical-methods/gradient-descent-simply-explained-with-example) that contains both theory and examples.

## 4\. Formulas

Calculate the output of a neuron (**f** is the sigmoid function, **f'** is the derivative of f, aka df/dx):  
**actualOutput = f(weights[0] * inputs[0] + weights[1] * inputs[1] + biasWeight)**

Calculate the global error (error for the **output neuron**)  
**globalError = f'(output) * (desiredOutput - actualOutput)**

Adjust the weights/bias of the **output neuron**  
**W13 += globalError * input13  
W23 += globalError * input23  
bias += globalError**

Calculate the error for each **hidden neuron**  
**error1 = f'(x) * globalError * W13  
error2 = f'(x) * globalError * W23**

Adjust the weights of the **hidden neurons**

**->> first hidden neuron**  
**W11 += error1 * input11  
W21 += error1 * input21  
bias1 += error1;**

**->> second hidden neuron**  
**W12 += error2 * input12  
W22 += error2 * input22  
bias2 += error2;**

## 5\. The code

The best part and also the easiest. There are many things backpropagation can do but as an example we can make it learn the **XOR** gate...since it's so special.  
I used 2 classes just to make everything more "visible" and OOP-ish.

Note: it requires about 2000 epochs to learn.

```csharp
using System;

namespace BackPropagationXor
{
    class Program
    {
        static void Main(string[] args)
        {
            train();
        }

        class sigmoid
        {
            public static double output(double x)
            {
                return 1.0 / (1.0 + Math.Exp(-x));
            }

            public static double derivative(double x)
            {
                return x * (1 - x);
            }
        }

        class Neuron
        {
            public double[] inputs = new double[2];
            public double[] weights = new double[2];
            public double error;

            private double biasWeight;

            private Random r = new Random();

            public double output
            {
                get { return sigmoid.output(weights[0] * inputs[0] + weights[1] * inputs[1] + biasWeight); }
            }

            public void randomizeWeights()
            {
                weights[0] = r.NextDouble();
                weights[1] = r.NextDouble();
                biasWeight = r.NextDouble();
            }

            public void adjustWeights()
            {
                weights[0] += error * inputs[0];
                weights[1] += error * inputs[1];
                biasWeight += error;
            }
        }

        private static void train()
        {
            // the input values
            double[,] inputs = 
            {
                { 0, 0},
                { 0, 1},
                { 1, 0},
                { 1, 1}
            };

            // desired results
            double[] results = { 0, 1, 1, 0 };

            // creating the neurons
            Neuron hiddenNeuron1 = new Neuron();
            Neuron hiddenNeuron2 = new Neuron();
            Neuron outputNeuron = new Neuron();

            // random weights
            hiddenNeuron1.randomizeWeights();
            hiddenNeuron2.randomizeWeights();
            outputNeuron.randomizeWeights();

            int epoch = 0;

        Retry:
            epoch++;
            for (int i = 0; i < 4; i++)  // very important, do NOT train for only one example
            {
                // 1) forward propagation (calculates output)
                hiddenNeuron1.inputs = new double[] { inputs[i, 0], inputs[i, 1] };
                hiddenNeuron2.inputs = new double[] { inputs[i, 0], inputs[i, 1] };

                outputNeuron.inputs = new double[] { hiddenNeuron1.output, hiddenNeuron2.output };

                Console.WriteLine("{0} xor {1} = {2}", inputs[i, 0], inputs[i, 1], outputNeuron.output);

                // 2) back propagation (adjusts weights)

                // adjusts the weight of the output neuron, based on its error
                outputNeuron.error = sigmoid.derivative(outputNeuron.output) * (results[i] - outputNeuron.output);
                outputNeuron.adjustWeights();

                // then adjusts the hidden neurons' weights, based on their errors
                hiddenNeuron1.error = sigmoid.derivative(hiddenNeuron1.output) * outputNeuron.error * outputNeuron.weights[0];
                hiddenNeuron2.error = sigmoid.derivative(hiddenNeuron2.output) * outputNeuron.error * outputNeuron.weights[1];

                hiddenNeuron1.adjustWeights();
                hiddenNeuron2.adjustWeights();
            }

            if (epoch < 2000)
                goto Retry;

            Console.ReadLine();
        }
    }
}
```

## 6\. Proof of concept

{% include image.html url="/imgs/posts/c-backpropagation-tutorial-xor/6.png" description="The presented model manages to learn the outputs of the XOR gate" %}


## 7\. Wrong values?

Yep, this happens sometimes, when the algorithm gets stuck on the **local minima**: the algorithm thinks it has found the minimum error, it doesn't know that the error could be even smaller.

This is usually solved by resetting the weights of the neural network and training again.