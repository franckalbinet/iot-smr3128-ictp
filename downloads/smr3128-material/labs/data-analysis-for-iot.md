Data analysis for IoT
==

我听见 我忘记; 我看见 我记住; 我做 我了解
*"I hear and I forget. I see and I remember. I do and I understand." --
 Confucius*


In this tutorial, we assume that we have collected some sensory data on Thingspeak, and it is time now to start analyzing it, in the hope of finding useful information. 

There are many possible reasons for wanting to explore the data:
* Monitoring some process, area, or phenomenon: what is the status, is it normal?
* Finding out if something is changing, if so, in what direction? What will happen in the future?
* Comparing and classifying different items: is this plant healthy or sick, is this insect a dangerous pest?

Always the end goal is to find sufficient information for *decision making*. This means that correct data processing is extremely important: mistakes or failures in data processing can result in wrong decisions, causing financial loss and even danger to people.

The best advice for getting good information out of the data is simple: *hire a professional!* A trained statistician will evaluate the data, using classical statistical tools or fashionable Machine Learning methods, as appropriate. They will find out not just trends and classifications, but also the uncertainty of the results.

However, we don't always have the luxury of hiring statisticians. In this tutorial we will take a look at some data processing techniques that are within reach for all of us, using Python with open source libraries and packages. 

We will work on two common tasks:
1. Time series analysis: cleaning the data, prediction
2. Classification: using Machine Learning to separate two or more classes of images


For the tutorial, we use the following resources:
* A Thingspeak account with a channel
* Python libraries for time series analysis
* Python libraries for image classification

In a [separate tutorial](thing-speak-and-data-analysis-for-iot.md) I review how to get your data streaming to Thingspeak. If you want, you can visit it to refresh your knowledge.

Here we assume that you are already familiar with data collection, and start with the analysis part.


## Time Series Analysis

If you have your data in the cloud, often you have the option of doing your analysis there, without retrieving (downloading) the data. For instance, Thingspeak.com offers online MATLAB scripting for its users.

The advantage of local processing, instead of using e.g. Thingspeak's MATLAB service, is that cloud-based systems might not work well for *weakly connected* regions. When the net is down or congested, we would be stuck with waiting; while once we have downloaded the data, we can work with it at our leasure. 

Here we will first see how to retrieve data using Python, then we will analyze it also with Python libraries.

### Retrieving data from Thingspeak

