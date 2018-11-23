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
        for i in range(10):
            self.birds.append(Bird())
        self.gen = 0
        self.best_score = 0

    def simulate(self):
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
                bird.score = c
                # print(bird.model.layers)
                # print("config\n")
                # pprint(bird.model.get_config())
                # pprint(bird.model.get_weights())
                # print(bird.model.get_weights()[0][0][:6])
                # print(bird.model.get_weights()[0][0][6:])
                # exit()
                # print("first layer")
                # print("weights\n", bird.model.layers[0].get_weights()[0])
                # print("biases\n", bird.model.layers[0].get_weights()[1])
                # print("second layer")
                # print("weights\n", bird.model.layers[1].get_weights()[0])
                # print("biases\n", bird.model.layers[1].get_weights()[1])
                # exit()
                obstacle = None
                for obs in world.obstacles:
                    if obs.x > bird.x:
                        obstacle = obs
                        break
                if not obstacle is None:
                    features = bird.get_features(world.obstacles[0])
                    # print(f"features shape {features.shape}")
                    # print(f"features {features}")
                    prediction = bird.model.predict(features)
                    # print(prediction)
                    if prediction > 0.5:
                        bird.jump()

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

    def get_best(self, birds, n=2):
        scores = []
        for bird in birds:
            scores.append(bird.score)
        return [birds[i] for i in np.argsort(scores)[::-1][:n]]

    def fitness(self):
        pass

    def evolve(self):
        def crossover(bird1, bird2):
            layer1_w1, layer1_b1, layer2_w1, layer2_b1 = bird1.model.get_weights()
            layer1_w2, layer1_b2, layer2_w2, layer2_b2 = bird2.model.get_weights()

            # print("bird1")
            # pprint(bird1.model.get_weights())
            # print("layer1_w1")
            # print(layer1_w1)
            # print("bird2")
            # pprint(bird2.model.get_weights())

            layer1_w = []
            for l in range(layer1_w1.shape[0]):
                choices = np.random.random_integers(0, 1, layer1_w1.shape[1])
                for i, c in enumerate(choices):
                    layer1_w.append([layer1_w1[l], layer1_w2[l]][c][i])
            layer1_w = np.array(layer1_w).reshape(layer1_w1.shape)
            layer1_b = layer1_b1
            layer2_w = []
            for l in range(layer2_w1.shape[0]):
                choices = np.random.random_integers(0, 1, layer2_w1.shape[1])
                for i, c in enumerate(choices):
                    layer2_w.append([layer2_w1[l], layer2_w2[l]][c][i])
            layer2_w = np.array(layer2_w).reshape(layer2_w1.shape)
            layer2_b = layer2_b1
            weights = [layer1_w, layer1_b, layer2_w, layer2_b]
            bird = Bird()
            bird.model.set_weights(weights)
            return bird

        def mutate(bird):
            layer1_w, layer1_b, layer2_w, layer2_b = bird.model.get_weights()
            w1 = list(layer1_w.flatten())
            # print(w1)
            indices = np.random.randint(0, len(w1), 2)
            for i in indices:
                w1[i] = np.random.random_sample(1)-.5
            # print(w1)
            w1 = np.array(w1).reshape(layer1_w.shape)
            w2 = list(layer2_w.flatten())
            indices = np.random.randint(0, len(w2), 2)
            for i in indices:
                w2[i] = np.random.random_sample(1)-.5
            w2 = np.array(w2).reshape(layer2_w.shape)
            weights = [w1, layer1_b, w2, layer2_b]
            bird.model.set_weights(weights)

        self.gen += 1
        best_birds = self.get_best(self.birds)
        # for i, bird in enumerate(best_birds):
        #     print(i, "score:", bird.score)
        new_birds = []
        for i in range(8):
            new_birds.append(crossover(best_birds[0], best_birds[1]))
        for bird in new_birds:
            mutate(bird)
        for i in range(2):
            new_birds.append(Bird())
        self.birds = new_birds
