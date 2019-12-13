---
layout: post
title:  "C# Naive Bayes Basic OCR (w/ Example)"
date:   2016-11-17 20:02:05 +0300
categories: ai
thumbnail: /imgs/thumbnails/naive_bayes_ocr.png
---

Hello again; I'm back - once again sacrificing my time for homework so I can publish
something that I find more interesting.

So if anyone is still reading this: the whole article is about **OCR** (which stands for
*Optical Character Recognition*) by using a method called **Naive Bayes** (aka the probabilistic approach).
Considering the amount of information about this subject I thought some code/example might come
in handy. 



*// ps: if you're still wondering, it's the same **Bayes** from the math class.*
{: style="color:green;"}

## About Naive Bayes

This is a method that is used to solve **classification** problems. Basically **OCR**
can be classified as a classification problem (*see what I did there? :D*). Here I'm going
to explain this in a generic manner and then add the **OCR** part.

<u>The idea is this:</u> given an input, the program should be able to match it with a known 
output by taking into account various properties and comparing them to the ones that we used
for training.

**Naive Bayes** implies a probabilistic approach; so it outputs a bunch of probabilities
that our object is, in fact, an object that it already knows.

It is all based on **Bayes' theorem** which looks like this:

$$ P(A|B,C) = \frac{P(A,B,C)}{P(B,C)} = \frac{P(A,B,C)}{P(A)} \cdot  \frac{P(A)}{P(B,C)} = \frac{P(A)\cdot P(B,C|A)}{P(B,C)} $$

However, this theorem is supposed to work with independent variables, and we can't always
guarantee that. So, it is <span style="color:red">incorrect</span> to expand the denominator like this:



$$ P(B,C) = P(B) \cdot P(C) $$


You can try it but you may get probabilities **higher than 1** for some cases.

To avoid this, it might be better to think this in terms of **likelihoods** and to use this
property:



$$ P(A|B,C) \propto P(A) \cdot P(B|A) \cdot P(C|A) $$

The equation above says that the **likelihood** is <u>directly proportional</u> to the **probability** itself,
so we can consider only the **likelihood** when we do the classification (highest likelihood = highest chance).

You can later convert the likelihoods to probabilities between 0 and 1 - I'll explain below.


## Implementing a basic OCR

Moving on, it should be clear by now how our program should look:

- take a set of training images
- train using each image by taking the color of each pixel (where white color = ~P and black = P)
- for each unknown image: using its pixels compute the likelihood it resembles an image that
was used during the training procedure 

Something like this:

{% include image.html url="/imgs/posts/c-naive-bayes-basic-ocr-w-example/1.png" description="Naive Bayes model for Basic OCR" %}


Where P(one\|...) is the probability the image matches the one I used to train the classifier.

## Computing the likelihoods

First, there's going to be one big table containg both the data from the images and some additional
sums that we'll need in order to compute some probabilities - usually it's called **Frequency Table**.

The table looks like this:

<table>
<th><td style="width:50px"></td><td style="width:100px">one</td><td style="width:100px">two</td><td style="width:100px">three</td><td style="width:100px">...</td></th>
<tr><td style="width:50px">P1</td><td style="width:100px"></td><td style="width:100px">0 or 1</td><td style="width:100px">0 or 1</td><td style="width:100px">0 or 1</td><td style="width:100px">...</td></tr>
<tr><td style="width:50px">P2</td><td style="width:100px"></td><td style="width:100px">0 or 1</td><td style="width:100px">0 or 1</td><td style="width:100px">0 or 1</td><td style="width:100px">...</td></tr>
<tr><td style="width:50px">P3</td><td style="width:100px"></td><td style="width:100px">0 or 1</td><td style="width:100px">0 or 1</td><td style="width:100px">0 or 1</td><td style="width:100px">...</td></tr>
<tr><td style="width:50px">...</td><td style="width:100px"></td><td style="width:100px">...</td><td style="width:100px">...</td><td style="width:100px">...</td><td style="width:100px">...</td></tr>
<tr><td style="width:50px">sums_cols</td><td style="width:100px"></td><td style="width:100px">sum_col#1</td><td style="width:100px">sum_col#2</td><td style="width:100px">sum_col#3</td><td style="width:100px">...</td></tr>
</table>
{: style="text-align: center;" }
<br>

Where `table[P1][one]` is:

- `1` if the training image containing an **1** has the first pixel(P1) colored black (so the pixel contributes to drawing the digit)
- `0` if the pixel is white

`sum_col#1` means the sum of the first (current) column.


We need these in order to compute some probabilities while applying **Bayes' theorem**.
<br>

Once all the sums are computed we can start determining **likelihoods**.

Now, we implement the **Bayes' theorem** and apply the data from the table.

---
Intermission.

The formula, for an image with 3 pixels, should look like this:

$$ P(one|P1, P2, \sim P3) = P(one) \cdot P(P1|one) \cdot P(P2 | one) \cdot (1 - P(P3|one)) $$

Where: 

`P(one) = 1 / number_of_digits_we_are_training_for`

`P(P1|one) = table[P1][one] / sum_col#1`

`P(~P3|one) = 1 - table[P3][one] / sum_col#1`

^ ehm...these are actually likelihoods, not probabilities. Don't get confused.

---
Now the real deal - applying this for `N_OF_IMAGES` images, each one containing `IMG_SIZE` * `IMG_SIZE`
pixels.


