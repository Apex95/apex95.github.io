---
layout: post
title:  "Gradient Descent Simply Explained (with Example)"
date:   2019-08-13 00:45:05 +0300
categories: numerical-methods
image: /imgs/thumbnails/mse-slope-plot.webp
---

So... I'll try to explain here the concept of **gradient descent** as simple as possible in order to provide some insight of what's happening from a mathematical perspective and why the formula works. I'll try to keep it short and split this into 2 _chapters_: **theory** and **example** - take it as a ELI5 *5 minutes* linear regression tutorial.

Feel free to skip the mathy stuff and jump directly to the **example** if you feel that it might be easier to understand.


## Theory and Formula

For the sake of simplicity, we'll work in the **1D** space: we'll optimize a function that has only one **coefficient** so it is easier to plot and comprehend.
The function can look like this:

$$ f(x) = w \cdot x + 2$$

where we have to determine the value of $$ w $$ such that the function successfully matches / approximates a set of known points. 

Since our interest is to find the best coefficient, we'll consider $$ w $$ as a **variable** in our formulas and while computing the derivatives while $$ x $$ is treated as a **constant**. In other words, we don't compute the **derivative** with respect to $$ x $$ since we don't want to find values for it - we already have a set of inputs for the function, we're not allowed to change them.

To properly grasp the gradient descent, as an optimization method, you need to know the following mathematical fact:


- The **derivative** of a function is <span style="color:green">positive</span> when the function <span style="color:green">increases</span> and is <span style="color:red">negative</span> when the function <span style="color:red">decreases</span>.

 
And writing this mathematically...

$$ \frac{\mathrm{d} }{\mathrm{d} w}f(w) {\color{Green}> 0} \rightarrow  f(w) {\color{Green}\nearrow }$$

$$ \frac{\mathrm{d} }{\mathrm{d} w}f(w) {\color{Red}< 0} \rightarrow  f(w) {\color{Red}\swarrow } $$

This is happening because the derivative can be seen as the slope of a function's plot at a given point. I won't go into details here, but check out the graph below - it should help.




_Why is this important?_

Because, as you probably know already, **gradient descent** attempts to <span style="color:red">minimize</span> the **error function** (aka cost function).

Now, assuming we use the **MSE** (*Mean Squared Error*) function, we have something that looks like this:

$$ \hat{y_i} = f(x_i) $$

$$ MSE = \frac{1}{n} \cdot \sum_{i=1}^{i=n}{(y_i - \hat{y_i})^2} $$

Where: $$ y_i $$ is the correct value, $$ \hat{y_i} $$ is the current (computed) value and $$ n $$ is the number of points we're using to compute the $$ MSE $$.

