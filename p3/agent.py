import numpy as np
import p3.ANN as nnet
import p3.pad
import p3.config as c
from p3.state import BodyState
from p3.state import ActionState

class Agent:
    def __init__(self, number, nnet):
        self.number         = number
        self.brain          = nnet
        self.action_list    = []
        self.last_action    = 0
        self.fitness        = 0
        self.reset()

    def reset(self):
        self.fitness = 0

    def fit(self, state, pad):
        x = (state.players[0].pos_x - state.players[2].pos_x) ** 2 # diff between player 1 and agent x pos
        y = (state.players[0].pos_y - state.players[2].pos_y) ** 2 # diff between player 1 and agent y pos
        d = np.sqrt(x + y) # sqrt of sum of diffs

        # decrease fitness by d in case of getting hit
        if state.players[2].hitlag > 0:
            self.fitness -= d
        # increase fitness by d if player is on the stage but not in rebirth/rebirthWait states
        if (np.absolute(state.players[2].pos_x) <= c.game['stage_width']
            and not(state.players[2].action_state == ActionState.Rebirth
            or state.players[2].action_state == ActionState.RebirthWait)):
            self.fitness += d
        # decrease fitness by d if player is off stage and not dead
        elif ((np.absolute(state.players[2].pos_x) > c.game['stage_width']
            or np.absolute(state.players[2].pos_y < 0))
            and state.players[2].action_state != ActionState.DeadDown): # DeadDown is ActionState for dying off the bottom
            self.fitness -= d

    # execute actions from action list
    def advance(self, state, pad):
        while self.action_list:
            wait, func, args = self.action_list[0]
            if state.frame - self.last_action < wait:
                return
            else:
                self.action_list.pop(0)
                if func is not None:
                    func(*args)
                self.last_action = state.frame
        else:
            self.update(state, pad) # populate actions list

    def update(self, state, pad):
        inputs = [] # nnet inputs
        inputs.append(np.absolute(state.players[0].pos_x - state.players[2].pos_x)) # x pos diff between agent and player 1
        inputs.append(c.game['stage_width'] - np.absolute(state.players[0].pos_x)) # distance between player 1 and nearest edge of stage
        inputs.append(c.game['stage_width'] - np.absolute(state.players[2].pos_x)) # distance between agent and nearest edge of stage

        outputs = self.brain.evaluate(inputs)
        if outputs[0] >= .5:
            self.action_list.append((1, None, [])) # empty action
            self.action_list.append((1, None, []))
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.0, 0.5])) # tilt stick left
        if outputs[1] >= .5:
            self.action_list.append((1, None, []))
            self.action_list.append((1, None, []))
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 1.0, 0.5])) # tilt stick right
        if outputs[2] >= .5:
            self.action_list.append((1, None, []))
            self.action_list.append((1, None, []))
            self.action_list.append((0, pad.press_button, [p3.pad.Button.Y])) # press jump
            self.action_list.append((1, None, []))
            self.action_list.append((1, None, []))
            self.action_list.append((1, pad.release_button, [p3.pad.Button.Y])) # release jump
        if outputs[0] < .5 and outputs[1] < .5 and outputs[2] < .5:
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.5, 0.5])) # tilt stick neutral