import numpy as np
import p3.pad
import p3.config as c
from p3.agent import Agent

class Fox:
    def __init__(self):
        self.agent       = 0
        self.agents      = []
        self.generation  = 0

    def reset(self):
        self.agent  = 0
        self.agents = []

    def add_agent(self, nnet):
        self.agents.append(Agent(len(self.agents), nnet))

    def get_ind_fitness(self, ind):
        fits = []
        for a in self.agents:
            fits.append(a.fitness)
        return fits

    def advance(self, state, pad, mm):
        if self.agent < len(self.agents):
            if state.frame % 1 == 0:
                self.agents[self.agent].fit(state, pad)
            if state.frame % 4 == 0:
                self.agents[self.agent].advance(state, pad)
            if state.frame % 300 == 0:
                self.agent += 1
        return self.agent