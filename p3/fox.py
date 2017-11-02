import numpy as np
import p3.pad
import p3.config as c
from p3.agent import Agent


class Fox:
    def __init__(self):
        self.agent       = 0 # individual agent number
        self.agents      = [] # list of agents
        self.generation  = 0 # generation number
        self.special     = [0, 0] # stores percentages for last agent in a generation

    def reset(self):
        self.agent  = 0
        self.agents = []

    # Add agent to agents list
    def add_agent(self, nnet):
        self.agents.append(Agent(len(self.agents), nnet))

    # Return list of fitness values for all agents
    def get_ind_fitness(self):
        fits = []
        for a in self.agents:
            fits.append(a.fitness)
        return fits

    # Advance frame by 1
    def advance(self, state, pad, mm):
        if self.agent < len(self.agents):
            # Change agent move
            if state.frame % 2 == 0:
                self.agents[self.agent].advance(state, pad) # See Agent class for more on advance()
            # Change agent every x frames
            if state.frame % 300 == 0:
                # self.agents[self.agent].restart(state, pad)
                # set the previous percent equal to the stored percent from last generation
                if (self.agent == 0):
                    self.agents[self.agent].prev_percent[0] = self.special[0]
                    self.agents[self.agent].prev_percent[1] = self.special[1]

                # Adjust agent fitness value
                self.agents[self.agent].fit(state, pad) # See Agent class for more on fit()

                # set the next agents prev_percent to be the current percent
                # unless you are the last agent (prevent index out of bounds error)
                if (self.agent + 1 < len(self.agents)):
                    a = self.agents[self.agent]
                    self.agents[self.agent + 1].prev_percent[0] = state.players[2].percent
                    self.agents[self.agent + 1].prev_percent[1] = state.players[1].percent
                    # print(a.number, ": [{0:.2f}".format(a.prev_percent[0]), ", {0:.2f}] ".format(a.prev_percent[1]), "[{0:.2f}".format(a.fitness[0]), ", {0:.2f}] ".format(a.fitness[1]))
                # store the last percent of each generation, use it for first agent of next generation
                else:
                    self.special[0] = state.players[2].percent
                    self.special[1] = state.players[1].percent

                self.agent += 1
        return self.agent

