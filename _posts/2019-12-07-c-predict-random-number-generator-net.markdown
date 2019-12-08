---
layout: post
title:  "C# Predict the Random Number Generator of .NET"
date:   2019-12-07 00:45:05 +0300
categories: security
thumbnail: /imgs/thumbnails/predict_random_net.png
---

This post targets to underline the **predictability** of the random... or better said **pseudo-random number generator** (PRNG) exposed by the **.NET** framework (aka the `Random()` class), under certain assumptions. Because of the nature of the implementation, **100% accuracy** can be obtained with a fairly simple idea and a rather short code snippet.

##### The presented method definitely isn't something new in the domain of cryptography, however the purpose of the article is to bring awareness about this specific weakness.

The following scenario is considered:

* **no access** to the **process's memory**
* must work for **any chosen seed**
* a limited set of generated **random numbers** is **visible** to the attacker
* we focus on `Random.nextDouble()` as there is no data loss because **int casting**

I'll be presenting a short summary of the algorithm used by `Random()` and how can we predict the random numbers. If you feel like going directly to code, scroll down to the bottom of the article.

## The Random class

While many pseudo-random implementations (e.g., libc's `rand()`) rely on a [Linear Congruential Generator (LCG)](https://en.wikipedia.org/wiki/Linear_congruential_generator) which generates each number in the sequence by taking into account the previous one, I discovered that **.NET**'s **random number generator** uses a different approach.

By looking at the implementation of the `Random()` class ([available here](https://referencesource.microsoft.com/#mscorlib/system/random.cs)), one can easily observe that pseudo-random number generation is based on a [Subtractive Generator](https://rosettacode.org/wiki/Subtractive_generator), which permits the user to specify a custom seed or use `Environment.TickCount` (system's uptime in milliseconds) as default.

The core of the pseudo-random generator is the `InternalSample()` (line #100) method which constructs the sequence of numbers. `Random.nextDouble()` will actually call the `Sample()` method which returns the value of `InternalSample()` divided by `Int32.MaxValue`, as this is claimed to improve the distribution of random numbers.
Without going into much details regarding the included gimmicks, we can describe the generator as follows:

$$ R_i = R_i - R_j, j=i+21 $$

$$ R_i = \left\{\begin{matrix}
R_i - 1, if (R_i = Int32.Max)\\ 
R_i, else
\end{matrix}\right. $$

$$ R_i = \left\{\begin{matrix}
R_i + Int32.Max, if (R_i < 0)\\ 
R_i, if (R_i \geqslant 0)
\end{matrix}\right. $$


$$ retVal = \frac{R_i}{Int32.Max} $$

where $$R_i$$ contributes to describing the state of the algorithm and $$retVal$$ is, obviously, the returned value.

To store the state of the pseudo-random number generator, a **circular array** of **56 ints** is employed - this means $$ i $$ and $$ j $$ will get re-initialized to **1** whenever they exceed the length of the array - however the **offset** of **21** remains constant.



## Predicting Random Numbers

In my opinion, it seems rather difficult to determine the starting state of the algorithm without knowing the seed. But... we notice that the algorithm is outputting pseudo-random numbers which properly describe each value of its state array.

In other words, if we have access to a randomly generated number $$ retVal $$, we can compute $$ R_i $$ and $$ R_i $$ is used to generate future states & numbers in the sequence. However, we will need values for $$ i = 1,55 $$ in order to cover all the properties. 

##### If we manage to leak a continuous set of **55** generated numbers, we have enough information to describe and construct a new generator (by providing a circular array of states) which will output the same numbers as the original but can be used as a predictor.


In my implentation, I'm using the following trick to simplify the things: I don't convert the leaked $$ retVal $$ back to $$R_i$$ (by multiplying with the `Int32.MaxValue`) because I'll have to divide it again to compare the results. So I'm working directly with differences of leaked values (instead of differences of $$ R_i $$'s) -- I hope it makes sense.

Here's the code I used, it should help clear things up.

{% highlight csharp linenos %}		
public class Program
{
	/* predicts random numbers, given 2 state descriptors */
	public static double computeDiffAndOffset(double r1, double r2)
	{
		double diff = r1 - r2;
		
		if (diff == Int32.MaxValue)
			diff=- 1/(double)Int32.MaxValue;
		if (diff < 0)
			return diff + 1;
		else
			return diff;
	}
	
	public static void Main()
	{
		/* this we break */
		Random r = new Random();
		
		/* describes the state of the subtractive generator */
		double[] SeedArray = new double[56];
		
		/* leaking the state by observing the first 55 random numbers */
		for (int i = 1; i < 56; i++)
			SeedArray[i] = r.NextDouble();
		
		/* the offset is known from the original implementation */
		int offset = 21;
		
		/* from the theory part: i = index1, j = index2 */
		int index1 = 1, index2 = index1 + offset;
		
		/* running a few tests */
		for (int i = 0; i < 1000; i++)
		{
			/* handling the circular array limits */
			if (index1 >= 56)
				index1 = 1;
			
			if (index2 >= 56)
				index2 = 1;
			
			/* this is the predicted random number */
			double predictedValue = computeDiffAndOffset(SeedArray[index1], SeedArray[index2]);

			/* this is the correct random number */
			double correctRandom =  r.NextDouble();
			
			/* we compare them as doubles */
			if (Math.Abs(predictedValue - correctRandom) > 0.00001)
				throw new Exception(String.Format("Failed at {0} vs {1}", predictedValue, correctRandom));
			
			/* printing the results */
			Console.WriteLine("Predicted: " + predictedValue + " | Correct: " + correctRandom);

			/* updating the state of the generator */
			SeedArray[index1] = predictedValue;
			
			index1++;
			index2++;
		}
	}
}
{% endhighlight %}


You should get something like this when running it (well, different numbers because you'll have a different seed - but you get the point). Tested it on **.NET 4.7.2**.

```
Predicted: 0.562743733899083 | Correct: 0.562743733899083
Predicted: 0.0782367256834342 | Correct: 0.0782367256834343
Predicted: 0.48149561019684 | Correct: 0.48149561019684
Predicted: 0.768610569075034 | Correct: 0.768610569075034
Predicted: 0.288163338456379 | Correct: 0.288163338456379
Predicted: 0.652038850659523 | Correct: 0.652038850659523
Predicted: 0.331446861071254 | Correct: 0.331446861071255
Predicted: 0.573066327056413 | Correct: 0.573066327056413
[...]
```

## Conclusions

Definitely don't use `Random()` for cryptographic functions. Bad idea.
However, limiting the information provided to the adversary (i.e. hiding the randomly generated numbers) would greatly diminish the effectiveness of this attack.

Not much else to be said. It's my first take at breaking something which is not an LCG - it might not be state-of-the-art level (performance-wise) but I hope you found this informative.