---
layout: post
title:  "Matlab/Octave Lagrange Interpolation Polynomial"
date:   2015-08-19 20:02:05 +0300
categories: numerical-methods
thumbnail: /imgs/thumbnails/plot.webp
---

_Ok, I've been missing for a few days...months...almost a year. Ran out of ideas and time for new articles (thanks to the university) so I'll publish some stuff related to numerical methods, starting with a basic **interpolation** method using the **Lagrange Polynomial**. And since there's a lot of C# here, I thought it would be a good idea, for "programming diversity", to write this in **Matlab/Octave**. Forgive me guys :/_

## The Lagrange Polynomial

This **Lagrange Polynomial** is a function (curve) that you create, that goes through a specific set of points (the basic interpolation rule).

For **N** sets of points (**x y**) the general formula is the one below:

$$ Y(x) = \sum_{i=1}^{n} y_i \cdot \prod_{j=1, j \neq i} \frac{x-x_j}{x_i-x_j} $$

Now a sum of products may look intimidating, but it's a really simple method - whatever is not needed is cancelled (in this case multiplied with 0) so it won't change the final result unless it's necessary.

Don't worry if you don't understand the formula, take a look at the example below, it should be way clearer after.

## Example & Explaination

Let's take the... factorial function (**x!**) and try to write a **Lagrange Polynomial** that produces "similar" results.  
_It won't produce very precise outputs since we gave it a low number of points - don't expect miracles_.

Given this set of **4 points**:

<table cellpading="3" style="border-collapse:collapse;text-align:center;color:#444;" border="1" cellpadding="6" cellspacing="10">

<tbody>

<tr>

<td><strong>x</strong></td>

<td><strong>y</strong></td>

</tr>

<tr>

<td>2</td>

<td>2</td>

</tr>

<tr>

<td>3</td>

<td>6</td>

</tr>

<tr>

<td>4</td>

<td>24</td>

</tr>

<tr>

<td>5</td>

<td>120</td>

</tr>

</tbody>

</table>

We construct the polynomial this way (using **Lagrange Multipliers**)

$$ {\color{Red} {2}} \cdot \frac{(x-3)(x-4)(x-5)}{(2-3)(2-4)(2-5)} + {\color{Red}{6}} \cdot \frac{(x-2)(x-4)(x-5)}{(3-2)(3-4)(3-5)} + {\color{Red}{24}} \cdot \frac{(x-2)(x-3)(x-5)}{(4-2)(4-3)(4-5)} + {\color{Red}{120}} \cdot \frac{(x-2)(x-3)(x-4)}{(5-2)(5-3)(5-4)} $$

Notice that if **x** is equal to one of the **known values** (from the table), many of these fractions will be **0** and only **one of them** will be **1**. That **1** is multiplied with the expected output and you get the result.

For **x = 2**: the equation becomes: **2 * 1 + 6 * 0 + 24 * 0 + 120 * 0** = 2\. Got the point? This ensures us that no matter what, the graph of this function will go through our set of points and since this polynomial will have an order <= n-1, there's no need to worry about any edges.

After creating the polynomial and testing it, we may find out that...we'll need more than 4 points to obtain a good approximation of the factorial function.

You can see below a **plot** that contains the <span style="color:red">Lagrange Polynomial</span> and the <span style="color:green">values computed with Gamma function</span>(or the correct factorial values).

{% include image.html url="/imgs/posts/matlab-octave-lagrange-interpolation-polynomial/3.png" description="Comparing the Lagrange approximation (Red) with the Gamma function (Green)." %}

And this is for inputs **inside the interval** of known values **[2;5]** - for values greater than 5 or lower than 2, the function still works but the outputs are completely wrong since there are no points to guide the curve.

Still it provides exact values for 2!, 3!, 4! and 5!

{% include image.html url="/imgs/posts/matlab-octave-lagrange-interpolation-polynomial/4.png" description="Meh..." %}

## Matlab/Octave Sourcecode

Here goes the code:

```matlabfunction [y] = lagrange(x, x0, y0)

    % x0 - vector containing inputs (x values)
    % y0 - vector containing outputs (results for these x values
    % x - value you want to compute, for interpolation
    % y - computed value

    n = size(x0, 1); 
    y = 0;

    for i=1:n
        p = 1;
        for j=1:n

            if j == i   % avoiding fancy division by 0
                continue;
            endif;

            p *= (x-x0(j)) / (x0(i)-x0(j));

        endfor;

        y += y0(i) * p;   
    endfor;
endfunction;
```

## Conclusions

Pretty useful to approximate another polynomials, not that great when it comes to "unusual" functions - it requires many known points in order to work...precisely => pretty bad for a **predictor**. Maybe the factorial function is not the best example here, since it's not that easy to approximate it, but I chose it for simplicity.

On the bright side: might be a nice way to approximate factorials for non-natural numbers.