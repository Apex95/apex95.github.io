---
layout: post
title:  "PyTorch Iterative FGVM: Targeted Adversarial Samples for Traffic-Sign Recognition"
date:   2020-05-01 00:45:05 +0300
categories: ai
image: /imgs/thumbnails/fgvm-gtsrb-adversarial-sample.png
---

Inspired by the progress of driverless cars and by the fact that this subject is not thoroughly discussed I decided to give it a shot at creating smooth **targeted** adversarial samples that are interpreted as legit traffic signs with a high confidence by a PyTorch Convolutional Neural Network (**CNN**) classifier trained on the [GTSRB](http://benchmark.ini.rub.de/?section=gtsrb&subsection=dataset){:rel="nofollow"} dataset. 

I'll be using the Fast Gradient Value Method (**FGVM**) in an iterative manner - which is also called the Basic Iterative Method (BIM). I noticed that most articles only present PyTorch code for non-targeted Fast Gardient Sign Method (FGSM) - which performs well in evading classifiers but is, in my opinion, somehow limited.

{% include image.html url="/imgs/posts/pytorch-iterative-fgvm-targeted-adversarial-samples-traffic-sign-recognition/fgvm-gtsrb-adversarial-sample.png" description="Smooth targeted adversarial sample generated using the current implementation, being misclassified as a 'Stop' sign." %}



##### I'll try to discuss in this article only the important aspects of this problem. However, I also prepared a [Google Colab Notebook](https://colab.research.google.com/drive/1CndPD5ZsW022qO1xgEAWbmcXJwkJKBAX){:rel="nofollow"}.

## Targeted Network

For this experiment, I've constructed a basic **LeNet5** CNN in PyTorch. It performs 2 convolutions of size 5x5 on 32x32 grayscale images, separated by max-pooling. The dataset is slightly unbalanced, but this was compensated for during the training process.



{% include image.html url="/imgs/posts/pytorch-iterative-fgvm-targeted-adversarial-samples-traffic-sign-recognition/gtsrb-results.png" description="Results of the Traffic-Sign Recognition CNN on the GTSRB Test Dataset" %}


This network is represented using the following PyTorch snippet:

```python
class LeNet(nn.Module):
  def __init__(self, num_classes=47, affine=True):

      super().__init__()
      self.conv1 = nn.Conv2d(1, 32, 5)
      self.in1 = nn.InstanceNorm2d(32, affine=affine)

      self.conv2 = nn.Conv2d(32, 64, 5)
      self.in2 = nn.InstanceNorm2d(64, affine=affine)
      
      self.fc1 = nn.Linear(64 * 5 * 5, 256)
      self.fc2 = nn.Linear(256, 128)
      self.fc3 = nn.Linear(128, num_classes)


  def forward(self, x):
      out = F.relu(self.in1(self.conv1(x)))
      out = F.max_pool2d(out, 2)

      out = F.relu(self.in2(self.conv2(out)))
      out = F.max_pool2d(out, 2)
      
      out = out.view(out.size(0), -1)
      
      out = F.relu(self.fc1(out))
      out = F.relu(self.fc2(out))
      out = self.fc3(out)

      return out
```

The architecture is not optimal for the sake of simplicity; additionally, achieving state-of-the-art traffic-sign recognition is not in the scope of this article. Evaluation results on the GTSRB testing set are as follows:
* **Accuracy:** ~95%
* **Precision:** ~93%
* **Recall:** ~93%


## Targeted Adversarial Samples with Iterative FGVM

When **training** a neural network the focus is on optimizing parameters (i.e. weights) in order to minimize the **loss** (e.g.: Mean Squared Error, Cross Entropy, etc.) between the **current output** and **desired output** while the inputs are fixed. This is done through [gradient descent](https://codingvision.net/numerical-methods/gradient-descent-simply-explained-with-example). As an example, if a neural network models the function below, the $$w$$ (weight) and $$b$$ (bias) variables are adjusted during the training.

$$ f(x) = w \cdot x + b$$


When talking about targeted **FGVM**, $$w$$ and $$b$$ are fixed and the input $$x$$ is adjusted through **gradient descent** (computed w.r.t. different variables, obviously). Usually this implies minimizing the error between the **targeted adversarial output** and the **current output** - basically shifting the current output towards the targeted output.

Moreover, when the input is in image-format, additional constraints must be addressed:
* images (inputs) must be clamped between 0 and 1 (float representation)
* images must be smooth in order to mitigate basic noise filtering mechanisms


## PyTorch: Generating Adversarial Samples

The code I ended up with is posted below; further implementation details will also be presented.

```python
targeted_adversarial_class = torch.tensor([INV_TRAFFIC_SIGNS_LABELS['stop']])
adversarial_sample = torch.rand((1, 1, 32, 32)).requires_grad_() 

# optimizer for the adversarial sample
adversarial_optimizer = torch.optim.Adam([adversarial_sample], lr=1e-3)

for i in range(10000):

  adversarial_optimizer.zero_grad()

  prediction = net(adversarial_sample)
  
  # classification loss + 0.05 * image smoothing loss
  loss = torch.nn.CrossEntropyLoss()(prediction, targeted_adversarial_class) + \
          0.05*((torch.nn.functional.conv2d(torch.nn.functional.pad(adversarial_sample, (1,1,1,1), 'reflect'), torch.FloatTensor([[[0, 0, 0], [0, -3, 1], [0, 1, 1]]]).view(1,1,3,3))**2).sum())
  

  # this is the predicted class number
  predicted_class = np.argmax(prediction.detach().numpy(), axis=1)

  # updates gradient and backpropagates errors to the input
  loss.backward()
  adversarial_optimizer.step()

  # ensuring that the image is valid
  adversarial_sample.data = torch.clamp(adversarial_sample.data, 0, 1)

  if i % 500 == 0:
    plt.imshow(adversarial_sample.data.view(32, 32), cmap='gray')
    plt.show()

    print('Predicted:', TRAFFIC_SIGNS_LABELS[predicted_class[0]])
    print('Loss:', loss)
```


The current CNN is trained on 32x32 grayscale images so it makes sense to start with an adversarial sample of same size which consists of random noise distributed over one channel. It is also required to indicate through `requires_grad_()` that this variable should be updated by Autograd.

```python
adversarial_sample = torch.rand((1, 1, 32, 32)).requires_grad_() 
```

Next, an optimizer is created that instead of tweaking weights will tweak the `adversarial_sample` defined above:
```python
adversarial_optimizer = torch.optim.Adam([adversarial_sample], lr=1e-3)
```

The loss function is defined using `torch.nn.CrossEntropyLoss()` - which is the same criterion used for training. In this example, I'll try to create a sample that is classified as a stop sign (`targeted_adversarial_class`). 

```python
targeted_adversarial_class = torch.tensor([INV_TRAFFIC_SIGNS_LABELS['stop']])

prediction = net(adversarial_sample)

# classification loss
loss = torch.nn.CrossEntropyLoss()(prediction, targeted_adversarial_class)
```

This loss function does well in generating adversarial images but the results have a **noisy** aspect (e.g., powerful contrasts between small groups of pixels) and might look suspicious. Since this noise can be easily removed using basic filtering, **smooth** images are wanted. 

Defining a smooth-image constraint can be done by minimizing the **Mean Squared Error** between **adjacent** pixels. Think of it as applying an edge-detection filter and attempting to minimize the overall result. However, this has an impact on the efficiency of the generated sample as it adds dependencies between pixels. To minimize the loss of freedom, only the adjacent pixels from the bottom-right side are taken into account.
The following 3x3 **convolution** kernel is used to determine the color difference between a pixel and its 3 other neighbors:

K | |   
------------ | ------------- | -------------
0 | 0 | 0
0 | -3 | 1
0 | 1 | 1
{: .data-table }


In PyTorch, I implemented the aforementioned method using `torch.nn.functional.conv2d()` and `torch.nn.functional.pad()`:
```python
# image smoothing loss
loss += (torch.nn.functional.conv2d(torch.nn.functional.pad(adversarial_sample, (1,1,1,1), 'reflect'), torch.FloatTensor([[[0, 0, 0], [0, -3, 1], [0, 1, 1]]]).view(1, 1, 3, 3))**2).sum()
```

Finally, the image is clamped to create a valid float tensor using:
```python
adversarial_sample.data = torch.clamp(adversarial_sample.data, 0, 1)
```

Multiple iterations are required in order to properly optimize the input.


## Conclusions

FGVM proves reliable in crafting smooth targeted adversarial samples for basic classifiers implemented with CNNs. However, additional problems need to be addressed in order to become a feasible attack. The crafted sample must be picked up by the segmentation algorithm as a possible traffic sign in the detection phase. Next, the adversarial sample's efficiency should not be impacted by small affine transformations (e.g., being shifted 3 pixels to the left) - this might be fixed through data augmentation. Additionally, factors such as brightness, contrast or various camera properties can still reduce the success rate of an adversarial sample.

Samples which are more resistant to uniformly distributed noise can be obtained by removing the image smoothing constraint.
