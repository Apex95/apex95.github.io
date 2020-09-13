---
layout: post
title:  "Hamming Error Correction - with Example"
date:   2016-06-30 20:02:05 +0300
tags: error-correction algorithm
redirect_from: /networking/hamming-error-correction-w-example
image: /imgs/thumbnails/hamming.webp
---

This article will focus on **Hamming** codes - mainly, this represents an attempt to explain a little bit better
how this method can help in **detecting** and **correcting**... **1 bit errors**. 

This method is not really useful
at "higher level" - just because the data we work with is either 100% correct or has way more than 1 bit corrupted - and in this
case, the Hamming code _doesn't work_. It seems to be used in low-level (data link layer) networking and in some DRAMs - to prevent interferences
from corrupting data.


As an example, we can consider this **byte** of data: `11010010`


## Hamming Encoding

The encoding implies taking the bits of the original message and computing a set of *parity/control bits* that will help us detect
possible errors - we'll know which bit is flipped, so the correction consists in **negating** that one bit. 
In the end, we insert the parity bits at positions equal to *powers of 2* (1,2,4,8,...).

The encoded message will look like this: <span style="color:red;">P<sub>1</sub></span><span style="color:red;">P<sub>2</sub></span>D<sub>1</sub><span style="color:red;">P<sub>4</sub></span>D<sub>2</sub>D<sub>3</sub>D<sub>4</sub><span style="color:red;">P<sub>8</sub></span>D<sub>5</sub>D<sub>6</sub>D<sub>7</sub>D<sub>8</sub>
- where **D** is a data bit, from our original message, and **P** a parity bit => **12 bits**.

In order to determine the formulas for the parity bits it is important to understand the following part:

We say that a bit at position **n**, from our encoded data, is "controlled" by the **parity bits** whose positions, once summed, are equal to **n**.
This can be written as:

<table border="1" style = "border-collapse: collapse;">
<tr><th>Position (n)</th><th>Bit</th><th>is controlled by parity bit(s)</th></tr>
<tr><td>1</td><td>P<sub>1</sub></td><td><span style="color:red;">P<sub>1</sub></span></td></tr>
<tr><td>2</td><td>P<sub>2</sub></td><td><span style="color:red;">P<sub>2</sub></span></td></tr>
<tr><td>3</td><td>D<sub>1</sub></td><td><span style="color:red;">P<sub>1</sub></span> + <span style="color:red;">P<sub>2</sub></span></td></tr>
<tr><td>4</td><td>P<sub>4</sub></td><td><span style="color:red;">P<sub>4</sub></span></td></tr>
<tr><td>5</td><td>D<sub>2</sub></td><td><span style="color:red;">P<sub>1</sub></span> + <span style="color:red;">P<sub>4</sub></span></td></tr>
<tr><td>6</td><td>D<sub>3</sub></td><td><span style="color:red;">P<sub>2</sub></span> + <span style="color:red;">P<sub>4</sub></span></td></tr>
<tr><td>7</td><td>D<sub>4</sub></td><td><span style="color:red;">P<sub>1</sub></span> + <span style="color:red;">P<sub>2</sub></span> + <span style="color:red;">P<sub>4</sub></span></td></tr>
<tr><td>8</td><td>P<sub>8</sub></td><td><span style="color:red;">P<sub>8</sub></span></td></tr>
<tr><td>9</td><td>D<sub>5</sub></td><td><span style="color:red;">P<sub>1</sub></span> + <span style="color:red;">P<sub>8</sub></span></td></tr>
<tr><td>10</td><td>D<sub>6</sub></td><td><span style="color:red;">P<sub>2</sub></span> + <span style="color:red;">P<sub>8</sub></span></td></tr>
<tr><td>11</td><td>D<sub>7</sub></td><td><span style="color:red;">P<sub>1</sub></span> + <span style="color:red;">P<sub>2</sub></span> + <span style="color:red;">P<sub>8</sub></span></td></tr>
<tr><td>12</td><td>D<sub>8</sub></td><td><span style="color:red;">P<sub>4</sub></span> + <span style="color:red;">P<sub>8</sub></span></td></tr>
</table>

\* notice that the sum of the indexes is equal to the position, for each row.

&nbsp;

From the table, we observe that: 

*   <span style="color:red;">P<sub>1</sub></span> "controls" data bits: D<sub>1</sub>, D<sub>2</sub>, D<sub>4</sub>, D<sub>5</sub>, D<sub>7</sub>.
*   <span style="color:red;">P<sub>2</sub></span> "controls" data bits: D<sub>1</sub>, D<sub>3</sub>, D<sub>4</sub>, D<sub>6</sub>, D<sub>7</sub>.
*   <span style="color:red;">P<sub>4</sub></span> "controls" data bits: D<sub>2</sub>, D<sub>3</sub>, D<sub>4</sub>, D<sub>8</sub>.
*   <span style="color:red;">P<sub>8</sub></span> "controls" data bit: D<sub>5</sub>, D<sub>6</sub>, D<sub>7</sub>, D<sub>8</sub>.

