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
        # decrease fitness in case of getting hit
        if (state.players[2].hitlag > 0 or state.players[2].hitstun > 0):
            self.fitness -= 100
        # decrease fitness in case of dying
        if (state.players[2].action_state == ActionState.Rebirth):
            self.fitness -= 1000
        # increase fitness in case of hitting opponent
        if (state.players[0].hitlag > 0 or state.players[0].hitstun > 0):
            self.fitness += 100
        # increase fitness in case of killing opponent
        if (state.players[0].action_state == ActionState.Rebirth):
            self.fitness += 1000

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
        inputs.append(state.players[0].pos_x) # opponent x pos
        inputs.append(state.players[0].pos_y) # opponent y pos
        inputs.append(state.players[2].pos_x) # x pos
        inputs.append(state.players[2].pos_y) # y pos
        inputs.append(state.players[2].facing) # facing
        inputs.append(state.players[0].percent) # percent
        # inputs.append(state.players[0].action_state) # action state
        inputs.append(state.players[2].action_frame) # action frame
        inputs.append(state.players[2].hitlag) # hitlag
        inputs.append(state.players[2].hitstun) # hitstun
        inputs.append(state.players[2].jumps_used) # jumps used
        inputs.append(state.players[2].shield_size) # shield size
        inputs.append(state.players[2].on_ground) # in air
        inputs.append(state.players[2].self_air_vel_x) # speed x
        inputs.append(state.players[2].self_air_vel_y) # speed y
        inputs.append(state.players[2].attack_vel_x) # attack speed x
        inputs.append(state.players[2].attack_vel_y) # attack speed y

        inputs.append(state.players[0].facing) # facing
        inputs.append(state.players[2].percent) # percent
        # inputs.append(state.players[0].action_state) # action state
        inputs.append(state.players[0].action_frame) # action frame
        inputs.append(state.players[0].hitlag) # hitlag
        inputs.append(state.players[0].hitstun) # hitstun
        inputs.append(state.players[0].jumps_used) # jumps used
        inputs.append(state.players[0].shield_size) # shield size
        inputs.append(state.players[0].on_ground) # in air
        inputs.append(state.players[0].self_air_vel_x) # speed x
        inputs.append(state.players[0].self_air_vel_y) # speed y
        inputs.append(state.players[0].attack_vel_x) # attack speed x
        inputs.append(state.players[0].attack_vel_y) # attack speed y


        outputs = self.brain.evaluate(inputs)
        if outputs[0] >= .5: # Left
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.0, 0.5]))
        if outputs[1] >= .5: # Right
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 1.0, 0.5]))
        if outputs[2] >= .5: # Down
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.5, 0.0]))
        if outputs[3] >= .5: # Up
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.5, 1.0]))
        if outputs[4] >= .5: # Top-Left
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.0, 1.0]))
        if outputs[5] >= .5: # Top-Right
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 1.0, 1.0]))
        if outputs[6] >= .5: # Bottom-Left
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.0, 0.0]))
        if outputs[7] >= .5: # Bottom-Right
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 1.0, 0.0]))
        if outputs[8] >= .5: # Neutral
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.5, 0.5]))
        if outputs[9] >= .5: # A Button
            self.action_list.append((0, pad.press_button, [p3.pad.Button.A]))
            self.action_list.append((1, pad.release_button, [p3.pad.Button.A]))
        if outputs[10] >= .5: # B Button
            self.action_list.append((0, pad.press_button, [p3.pad.Button.B]))
            self.action_list.append((1, pad.release_button, [p3.pad.Button.B]))
        if outputs[11] >= .5: # Y Button
            self.action_list.append((0, pad.press_button, [p3.pad.Button.Y]))
            self.action_list.append((1, pad.release_button, [p3.pad.Button.Y]))
        if outputs[12] >= .5: # Z Button
            self.action_list.append((0, pad.press_button, [p3.pad.Button.Z]))
            self.action_list.append((1, pad.release_button, [p3.pad.Button.Z]))
        if outputs[13] >= .5: # L Trigger
            self.action_list.append((0, pad.press_trigger, [p3.pad.Trigger.L, 1]))
            self.action_list.append((1, pad.press_trigger, [p3.pad.Trigger.L, 0]))