{% highlight csharp linenos %}
// for each known image
for (int k = 0; k < N_OF_IMAGES; k++)
{
    // determining P(one) / P(two) / P(three) 
    likelihoods[k] = 1 / (double)N_OF_IMAGES;

    int crtPixel = 0;

    for (int i = 0; i < IMG_SIZE; i++)
        for (int j = 0; j < IMG_SIZE; j++)
        {
            // getting the current pixel's position in the table
            crtPixel = i * IMG_SIZE + j;
            
            // applying the formula
            likelihoods[k] *= (testBmp.GetPixel(i, j).ToArgb() != Color.White.ToArgb() ? frequencies[crtPixel, k] / frequencies[N_OF_PIXELS, k] : (1 - frequencies[crtPixel, k] / frequencies[N_OF_PIXELS, k]));
        }

    // I use this to convert from likelihoods to probabilities (0-1)
    totalLikelihood += likelihoods[k];
}
{% endhighlight %}

---
<u>Short note:</u>

You can get the probability for each image by doing: `likelihoods[k] / totalLikelihood`.

---

## Laplace smoothing

Given the fact that the **frequency table** may contain **0**'s (not all pixels are black), 
we need to apply some **smoothing** to prevent working with null probabilities in our formula.

We add some "fake" inputs in the **frequency table** - kinda like a black background image
for each digit. If it makes it easier think of it as adding **1** to the numerator and **n**
to the denominator (n = number of pixels) when computing probabilities.

So...if in our **frequency table** there's something like: `table[P1][one] == 0` and `sum_col#1 == 10`, then we'd get `P(P1|one) = 0/10 = 0`

Now, with **Laplace smoothing**: `table[P1][one] == 1` and `sum_col#1 == 10 + n` (let's say n = 100 pixels, because the images I'm using are 10x10). 
Notice that `P(P1|one) = 1/(10+100) = 0.009`. 



## Results

These were the inputs

{% include image.html url="/imgs/posts/c-naive-bayes-basic-ocr-w-example/2.png" description="Images used for Training and Testing the Naive Bayes model" %}


And the outputs:

{% include image.html url="/imgs/posts/c-naive-bayes-basic-ocr-w-example/3.png" description="The results achieved by the current implementation" %}

## Complete Sourcecode

The sourcecode that I used in this article; I guess there's no need for additional documentation :))

Final note: to me it seems to be working, but it's the first time I'm coding stuff like this, so... it might contain mistakes.

{% highlight csharp linenos %}
using System;
using System.Drawing;
using System.IO;

namespace Bayes_Classifier
{
    class Program
    {
        static void Main(string[] args)
        {
            string[] files = Directory.GetFiles(AppDomain.CurrentDomain.BaseDirectory + "/train/", "*.png");

            int N_OF_IMAGES = files.Length;
            int IMG_SIZE = 10; // 10x10 image
            int N_OF_PIXELS = IMG_SIZE * IMG_SIZE;

            double[,] table = new double[N_OF_PIXELS+1, N_OF_IMAGES];

            // Laplace smoothing
            for (int i = 0; i < N_OF_IMAGES; i++)
                for (int j = 0; j < N_OF_PIXELS; j++)
                    table[j, i] = 1;

            Bitmap bmp = null;

            // copying data in the frequency table
            for (int i = 0; i < N_OF_IMAGES; i++)
            {
                bmp = (Bitmap)Image.FromFile(files[i]);

                for (int j = 0; j < IMG_SIZE; j++)
                {
                    for (int k = 0; k < IMG_SIZE; k++)
                        if (bmp.GetPixel(j, k).ToArgb() != Color.White.ToArgb())
                            table[j * IMG_SIZE + k, i]++;
                }
            }

            // -- computing the sums
            for (int i = 0; i < N_OF_PIXELS; i++)
            {
                for (int j = 0; j < N_OF_IMAGES; j++)
                    table[N_OF_PIXELS, j] += table[i, j];
            }


            string[] testFiles = Directory.GetFiles(AppDomain.CurrentDomain.BaseDirectory + "/test/", "*.png");

            for (int testFileIndex = 0; testFileIndex < testFiles.Length; testFileIndex++)
            {
                Console.WriteLine("File: " + testFiles[testFileIndex]);
                Bitmap testBmp = (Bitmap)Image.FromFile(testFiles[testFileIndex]);

                double[] likelihoods = new double[N_OF_IMAGES];
                double totalLikelihood = 0;

                for (int k = 0; k < N_OF_IMAGES; k++)
                {
                    likelihoods[k] = 1 / (double)N_OF_IMAGES;

                    int crtPixel = 0;

                    for (int i = 0; i < IMG_SIZE; i++)
                        for (int j = 0; j < IMG_SIZE; j++)
                        {
                            crtPixel = i * IMG_SIZE + j;
                            likelihoods[k] *= (testBmp.GetPixel(i, j).ToArgb() != Color.White.ToArgb() ? table[crtPixel, k] / table[N_OF_PIXELS, k] : (1 - table[crtPixel, k] / table[N_OF_PIXELS, k]));
                        }

                    totalLikelihood += likelihoods[k];
                }


                for (int i = 0; i < N_OF_IMAGES; i++)
                    Console.WriteLine((i + 1) + " : " + likelihoods[i] / totalLikelihood);

                Console.WriteLine();
            }
            Console.ReadLine();

        }
    }
}

{% endhighlight %}







 










   