If we know this, we can write the **equations** for the **parity bits**:

<span style="color:red;">P<sub>1</sub></span> = D<sub>1</sub> ^ D<sub>2</sub> ^ D<sub>4</sub> ^ D<sub>5</sub> ^ D<sub>7</sub>

<span style="color:red;">P<sub>2</sub></span> = D<sub>1</sub> ^ D<sub>3</sub> ^ D<sub>4</sub> ^ D<sub>6</sub> ^ D<sub>7</sub>

<span style="color:red;">P<sub>4</sub></span> = D<sub>2</sub> ^ D<sub>3</sub> ^ D<sub>4</sub> ^ D<sub>8</sub>

<span style="color:red;">P<sub>8</sub></span> = D<sub>5</sub> ^ D<sub>6</sub> ^ D<sub>7</sub> ^ D<sub>8</sub>

\* that's **XOR** between them, ok?


&nbsp;

&nbsp;

If we apply this theory to our **example** `11010010`, we get:

<span style="color:red;">P<sub>1</sub></span> = 1 ^ 1 ^ 1 ^ 0 ^ 1 = 0

<span style="color:red;">P<sub>2</sub></span> = 1 ^ 0 ^ 1 ^ 0 ^ 1 = 1

<span style="color:red;">P<sub>4</sub></span> = 1 ^ 0 ^ 1 ^ 0 = 0

<span style="color:red;">P<sub>8</sub></span> = 0 ^ 0 ^ 1 ^ 0 = 1

So the encoded data is: <span style="color:red;">01</span>1<span style="color:red;">0</span>101<span style="color:red;">1</span>0010.



## Hamming Decoding


This part verifies the original bits and flips one of them if it's corrupted.
Keeping the same **example**, we use the value that we determined before, but to make it more interesting, we'll **corrupt 1 bit**.

original: 011010110<span style="color:green;">0</span>10

corrupted: 011010110<span style="color:red;">1</span>10

\* in this case I corrupted a **data bit** - if a **parity bit** gets **corrupted** there's no need to correct anything, we only care about the data bits.


We have to recalculate the parity bits, but this time we'll also include their values (taken from the encoded data):

<span style="color:red;">P<sub>1</sub></span> = <span style="color:red;">P<sub>1</sub></span> ^ D<sub>1</sub> ^ D<sub>2</sub> ^ D<sub>4</sub> ^ D<sub>5</sub> ^ D<sub>7</sub>

<span style="color:red;">P<sub>2</sub></span> = <span style="color:red;">P<sub>2</sub></span> ^ D<sub>1</sub> ^ D<sub>3</sub> ^ D<sub>4</sub> ^ D<sub>6</sub> ^ D<sub>7</sub>

<span style="color:red;">P<sub>4</sub></span> = <span style="color:red;">P<sub>4</sub></span> ^ D<sub>2</sub> ^ D<sub>3</sub> ^ D<sub>4</sub> ^ D<sub>8</sub>

<span style="color:red;">P<sub>8</sub></span> = <span style="color:red;">P<sub>8</sub></span> ^ D<sub>5</sub> ^ D<sub>6</sub> ^ D<sub>7</sub> ^ D<sub>8</sub>



If there were no bits corrupted, each new parity bit should be **0** (because we're **XOR**-ing 2 identical bits).
Replacing the values with the ones in the **example**, we get:

<span style="color:red;">P<sub>1</sub></span> = <span style="color:red;">0</span> ^ 1 ^ 1 ^ 1 ^ 0 ^ 1 = 0

<span style="color:red;">P<sub>2</sub></span> = <span style="color:red;">1</span> ^ 1 ^ 0 ^ 1 ^ 1 ^ 1 = 1

<span style="color:red;">P<sub>4</sub></span> = <span style="color:red;">0</span> ^ 1 ^ 0 ^ 1 ^ 0 = 0

<span style="color:red;">P<sub>8</sub></span> = <span style="color:red;">1</span> ^ 0 ^ 1 ^ 1 ^ 0 = 1


&nbsp;

This result is somehow obvious since I flipped/corrupted the **6th bit of data**, and from the formulas, only <span style="color:red;">P<sub>2</sub></span> and 
<span style="color:red;">P<sub>4</sub></span> include that bit. 

However, in a general case we won't know which bit is corrupted...so here's how these **parity bits** become useful. We use them to create the 
**sindrome**, so we arrange these bits like this:

<span style="color:red;">P<sub>8</sub>P<sub>4</sub>P<sub>2</sub>P<sub>1</sub></span>

and by replacing, we get this number in binary: `1010` (10 in decimal) => the **10th** bit, in the encoded data, is corrupted and needs some flippin'.
Aand...finally, we get the original encoded message: `011010110010`. From here, we extract the data bits => `11010010`.


## The end

That's all...probably not the most interesting article, but my teachers seem to love this subject (especially during the finals), 
so...just trying to help.
