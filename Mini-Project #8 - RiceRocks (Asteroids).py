# import modules
#start_fold
import simplegui
import math
import random
#end_fold

# globals for user interface
#start_fold
WIDTH = 800
HEIGHT = 600
SPLASH_POS = [WIDTH /2, HEIGHT / 2]
time = 0
#end_fold

class ImageInfo:
    #start_fold
    def __init__(self, center, size, dim = None, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.dim = dim
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_dim(self):
        return self.dim

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated
    #end_fold

#Images and sounds    
#start_fold
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")
ship_image_size = [180, 90]
ship_image_center = [x / 2 for x in ship_image_size]
ship_info = ImageInfo(center = ship_image_center, size = ship_image_size, radius = 35)

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo(center = [5, 5], size = [10, 10], radius = 3, lifespan = 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo(center = [45, 45], size = [90, 90], radius = 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
rock_explosion_info = ImageInfo(center = [64, 64], size = [128, 128], dim = [24, 1], radius = 17, lifespan = 24, animated = True)
rock_explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
ship_explosion_info = ImageInfo(center = [50, 50], size = [100, 100], dim = [9, 9], radius = 25, lifespan = 60, animated = True)
ship_explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/explosion.hasgraphics.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
soundtrack_2 = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")
#end_fold

# helper functions to handle transformations
#start_fold
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)
#end_fold

# Ship class
#start_fold
class Ship:
    def __init__(self, pos, vel, angle, image, info, sound = None):
        #start_fold
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.ang = angle
        self.ang_vel = 0
        self.friction_coeff = 0.99
        self.reduce_forward_coeff = 0.3
        self.image = image
        self.thrust_off_image_center = [info.get_center()[0] * 1/2, info.get_center()[1]]
        self.thrust_on_image_center = [info.get_center()[0] * 3/2, info.get_center()[1]]
        self.image_size = [info.get_size()[0] / 2, info.get_size()[1]]
        self.radius = info.get_radius()
        self.forward = [0, 0]
        if sound:
            sound.rewind()
            sound.play()
        #end_fold
        
    def draw(self,canvas):
        #start_fold
        if self.thrust:
            canvas.draw_image(self.image, self.thrust_on_image_center, self.image_size, self.pos, self.image_size, self.ang)
        else:
            canvas.draw_image(self.image, self.thrust_off_image_center, self.image_size, self.pos, self.image_size, self.ang)
        #end_fold

    def update(self):
        #start_fold
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
        self.ang += self.ang_vel
        self.vel = [x * self.friction_coeff for x in self.vel]
        if self.thrust:
            self.vel[0] += self.forward[0] * self.reduce_forward_coeff
            self.vel[1] += self.forward[1] * self.reduce_forward_coeff
        #end_fold

    def turn_on_rotation(self, is_clockwise):
        #start_fold
        if is_clockwise:
            self.ang_vel = math.pi / 50
        else:
            self.ang_vel = -math.pi / 50
        #end_fold

    def turn_off_rotation(self):
        self.ang_vel = 0

    def turn_on_thrust(self):
        #start_fold
        self.thrust = True
        ship_thrust_sound.play()
        self.forward = angle_to_vector(self.ang) 
        #end_fold

    def turn_off_thrust(self):
        #start_fold
        self.thrust = False
        ship_thrust_sound.pause()
        self.forward = [0, 0]
        #end_fold

    def shoot(self):
        #start_fold
        missile_speed_forward_coeff = 10
        missile_pos = [self.pos[0] + math.cos(self.ang) * self.image_size[0] / 2, self.pos[1] + math.sin(self.ang) * self.image_size[1] / 2]
        missile_vel = list(self.vel)
        missile_vel[0] += angle_to_vector(self.ang)[0] * missile_speed_forward_coeff
        missile_vel[1] += angle_to_vector(self.ang)[1] * missile_speed_forward_coeff
        missile = Sprite(pos = missile_pos, vel = missile_vel, ang = 0, ang_vel = 0, image = missile_image, info = missile_info, sound = missile_sound)
        missile_group.add(missile)
        #end_fold

    def get_pos(self):
        return self.pos

    def get_radius(self):
        return self.radius
#end_fold

def my_ship_keydown_handler(key):
    #start_fold
    if is_in_game:
        if key == simplegui.KEY_MAP['left']:
            my_ship.turn_on_rotation(is_clockwise=False);
        if key == simplegui.KEY_MAP['right']:
            my_ship.turn_on_rotation(is_clockwise=True);
        if key == simplegui.KEY_MAP['up']:
            my_ship.turn_on_thrust()
        if key == simplegui.KEY_MAP['space']:
            my_ship.shoot()
    #end_fold

def my_ship_keyup_handler(key):
    #start_fold
    if is_in_game:
        if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['right']:
            my_ship.turn_off_rotation()
        if key == simplegui.KEY_MAP['up']:
            my_ship.turn_off_thrust()
    #end_fold

# Sprite class
    #start_fold
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        #start_fold
        if pos == 'random':
            self.pos = [random.randrange(0, WIDTH + 1), random.randrange(0, HEIGHT + 1)]
        else:
            self.pos = [pos[0],pos[1]]
        self.vel = vel
        self.ang = ang
        self.ang_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.image_dim = info.get_dim()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
        #end_fold
   
    def draw(self, canvas):
        if self.animated:
            explosion_index = [self.age % self.image_dim[0], (self.age // self.image_dim[0]) % self.image_dim[1]]
            canvas.draw_image(self.image, [self.image_center[0] + explosion_index[0] * self.image_size[0], self.image_center[1] + explosion_index[1] * self.image_size[1]], self.image_size, self.pos, self.image_size, self.ang)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.ang)
    
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        if is_in_game:
            self.pos[0] %= WIDTH
            self.pos[1] %= HEIGHT
        self.ang += self.ang_vel
        self.age += 1
        if self.age >= self.lifespan:
            return True
        return False

    def get_pos(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def get_vel(self):
        return self.vel

    def set_vel(self, vel):
        self.vel = vel

    def collide(self, other_object):
        if dist(self.pos, other_object.get_pos()) <= self.radius + other_object.get_radius():
            return True
        return False
    #end_fold

# timer handler that spawns a rock    
#start_fold
def rock_spawner():
    if len(rock_group) < 12 and is_in_game:
        vel_direction = [random.choice([-1, 1]), random.choice([-1, 1])]
        vel_x = (random.random() * (rock_max_vel[0] - rock_min_vel[0]) + rock_min_vel[0]) * vel_direction[0]
        vel_y = (random.random() * (rock_max_vel[1] - rock_min_vel[1]) + rock_min_vel[1]) * vel_direction[1]
        vel = [vel_x, vel_y]

        ang_vel_direction = random.choice([-1, 1])
        min_ang_vel = 0
        max_ang_vel = math.pi / 30
        ang_vel = (random.random() * (max_ang_vel - min_ang_vel) + min_ang_vel) * ang_vel_direction

        rock = Sprite(pos = 'random', vel = vel, ang = 0, ang_vel = ang_vel, image = asteroid_image, info = asteroid_info, sound = None)
        if dist(rock.get_pos(), my_ship.get_pos()) > \
                (rock.get_radius() + my_ship.get_radius()) * 3:
            rock_group.add(rock)
#end_fold

def draw(canvas):
    #start_fold
    global time
    
    # animiate background
    #start_fold
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    #end_fold

    if is_show_splash:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), SPLASH_POS, splash_info.get_size())
    else:
        if is_in_game:
            my_ship.draw(canvas)
            my_ship.update()
        process_sprite_group(rock_group, canvas)
        if not is_in_game:
            finish_game(canvas)
        score_text = 'Score: ' + str(score)
        lives_text = 'Lives: ' + str(lives)
        level_text = 'Level: ' + str(level)
        canvas.draw_text(score_text, (WIDTH - WIDTH / 6, HEIGHT * 0.09), 20, 'white')
        canvas.draw_text(level_text, (WIDTH - WIDTH / 6, HEIGHT * 0.12), 20, 'white')
        canvas.draw_text(lives_text, (WIDTH / 16, HEIGHT * 0.10), 20, 'white')
    #end_fold

def splash_click_handler(position):
    #start_fold
    global is_in_game, is_show_splash

    splash_pos_x_min = SPLASH_POS[0] - splash_info.get_size()[0] / 2;
    splash_pos_x_max = SPLASH_POS[0] + splash_info.get_size()[0] / 2;

    splash_pos_y_min = SPLASH_POS[1] - splash_info.get_size()[1] / 2;
    splash_pos_y_max = SPLASH_POS[1] + splash_info.get_size()[1] / 2;

    if position[0] in range(splash_pos_x_min, splash_pos_x_max) and position[1] in range(splash_pos_y_min, splash_pos_y_max):
        is_in_game = True
        is_show_splash = False
        soundtrack.rewind()
        soundtrack_2.play()
    #end_fold

def process_sprite_group(rock_group, canvas):
    #start_fold
    global lives, score, level, my_ship, is_level_up, rock_min_vel, rock_max_vel

    rock_group_copy = set(rock_group)
    missile_group_copy = set(missile_group)
    explosion_group_copy = set(explosion_group)

    for rock in rock_group_copy:
        rock.draw(canvas)
        rock.update()
        if is_in_game and rock.collide(my_ship):
            explosion = Sprite(pos = rock.get_pos(), vel = [0, 0], ang = 0, ang_vel = 0, image = rock_explosion_image, info = rock_explosion_info, sound = explosion_sound)
            explosion_group.add(explosion)
            rock_group.discard(rock)
            lives -= 1
            if lives <= 0:
                for i in range(100): # more explosions to god of exlosions!
                    x_offset = random.randrange(-50, 50)
                    y_offset = random.randrange(-50, 50)
                    explosion_pos_x = my_ship.get_pos()[0] + x_offset
                    explosion_pos_y = my_ship.get_pos()[1] + y_offset
                    explosion_pos = [explosion_pos_x, explosion_pos_y]
                    explosion = Sprite(pos = explosion_pos, vel = [0, 0], ang = 0, ang_vel = 0, image = ship_explosion_image, info = ship_explosion_info, sound = explosion_sound)
                    explosion_group.add(explosion)
        if lives <= 0:
            finish_game(canvas, rock = rock)
            rock_vel = [x * 1.005 for x in rock.get_vel()]
            rock.set_vel(rock_vel)
        for missile in missile_group_copy:
            if rock.collide(missile):
                explosion = Sprite(pos = rock.get_pos(), vel = [0, 0], ang = 0, ang_vel = 0, image = rock_explosion_image, info = rock_explosion_info, sound = explosion_sound)
                explosion_group.add(explosion)
                rock_group.discard(rock)
                missile_group.discard(missile)
                score += 1
                if score % 10 == 0 and is_level_up:
                    rock_min_vel = [x * 2 for x in rock_min_vel]
                    rock_max_vel = [x * 2 for x in rock_max_vel]
                    level += 1
                    is_level_up = False
                else:
                    is_level_up = True
    for missile in missile_group_copy:
        missile.draw(canvas)
        if missile.update():
            missile_group.discard(missile)
    for explosion in explosion_group_copy:
        explosion.draw(canvas)
        if explosion.update():
            explosion_group.discard(explosion)
    #end_fold

def restart_game():
    #start_fold
    global is_in_game, is_show_splash, is_level_up, my_ship, rock_group, missile_group, explosion_group, lives, score, level, text_transperancy, soundtrack_volume, rock_min_vel, rock_max_vel, stop_dec_transparancy_looser_text

    soundtrack_2.rewind()
    soundtrack_volume = 0.6
    soundtrack_2.set_volume(soundtrack_volume)
    soundtrack.play()

    is_in_game = False
    is_show_splash = True
    is_level_up = False
    my_ship = Ship(pos = [WIDTH / 2, HEIGHT / 2], vel = [0, 0], angle = 0, image = ship_image, info = ship_info, sound = None)
    rock_group = set()
    missile_group = set()
    explosion_group = set()
    lives = 3
    score = 0
    level = 1
    text_transperancy = 0
    rock_min_vel = [WIDTH / 5000.0, HEIGHT / 5000.0]
    rock_max_vel = [WIDTH / 500.0, HEIGHT / 500.0]
    stop_dec_transparancy_looser_text = False
    #end_fold

def finish_game(canvas, rock = None):
    #start_fold
    global is_in_game, my_ship, text_transperancy, soundtrack_volume, stop_dec_transparancy_looser_text

    is_in_game = False

    # destroy ship
    ship_thrust_sound.pause()
    del my_ship

    # nice printing of loser text
    text = 'WASTED'
    text_color = 'rgba(255, 0, 0, ' + str(text_transperancy) + ')'
    text_pos = [WIDTH / 4, HEIGHT / 2]
    text_size = 100
    canvas.draw_text(text, text_pos, text_size, text_color)
    if text_transperancy < 1 and not stop_dec_transparancy_looser_text:
        text_transperancy += 0.005
    elif len(rock_group) == 0 and text_transperancy >= -1:
        stop_dec_transparancy_looser_text = True
        text_transperancy -= 0.005
        soundtrack_volume -= soundtrack_volume / 100
        soundtrack_2.set_volume(soundtrack_volume)
    elif text_transperancy <= -1:
        restart_game()

    # destroy rocks which outside of screen to low computer power usage
    if rock != None and \
            int(rock.get_pos()[0]) not in range(int(-rock.vel[0]), WIDTH + int(rock.vel[0])) and  \
            int(rock.get_pos()[1]) not in range(int(-rock.vel[1]), HEIGHT + int(rock.vel[1])):
        rock_group.discard(rock)
    #end_fold

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# register handlers
#start_fold
frame.set_draw_handler(draw)
frame.set_keydown_handler(my_ship_keydown_handler)
frame.set_keyup_handler(my_ship_keyup_handler)
timer_rock_spawner = simplegui.create_timer(1000.0, rock_spawner)
frame.set_mouseclick_handler(splash_click_handler)
#end_fold

# get things rolling
#start_fold
restart_game()
timer_rock_spawner.start()
frame.start()
#end_fold
