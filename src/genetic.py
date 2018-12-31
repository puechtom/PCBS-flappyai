import pygame
from pygame.locals import *
from constant import *
import numpy as np
from obstacle import Obstacle
from bird import Bird
from world import World
from pprint import pprint

pygame.init()
screen = pygame.display.set_mode((W, H+HUD_H), DOUBLEBUF)
screen.set_alpha(None)
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 25)
hud_background = pygame.Rect(0, H, W, HUD_H)

class GeneticAlg(object):
    def __init__(self):
        self.birds = []
        self.nbBirds = 50
        for i in range(self.nbBirds):
            self.birds.append(Bird())
        self.gen = 0
        self.best_score = 0

    def simulate(self):
        pygame.time.wait(200)
        world = World(self.birds)
        clock = pygame.time.Clock()
        done = False
        c = 0
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                exit()
            if len([bird for bird in world.birds if bird.alive])==0:
                done = True

            dt = clock.tick(60)
            screen.fill(BG_COLOR)

            c+=1
            score_surface = myfont.render("Score: {}".format(c), True, (0, 0, 0))

            for bird in [bird for bird in world.birds if bird.alive]:
                obstacle = None
                min_dist = W
                for obs in world.obstacles:
                    if obs.x > bird.x and (obs.x - bird.x) < min_dist:
                        obstacle = obs
                        min_dist = (obs.x - bird.x)
                if not obstacle is None:
                    features = bird.get_features(obstacle)
                    prediction = bird.model.forward(features)
                    if prediction > 0.5:
                        bird.jump()
                    bird.score = c
                    bird.fitness = - abs(list(features[0])[0]) - abs(list(features[0])[1])
                    bird.fit = c*100 - abs(list(features[0])[0])

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                for bird in [bird for bird in world.birds if bird.alive]:
                    bird.jump()

            world.update(dt)
            world.draw(screen)

            pygame.draw.rect(screen, (255, 255, 255), hud_background)
            screen.blit(score_surface, (2,H))
            best_score_srf = myfont.render("Best: {}".format(self.best_score),
                                               True, (0, 0, 0))
            screen.blit(best_score_srf, (2,H+20))
            gen_surface = myfont.render("Generation: {}".format(self.gen),
                                               True, (0, 0, 0))
            screen.blit(gen_surface, (W/2-60,H))
            fps_surface = myfont.render("FPS: {:.0f}".format(clock.get_fps()),
                                        True, (0, 0, 0))
            screen.blit(fps_surface, (W-65,H))

            pygame.display.flip()

        if c > self.best_score:
            self.best_score = c

    def sort_birds(self, birds):
        scores = []
        for bird in birds:
            scores.append(bird.fit)
        return [birds[i] for i in np.argsort(scores)[::-1]]

    def fitness(self):
        pass

    def evolve(self, retain=.2, random=.05, mutation=.01):
        def crossover(bird1, bird2, k=1):
            b1_layers = bird1.get_layers()
            b2_layers = bird2.get_layers()

            b_layers = []
            for layers in zip(b1_layers, b2_layers):
                flatten_layer1 = layers[0].flatten()
                flatten_layer2 = layers[1].flatten()
                flatten_layers = [flatten_layer1, flatten_layer2]
                length = len(flatten_layer1)
                k_points = [0]
                k_points += sorted(np.random.choice(range(0, length), k))
                k_points.append(length)
                choices = []
                for i, (k1, k2) in enumerate(zip(k_points, k_points[1:])):
                    for n in range(k2-k1):
                        choices.append(i%2)
                b_layer = []
                for i, c in enumerate(choices):
                    b_layer.append(flatten_layers[c][i])
                b_layer = np.array(b_layer).reshape(layers[0].shape)
                b_layers.append(b_layer)

            bird = Bird()
            bird.set_layers(b_layers)
            return bird

        def mutate(bird, k=1):
            layers = bird.get_layers()
            lengths = []
            for layer in layers:
                lengths.append(layer.shape[0]*layer.shape[1])
            choice = np.random.randint(0, len(layers))
            layer = layers[choice]
            x = np.random.randint(0, layer.shape[0])
            y = np.random.randint(0, layer.shape[1])
            value = np.random.randn()
            layers[choice][x][y] = value
            bird.set_layers(layers)

        self.gen += 1
        new_birds = []
        retain_length = int(len(self.birds)*retain)
        sorted_birds = self.sort_birds(self.birds)
        new_birds += sorted_birds[:retain_length]
        random_length = int(len(self.birds)*random)
        new_birds += list(np.random.choice(sorted_birds[retain_length:],
                                           random_length))
        childrens = []
        for i in range(self.nbBirds-len(new_birds)):
            c = sorted(np.random.choice(range(0, len(new_birds)), 2))
            children = crossover(new_birds[c[0]], new_birds[c[1]])
            if np.random.randn() < random:
                mutate(children)
            childrens.append(children)

        new_birds += childrens

        del(self.birds)
        self.birds = new_birds
