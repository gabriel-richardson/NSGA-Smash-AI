import math

import p3.pad

class MenuManager:
    def __init__(self):
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
            if state.frame % 400 == 0:
                pad.press_button(p3.pad.Button.D_LEFT)
            elif state.frame % 405 == 0:
                pad.release_button(p3.pad.Button.D_LEFT)
            elif state.frame % 410 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 415 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 420 == 0:
                pad.press_button(p3.pad.Button.D_LEFT)
            elif state.frame % 425 == 0:
                pad.release_button(p3.pad.Button.D_LEFT)
            elif state.frame % 430 == 0:
                pad.press_button(p3.pad.Button.D_LEFT)
            elif state.frame % 435 == 0:
                pad.release_button(p3.pad.Button.D_LEFT)
            elif state.frame % 440 == 0:
                pad.press_button(p3.pad.Button.D_UP)
            elif state.frame % 445 == 0:
                pad.release_button(p3.pad.Button.D_UP)
            elif state.frame % 450 == 0:
                pad.press_button(p3.pad.Button.D_UP)
            elif state.frame % 455 == 0:
                pad.release_button(p3.pad.Button.D_UP)
            elif state.frame % 460 == 0:
                pad.press_button(p3.pad.Button.A)
            elif state.frame % 465 == 0:
                pad.release_button(p3.pad.Button.A)
            elif state.frame % 470 == 0:
                pad.press_button(p3.pad.Button.D_UP)
            elif state.frame % 475 == 0:
                pad.release_button(p3.pad.Button.D_UP)
            elif state.frame % 480 == 0:
                pad.press_button(p3.pad.Button.A)
            elif state.frame % 485 == 0:
                pad.release_button(p3.pad.Button.A)
            elif state.frame % 490 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 495 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 500 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 505 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 510 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 515 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 520 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 525 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 530 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 535 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 540 == 0:
                pad.press_button(p3.pad.Button.A)
            elif state.frame % 545 == 0:
                pad.release_button(p3.pad.Button.A)
            elif state.frame % 550 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 555 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 560 == 0:
                pad.press_button(p3.pad.Button.A)
            elif state.frame % 565 == 0:
                pad.release_button(p3.pad.Button.A)
            elif state.frame % 570 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 575 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 580 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 585 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 590 == 0:
                pad.press_button(p3.pad.Button.A)
            elif state.frame % 595 == 0:
                pad.release_button(p3.pad.Button.A)
            elif state.frame % 600 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 605 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 610 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 615 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 620 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 625 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 630 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 635 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 640 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 645 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 650 == 0:
                pad.press_button(p3.pad.Button.A)
            elif state.frame % 655 == 0:
                pad.release_button(p3.pad.Button.A)
            elif state.frame % 660 == 0:
                pad.press_button(p3.pad.Button.D_DOWN)
            elif state.frame % 665 == 0:
                pad.release_button(p3.pad.Button.D_DOWN)
            elif state.frame % 670 == 0:
                pad.press_button(p3.pad.Button.A)
            elif state.frame % 675 == 0:
                pad.release_button(p3.pad.Button.A)
            elif state.frame % 680 == 0:
                pad.press_button(p3.pad.Button.B)
            elif state.frame % 685 == 0:
                pad.release_button(p3.pad.Button.B)
            elif state.frame % 690 == 0:
                pad.press_button(p3.pad.Button.B)
            elif state.frame % 695 == 0:
                pad.release_button(p3.pad.Button.B)
            elif state.frame % 700 == 0:
                pad.press_button(p3.pad.Button.B)
            elif state.frame % 705 == 0:
                pad.release_button(p3.pad.Button.B)
                self.changed_settings = True

    def pick_cpu(self, state, pad):
        if self.selected_cpu:
            pad.release_button(p3.pad.Button.A)
            pad.tilt_stick(p3.pad.Stick.MAIN, 0.5, 0.5)
            self.get_settings(state, pad)
        else:
            target_x = -18.0
            target_y = 0.7
            dx = target_x - state.players[2].cursor_x
            dy = target_y - state.players[2].cursor_y
            mag = math.sqrt(dx * dx + dy * dy)
            if mag < .5:
                pad.press_button(p3.pad.Button.A)
                self.selected_cpu = True
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

