# Flappy Ai: A genetic algorithm approach

![demo](https://i.imgur.com/qOK2TIC.gifv)

The goal of this project was to try out neural networks with genetic algorithms. In order to do this, I choosed a flappy bird like game due to its simplicity of development. The aim is to implement little birds with really simple "brains" and let them try to go as far as possible in the virtual world. When all the birds are dead, we select the best ones, make them reproduce to create a new generation of bird and we start the process over again. After a few generation, thanks to natural selection principle, we should see some interesting behaviours appearing in the population and at each new generation, the birds should performs better.

## Virtual world
The virtual world is composed of obstacles and the birds have to avoid them in order to progress in the virtual world.

Obstacles are composed of two parts, the top one and the bottom one. We can adjust the difficulty of the obstacles by changing three parameters:
* the distance between the top and bottom parts
* the distance between two obstacles
* the range in which the hole in the obstacle can be placed


## Birds
Each bird has a small neural network which can be roughly assimilated to their "brain". This neural network is composed of 3 layers of neurons. The first layer is the input layer, the second layer is called the hidden layer and the third one is the output of the network.




## Genetic algorithm