*Observation: the **MSE** is **always positive** (since it's a sum of squared values) and therefore has a **known minimum**, which is **0** - so it can be <span style="color:red">minimized</span> using the aforementioned derivatives method.*

Take a look at the plot below: the **sign** of the **slope** provides useful information of where the **minimum** of the function is. We can use the value of the **slope** (the derivative) to adjust the value of the coefficient **w** (i.e.: `w = w - slope`).


{% include image.html url="/imgs/posts/gradient-descent-simply-explained-with-example/mse-slope-plot.png" description="The sign of the slope can be used to locate the function's minimum value." %}


Time to compute the derivative. Before that, I must warn you: it's quite a *long* formula but I tried to do it step by step. Behold!


$$ \frac{\mathrm{d}}{\mathrm{d} w}MSE = \frac{\mathrm{d}}{\mathrm{d} w} (\frac{1}{n} \cdot \sum_{i=1}^{i=n}{(y_i - \hat{y_i})^2}) = $$ 

$$ = \frac{1}{n} \cdot \frac{\mathrm{d}}{\mathrm{d} w} (\sum_{i=1}^{i=n}{(y_i - \hat{y_i})^2}) = $$

$$ = \frac{1}{n} \cdot \sum_{i=1}^{i=n}{\frac{\mathrm{d}}{\mathrm{d} w}((y_i - \hat{y_i})^2}) = $$

$$ = \frac{1}{n} \cdot \sum_{i=1}^{i=n}{\frac{\mathrm{d}}{\mathrm{d} w}((y_i - \hat{y_i})^2}) = $$ 

$$ = \frac{2}{n} \cdot \sum_{i=1}^{i=n}{(y_i - \hat{y_i})} \cdot (-1) \cdot \frac{\mathrm{d \hat{y_i}}}{\mathrm{d} w} $$


Phew. 
From here, you'd have to replace $$ \frac{\mathrm{d \hat{y_i}}}{\mathrm{d} w} $$ with the derivative of the function you chose to optimize. For $$ \hat{y} = w \cdot x + 2 $$, we get:

$$ = \frac{2}{n} \cdot \sum_{i=1}^{i=n}{(y_i - \hat{y_i})} \cdot (-1) \cdot x $$

And that's about it. You can now update the values of your coefficient $$w$$ using the following formula:

$$ w = w - learning\_rate \cdot \frac{\mathrm{d }}{\mathrm{d} w}MSE(w) $$


## Example

We'll do the example in a **2D** space, in order to represent a basic **linear regression** (a **Perceptron**). 
Given the function below:

$$ f(x) = w_1 \cdot x + w_2 $$

we have to find $$ w_1 $$ and $$ w_2 $$, using **gradient descent**, so it approximates the following set of points:

$$ f(1) = 5, f(2) = 7 $$


We start by writing the **MSE**:

$$ MSE = \frac{1}{n} \cdot \sum_{i=1}^{i=2}{(y_i - (w_1 \cdot x + w_2))^2} $$


And then the differentiation part. Since there are **2 coefficients**, we compute **partial derivatives** - each one corresponds to its coefficient.

For $$ w_1 $$:

$$ \frac{\partial}{\partial w_1} (\frac{1}{n} \cdot \sum_{i=1}^{i=2}{(y_i - (w_1 \cdot x_i + w_2))^2}) = $$

$$ = \frac{1}{n} \cdot \sum_{i=1}^{i=2}{(y_i - \frac{\partial}{\partial w_1}(w_1 \cdot x_i + w_2))^2} = $$

$$ = \frac{1}{n} \cdot 2 \cdot \sum_{i=1}^{i=2}{(y_i - (w_1 \cdot x_i + w_2)) \cdot (-1) \cdot x_i} = $$

$$ = -\frac{2}{n} \cdot \sum_{i=1}^{i=2}{(y_i - (w_1 \cdot x_i + w_2)) \cdot x_i} $$


For $$ w_2 $$:

$$ \frac{\partial}{\partial w_2} (\frac{1}{n} \cdot \sum_{i=1}^{i=2}{(y_i - (w_1 \cdot x_i + w_2))^2}) = $$

$$ = -\frac{2}{n} \cdot \sum_{i=1}^{i=2}{(y_i - (w_1 \cdot x_i + w_2))} $$



Now, we pick some **random** values for our coefficients. Let's say $$ w_1 = 9 $$ and $$ w_2 = 10 $$.

We compute:

$$ f(1) = 9 \cdot 1 + 10 = 19, f(2) = 9 \cdot 2 + 10 = 28 $$

Obviously, these are not the outputs we're looking for, so we'll continue by adjusting the coefficients (we'll consider a **0.15** learning rate):

$$ w_1 = w_1 - learning\_rate \cdot \frac{\partial}{\partial w_1} MSE = $$

$$ = 9 + 0.15 \cdot \frac{2}{2} \cdot \sum_{i=1}^{i=2}{(y_i - (w_1 \cdot x_i + w_2)) \cdot x_i} = $$

$$ = 9 + 0.15 \cdot ((5 - (9 \cdot 1 + 10)) \cdot 1 + (7 - (9 \cdot 2 + 10)) \cdot 2) = $$
 
$$ = 9 - 0.15 \cdot 56 = 0.6 $$ 

$$ w_2 = w_2 - learning\_rate \cdot \frac{\partial}{\partial w_2} MSE = $$

$$ = 10 + 0.15 \cdot \frac{2}{2} \cdot \sum_{i=1}^{i=2}{(y_i - (w_1 \cdot x_i + w_2))} = $$

$$ = 10 + 0.15 \cdot ((5 - (9 \cdot 1 + 10)) + (7 - (9 \cdot 2 + 10))) = $$
 
$$ = 10 - 0.15 \cdot 35 = 4.75 $$ 


Recalculating the output of our function, we observe that the outputs are somehow closer to our expected values.

$$ f(1) = 0.6 \cdot 1 + 4.75 = 5.35, f(2) = 0.6 \cdot 2 + 1.25 = 5.95 $$



Running a second step of optimization:

$$ w_1 = 0.6 + 0.15 \cdot ((5 - (0.6 \cdot 1 + 4.75)) \cdot 1 + (7 - (0.6 \cdot 2 + 4.75)) \cdot 2) = $$

$$ = 0.6 + 0.15 \cdot 1.75 = 0.86 $$

$$ w_2 = 4.75 + 0.15 \cdot ((5 - (0.6 \cdot 1 + 4.75)) + (7 - (0.6 \cdot 2 + 4.75))) = $$
 
$$ = 4.75 + 0.15 \cdot 0.7 = 4.85 $$ 


Now, this is going to take multiple iterations in order to converge and we're not going to do everything by hand.
Writing this formula as a Python script yields the following results:

```
1: w1 = 9.000, w2 = 10.000, MSE: 318.5 
   f(1) = 19.000, f(2) = 28.000
------------------------------------------------
2: w1 = 0.600, w2 = 4.750, MSE: 0.6125 
   f(1) = 5.350, f(2) = 5.950
------------------------------------------------
3: w1 = 0.862, w2 = 4.855, MSE: 0.345603125 
   f(1) = 5.718, f(2) = 6.580
------------------------------------------------
4: w1 = 0.881, w2 = 4.810, MSE: 0.330451789063 
   f(1) = 5.691, f(2) = 6.572
------------------------------------------------
5: w1 = 0.906, w2 = 4.771, MSE: 0.316146225664 
   f(1) = 5.676, f(2) = 6.582
------------------------------------------------
6: w1 = 0.929, w2 = 4.732, MSE: 0.302460106908 
   f(1) = 5.662, f(2) = 6.591
------------------------------------------------
7: w1 = 0.953, w2 = 4.694, MSE: 0.289366466781 
   f(1) = 5.647, f(2) = 6.600
------------------------------------------------
8: w1 = 0.976, w2 = 4.657, MSE: 0.276839656487 
   f(1) = 5.633, f(2) = 6.609
------------------------------------------------
9: w1 = 0.998, w2 = 4.621, MSE: 0.264855137696 
   f(1) = 5.619, f(2) = 6.617


[...]


------------------------------------------------
195: w1 = 1.984, w2 = 3.026, MSE: 7.04866766459e-05 
     f(1) = 5.010, f(2) = 6.994
------------------------------------------------
196: w1 = 1.984, w2 = 3.026, MSE: 6.74352752985e-05 
     f(1) = 5.010, f(2) = 6.994
------------------------------------------------
197: w1 = 1.984, w2 = 3.025, MSE: 6.45159705491e-05 
     f(1) = 5.010, f(2) = 6.994
------------------------------------------------
198: w1 = 1.985, w2 = 3.025, MSE: 6.17230438739e-05 
     f(1) = 5.009, f(2) = 6.994
------------------------------------------------
199: w1 = 1.985, w2 = 3.024, MSE: 5.90510243065e-05 
     f(1) = 5.009, f(2) = 6.994
------------------------------------------------
200: w1 = 1.985, w2 = 3.024, MSE: 5.64946777215e-05 
     f(1) = 5.009, f(2) = 6.994
```
 
It converges to $$ w_1 = 2 $$ and $$ w_2 = 3 $$ which are, indeed, the coefficients we were looking for.

In practice, I recommend experimenting with **smaller** learning rates and more iterations - large learning rates can lead to **divergence** (the coefficients stray from their correct values and tend to plus or minus infinity).


## Conclusion

I guess this is all. Reading it now, I think it might take more than 5 minutes but... I guess it's still a short article when compared to others that discuss the same subject :))

I hope this proves useful as a starting point and you've got something out of it. **Backpropagation** of errors in **nerual networks** works in a similar fashion, although the number of dimensions is way larger than what was presented here. Aaand it contains some additional features in order to handle **non-convex** functions (and avoid getting stuck in **local minima**). Maybe in other article we'll take a look at those, too.
