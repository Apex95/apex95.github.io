---
layout: post
title:  "Avoid a Mistake: Correctly Calculate Multiclass Accuracy"
date:   2019-12-11 00:45:05 +0300
tags: sklearn python metric
redirect_from: /tips-and-tricks/avoid-a-mistake-correctly-calculate-multiclass-accuracy
image: /imgs/thumbnails/correctly_calculate_multiclass_accuracy.webp
---

Today I held a short laboratory which tackled different metrics used in evaluating classifiers. One of the tasks required that, given the performances of 2 classifiers as **confusion matrices**, the students will calculate the **accuracy** of the 2 models. One model was a **binary classifier** and the other was a **multiclass classifier**.

Many students resorted to googling for an **accuracy formula** which returned the following function:

$$ {\color{Red}{ACC = \frac{TP + TN}{TP + TN + FP +FN}}} $$

Then, they calculated a **'per-class' accuracy** (for class $$i$$, they had $$ ACC_i $$) and **macro-averaged** the results like below:

$$ ACC = \frac{\sum_{i=1}^{i=N}{ACC_i}}{N} $$

To their surprise, the resulted accuracy for the **multiclass classifier** was **erroneous** and highly different (when compared to `accuracy_score()` from **sklearn**). However, the accuracy of the **binary classifier** was correct.

As there wasn't much time available, I told them to use the following **accuracy formula** to match the results of **sklearn** and I'll send an explanation later:

$$ {\color{Green}{ACC = \frac{\sum_{i=1}^{i=N}{TP_i}}{\sum_{i = 1}^{i=N}{(TP_i + FP_i)}}}} $$

Some of you might recognize this as **micro-averaged precision**.

The purpose of this article is to serve as a list of DO's and DONT's so we can avoid such mistakes in the future.


## What was wrong?

Basically, you're prone to get invalid results if you **average** accuracy values in an attempt to obtain the **global accuracy**. But... even if you directly calculate the **global accuracy** using the <span style="color:red">above formula</span>, you'd get skewed values.

Take a look at the following classifier, described using a **confusion matrix**:

\ | Class #0 | Class #1 | Class #2
------------ | ------------- | -------------
**Class #0** | 0 | 100 | 100
**Class #1** | 100 | 0 | 100
**Class #2** | 100 | 100 | 0
{: .data-table }

You'll notice that $$TP = 0$$ thus the classifier is doing a really bad job.

If we follow the students' approach and calculate the **'per-class' accuracy** (let's say **Class #0**), we have:

$$ TP_0 = 0, TN_0 = 200, FP_0 = 200, FN_0 = 200 $$

$$ \color{Red}{ACC_0 = \frac{0 + 200}{0+200+200+200} = 0.333(3)} $$

This already looks suspicious. You'll get the same results for the other 2 classes, so... on average, $$ \color{Red}{ACC = 0.333(3)} $$.
This is definitely wrong.

If you directly compute **global accuracy** using the <span style="color:red">same formula</span> (summing all $$TP's$$, $$TN's$$, ...), you get the same result because of the symmetry. This happens mainly because of the $$ TN $$ in the numerator which grows faster than any other term. In other words, as the number of classes grows, this error grows as well; a similar model, but with **4 classes**, gets a **0.5** accuracy.

Using the <span style="color:green">second formula</span>, the **global accuracy** becomes:

$$ \color{Green}{ACC = \frac{0+0+0}{(0+200) + (0+200) + (0 + 200)} = 0} $$

Which yields, indeed, a better result. Moreover, it generates the same results as `accuracy_score()` from **sklearn**, given more diverse confusion matrices.

##### If you compute **'per class' accuracies** using the <span style="color:green">second formula</span> and average the values, you're basically getting a **macro-averaged precision**. Point is, that's not **accuracy** - so don't do that. 

## Conclusion

I'd recommend avoiding:
* the idea of calculating a **global accuracy** by averaging **'per-class' accuracies**
* the <span style="color:red">red formula</span>, which includes $$ TN $$, since the <span style="color:green">other one</span> returns correct values for any number of classes


Overall, you can compute **precision**, **recall**, **F1** in a 'per-class' manner. But I'm not so sure it also works with the **accuracy**.



