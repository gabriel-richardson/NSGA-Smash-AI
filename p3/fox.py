import numpy as np
import p3.pad
import p3.config as c
from p3.agent import Agent
from p3.state import ActionState


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
    def get_ind_fitness(self):
        fits = []
        for a in self.agents:
            fits.append(a.fitness)
        return fits

    # Advance frame by 1
    def advance(self, state, pad, mm):
        a = self.agents[self.agent]
        # For every agent in the population
        if self.agent < len(self.agents):
            if (state.players[1].action_state == ActionState.DeadDown):
                a.damage_dealt.append(-1)
            else:
                a.damage_dealt.append(state.players[1].percent) # append cpu's percent
            if (state.players[2].action_state == ActionState.DeadDown):
                a.damage_received.append(-1)
            else:
                a.damage_received.append(state.players[2].percent) # append ai's percent
            # Collect fitness and change agent every x frames
            if state.frame % 600 == 0:
                a.pause(state, pad)
                print(a.damage_dealt)
                print(a.damage_received)
                a.fit(state, pad) # See Agent class for more on fit()
                # print(a.number, ": [{0:.2f}".format(a.fitness[1]), ", {0:.2f}] ".format(a.fitness[0]))
                a.restart(state, pad)
                self.agent += 1
            # Change agent move
            elif state.frame % 2 == 0:
                a.advance(state, pad) # See Agent class for more on advance()
        return self.agent

