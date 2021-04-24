#import necessary modules
import pygame, math, random
from .exceptions import *

#this class is used from the class ParticleSystem
#it should not be used by the user
class _Particle:
    "This class holds data and modules for a single particle"
    #here we make thing like vector and coordinates
    def __init__(self, time_lived = 0, x = 0, y = 0):
        self.time_lived = time_lived
        self.x = x
        self.y = y
        self.vector = (0, 10)
    #here we can change the vector and give it a little bit of variation
    def set_vector(self, vector, variation):
        self.vector = [vector[0] + random.randint(variation[0], variation[1]), vector[1] + random.randint(variation[0], variation[1])]
    #we can update the particle's position using the vector
    def move(self):
        self.x += self.vector[0]
        self.y += self.vector[1]
    #we can finally blit the particle onto a surface, depending on it's shape
    def blit(self, surface, shape, size, color):
        if shape == "circle":
            pygame.draw.circle(surface, color, (self.x, self.y), size)
        elif shape == "square":
            pygame.draw.rect(surface, color, (self.x, self.y, size, size))
        elif shape[0] == "ellipse":
            pygame.draw.ellipse(surface, color, (self.x, self.y, size * shape[1][0], size  * shape[1][1]),)
        else:
            raise ParticleShapeNotFound

#the ParticleSystem class is what th end user will do
class ParticleSystem:
    "A class to store particle's configs, and data about all of it's particles"
    #we have a lot of variables, size, vector, vector variation and more
    #some of them will be used for making _Particle objects
    #other to specify how much of them and other things
    def __init__(self, shape="circle", size = 5, vector = (0, -1),
                vector_variation = (-5, 5), lifetime = 480, density = 5,
                 color = (255, 255, 255)):
        self.vector = vector
        self.lifetime = lifetime
        self.shape = shape
        self.particles = []
        self.surface = pygame.Surface((7000, 7000))
        self.density = density
        self.vector_variation = vector_variation
        self.size = size
        self.color = color
    #we move every particle, generate some based on the density
    #and we delete dead ones
    def update(self):
        #first of all we fill the surface with an unused
        #color to key out later
        if self.color == (0, 0, 0):
            self.surface.fill((255, 255, 255))
            self.surface.set_colorkey((255, 255, 255))
        else:
            self.surface.fill((0, 0, 0))
            self.surface.set_colorkey((0, 0, 0))
        #then we run a loop as many times as the density
        for _ in range(self.density):
            #we create a new particle with a bit of randomized position
            p = _Particle(x = 350 + int(random.randint(-1*self.size/2.5, self.size/2.5)), y = 350 + int(random.randint(-1*self.size/2.5, self.size/2.5)))
            #we change it's vector to the vector of the particle system
            p.set_vector(self.vector, self.vector_variation)
            #we add it to the particles list
            self.particles.append(p)
        #then we look at our particles
        for particle in self.particles:
            #we delete the ones too old
            if particle.time_lived >= self.lifetime:
                self.particles.remove(particle)
            else:
                #and if they're still to be showed, we increase their lifetime
                particle.time_lived += 1
            #then we move the particle, blit it on the surface and go to the nex one
            particle.move()
            particle.blit(self.surface, self.shape, self.size, self.color)
        #then we return the entire surface
        return self.surface
