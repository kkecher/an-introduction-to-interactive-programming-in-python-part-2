# Basic infrastructure for Bubble Shooter

import simplegui
import random
import math

# Global constants
WIDTH = 800
HEIGHT = 600
#FIRING_POSITION = [WIDTH // 2, HEIGHT] #exercise value. Only half of bubble is drawn in a such way
FIRING_POSITION = [WIDTH // 2, HEIGHT - 0.1 * HEIGHT]
FIRING_LINE_LENGTH = 60
FIRING_ANGLE_VEL_INC = 0.02
BUBBLE_RADIUS = 20
COLOR_LIST = ["Red", "Green", "Blue", "White"]

# global variables
firing_angle = math.pi + math.pi / 4
firing_angle_vel = 0
bubble_stuck = True

#firing sound
firing_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/Collision8-Bit.ogg")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)

# class defintion for Bubbles
class Bubble:
    def __init__(self, pos = None, vel = None, color = None, sound = firing_sound):
        if pos == None:
            self.pos = list(FIRING_POSITION)
        else:
            self.pos = pos
        if vel == None:
            self.vel = [0, 0]
        else:
            self.vel = vel
        if color == None:
            self.color = random.choice(COLOR_LIST)
        else:
            self.color = color
        self.sound = sound
    
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        if self.pos[0] <= BUBBLE_RADIUS or self.pos[0] >= WIDTH - BUBBLE_RADIUS:
            self.vel[0] *= -1

    def fire_bubble(self, vel):
        self.vel = vel
        if self.sound:
            self.sound.play()
        
    def is_stuck(self, stuck_bubble): 
        if self.pos[1] <= BUBBLE_RADIUS or self.pos[1] >= HEIGHT - BUBBLE_RADIUS or dist(self.pos, stuck_bubble.pos) <= BUBBLE_RADIUS  * 2:
            return True
        return False

    def draw(self, canvas):
        canvas.draw_circle(self.pos, BUBBLE_RADIUS, 1, self.color, self.color) 

# define keyhandlers to control firing_angle
def keydown(key):
    global a_bubble, firing_angle_vel, bubble_stuck
    if key == simplegui.KEY_MAP['right']:
        firing_angle_vel = FIRING_ANGLE_VEL_INC
    if key == simplegui.KEY_MAP['left']:
        firing_angle_vel = -FIRING_ANGLE_VEL_INC
    if key == simplegui.KEY_MAP['space'] and bubble_stuck:
        bubble_stuck = False
        speed_force_coeff = 10
        vel = angle_to_vector(firing_angle)
        vel = [speed_force_coeff * x for x in vel] #make a bubble a little faster
        a_bubble.fire_bubble(vel)

def keyup(key):
    global firing_angle_vel
    if key in [simplegui.KEY_MAP['right'], simplegui.KEY_MAP['left']]:
        firing_angle_vel = 0
    

# define draw handler
def draw(canvas):
    global firing_angle, a_bubble, bubble_stuck


    # update firing angle
    firing_angle += firing_angle_vel
    
    # draw firing line
    firing_line_point_1 = list(FIRING_POSITION)
    firing_line_point_2 = angle_to_vector(firing_angle)
    firing_line_point_2[0] = firing_line_point_2[0] * FIRING_LINE_LENGTH + firing_line_point_1[0]
    firing_line_point_2[1] = firing_line_point_2[1] * FIRING_LINE_LENGTH + firing_line_point_1[1]

    canvas.draw_line(firing_line_point_1, firing_line_point_2, 3, "White")

    # update a_bubble and check for sticking
    a_bubble.update()
    
    # draw a bubble and stuck bubbles
    a_bubble.draw(canvas)
    is_stucked = False
    for stuck_bubble in stuck_bubbles:
        stuck_bubble.draw(canvas)
        if a_bubble.is_stuck(stuck_bubble):
            is_stucked = True
    if is_stucked:
        stuck_bubbles.add(a_bubble)
        a_bubble = Bubble()
        bubble_stuck = True
        is_stucked = False
    
# create frame and register handlers
frame = simplegui.create_frame("Bubble Shooter", WIDTH, HEIGHT)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_draw_handler(draw)

# create initial buble and start frame
a_bubble = Bubble()
stuck_bubbles = set([Bubble(pos=[WIDTH / 2, -HEIGHT], sound = None)])
frame.start()
