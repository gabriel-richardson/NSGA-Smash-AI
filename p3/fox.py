import numpy as np
import p3.pad
import p3.config as c
from p3.agent import Agent

class Fox:
    def __init__(self):
        self.agent       = 0 # individual agent number
        self.agents      = [] # list of agents
        self.generation  = 0 # generation number

    def reset(self):
        self.agent  = 0
        self.agents = []

    # Add agent to agents list
    def add_agent(self, nnet):
        self.agents.append(Agent(len(self.agents), nnet))

    # Return list of fitness values for all agents
    def get_ind_fitness(self, ind):
        fits = []
        for a in self.agents:
            fits.append(a.fitness)
        return fits

    # Advance frame by 1
    def advance(self, state, pad, mm):
        if self.agent < len(self.agents):
            # Adjust agent fitness value
            if state.frame % 1 == 0:
                self.agents[self.agent].fit(state, pad) # See Agent class for more on fit()
            # Change agent move
            if state.frame % 2 == 0:
                self.agents[self.agent].advance(state, pad) # See Agent class for more on advance()
            # Change agent every x frames
            if state.frame % 900 == 0:
                self.agent += 1
        return self.agent