import math

import p3.pad

class MenuManager:
    def __init__(self):
        self.dragged_to_9      = False
        self.level_9           = False
        self.selected_falco   = False
        self.selected_fox      = False
        self.selected_settings = False
        self.changed_settings  = False
        self.selected_cpu      = False
        self.action_list       = []
        self.last_action       = 0

    def pick_fox(self, state, pad):
        if self.selected_fox:
            pad.release_button(p3.pad.Button.A)
            pad.tilt_stick(p3.pad.Stick.MAIN, 0.5, 0.5)
            self.pick_cpu(state, pad)
        else:
            # Go to fox and press A
            target_x = -23.5
            target_y = 11.5
            dx = target_x - state.players[2].cursor_x
            dy = target_y - state.players[2].cursor_y
            mag = math.sqrt(dx * dx + dy * dy)
            if mag < 0.5:
                pad.press_button(p3.pad.Button.A)
                self.selected_fox = True
            else:
                pad.tilt_stick(p3.pad.Stick.MAIN, 0.5 * (dx / mag) + 0.5, 0.5 * (dy / mag) + 0.5)

    def pick_falco(self, state, pad):
        if self.selected_falco:
            pad.release_button(p3.pad.Button.A)
            pad.tilt_stick(p3.pad.Stick.MAIN, 0.5, 0.5)
            self.pick_cpu(state, pad)
        else:
            # Go to falco and press A
            target_x = -30
            target_y = 11.5
            dx = target_x - state.players[2].cursor_x
            dy = target_y - state.players[2].cursor_y
            mag = math.sqrt(dx * dx + dy * dy)
            if mag < 0.5:
                pad.press_button(p3.pad.Button.A)
                self.selected_falco = True
            else:
                pad.tilt_stick(p3.pad.Stick.MAIN, 0.5 * (dx / mag) + 0.5, 0.5 * (dy / mag) + 0.5)


    def get_settings(self, state, pad):
        if self.selected_settings:
            pad.release_button(p3.pad.Button.A)
            pad.tilt_stick(p3.pad.Stick.MAIN, 0.5, 0.5)
            self.change_settings(state, pad)
        else:
            target_x = 0.0
            target_y = 30.0
            dx = target_x - state.players[2].cursor_x
            dy = target_y - state.players[2].cursor_y
            mag = math.sqrt(dx * dx + dy * dy)
            if mag < 5.1:
                pad.press_button(p3.pad.Button.A)
                self.selected_settings = True
            else:
                pad.tilt_stick(p3.pad.Stick.MAIN, 0.5 * (dx / mag) + 0.5, 0.5 * (dy / mag) + 0.5)

    def change_settings(self, state, pad):
        if self.changed_settings:
            pad.reset()
            self.press_start_lots(state, pad)
        else:
            if state.frame % 440 == 0:
                pad.press_button(p3.pad.Button.D_LEFT)
            elif state.frame % 442 == 0:
                pad.release_button(p3.pad.Button.D_LEFT)
            elif state.frame % 444 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 446 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 448 == 0:
                pad.press_button(p3.pad.Button.D_LEFT)
            elif state.frame % 450 == 0:
                pad.release_button(p3.pad.Button.D_LEFT)
            elif state.frame % 455 == 0:
                pad.press_button(p3.pad.Button.D_LEFT)
            elif state.frame % 460 == 0:
                pad.release_button(p3.pad.Button.D_LEFT)
            elif state.frame % 465 == 0:
                pad.press_button(p3.pad.Button.D_UP)
            elif state.frame % 470 == 0:
                pad.release_button(p3.pad.Button.D_UP)
            elif state.frame % 475 == 0:
                pad.press_button(p3.pad.Button.D_UP)
            elif state.frame % 480 == 0:
                pad.release_button(p3.pad.Button.D_UP)
            elif state.frame % 485 == 0:
                pad.press_button(p3.pad.Button.A)
            elif state.frame % 490 == 0:
                pad.release_button(p3.pad.Button.A)
            elif state.frame % 495 == 0:
                pad.press_button(p3.pad.Button.D_UP)
            elif state.frame % 500 == 0:
                pad.release_button(p3.pad.Button.D_UP)
            elif state.frame % 505 == 0:
                pad.press_button(p3.pad.Button.A)
            elif state.frame % 510 == 0:
                pad.release_button(p3.pad.Button.A)
            elif state.frame % 515 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 520 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 525 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 530 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 535 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 540 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 545 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 550 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 555 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 560 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 565 == 0:
                pad.press_button(p3.pad.Button.A)
            elif state.frame % 570 == 0:
                pad.release_button(p3.pad.Button.A)
            elif state.frame % 575 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 580 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 585 == 0:
                pad.press_button(p3.pad.Button.A)
            elif state.frame % 590 == 0:
                pad.release_button(p3.pad.Button.A)
            elif state.frame % 595 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 600 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 605 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 610 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 615 == 0:
                pad.press_button(p3.pad.Button.A)
            elif state.frame % 620 == 0:
                pad.release_button(p3.pad.Button.A)
            elif state.frame % 625 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 630 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 635 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 640 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 645 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 650 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 655 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 660 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 665 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 670 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 675 == 0:
                pad.press_button(p3.pad.Button.A)
            elif state.frame % 680 == 0:
                pad.release_button(p3.pad.Button.A)
            elif state.frame % 685 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 690 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 695 == 0:
                pad.press_button(p3.pad.Button.A)
            elif state.frame % 700 == 0:
                pad.release_button(p3.pad.Button.A)
            elif state.frame % 705 == 0:
                pad.press_button(p3.pad.Button.B)
            elif state.frame % 710 == 0:
                pad.release_button(p3.pad.Button.B)
            elif state.frame % 715 == 0:
                pad.press_button(p3.pad.Button.B)
            elif state.frame % 720 == 0:
                pad.release_button(p3.pad.Button.B)
            elif state.frame % 725 == 0:
                pad.press_button(p3.pad.Button.B)
            elif state.frame % 730 == 0:
                pad.release_button(p3.pad.Button.B)
                self.changed_settings = True

    def pick_cpu(self, state, pad):
        if self.selected_cpu:
            pad.release_button(p3.pad.Button.A)
            pad.tilt_stick(p3.pad.Stick.MAIN, 0.5, 0.5)
            self.pick_cpu_level_9(state, pad)
        else:
            target_x = -16.0
            target_y = -2
            dx = target_x - state.players[2].cursor_x
            dy = target_y - state.players[2].cursor_y
            mag = math.sqrt(dx * dx + dy * dy)
            if mag < .5:
                pad.press_button(p3.pad.Button.A)
                self.selected_cpu = True
            else:
                pad.tilt_stick(p3.pad.Stick.MAIN, 0.5 * (dx / mag) + 0.5, 0.5 * (dy / mag) + 0.5)

    def pick_cpu_level_9(self, state, pad):
        if self.level_9:
            pad.release_button(p3.pad.Button.A)
            pad.tilt_stick(p3.pad.Stick.MAIN, 0.5, 0.5)
            self.drag_to_9(state, pad)
        else:
            target_x = -16.0
            target_y = -15.0
            dx = target_x - state.players[2].cursor_x
            dy = target_y - state.players[2].cursor_y
            mag = math.sqrt(dx * dx + dy * dy)
            if mag < .6:
                pad.press_button(p3.pad.Button.A)
                self.level_9 = True
            else:
                pad.tilt_stick(p3.pad.Stick.MAIN, 0.5 * (dx / mag) + 0.5, 0.5 * (dy / mag) + 0.5)


    def drag_to_9(self, state, pad):
        if self.dragged_to_9:
            pad.release_button(p3.pad.Button.A)
            pad.tilt_stick(p3.pad.Stick.MAIN, 0.5, 0.5)
            self.get_settings(state, pad)
        else:
            target_x = -7.0
            target_y = -15.0
            dx = target_x - state.players[2].cursor_x
            dy = target_y - state.players[2].cursor_y
            mag = math.sqrt(dx * dx + dy * dy)
            if mag < .5:
                pad.press_button(p3.pad.Button.A)
                self.dragged_to_9 = True
            else:
                pad.tilt_stick(p3.pad.Stick.MAIN, 0.5 * (dx / mag) + 0.5, 0.5 * (dy / mag) + 0.5)


    def press_start_lots(self, state, pad):
        if state.frame % 2 == 0:
            pad.press_button(p3.pad.Button.START)
        else:
            pad.release_button(p3.pad.Button.START)

    def press_start_once(self, state, pad):
        if state.frame % 2 == 0:
            pad.press_button(p3.pad.Button.START)

