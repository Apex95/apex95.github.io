---
layout: post
title:  "C# Making a Neural Network that plays Flappy Bird"
date:   2017-08-01 00:45:05 +0300
tags: genetic-algorithm neural-network unsupervised-learning
redirect_from: /ai/c-making-a-neural-network-that-plays-flappy-bird
image: /imgs/thumbnails/flappy_bird_ann.webp
---

All right, people; now that I'm done with the projects & finals for...a couple of days...I thought it would be a good idea
to keep an old promise and finally publish this article too. It's about how to make a **neural network** that learns to play a simple game (**Flappy Bird** in this case) - and training it with a **genetic algorithm**.
This way, maybe, I won't have to answer any more comments on YouTube...


Btw, here's a short demo:
<iframe width="560" height="315" src="https://www.youtube.com/embed/UmDeboEOIfM" frameborder="0" allowfullscreen></iframe>



Hopefully I can still understand the code that I wrote ~7 months ago. Yep.

##### this was my first project that involved this kind of stuff...the code is rather sketchy and I don't really have the time to rewrite it - probably better than nothing but...sorry. The encoding / decoding parts can be skipped - however the most important part is to grasp the idea behind it. Can't say I really recommend implementing your own GA's.



## Basics

Well, to better understand this concept, a good starting point is to think of how you play this game: what are the <u>factors</u> that you take into account?
How do you know when the bird should jump? 

Pretty sure you are probably using a set of metrics like the following ones:

- horizontal distance between the bird and the closest set of pipes (**dist1**)
- vertical distance between the bird and the lower pipe (**dist2**)
- vertical distance between the bird and the upper pipe (**dist3**)

{% include image.html url="/imgs/posts/c-making-a-neural-network-that-plays-flappy-bird/1.png" description="Metrics used as Inputs for the Neural Network" %}


What we actually want now is a **function** that takes these **3 parameters** and has **1 output** (because the whole game can be resumed to a single command).

$$ f(dist_1, dist_2, dist_3) = \left\{\begin{matrix}
> 0.5 => jump()\\ 
<= 0.5 => do\_nothing
\end{matrix}\right. $$

Considering we don't know the relationship between the 3 distances, we can try to approximate the behavior of this function using a **neural network**.

In my project I used a network with:

- 3 input neurons
- 2 hidden ones
- 1 output neuron.

---
I'm going to presume you know the basics of multilayer neural networks - especially the forward propagation (y'know, that part where you multiply each input with the corresponding weight, then sum all of this and pass it to
an activation function...and the result gets fed as an input to a neuron from the next layer). I'm using the matrix version in this code because it looks a little bit more "elegant", but it's the same formula, ok?


## The training part

