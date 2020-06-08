---
layout: post
title:  "Improving Tesseract 4's OCR Accuracy through Image Preprocessing"
date:   2020-06-08 00:45:05 +0300
categories: ai
image: /imgs/thumbnails/tesseract-convolutional-preprocessor.webp
---

In this work I took a look at Tesseract 4's performance at recognizing characters from a challenging dataset and proposed a minimalistic convolution-based approach for input image preprocessing that can boost the character-level **accuracy** from **13.4%** to **61.6%** (+359% relative change), and the **F1 score** from **16.3%** to **72.9%** (+347% relative change) on the aforementioned dataset. The convolution kernels are determined using reinforcement learning; moreover, to simulate the lack of ground truth in realistic scenarios, the **training set** consists of only **30** images while the **testing set** includes **10,000**.

The dataset in cause is called [Brno Mobile](https://pero.fit.vutbr.cz/brno_mobile_ocr_dataset){:rel='nofollow'}, and contains colored photographs of typed text, taken with handheld devices. Factors such as blurriness, low resolution, contrast, brightness are contributing to making the images challenging for an OCR engine.

{% include image.html url="/imgs/posts/improving-tesseract-4-ocr-accuracy-through-image-preprocessing/dataset-sample.webp" description="Resized image from the Brno dataset which contains text that was not recognized by Tesseract 4 during the evaluation (an empty string was returned)" %}

During this experiment, the *out of the box* version of Tesseract 4 has been used, which implies:
* no retraining of the OCR engine
* no lexicon / dictionary augmentations
* no hints about the language used in the dataset
* no hints about segmentation methods; default (automatic) segmentation is used
* default settings for the recognition engine (LSTM + Tesseract)

## Problem Analysis

Tesseract 4 has proven great performance when tested on favorable datasets by achieving good balance between precision and recall. It is presumed that this evaluation is performed on images that resemble scanned documents or book pages (with or without additional preprocessing) in which the number of camera-caused distortions is minimal. Tests on the Brno dataset led to much worse performance that will be discussed later in the article.

{% include image.html url="/imgs/posts/improving-tesseract-4-ocr-accuracy-through-image-preprocessing/tesseract-stats.webp" description="Tesseract 4's performance when evaluated using the Google Books Dataset - taken from [DAS 2016](https://github.com/tesseract-ocr/docs/tree/master/das_tutorial2016){:rel='nofollow'}" %}

In the above figure, a high **precision** indicates favorable *True-Positives* to *False-Positives* ratio thus revealing proper differentiation between characters (i.e. a relatively small number of misclassifications). Despite this, almost no improvements in **recall** can be observed when switching from the **base** classification method to the *Long Short-Term Memory* (**LSTM**) based *Convolutional Recurrent Neural Network* (**CRNN**) for *sequence to sequence* mapping.   

> "Despite being designed over 20 years ago, the current Tesseract classifier is incredibly difficult to beat with so-called modern methods." - Ray Smith, author of Tesseract

I assume that further training for different fonts might not provide significant improvements and neither will a different model of classifier. *Is there a chance that the classifier doesn't receive the correct input?*

It was pointed out in a previous article that [Tesseract is not robust to noise](https://codingvision.net/ai/evaluating-the-robustness-of-ocr-systems); certain *salt-and-pepper* noise patterns disrupt the character recognition process, leading to large segments of text being completely ignored by the OCR engine - the infamous **empty string**. From empirical observations, these errors seem to occur either for a whole word or sentence or not at all thus suggesting a weakness in the segmentation methodology.

The existence of similar behavior, given images which present more natural distortions, is questioned - hence this experiment.


## Black-box Considerations

Since analyzing Tesseract's segmentation methods is a daunting task, I opted for an adaptive external image correction method. To avoid diving into Tesseract 4's source code, the OCR engine is considered a black-box; in this case, an unsupervised learning method must be employed. This ensures easier transitions to other OCR engines as it doesn't directly rely on concrete implementations but only on outputs - at the cost of processing power and optimality.


## Proposed Solution
The solution consists in directly preprocessing images before they are fed to Tesseract 4. An adaptive preprocessing operation is required, in order to properly compensate for any image features that cause problems in the segmentation process. In other words, an input image must be adapted so it complies with Tesseract 4's preferences and maximizes the chance of producing the correct output, preferably without performing down-sampling.

I choose a convolution-based approach for flexibility and speed; other articles tend to perform more rigid image adjustments (such as global changes in brightness, fixed-constant conversion to grayscale, histogram equalization, etc.). I preferred an approach that can properly learn to highlight or mask regions of the image according to various features. For this, the kernels are optimized using reinforcement learning using an actor-critic model. To be more specific, it relies on *Twin Delayed Deep Deterministic Policy Gradient* (**TD3** for short), for discovering features which minimize the *Levenshtein distance* between the **recognized text** and the **ground truth**. I'll not dive into implementation details of TD3 here as it would be somehow out of scope but think of it as a method of optimizing the following formula:

$$ \max_{K1,K2,K3,K4,K5}\sum_{i=1}^{N}{-Levenshtein(OCR(Image_i * K1 * K2 * K3 * K4 * K5),Text_i)}$$

Where $$K_j$$ is a kernel, and $$<Image_i, Text_i>$$ is a tuple from the training set.

##### A short (simpler) proof of concept of the convolutional preprocessor is presented in [this Google Colab](https://colab.research.google.com/drive/1l0qT2S3tkY4WHTRbkVK_J5jATPg0t41-?usp=sharing){:rel='nofollow'}. It uses a different architecture than the final one and has the purpose of verifying if the idea of using convolutions is feasible and offers good results. A comparison is presented between original and preprocessed images including recognized texts for each sample. 

The final model is illustrated below, with **ReLU** activations in-between each convolution step to capture nonlinearities and prevent negative values as pixels' colors.

{% include image.html url="/imgs/posts/improving-tesseract-4-ocr-accuracy-through-image-preprocessing/convolutional-preprocessor.webp" description="Architecture of the Convolutional Preprocessor used to adapt images for Tesseract 4" %}

To properly compensate for image coloring and reduce the number of channels (<span style='color:red'>R</span>, <span style='color:green'>G</span>, <span style='color:blue'>B</span>), 1x1 convolutions are used. This prevents overfitting up to a point while also ensuring grayscale output. Further convolutions are applied only on the grayscale image.

*Symmetry constraints* are additionally enforced for each 3x3 kernel in order to minimize the number of trainable parameters and avoid overfitting. This means that for a 3x3 kernel only 6 variables out of 9 must be determined while the rest can be generated through *mirroring*. Below are the values I got for the five kernels (bold to emphasize symmetry):

| #1 | #2 |  |  | #3 |  |  |
|-|-|-|-|-|-|-|
| <span style='color:red'>**0.7**</span> | 0.2573 | -0.3 | 0.3 | 0.3 | **-0.2996** | 0.3 |
| <span style='color:green'>**1.3**</span> | **0.3** | **1.3** | **-0.295** | 0.3 | **1.2949** | 0.3 |
| <span style='color:blue'>**1.3**</span> | 0.2573 | -0.3 | 0.3 | -0.2802 | **0.2922** | -0.2802 |
{: .data-table }

| #4 |  |  | #5 |  |  |
|-|-|-|-|-|-|
| **-0.2793** | 0.2395 | 0.2885 | -0.294 | -0.2905 | **-0.2939** |
| 0.2395 | **0.7119** | 0.3 | 0.3 | **1.162** | -0.2905 |
| 0.2885 | 0.3 | **-0.2828** | **-0.2328** | 0.3 | -0.294 |
{: .data-table }


## Preprocessing Results

I extracted the image from each convolution layer and clamped its values to the *0-255* interval to properly view each transformation:

{% include image.html url="/imgs/posts/improving-tesseract-4-ocr-accuracy-through-image-preprocessing/transformations.webp" description="Transformations of an image as it passes through the convolutional preprocessor, viewed from left (original) to right (final sample); observe the removal of incomplete characters from the upper-left region" %}


## Comparison

I used 10,000 images from the testing set for the evaluation of the current methodology and compiled the following graphs. The differences between original and preprocessed samples are illustrated with three metrics of interest: *Character Error Rate* (**CER**), *Word Error Rate* (**WER**) and *Longest Common Subsequence Error* (**LCSE**). In this article, **LCSE** is computed as follows:

$$ LCSE(Text_1,Text_2 )=|Text_1 |-|LCS(Text_1,Text_2 )|+|Text_2 |-|LCS(Text_1,Text_2 )| $$



{% include image.html url="/imgs/posts/improving-tesseract-4-ocr-accuracy-through-image-preprocessing/results-comparison.webp" description="<span style='color:green'>Preprocessed</span> vs <span style='color:red'>Original</span> Images from the testing set; lower is better for each metric; dashed lines represent first degree approximations using least squares regression for the ease of interpretation" %}


Additionally, I plotted everything in histogram format to properly see the distributions of errors. For **CER** and **WER**, it is easy to observe the spikes around **1** (100%) that suggest the aforementioned segmentation problem (at block-of-text level) produces the most frequent error (**empty strings** are returned so all characters are wrong). In certain situations, the **WER** is larger than **1** because the preprocessing step introduces artifacts near the border of the image thus leading to recognition of non-existent characters. When looking at the **LCSE** plot, a distribution shift can be seen from the original approximately gaussian shape with its peak (mode) near the average number of characters in an image (**56.95**) to a more favorable shape with overall lower error rates.

{% include image.html url="/imgs/posts/improving-tesseract-4-ocr-accuracy-through-image-preprocessing/results-distributions.webp" description="<span style='color:green'>Preprocessed</span> vs <span style='color:red'>Original</span> Images from the testing set; comparison of distributions of errors" %}

A numeric comparison is presented below:

| Metric | Original (Avg.) | Preprocessed (Avg.) |
|-|-|-|
| CER | 0.866 | 0.384 |
| WER | 0.903 | 0.593 |
| LCSE | 48.834 | 24.987 |
| Precision | 0.155 | 0.725 |
| Recall | 0.172 | 0.734 |
| F1 Score | 0.163 | 0.729 |
{: .data-table }

## Takeaways

Significant improvements can be observed through this preprocessing operation. Moreover, the majority of errors probably do not occur in the *sequence to sequence* classifier (since all the recognized characters are erroneous and would contradict previous performance analysis). A page-segmentation issue, when automatic mode is used seems more plausible. It is shown that an array of convolutions is sufficient, in this case, to decrease error rates substantially.

The OCR performance on the preprocessed images is overall better but not good enough to be reliable. A 38% character error rate is still a large setback. I'm pretty sure that better recognitions can be obtained with more fine-tuning, a more complex architecture for the convolutional preprocessor and a more diverse training set. However, the current implementation is already very slow to train which makes me question if the entire methodology is feasible from this point of view.



