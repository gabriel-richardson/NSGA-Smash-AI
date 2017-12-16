import numpy as np
import p3.ANN as nnet
import p3.pad
from p3.pad import Button
import p3.menu_manager as mm
import p3.config as c
from p3.state import BodyState
from p3.state import ActionState

class Agent:
    def __init__(self, number, nnet):
        self.number          = number
        self.brain           = nnet
        self.action_list     = []
        self.last_restart    = 0
        self.last_action     = 0
        self.last_move       = 0
        self.last_pos        = 60
        self.fitness         = [0, 0] # Damage received, damage dealt
        self.damage_received = []
        self.damage_dealt    = []
    
    # restart the game
    def restart(self, state, pad):
        state.players[1].percent = 0
        state.players[2].percent = 0
        pad.reset()
        pad.press_button(Button.L)
        pad.press_button(Button.R)
        pad.press_button(Button.A)
        pad.press_button(Button.B)
        for x in range(0, 30000):
            pad.press_button(Button.START)
            pad.release_button(Button.START)
        pad.reset()

    def pause(self, state, pad):
        pad.reset()
        pad.press_button(Button.START)
        pad.reset()

    # iterate through damage lists, sum values that preceed a 0 (death), and last value
    # start iterating at 2nd position to avoid index out of bounds error
    def fit(self, state, pad):
        received = 0
        for i in range(1, len(self.damage_received)):
            if (self.damage_received[i] == -1 and self.damage_received[i-1] != -1):
                received += self.damage_received[i-1]
            elif (self.damage_received[i] == -1):
                received += 1
            if (i == len(self.damage_received)-1 and self.damage_received[i] != -1):
                received += self.damage_received[i]
        damage_received = []
        self.fitness[0] += received
        
        dealt = 0
        for i in range(1, len(self.damage_dealt)):
            if (self.damage_dealt[i] == -1 and self.damage_dealt[i-1] != -1):
                dealt += self.damage_dealt[i-1]
            # elif (self.damage_dealt[i] == -1):
            #     dealt += 1
            if (i == len(self.damage_dealt)-1 and self.damage_dealt[i] != -1):
                dealt += self.damage_dealt[i]
        damage_dealt = []
        self.fitness[1] += dealt

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

    # normalize inputs between -1 and 1
    def normalize(self, x, A, B):
        a = -1
        b = 1
        return a+(x-A)*(b-a)/(B-A)

    # update neural network
    def update(self, state, pad):
        inputs = [] # nnet inputs
        inputs.append(self.normalize(state.players[1].pos_x, -246, 246)) # x
        inputs.append(self.normalize(state.players[1].pos_y, -140, 140)) # y
        inputs.append(self.normalize(state.players[1].facing, -1, 1)) # facing
        # inputs.append(self.normalize(state.players[1].action_frame, 0, 260)) # action frame
        # inputs.append(self.normalize(state.players[1].hitstun, 0, 50)) # hitstun
        # inputs.append(self.normalize(state.players[1].on_ground, int(False), int(True))) # in air
        # inputs.append(self.normalize(state.players[1].self_air_vel_x, -2.3, 2.3)) # speed x
        # inputs.append(self.normalize(state.players[1].self_air_vel_y, -2.9, 3.22)) # speed y

        inputs.append(self.normalize(state.players[2].pos_x, -246, 246)) # x
        inputs.append(self.normalize(state.players[2].pos_y, -140, 140)) # y
        inputs.append(self.normalize(state.players[2].facing, -1, 1)) # facing
        # inputs.append(self.normalize(state.players[2].action_frame, 0, 260)) # action frame
        # inputs.append(self.normalize(state.players[2].hitstun, 0, 50)) # hitstun
        # inputs.append(self.normalize(state.players[2].on_ground, int(False), int(True))) # in air
        # inputs.append(self.normalize(state.players[2].self_air_vel_x, -2.17, 2.17)) # speed x
        # inputs.append(self.normalize(state.players[2].self_air_vel_y, -2.17, 3.22)) # speed y

        outputs = self.brain.evaluate(inputs)
        if outputs[0] >= .5:
            if (state.players[2].body_state == BodyState.Normal and state.players[2].pos_x > 87):
                self.fitness[1] += .1
            self.current_move = 0
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.0, 0.5]))
        if outputs[1] >= .5:
            if (state.players[2].body_state == BodyState.Normal and state.players[2].pos_x < -87):
                self.fitness[1] += .1
            self.current_move = 1
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 1.0, 0.5]))
        if outputs[2] >= .5:
            self.current_move = 2
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.5, 0.0]))
        if outputs[3] >= .5:
            self.current_move = 3
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.5, 1.0]))
        if outputs[4] >= .5:
            self.current_move = 8
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.5, 0.5]))
        if outputs[5] >= .5:
            self.current_move = 9
            self.action_list.append((0, pad.press_button, [p3.pad.Button.A]))
            self.action_list.append((1, pad.release_button, [p3.pad.Button.A]))
        if outputs[6] >= .5:
            self.current_move = 10
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.0, 0.5]))
            self.action_list.append((0, pad.press_button, [p3.pad.Button.A]))
            self.action_list.append((1, pad.release_button, [p3.pad.Button.A]))
        if outputs[7] >= .5:
            self.current_move = 11
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 1.0, 0.5]))
            self.action_list.append((0, pad.press_button, [p3.pad.Button.A]))
            self.action_list.append((1, pad.release_button, [p3.pad.Button.A]))
        if outputs[8] >= .5:
            self.current_move = 12
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.5, 0.0]))
            self.action_list.append((0, pad.press_button, [p3.pad.Button.A]))
            self.action_list.append((1, pad.release_button, [p3.pad.Button.A]))
        if outputs[9] >= .5:
            self.current_move = 13
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.5, 1.0]))
            self.action_list.append((0, pad.press_button, [p3.pad.Button.A]))
            self.action_list.append((1, pad.release_button, [p3.pad.Button.A]))
        if outputs[10] >= .5:
            self.current_move = 14
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.0, 1.0]))
            self.action_list.append((0, pad.press_button, [p3.pad.Button.A]))
            self.action_list.append((1, pad.release_button, [p3.pad.Button.A]))
        if outputs[11] >= .5:
            self.current_move = 15
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 1.0, 1.0]))
            self.action_list.append((0, pad.press_button, [p3.pad.Button.A]))
            self.action_list.append((1, pad.release_button, [p3.pad.Button.A]))
        if outputs[12] >= .5:
            self.current_move = 16
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.0, 0.0]))
            self.action_list.append((0, pad.press_button, [p3.pad.Button.A]))
            self.action_list.append((1, pad.release_button, [p3.pad.Button.A]))
        if outputs[13] >= .5:
            self.current_move = 17
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 1.0, 0.0]))
            self.action_list.append((0, pad.press_button, [p3.pad.Button.A]))
            self.action_list.append((1, pad.release_button, [p3.pad.Button.A]))
        if outputs[14] >= .5:
            self.current_move = 18
            self.action_list.append((0, pad.press_button, [p3.pad.Button.B]))
            self.action_list.append((1, pad.release_button, [p3.pad.Button.B]))
        if outputs[15] >= .5:
            self.current_move = 19
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.0, 0.5]))
            self.action_list.append((0, pad.press_button, [p3.pad.Button.B]))
            self.action_list.append((1, pad.release_button, [p3.pad.Button.B]))
        if outputs[16] >= .5:
            self.current_move = 20
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 1.0, 0.5]))
            self.action_list.append((0, pad.press_button, [p3.pad.Button.B]))
            self.action_list.append((1, pad.release_button, [p3.pad.Button.B]))
        if outputs[17] >= .5:
            self.current_move = 21
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.5, 0.0]))
            self.action_list.append((0, pad.press_button, [p3.pad.Button.B]))
            self.action_list.append((1, pad.release_button, [p3.pad.Button.B]))
        if outputs[18] >= .5:
            self.current_move = 22
            if (state.players[2].body_state == BodyState.Normal and (state.players[2].pos_x > 87 or state.players[2].pos_x < -87)):
                self.fitness[1] += .1
            else:
                self.fitness[0] += 1.5
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.5, 1.0]))
            self.action_list.append((0, pad.press_button, [p3.pad.Button.B]))
            self.action_list.append((1, pad.release_button, [p3.pad.Button.B]))
        if outputs[19] >= .5:
            self.current_move = 23
            if (state.players[2].pos_x > 87):
                self.fitness[1] += .1
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.0, 0.5]))
            self.action_list.append((0, pad.press_button, [p3.pad.Button.Y]))
            self.action_list.append((1, pad.release_button, [p3.pad.Button.Y]))
        if outputs[20] >= .5:
            self.current_move = 24
            if (state.players[2].pos_x < -87):
                self.fitness[1] += .1
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 1.0, 0.5]))
            self.action_list.append((0, pad.press_button, [p3.pad.Button.Y]))
            self.action_list.append((1, pad.release_button, [p3.pad.Button.Y]))
        if outputs[21] >= .5:
            self.current_move = 25
            self.action_list.append((0, pad.press_button, [p3.pad.Button.Y]))
            self.action_list.append((1, pad.release_button, [p3.pad.Button.Y]))
        if outputs[22] >= .5:
            self.current_move = 26
            self.action_list.append((0, pad.press_button, [p3.pad.Button.Z]))
            self.action_list.append((1, pad.release_button, [p3.pad.Button.Z]))
        if outputs[23] >= .5:
            self.current_move = 27
            self.action_list.append((0, pad.press_trigger, [p3.pad.Trigger.L, 1]))
            self.action_list.append((1, pad.press_trigger, [p3.pad.Trigger.L, 0]))
        if outputs[24] >= .5:
            self.current_move = 28
            self.action_list.append((0, pad.press_trigger, [p3.pad.Trigger.L, 1]))
            self.action_list.append((0, pad.press_button, [p3.pad.Button.A]))
            self.action_list.append((1, pad.release_button, [p3.pad.Button.A]))
            self.action_list.append((1, pad.press_trigger, [p3.pad.Trigger.L, 0]))
        if outputs[25] >= .5:
            self.current_move = 29
            self.action_list.append((0, pad.press_trigger, [p3.pad.Trigger.L, 1]))
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.5, 0.5]))
            self.action_list.append((1, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.0, 0.5]))
            self.action_list.append((1, pad.press_trigger, [p3.pad.Trigger.L, 0]))
        if outputs[26] >= .5:
            self.current_move = 30
            self.action_list.append((0, pad.press_trigger, [p3.pad.Trigger.L, 1]))
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.5, 0.5]))
            self.action_list.append((1, pad.tilt_stick, [p3.pad.Stick.MAIN, 1.0, 0.5]))
            self.action_list.append((1, pad.press_trigger, [p3.pad.Trigger.L, 0]))
        if outputs[27] >= .5:
            self.current_move = 31
            self.action_list.append((0, pad.press_trigger, [p3.pad.Trigger.L, 1]))
            self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.5, 0.5]))
            self.action_list.append((1, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.5, 0.0]))
            self.action_list.append((1, pad.press_trigger, [p3.pad.Trigger.L, 0]))
        if (self.current_move != self.last_move):
            self.fitness[1] += .5
        self.last_move = self.current_move