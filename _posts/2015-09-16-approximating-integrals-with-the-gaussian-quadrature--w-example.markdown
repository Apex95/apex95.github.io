---
layout: post
title:  "Approximating Integrals with the Gaussian Quadrature (w/ example)"
date:   2015-09-16 20:02:05 +0300
categories: numerical-methods
thumbnail: /imgs/thumbnails/gauss.gif
---

This is more like a memory dump so I will have a backup in case I'll ever need it again. And if someone else finds this information useful, the better it is.

## Intro

The **Gaussian Quadrature** is a method used to approximate the value of a given integral by choosing a set of points (**x<sub>1</sub>, x<sub>2</sub>, x<sub>3</sub>, ... x<sub>n</sub>**) that will maximize the accuracy. Basically the integral can be approximated using coefficients and known values of our function. It's a pretty neat method since it doesn't require many points and it works for a set of integrals - not only for one.

$$ \int_{-1}^{1}f(x)w(x) dx = \sum_{i=1}^{n} A_if(x_i) $$

On the example above, we have an integral that we want to approximate and on the right side of the equal sign is the **Gaussian Quadrature**.

**f(x)** is our function (it's not required to know how it looks like), **w(x)** is a **weight function**.

As you noticed we'll be working within the interval **[-1;1]** - and we'll consider **w(x) = 1** (Legendre).  
_- But...what if the integral has a <u>different interval</u>?_; use this little trick:

$$ \int_{a}^{b}f(x)dx = \frac{b-a}{2}\int_{-1}^{1}f(\frac{b-a}{2}x + \frac{b+a}{2})dx $$

Our purpose is to find a set of coefficients (**A<sub>1</sub>, A<sub>2</sub>, ... A<sub>n</sub>**) and a set of points (**x<sub>1</sub>, x<sub>2</sub>, ... x<sub>n</sub>**) that will make this quadrature as exact as possible, for a set of integrals.

To keep everything simple we'll take **n=2** so our equation will look like this:

$$ \int_{-1}^{1}f(x)w(x)dx = A_1f(x_1) + A_2f(x_2) $$

From now on I'll be working with this example, however it's the same method when **n** has a different value.

## How to find the 'x' values

In order to calculate the coefficients (**A<sub>1</sub>, A<sub>2</sub>**) we need to know the values of **x<sub>1</sub>** and **x<sub>2</sub>**. If these are not given, we will have to calculate them using some theory implying **orthogonal polynomials**.

<u>Now here's how you do this:</u>

Create a polynomial (usually noted **π**), that has **n=2** roots: **x<sub>1</sub>** and **x<sub>2</sub>**.  
It will look like this:

$$ \pi = \prod_{i=1}^{n=2}x-x_i \Rightarrow \pi = (x-x_1)(x-x_2) $$

Here you need to know this little part of theory related to **orthogonal polynomials**:

1.  polynomials **P** and **Q** are orthogonal if their **inner product** is **0** (**&lt;p, q&gt;= 0**)
2.  a polynomial of degree **n** is orthogonal to any other polynomial of degree lower than **n**

These properties are required in order to produce a system of equations which will provide us the values for **x<sub>1</sub>** and **x<sub>2</sub>**.

We define that **inner product** that I was talking about earlier:

$$ <P,Q> = \int_{-1}^{1} P(x)Q(x)w(x)dx $$

where **P** and **Q** are 2 polynomials and **w(x)** is the **weight function**.

Ok enough with the theory, moving back to our example: we had that **?** polynomial.  
Now we pick the first **n=2** terms from the **monomial basis** (**1**, **x**, x<sup>2</sup>, x<sup>3</sup>...).

Notice that those 2 "polynomials" are of degree **0** and **1** - both lower than **n=2**(the degree of our **π** polynomial) => these are **orthogonal** to **π**. Knowing this we can create the following system of equations:

$$ <\pi,1> = \int_{-1}^{1} \pi(x)\cdot 1 \cdot 1dx = 0 $$

$$ <\pi,x> = \int_{-1}^{1} \pi(x)\cdot x \cdot 1dx = 0 $$

Note that in there I already did the substitution **w(x)=1**.  
By solving the integrals...

$$ \frac{2}{3} + 2x_1x_2 = 0 $$

$$ -\frac{2}{3}(x_1 + x_2) = 0 $$

So we get these values:

$$ x_1 = -\frac{\sqrt{3}}{3} $$

$$ x_2 = \frac{\sqrt{3}}{3} $$

## Finding the coefficients

This is the easy part - if you managed to get here then you're almost done.  
To find the values of the coefficients, we'll use the same **Gauss Quadrature**, but this time on these functions:

**f<sub>1</sub>(x) = 1  
f<sub>2</sub>(x) = x**

where **1** and **x** are the monomials we chose before.

If we rewrite the **Gaussian Quadrature** for these 2 functions we get:

$$ \int_{-1}^{1} 1 \cdot 1 dx = A_1f_1(x_1) + A_2f_1(x_2) \Rightarrow A_1+A_2 = 2 $$

$$ \int_{-1}^{1} x \cdot 1 dx = A_1f_2(x_1) + A_2f_2(x_2) \Rightarrow A_1x_1+A_2x_2 = 0 $$

(substitued **w(x) = 1**)

So **A<sub>1</sub> = A<sub>2</sub> = 1**, hence the <u>final equation</u>:

$$ \int_{-1}^{1} f(x)d = f(-\frac{\sqrt{3}}{3}) + f(\frac{\sqrt{3}}{3}) $$

## Precision

The degree of precision for this example is **2*n-1 = 3**. This means if the integrand is a polynomial of degree **3** (or lower) the result will be exact. If not, the result will be an approximation.

Note that this also works for non-polynomial functions; if we integrate **cos(x)** from **-1** to **1**

*   **original** result: **2*sin(1) ~ 1.6829**
*   result approximated with the **Gaussian Quadrature**: **cos(-sqrt(3)/3) + cos(sqrt(3)/3) = 1.6758**

Not the best result, but will do - usually adding more points helps gaining precision.