Consider my two public datasets on Thingspeak:
1. [mygarden](https://thingspeak.com/channels/283445): about 8000 datapoints (humidity, temperature, barometric pressure) collected by a TI Sensortag
2. [soil](https://thingspeak.com/channels/285666): about 2000 datapoints (soil moisture) collected by a nodeMCU processor



We can download directly the accumulated data by navigating to “mygarden” -> “Data Import/Export” -> “Export” -> “Download”. This will result in a CSV formatted spreadsheet, that is readable by e.g. LibreOffice.

Thingspeak also provides a Python interface for accessing uploaded data:
http://thingspeak.readthedocs.io/en/latest/index.html

We can use it either on the command line, or in a Python program. First, let’s try to just get a CSV file from “My Little Garden”.

`thingspeak -q -r 100 -f csv 283445 > garden.csv`

Unfortunately, the resulting file is not really a CSV file, only a printout of the data in Python format. Actually, CSV output is not yet implemented for the thingspeak Python module, only JSON; CSV download is waiting for someone to implement <hint hint>!

On the other hand, working inside Python we can do better, creating any file formats, or processing the data directly. Getting the same data and then printing it out as a text file suitable for further processing is not much more difficult:

```Python
import thingspeak
import time
import sys

def main(count=8000):
  ch = thingspeak.Channel(283445)
  r=ch.get({'results': count})
  e=eval(r)
  f=e['feeds']
  x1=[eval(t['field1']) for t in f]
  x2=[eval(t['field2']) for t in f]
  x3=[eval(t['field3']) for t in f]
  tx=[time.mktime(time.strptime(t['created_at'],"%Y-%m-%dT%H:%M:%SZ")) for t in f]
  f=open("garden.dat","w")
  for i in range(len(x1)):
    f.write("%f %f %f %f\n" % (tx[i],x1[i],x2[i],x3[i]))
  f.close()

if __name__ == "__main__":
  main()
```

The generated datafile “garden.dat” is fine for plotting by Gnuplot, or for reading into Python.
The same method can be used to retrieve the second example channel as "soil.dat".

### Analyzing the data with Python

From this point we are using the **pandas** module, which implements a rich set of time series manipulations. You can get **pandas** using *pip* or *pip3*. 

For the first tests we will use the soil moisture dataset. First, let's just plot it as it is, using *matplotlib*. We read in the data, then call the plotting function.

```python
# https://ocefpaf.github.io/python4oceanographers/blog/2015/03/16/outlier_detection/
from pandas import read_table
import matplotlib.pyplot as plt

# Read in the data file 
fname = 'soil.dat'
cols = ['t', 'u']
df = read_table(fname , delim_whitespace=True, names=cols)

plt.plot(df['t'],df['u'])
plt.show()
```

![](https://i.imgur.com/z5LFpN6.png)

There are suspicious data points at around 0.9 hour and 1.5 hour. As the soil moisture probably cannot jump up and down, these are measurement errors.

We can try to remove them by *median filtering*. The median filter is a simple non-linear filter: for each data point, it sorts the values before and after it, then takes the middle value.

We can use the median filter from the scikit package:

```python
from scipy.signal import medfilt
df['m'] = medfilt(df['u'])

plt.plot(df['t'],df['m'])
plt.show()
```

The result is much more believable:

![](https://i.imgur.com/oaRAsXI.png)

One advantage of the median filter can be seen in the graph: the step at time 1.1 is kept intact. This is in contrast with other (linear) filtering techniques; they would reduce the high frequency components, thus the steps in the data would be delayed and smoothed out.

You will need to balance the advantage of getting smoother, more visible graphs, against the potential loss of information hidden in the noise.

### Prediction of time series data

The first prediction test will use the **Pyflux** library, which provides statistical time-series processing. We follow the example given at their website:
http://www.pyflux.com/arimax-models/

For prediction, we use the garden data (which is actually just local weather data). Let us see a plot of the temperature (field2): 

```Python=
# http://www.pyflux.com
from pandas import read_csv
from pandas import datetime
from pandas import DataFrame
from statsmodels.tsa.arima_model import ARIMA
from matplotlib import pyplot
 
def parser(x):
	return datetime.strptime('190'+x, '%Y-%m')
 
series = read_csv('mygarden.csv', header=0, parse_dates=[0], index_col=0, squeeze=True) 

series=series.loc[:,('created_at','field2')]
series=series.set_index('created_at');
X = series.values
pyplot.plot(X)
pyplot.show();
```
This gives the graph of all temperature values:

![](https://i.imgur.com/VzXkHpN.png)


Let us use only the last 3 days, and only every 10th observations.

```Python=
X = X[4000:]
X = [X[t] for t in range(0,len(X),10)]
pyplot.plot(X)
pyplot.show();
```

![](https://i.imgur.com/Y5EbSbl.png)

Now we can construct an ARIMA model and use it as a rolling predictor: predict the next observation, then extend the history with the next actual observation.

```Python=
# fit model
size = int(len(X) * 0.66)
train, test = X[0:size], X[size:len(X)]
history = [x for x in train]
predictions = list()
for t in range(len(test)):
	model = ARIMA(history, order=(5,1,0))
	model_fit = model.fit(disp=0)
	output = model_fit.forecast()
	yhat = output[0]
	predictions.append(yhat)
	obs = test[t]
	history.append(obs)
	#print('predicted=%f, expected=%f' % (yhat, obs))
error = mean_squared_error(test, predictions)
print('Test MSE: %.3f' % error)
# plot
pyplot.plot(test)
pyplot.plot(predictions, color='red')
pyplot.show()

```

![](https://i.imgur.com/i0e4UdS.png)

The result shows that while the prediction sometimes overshoots, it can generally follow the trend in the data.


## Image Classification

An image (photo, video) is a powerful tool to obtain information about many things: plants, animals, people, buildings, roads, equipment, almost anything that we can *imagine*.

The question is: after collecting images, what can we do with them? If there are only a few, human classification is difficult to beat; we are extremely skilled image processors. We can look at the images and tell: this one is a firefly, this one is a cockroach, ...

However, if it comes to thousands or millions of images, human processing is no longer an attractive option. We want automatic processing, which is now getting increasingly more and more feasible, fortunately. We will now try our hand on automatic image classification.

Let us consider a hypothetical example. We have collected two sets of images about **Item X**:
* Images of **Item X** in a desirable state
* Images of **Item X** in a bad state

Now we want to create a classifier, that when we feed it a new image of **Item X**, it tells us if it is good or bad.

The following Python program, taken from the [Mahotas tutorials](http://mahotas.readthedocs.io/en/latest/classification.html), does this training:
```Python=
#!/usr/bin/env python
from glob import glob
import mahotas
import mahotas.features
import milk

def features_for(imname):
    img = mahotas.imread(imname)
    return mahotas.features.haralick(img).mean(0)

def learn_model(features, labels):
    learner = milk.defaultclassifier()
    return learner.train(features, labels)

def classify(model, features):
     return model.apply(features)

positives = glob('positives/*')
negatives = glob('negatives/*')
unlabeledP = glob('unlabeledP/*')
unlabeledN = glob('unlabeledN/*')

features = map(features_for, negatives + positives)
labels = [0] * len(negatives) + [1] * len(positives)

model = learn_model(features, labels)

labeledP = [classify(model, features_for(u)) for u in unlabeledP]
labeledN = [classify(model, features_for(u)) for u in unlabeledN]
print labeledP
print labeledN
```
Let us call the program `classify.py`, put it in a directory `~/AItest`, and make it executable.

To run the program, we need to create four directories:

* `positives`
* `negatives`
* `unlabeledP`
* `unlabeledN`

The classifier is trained on the labeled samples in the `positives` and `negatives`, then we can test it on the unlabeled samples, which are nevertheless known to belong to the *positive* or *negative* class.

### First example: oranges

Let us try first classifying two sets of mandarine oranges. I have bought two bags in a market in Kobe: one bag of good quality mandarines, they are the **positives**, and one of half-price poor quality ones, the **negatives**. You can find the dataset here.

A "positive" sample:
![](https://i.imgur.com/JQWt8jT.jpg)

A "negative" sample:
![](https://i.imgur.com/S5yK6OL.jpg)


After creating the directory under `AItest` with the four subdirectories, we go there, and execute the Python program:

```
~/AItest/classify.py
```

This will execute the program in the current directory, where it will find the four subdirectories that it needs.

The result of execution is shown here:

> [1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
> [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

We can see that the classification of the two unlabeled sets is good but not perfect. Perhaps we can try to look at the mis-classified item, and think about the reason for the mistake.

### Second example: leaves

We can repeat the same process with another dataset, found here. These are photos of two clusters of bushes in the Kyoto Botanical Garden: a healthy one (the **positives**) and a diseased one (the **negatives**). I have also made a dataset with reduced image sizes: the originals are JPEGs with 1632x1080 resolution; I have reduced it to 408x270. 

A healthy plant:
![](https://i.imgur.com/9TxF72f.jpg)

A less healthy one:
![](https://i.imgur.com/rtAXNql.jpg)



Running `classifier.py` on the original images gives us:

> [1, 1, 1, 1]
> [0, 0, 0, 0]

So far, so good.
However, running it on the reduced-size image sets gives:

> [1, 1, 1, 1]
> [0, 0, 1, 0]

There is now a mis-classification.

### What goes on behind the curtain?

We are using machine learning with pre-processed image data. The pre-processing is done in `Line 9` of the program: Mahotas provides the "Haralick features" pre-processing algorithm, which looks at the texture of the image, and gives a short numerical vector. The machine learning algorithm then creates a classifier, that will give us a result `1` for vectors that are close to those in the **positives** class, and `0` for those in the **negatives**.

We can immediately raise some questions:

1. Is this pre-processing suitable for *any* image classification?
2. Is it enough to train with the two classes? What happens if we give the classifier that is neither **positive** nor **negative**, but instead a shot of Beyonce?

"Deep Learning" is the answer of the image processing community to the first question. Instead of trying to design good pre-processors, now the trend is to let the algorithms themselves create optimal pre-processors for the task, from the samples. This is an extremely hot topic right now, just ask Google!...

For classification in general, we would like to get not just a binary value: this image looks more like "A", rather than "B". We want a certainty level: it is "A" with probability 15%, "B" with probability 7% (so probably it is neither, with probability 78%).
