---
layout: post
title:  "PyTorch CRNN: Seq2Seq Digits Recognition w/ CTC"
date:   2020-07-31 00:45:05 +0300
tags: pytorch ocr ctc python conv-neural-network
redirect_from: /ai/pytorch-crnn-seq2seq-digits-recognition-ctc
image: /imgs/thumbnails/rnn-ctc-ocr.png
---

This article discusses handwritten character recognition (**OCR**) in images using *sequence-to-sequence* (**seq2seq**) mapping performed by a *Convolutional Recurrent Neural Network* (**CRNN**) trained with *Connectionist Temporal Classification* (**CTC**) loss. The aforementioned approach is employed in multiple modern OCR engines for handwritten text (e.g., [Google's Keyboard App](https://arxiv.org/pdf/1902.10525.pdf){:rel='nofollow'} - convolutions are replaced with Bezier interpolations) or typed text (e.g., [Tesseract 4's CRNN Based Recognition Module](https://github.com/tesseract-ocr/docs/blob/master/das_tutorial2016/6ModernizationEfforts.pdf){:rel='nofollow'}).

For the sake of simplicity, the example I'll be presenting performs only digit recognition but can be easily extended to accommodate more classes of characters. 

##### The overall source code for this project is quite long so I'm providing a [Google Colab](https://colab.research.google.com/drive/1VRyObLgslpzeB33xITPdm_3E2cAxLuX3?usp=sharing){:rel='nofollow'} document that includes a working example.


## Previous Inadequacies and Justification

> "Why not simply segment characters in the image and recognize them one by one?"

While the approach is, indeed, more straightforward and has been incorporated in older OCR engines, it has its caveats, especially when considering handwritten text. These are caused by the imperfections of the written characters which can produce segmentation issues thus attempting to recognize invalid glyphs or symbols. Consider the following images for clarification:



{% include image.html url="/imgs/posts/pytorch-crnn-seq2seq-digits-recognition/fragmented-characters.png" description="A fragmented '5' is segmented as 2 different characters that are later passed to the recognition module. " %}

{% include image.html url="/imgs/posts/pytorch-crnn-seq2seq-digits-recognition/merged-characters.png" description="The first 2 digits are 'merged' together and considered a single character by both segmentation mechanism and OCR engine." %}

Whereas the MNIST problem is considered solved thus implying that reliable classifiers can be constructed to individually recognize digits, the problem of correct segmentation still remains in realistic scenarios. Splitting or merging glyphs to form valid digits proves to be a difficult challenge and requires additional knowledge to be embedded into the segmentation module.

## Seq2Seq Classifications

In this context, the main advantage brought by a **seq2seq** classifier is that it diminishes the impact of erroneous segmentations and takes advantage of the ability of a neural network to generalize. It only requires a valid segmentation of the word or text line in cause.

Consider the following simplistic model that has a **sliding window** or **mask** (no convolutions), of size `(1, img_height)`. Each set of pixels covered by the sliding window is fed into a neural network made out of neurons with **memory** (e.g., **GRU** or **LSTM**); the job of the neural network is to take a sequence of such stripes and output recognized digits. Take a look at the following figure:

{% include image.html url="/imgs/posts/pytorch-crnn-seq2seq-digits-recognition/one-digit-rnn.png" description="The RNN learns to recognize the digit '5' only by seeing stripes of width equal to 1 of the digit in cause - think of it as time series; by combining information from previous and current inputs, the RNN can determine the correct class." %}

Multiple digits will be included in a single sequence - because we're feeding the network an image which contains more than a digit. It is up to the neural network to determine during the training phase how many stripes to take into account when classifying a digit (i.e., how much to memorize). The image below illustrates how a RNN should 'group' stripes together in order to recognize each digit in the sequence. 

{% include image.html url="/imgs/posts/pytorch-crnn-seq2seq-digits-recognition/rnn-ctc-ocr.png" description="The RNN receives sequences of 'vertical' arrays of pixels (stripes) covered by the sliding window of width equal to 1; once trained, the RNN will be able to memorize that certain sequences of arrays (here in colors) form specific digits and properly separate multiple digits (i.e., 'change the colors') even though they are merged in the given image." %}

Using this method, it is possible to train a neural network by simply saying that the image above contains the numbers '**55207**', without further information (e.g.: alignment, delimitations, bounding boxes etc.) 

## CTC and Duplicates Removal

CTC loss is most commonly employed to train seq2seq RNNs. It works by **summing** the **probabilities for all possible alignments**; the **probability of an alignment** is determined by **multiplying** the probabilities of having specific digits in certain slots. An alignment can be seen as a plausible sequence of recognized digits.

Going back to the '**55207**' example, we can express the probability of the alignment $$ A_{55207} $$ as follows:

$$ P(A_{55207}) = P(A_1 = 5) \cdot P(A_2 = 5) \cdot P(A_3 = 2) \cdot P(A_4 = 0) \cdot P(A_5 = 7)$$

To properly remove duplicates and also correctly handle numbers that contain repeating digits, the **blank** class is introduced, with the following rules:
1. 2 (or more) **repeating digits** are **collapsed** into a single instance of that digit unless separated by **blank** - this compensates for the fact that the RNN performs a classification for each stripe that represents a part of a digit (thus producing duplicates)
2. multiple **consecutive blanks** are **collapsed** into one blank - this compensates for the spacing before, after or between the digits

Given these aspects, there are multiple alignments that, once collapsed, lead to the correct alignment ('**55207**').

For example:
**55-55222--07** once collapsed leads to '**55207**' and suggests the correct sequence even though it has a different structure because of additional duplicates and blanks (marked as '**-**' here). The probability of this alignment ($$ A_{55-55222--07} $$) is computed as previously shown but it also includes the probabilities of the blank class:

$$ P(A_{55-55222--07}) = P(A_1 = 5) \cdot P(A_2 = 5) \cdot P(A_3 = -) \cdot P(A_4 = 5) \cdot P(A_5 = 5) \cdot P(A_6 = 2) \cdot P(A_7 = 2) \cdot P(A_8 = 2) \cdot P(A_9 = -) \cdot P(A_{10} = -) \cdot P(A_{11} = 0) \cdot P(A_{12} = 7)$$


Finally, the CTC probability of a sequence is calculated, as previously mentioned, by summing the probabilities for all different alignments:

$$ P(S_{55207}) = \sum_{A \in Alignments(55207)}{A} $$

When training, the neural network attempts to maximize this probability for the sequence provided as ground truth.

A **decoding** method is used to recover the text from a set of digits probabilities; a naive approach would be to pick, for **each slot** in the **alignment**, the digits with the **highest probability** and then collapse the result. This approach is easier to implement and might be enough for this example although **beam search** (i.e.: greedy approach that picks first N digits with highest probabilities, instead of only one) is employed for such tasks in larger projects.



## Including Convolutional Layers

Implementing convolutions in the previously described model simply implies that raw pixel information is replaced, in the input of the RNN, with higher level features. In PyTorch, the output of the convolution layers must be reshaped to the time sequence format `(batch_size, sequence_length, gru_input_size)`.

In the current project, the output of the convolution part has the following shape: `(batch_size, num_channels, convolved_img_height, convolved_img_width)`. I'm permuting the tensor to `(batch_size, convolved_img_width, convolved_img_height, num_channels)` and then reshaping the last 2 dimensions into one which becomes `gru_input_size`).


## Dataset Generation

To avoid additional steps such as image preprocessing, segmentation and class balancing I picked a more friendly dataset: **EMNIST** for digits. The following helper script randomly picks digits from the dataset, applies affine augmentations and concatenates them into sequences of a given length.

{% include image.html url="/imgs/posts/pytorch-crnn-seq2seq-digits-recognition/dataset-example.png" description="Dataset example for the seq2seq CRNN - Input and Ground Truth" %}

## CRNN Model

A LeNet-5 based convolution model is employed, with the following modifications:
* 5x5 filters are replaced with 2 consecutive 3x3 filters
* max-pooling is replaced with strided convolutions

The resulted higher level features are fed into a **Bi-GRU** RNN with a **linear** layer in the end which has **10** + 1 possible outputs ([0-9] digits + blank). I've chosen **GRU** over **LSTM** since it had similar results but required fewer resources. A `log_softmax` activation function is used in the final layer since it the loss function (PyTorch's `CTCLoss`) requires a logarithmized version of the output; also, this should provide better numerical properties as it highly penalizes incorrect classifications.


```python
class CRNN(nn.Module):

    def __init__(self):
        super(CRNN, self).__init__()

        self.num_classes = 10 + 1
        self.image_H = 28

        self.conv1 = nn.Conv2d(1, 32, kernel_size=(3,3))
        self.in1 = nn.InstanceNorm2d(32)

        self.conv2 = nn.Conv2d(32, 32, kernel_size=(3,3))
        self.in2 = nn.InstanceNorm2d(32)

        self.conv3 = nn.Conv2d(32, 32, kernel_size=(3,3), stride=2)
        self.in3 = nn.InstanceNorm2d(32)

        self.conv4 = nn.Conv2d(32, 64, kernel_size=(3,3))
        self.in4 = nn.InstanceNorm2d(64)

        self.conv5 = nn.Conv2d(64, 64, kernel_size=(3,3))
        self.in5 = nn.InstanceNorm2d(64)

        self.conv6 = nn.Conv2d(64, 64, kernel_size=(3,3), stride=2)
        self.in6 = nn.InstanceNorm2d(64)

        self.postconv_height = 3
        self.postconv_width = 31

        self.gru_input_size = self.postconv_height * 64
        self.gru_hidden_size = 128 
        self.gru_num_layers = 2
        self.gru_h = None
        self.gru_cell = None

        self.gru = nn.GRU(self.gru_input_size, self.gru_hidden_size, self.gru_num_layers, batch_first = True, bidirectional = True)

        self.fc = nn.Linear(self.gru_hidden_size * 2, self.num_classes)

    def forward(self, x):
        batch_size = x.shape[0]

        out = self.conv1(x) 
        out = F.leaky_relu(out)
        out = self.in1(out)

        out = self.conv2(out) 
        out = F.leaky_relu(out)
        out = self.in2(out)

        out = self.conv3(out)
        out = F.leaky_relu(out)
        out = self.in3(out)

        out = self.conv4(out)
        out = F.leaky_relu(out)
        out = self.in4(out)

        out = self.conv5(out)
        out = F.leaky_relu(out)
        out = self.in5(out)

        out = self.conv6(out)
        out = F.leaky_relu(out)
        out = self.in6(out)

        out = out.permute(0, 3, 2, 1) 
        out = out.reshape(batch_size, -1, self.gru_input_size)

        out, gru_h = self.gru(out, self.gru_h)
        self.gru_h = gru_h.detach()
        out = torch.stack([F.log_softmax(self.fc(out[i])) for i in range(out.shape[0])])

        return out

    def reset_hidden(self, batch_size):
        h = torch.zeros(self.gru_num_layers * 2, batch_size, self.gru_hidden_size)
        self.gru_h = Variable(h)

crnn = CRNN()
criterion = nn.CTCLoss(blank=10, reduction='mean', zero_infinity=True)
optimizer = torch.optim.Adam(crnn.parameters(), lr=0.001) 
```

When performing backpropagation, the `CTCLoss` method will take the following parameters:
* `log_probabilities` - this is the output from the `log_softmax`
* `targets` - a tensor which contains the expected sequence of digits
* `input_lengts` - the length of the input sequence after it processed by the convolutional layers (i.e. post-convolution width)
* `target_lengths` - the length of the target sequence

The last 2 parameters (`input_lengths` and `target_lengths`) are used to instruct the `CTCLoss` function to ignore additional padding (in case you added padding to the imagine or the target sequences to fit them into a batch).

`log_probabilities` will look like a `(T, C)`-shaped tensor (T = number of timesteps, C = number of classes) and specifies, for teach timestep, the probability of it belonging in a specific class. This tensor is decoded into text using a **best path** (greedy) approach: for each timestep, this algorithm picks the class with the maximum probability while also collapsing multiple occurences of the same character into one (unless they're separated by a blank).

In my implementation, I've used `y_pred.permute(1, 0, 2)` to match on the CRNN's output to match the `CTCLoss`'s desired input format.


Another aspect you should pay attention to is resetting the **hidden state** of the GRU layers (`crnn.reset_hidden(batch_size)`) before recognizing any new sequence; in my experience this provided better results.

Feel free to check the code on my Google colab (link above) for further details.







## Results

I've tested the model using 10,000 generated sequences: 8,000 for training and 2,000 for testing. Below are the plots for training and testing loss and also the evolution of **precision** - I'm considering that the dataset is approximately balanced. A *true positive* (**TP**) is counted only when the recognized sequence entirely matches the ground truth. The results are not ideal but I think the current model represents a decent starting point for greater projects.

The CRNN manifests some overfitting behavior but the results are acceptable considering its purpose.

{% include image.html url="/imgs/posts/pytorch-crnn-seq2seq-digits-recognition/loss-plot.png" description="Loss Evolution after 6 epochs" %}


{% include image.html url="/imgs/posts/pytorch-crnn-seq2seq-digits-recognition/precision-plot.png" description="Precision Evolution after 6 epochs" %}


After 6 epochs, the CRNN successfully recognizes **7567** out of **8000** sequences in the training set and **1776** out of **2000** from the testing set.


## References

* [An Intuitive Explanation of Connectionist Temporal Classification](https://towardsdatascience.com/intuitively-understanding-connectionist-temporal-classification-3797e43a86c){:rel='nofollow'}
* [Solving CAPTCHA](https://actamachina.com/notebooks/2019/03/28/captcha.html){:rel='nofollow'}