Ehm...this is tricky. We don't have a training set - so...we can't use the traditional **gradient descent** (we don't know the derivatives of the error function) for our neural network.

The alternative is to empirically find a set of **weights** using a **genetic algorithm**. Basically you start with a generation of birds which are rather...dumb
(they will either spam the jump command or not jump at all) - because the weights used by their neural networks are initially some random values. The goal is to simulate the evolutionary process
(survival of the fittest) so you'll obtain a generation of birds that will jump perfectly each time.

<u>Here are the steps:</u>

1. Start with N sets of random weights (that means N different networks) - this would be the first generation.
2. Allow each network to play until the bird hits a pipe and save the **scores**
3. Keep only the sets of weights that performed better than the others (first M from a list ordered by score) - these will make it to the next generation. Also keep the solutions with the highest score (this is called **elitism**, btw. - it's needed because you may not know if your new solutions are better than the old ones)
4. Pick 2 sets from the new population of weights, **encode** them, apply **crossover** (also **mutation**) and then **decode**. Save the results and add them to the new generation too.
5. Go back to step 2 and repeat until you get decent results.


## Fitness function

Now let's talk a bit about the function that assigns the score; it's quite an important part too, because it makes the difference between an algorithm that 
actually converges and one that just runs mindlessly and picks random / wrong solutions.

Usually it's not a good idea to say that the in-game score is the actual score of a solution; the approach doesn't offer a score with a good
"granularity" so you can end up with the algorithm not making a difference between a bird that actually learned to go between pipes but hits one by mistake and another which just hit the ground (they'll both have a 0 score).

It's not wrong, indeed, but it takes waaay too much time for the algorithm to discover a better solution - we need to offer a few more *hints*.

So...we can also take into account:

- how long the bird stayed alive (provides more accurate scores)
- the distance between the bird's last position and the center of the space between the pipes (because we prefer the birds that were actually close and didn't try to go straight through the pipe).

The fitness function that I used looks like this (if the in-game score is greater than 0)

`(game.time + game.score) / (1 + Math.Abs(game.floppy_bird.birdPosition.Y - centerPos) / 100) * 0.01f`

and this one if the bird didn't pass any group of pipes:

`weightsList[crtIndex].fitness = (game.time + game.score);`



## Mutation & Crossover Rates / Population Size

Another important part too; **crossover** tries to "center" the population around the best solution so far (in an attempt to rise the average score of the generation) while **mutation** brings diversity by altering
various *genes* (in our case weights), enabling the algorithm to discover better (or worse) solutions.

Anyway, the whole point is to keep these in a balance; values that are too high or too low will not lead to convergence. Also a population size that is too large will just slow down the whole process but going with a small number
of candidates could limit your search domain - so there's a chance of getting stuck in an unsatisfying local optimum. 

In my code I used a **CROSSOVER_RATE** of **0.8** and a **MUTATION_RATE** of **0.05**, with **POPULATION_SIZE** = **25**. 

I know this might look boring (it's already written in the code snippet, right?) but I felt that it should be mentioned here just in case someone encounters this exact problem. This and a wrong fitness function are usually
the main reasons the algorithm might not work as expected.



## Additional notes

It is fair to also mention this; there might be cases when a good solution fails (the bird hits one of the first pipes) and is thrown away (lost) - and the algorithm kind of falls back.
I guess it's probably caused by a particular set of distances that won't make the neural network trigger the jump function (considering that the pipes are random, there might be a chance).

Might be a good idea to make some kind of average between the previous scores and the current score. Never tried it though...

Aand...this project also uses some fancy **mutex synchronization** between processes - so multiple instances of the same game can share the best solution between them using a **memory mapped file** (*lazy parallelization* as I like to call it).
Wrote an article about using memory mapped files, you can find it here: [/tips-and-tricks/c-send-data-between-processes-w-memory-mapped-file](https://www.codingvision.net/tips-and-tricks/c-send-data-between-processes-w-memory-mapped-file).


## TODOs

Finally some small improvements that could prove useful; they're not included in the code but implementing them might boost the performance:

- picking weights for **crossover** using a weighted random function (**roulette wheel selection**); this way better solutions have a higher chance
to create new candidates for the next generation
- **weighted crossovers** - this implies that instead of a simple arithmetic mean between the weights you should assign more "importance" to the solution
which has a higher score (**weighted arithmetic mean**).
- adding a few random weights in each new generation (boosting diversity).


## Sourcecode

Ok, enough of me talking; I know this is the part that gets the most attention - that's why I'm always writing it at the end :P

*// I'm publishing only the part that is relevant - because I consider that having a wall of code attached in an article looks rather bad from the reader's point of view.*


```csharp

using Floppy_Bird;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading;

namespace ANN_FlappyBird
{
    public class ANN
    {
        [Serializable]
        public class WeightsInfo
        {
            // hidden layer weights
            public double[,] weights1;
            
            // output layer weights
            public double[,] weights2;
            
            // score
            public float fitness;

            public WeightsInfo(double[,] weights1, double[,] weights2, float fitness)
            {
                this.weights1 = weights1;
                this.weights2 = weights2;
                this.fitness = fitness;
            }

            public WeightsInfo()
            {
                this.fitness = 0;
                this.weights1 = new double[inputSize, hiddenSize];
                this.weights2 = new double[hiddenSize, outputSize];
            }
        }

        Game1 game;
        Random r = new Random();

        static int inputSize, hiddenSize, outputSize;
        double[,] input, output;

        List<WeightsInfo> weightsList = new List<WeightsInfo>();
        List<WeightsInfo> nextWeightsList = new List<WeightsInfo>();

        int crtIndex = 0;

        // this is for sharing data between processes
        DataSharer dataSharer = new DataSharer();
        Mutex mmfMutex = null;


        public ANN(Game1 game)
        {
            this.game = game;
        }

        // spawns the first generation of birds (w/ random weights)
        public void createFirstGeneration()
        {
            inputSize = 3;
            hiddenSize = 2;
            outputSize = 1;


            for (int k = 0; k < POPULATION_SIZE; k++)
            {
                double[,] _weights1 = new double[inputSize, hiddenSize];

                for (int i = 0; i < _weights1.GetLength(0); i++)
                    for (int j = 0; j < _weights1.GetLength(1); j++)
                        _weights1[i, j] = r.NextDouble() * 2 - 1;


                double[,] _weights2 = new double[hiddenSize, outputSize];

                for (int i = 0; i < _weights2.GetLength(0); i++)
                    for (int j = 0; j < _weights2.GetLength(1); j++)
                        _weights2[i, j] = r.NextDouble() * 2 - 1;

                weightsList.Add(new WeightsInfo(_weights1, _weights2, 0));
            }

        }

        float min = float.MaxValue;
        float minTowerY = 1, maxTowerY = 1;
        float distanceToTower = 0;
        float minDistanceToTower = 0;

        float centerPos = 0;

        // called by the game's update() method
        // returns: true if the bird should jump, false otherwise
        public bool runForward()
        {
            min = float.MaxValue;

            // indentifies the closest tower
            for (int i = 0; i < game.tower1.Count; i++)
            {
                distanceToTower = Math.Abs(game.tower1[i].towerPosition.X - game.floppy_bird.birdPosition.X - game.floppy_bird.birdRectangle.Width);

                if (distanceToTower < min)
                {
                    min = distanceToTower;
                    minDistanceToTower = distanceToTower;
                    maxTowerY = game.tower2[i].towerPosition.Y; 
                    minTowerY = maxTowerY - game.difference; 

                    centerPos = (maxTowerY + minTowerY) / 2;
                }
            }

            // the inputs for the neural network
            input = new double[1, inputSize];

            input[0, 0] = 1 - minDistanceToTower / (game.graphics.PreferredBackBufferWidth - game.floppy_bird.birdPosition.X - game.floppy_bird.birdRectangle.Width);
            input[0, 1] = (game.floppy_bird.birdPosition.Y + game.floppy_bird.birdRectangle.Height - maxTowerY) / game.graphics.PreferredBackBufferHeight;
            input[0, 2] = (game.floppy_bird.birdPosition.Y - minTowerY) / game.graphics.PreferredBackBufferHeight;

            // computing the inputs & outputs for the hidden layer
            double[,] hiddenInputs = multiplyArrays(input, weightsList[crtIndex].weights1);
            double[,] hiddenOutputs = applySigmoid(hiddenInputs);

            // then the final output
            output = applySigmoid(multiplyArrays(hiddenOutputs, weightsList[crtIndex].weights2));

           
            

            return output[0, 0] > 0.5;


        }


        // the whole encode / decode process (just for learning purposes)
        void encode(WeightsInfo weightsInfo, List<double> gene)
        {
            for (int i = 0; i < weightsInfo.weights1.GetLength(0); i++)
                for (int j = 0; j < weightsInfo.weights1.GetLength(1); j++)
                {
                    gene.Add(weightsInfo.weights1[i, j]);
                }

            for (int i = 0; i < weightsInfo.weights2.GetLength(0); i++)
                for (int j = 0; j < weightsInfo.weights2.GetLength(1); j++)
                {
                    gene.Add(weightsInfo.weights2[i, j]);
                }
        }
        
        void decode(WeightsInfo weightsInfo, List<double> gene)
        {
            for (int i = 0; i < weightsInfo.weights1.GetLength(0); i++)
                for (int j = 0; j < weightsInfo.weights1.GetLength(1); j++)
                {
                    weightsInfo.weights1[i, j] = gene[0];
                    gene.RemoveAt(0);
                }

            for (int i = 0; i < weightsInfo.weights2.GetLength(0); i++)
                for (int j = 0; j < weightsInfo.weights2.GetLength(1); j++)
                {
                    weightsInfo.weights2[i, j] = gene[0];
                    gene.RemoveAt(0);
                }
        }

        // creates a new candidate solution using crossover
        void crossover(List<double> gene1, List<double> gene2)
        {
            if (r.NextDouble() > CROSSOVER_RATE)
                return;


            List<double> descendant1 = new List<double>();
            List<double> descendant2 = new List<double>();

            // mixing the genes using the arithmetic mean
            for (int i = 0; i < gene1.Count; i++)
            {
                descendant1.Add((gene1[i] + gene2[i]) / 2.0);
                descendant2.Add((gene1[i] + gene2[i]) / 2.0);
            }
            

            // decoding the result back to the "weights-format"
            WeightsInfo weightsInfo1 = new WeightsInfo();
            decode(weightsInfo1, descendant1);
            nextWeightsList.Add(weightsInfo1);


            WeightsInfo weightsInfo2 = new WeightsInfo();
            decode(weightsInfo2, descendant2);
            nextWeightsList.Add(weightsInfo2);

        }

        // randomly adjusts a weight in order to improve it
        bool mutate(List<double> gene)
        {
            bool mutated = false;

            for (int i = 0; i < gene.Count; i++)
            {
                if (r.NextDouble() < MUTATION_RATE)
                {
                    gene[i] += (r.NextDouble() * 2 - 1);
                    mutated = true;
                }
            }

            return mutated;
        }

        // selection function for crossover (picks the better one from 2 random candidates)
        WeightsInfo select()
        {
            int i1 = 0;
            int i2 = 0;

            while (i1 == i2)
            {
                i1 = r.Next(0, weightsList.Count / 3);
                i2 = r.Next(0, weightsList.Count / 3);
            }

            if (weightsList[i1].fitness > weightsList[i2].fitness)
                return weightsList[i1];
            else
                return weightsList[i2];
        }


        double CROSSOVER_RATE = 0.8;
        double MUTATION_RATE = 0.05;
        int POPULATION_SIZE = 25;

        float averageFitness = 0;
        float maxFitness = 0;
        int generation = 0;

        public void breedNetworks()
        {

            // updates the score
            if (game.score == 0)
                weightsList[crtIndex].fitness = (game.time + game.score) / (1 + Math.Abs(game.floppy_bird.birdPosition.Y - centerPos) / 100) * 0.01f;
            else
                weightsList[crtIndex].fitness = (game.time + game.score);

            averageFitness += weightsList[crtIndex].fitness;
            maxFitness = maxFitness > weightsList[crtIndex].fitness ? maxFitness : weightsList[crtIndex].fitness;


            if (crtIndex + 1 < weightsList.Count)
                crtIndex++;
            else
            {
                crtIndex = 0;
                generation++;

                Debug.WriteLine("GEN: " + generation + " | AVG: " + averageFitness / (float)POPULATION_SIZE + " | MAX: " + maxFitness);
                averageFitness = 0;
                maxFitness = 0;


                weightsList = weightsList.OrderByDescending(wi => wi.fitness).ToList();

                // starting with a large mutation rate so there's will be more solutions to choose from
                if (weightsList[0].fitness < 2)
                    MUTATION_RATE = 0.9;
                else
                    MUTATION_RATE = 0.05;

                // adding better solutions from the other instances (if any)
                if (nextWeightsList.Count + 3 <= POPULATION_SIZE)
                {
                    // the whole synchronization thingy
                    try
                    {
                        if (mmfMutex == null)
                            mmfMutex = Mutex.OpenExisting("Global\\mmfMutex");

                        if (mmfMutex.WaitOne())
                        {

                            WeightsInfo wi = new WeightsInfo();
                            wi = dataSharer.getFromMemoryMap();
                            
                            if (wi == null || wi.fitness < weightsList[0].fitness)
                            {
                                if (wi == null)
                                    Debug.WriteLine("Updated - NULL -> " + weightsList[0].fitness);

                                if (wi != null)
                                    Debug.WriteLine("Updated - " + wi.fitness + " -> " + weightsList[0].fitness);

                                dataSharer.writeToMemoryMap(weightsList[0]);
                            }

                            if (wi != null && wi.fitness > weightsList[0].fitness)
                            {
                                nextWeightsList.Add(wi);
                            }

                            mmfMutex.ReleaseMutex();
                        }
                    }
                    catch (WaitHandleCannotBeOpenedException ex)
                    {
                        mmfMutex = new Mutex(true, "Global\\mmfMutex");
                        nextWeightsList.AddRange(weightsList.Take(3));

                        mmfMutex.ReleaseMutex();
                    }

                    // adding elites to the next generation
                    nextWeightsList.AddRange(weightsList.Take(3));
                }

                // creating a new generation 
                while (nextWeightsList.Count < POPULATION_SIZE)
                {
                    WeightsInfo w1 = select();
                    WeightsInfo w2 = select();


                    while (w1 == w2)
                    {
                        w1 = select();
                        w2 = select();
                    }

                    List<double> gene1 = new List<double>();
                    List<double> gene2 = new List<double>();

                    encode(w1, gene1);
                    encode(w2, gene2);


                    crossover(gene1, gene2);

                    if (mutate(gene1))
                        w1 = new WeightsInfo();

                    if (mutate(gene2))
                        w2 = new WeightsInfo();

                    decode(w1, gene1); 
                    decode(w2, gene2); 

                    if (!nextWeightsList.Contains(w1))
                        nextWeightsList.Add(w1);
                    
                    if (!nextWeightsList.Contains(w2))
                        nextWeightsList.Add(w2);
                }

                weightsList.Clear();
                nextWeightsList = nextWeightsList.OrderByDescending(wi => wi.fitness).ToList();


                weightsList.AddRange(nextWeightsList);

                nextWeightsList.Clear();
            }
        }

        // -- below are some methods used to compute the outputs of the neural networks

        #region MathHelpers

        double[,] applySigmoid(double[,] array)
        {
            for (int i = 0; i < array.GetLength(0); i++)
                for (int j = 0; j < array.GetLength(1); j++)
                    array[i, j] = sigmoid(array[i, j]);

            return array;
        }

        double sigmoid(double x)
        {
            return 1.0 / (1.0 + Math.Exp(-x));
        }

        double[,] multiplyArrays(double[,] a1, double[,] a2)
        {
            double[,] a3 = new double[a1.GetLength(0), a2.GetLength(1)];

            for (int i = 0; i < a3.GetLength(0); i++)
                for (int j = 0; j < a3.GetLength(1); j++)
                {
                    a3[i, j] = 0;
                    for (int k = 0; k < a1.GetLength(1); k++)
                        a3[i, j] = a3[i, j] + a1[i, k] * a2[k, j];
                }
            return a3;
        }
        #endregion MathHelpers
    }
}

```


## Auxiliary files

The **DataSharer** class:

```csharp
using System;
using System.Diagnostics;
using System.IO;
using System.IO.MemoryMappedFiles;
using System.Runtime.Serialization.Formatters.Binary;

namespace ANN_FlappyBird
{
    class DataSharer
    {
        MemoryMappedFile mmf = null;

        public void writeToMemoryMap(ANN_FlappyBird.ANN.WeightsInfo weightsInfo)
        {
            const int MMF_MAX_SIZE = 1024;  
            const int MMF_VIEW_SIZE = 1024;

            if (mmf == null)
                mmf = MemoryMappedFile.CreateOrOpen("mmf1", MMF_MAX_SIZE, MemoryMappedFileAccess.ReadWrite);

            MemoryMappedViewStream mmvStream = mmf.CreateViewStream(0, MMF_VIEW_SIZE);

            BinaryFormatter formatter = new BinaryFormatter();
            formatter.Serialize(mmvStream, weightsInfo);
            mmvStream.Seek(0, SeekOrigin.Begin);


        }


        public ANN.WeightsInfo getFromMemoryMap()
        {
            const int MMF_VIEW_SIZE = 1024;

            ANN.WeightsInfo weightsInfo = null;

            if (mmf == null)
            {
                try
                {
                    mmf = MemoryMappedFile.OpenExisting("mmf1");
                    weightsInfo = new ANN.WeightsInfo();
                }
                catch (Exception ex)
                {
                    Debug.WriteLine(ex.StackTrace);
                    weightsInfo = null;
                    return weightsInfo;
                }
            }
           
            MemoryMappedViewStream mmvStream = mmf.CreateViewStream(0, MMF_VIEW_SIZE);

            BinaryFormatter formatter = new BinaryFormatter();

            // needed for deserialization
            byte[] buffer = new byte[MMF_VIEW_SIZE];

            if (mmvStream.CanRead)
            {
                mmvStream.Read(buffer, 0, MMF_VIEW_SIZE);

                weightsInfo = (ANN_FlappyBird.ANN.WeightsInfo)formatter.Deserialize(new MemoryStream(buffer));
            }
            else
                weightsInfo = null;

            return weightsInfo;
        }
    }
}
```






