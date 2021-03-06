import pygame
from pygame.locals import *
from constant import *
import numpy as np
import uuid

X = np.array(([2, 9], [1, 5], [3, 6]), dtype=float)
y = np.array(([92], [86], [89]), dtype=float)
xPredicted = np.array(([4,8]), dtype=float)

# scale units
X = X/np.amax(X, axis=0) # maximum of X array
xPredicted = xPredicted/np.amax(xPredicted, axis=0) # maximum of xPredicted (our input data for the prediction)
y = y/100 # max test score is 100

class Neural_Network(object):
    def __init__(self, layers=None):
        #parameters
        self.inputSize = 2
        self.outputSize = 1
        self.hiddenSize = 6

        #weights
        self.W1 = np.random.randn(self.inputSize, self.hiddenSize) # (3x2) weight matrix from input to hidden layer
        self.W2 = np.random.randn(self.hiddenSize, self.outputSize) # (3x1) weight matrix from hidden to output layer

    def forward(self, X):
        #forward propagation through our network
        # print(f"X: {X}")
        # print(f"self.W1: {self.W1}")
        self.z = np.dot(X, self.W1) # dot product of X (input) and first set of 3x2 weights
        # print(f"self.z: {self.z}")
        self.z2 = self.sigmoid(self.z) # activation function
        self.z3 = np.dot(self.z2, self.W2) # dot product of hidden layer (z2) and second set of 3x1 weights
        o = self.sigmoid(self.z3) # final activation function
        return o

    def sigmoid(self, s):
        # print(f"s: {s}")
        # activation function
        return 1/(1+np.exp(-s))

    def sigmoidPrime(self, s):
        #derivative of sigmoid
        return s * (1 - s)

    def backward(self, X, y, o):
        # backward propagate through the network
        self.o_error = y - o # error in output
        self.o_delta = self.o_error*self.sigmoidPrime(o) # applying derivative of sigmoid to error

        self.z2_error = self.o_delta.dot(self.W2.T) # z2 error: how much our hidden layer weights contributed to output error
        self.z2_delta = self.z2_error*self.sigmoidPrime(self.z2) # applying derivative of sigmoid to z2 error

        self.W1 += X.T.dot(self.z2_delta) # adjusting first set (input --> hidden) weights
        self.W2 += self.z2.T.dot(self.o_delta) # adjusting second set (hidden --> output) weights

    def train(self, X, y):
        o = self.forward(X)
        self.backward(X, y, o)

class Bird(pygame.sprite.Sprite):
    def __init__(self, layers=None, radius=round(H/30)):
        pygame.sprite.Sprite.__init__(self)
        self.id = uuid.uuid4()
        self.x = W/4
        self.y = H/2 #np.random.randint(30, H-30)
        self.vx = 0
        self.vy = 0
        self.radius = radius
        self.score = 0
        self.color = (np.random.randint(50, 255),
                      np.random.randint(50, 255),
                      np.random.randint(50, 255))
        self.maxvy = .3
        self.rect = pygame.Rect(self.x-self.radius,
                                self.y-self.radius,
                                self.radius,
                                self.radius)
        self.alive = True
        self.score = 0
        self.obstaclex = 0
        self.obstacley = 0
        if layers is None:
            self.model = Neural_Network()
        else:
            self.model = Neural_Network(layers)

    def fitness(self):
        pass

    def set_layers(self, layers):
        self.model.W1 = layers[0]
        self.model.W2 = layers[1]

    def get_layers(self):
        return [self.model.W1, self.model.W2]

    def jump(self, jump_speed=.15):
        self.vy -= jump_speed
        if self.vy <= self.maxvy:
            self.vy = -self.maxvy

    def update(self, dt, g=.03):
        if abs(self.vy) <= self.maxvy:
            self.vy += g
        self.y += self.vy * dt * BOOST
        self.y = round(self.y)

    def draw(self, output):
        self.rect = pygame.Rect(self.x-self.radius,
                                self.y-self.radius,
                                self.radius,
                                self.radius)
        pygame.draw.circle(output, self.color, (round(self.x), round(self.y)), self.radius)

    def get_features(self, obstacle):
        self.obstaclex = obstacle.x+obstacle.w/2
        self.obstacley = obstacle.y
        self.dist = (self.obstaclex+obstacle.w/2 - self.x) / W
        self.height = (self.obstacley - self.y) / H
        return np.array([self.dist, self.height]).reshape((1,2))

    def draw_features(self, output):
        pygame.draw.line(output, TEST_COLOR, (self.x, self.y), (self.obstaclex, self.y), 3)
        pygame.draw.line(output, TEST_COLOR, (self.x, self.y), (self.x, self.obstacley), 3)

    def draw_goal(self, output):
        pygame.draw.circle(output, TEST_COLOR, (round(self.obstaclex), round(self.obstacley)), 3)
