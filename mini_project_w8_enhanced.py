# Spaceship - Python mini-project for week 7

import simplegui

import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
FRICTION = 0.02
MAX_ROCKS = 12
MIN_SPAWN_DISTANCE = 60
score = 0
lives = 3
time = 0.5
started = False

rock_group = set([])
missile_group = set([])
explosion_group = set([])

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
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

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_thrust_info = ImageInfo([135,45],[90,90],35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5, 5], [10, 10], 3, 40)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    
    # this is static (i.e. the same value for all Ship instances)
    _ANGLE_VEL = .06
    
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.fwd = [0,0]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_info = info
        self.update_info()
        self.blown = 0
        
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)


    def update(self):
        self.update_info();
        
        self.angle += self.angle_vel   
        self.fwd = angle_to_vector(self.angle)
        
        for i in range(2):
            self.vel[i] *= (1 - FRICTION)
            if self.thrust:
                self.vel[i] += 0.2 * self.fwd[i]
                            
            self.pos[i] += self.vel[i]

        # wrap the spaceship around the edges
        if (self.pos[0] > WIDTH):
            self.pos[0] -= WIDTH
        if (self.pos[0] < 0):
            self.pos[0] = WIDTH - self.pos[0]
        if (self.pos[1] > HEIGHT):
            self.pos[1] -= HEIGHT
        if (self.pos[1] < 0):
            self.pos[1] = HEIGHT - self.pos[1]

    def update_info(self):
        self.image_center = self.image_info.get_center()
        self.image_size = self.image_info.get_size()
        self.radius = self.image_info.get_radius()    
    
    def thrust_on(self):
        self.thrust = True
        self.image_info = ship_thrust_info
        ship_thrust_sound.play()

    def thrust_off(self):
        self.thrust = False
        self.image_info = ship_info
        ship_thrust_sound.rewind()
        
    def turn_cw(self):
        self.angle_vel = self._ANGLE_VEL

    def turn_ccw(self):
        self.angle_vel = -self._ANGLE_VEL

    def stop_turn(self):
        self.angle_vel = 0

    def shoot(self):
        global a_missile
        vel_multiplier = 5
        
        missile_vel=[0,0]
        missile_pos = [0,0]
        # position the missile in front of the "cannon"
        missile_pos[0] = self.pos[0] + (self.image_info.get_size()[0]/2 * math.cos(self.angle))
        missile_pos[1] = self.pos[1] + (self.image_info.get_size()[1]/2 * math.sin(self.angle))
       
        for i in range(2):
            missile_vel[i] = self.vel[i] + vel_multiplier * self.fwd[i]

        a_missile = Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)

    def get_position(self):
        return self.pos;

    def set_position(self, new_pos):
        self.pos = new_pos

    def get_radius(self):
        return self.image_info.get_radius()

    def collide(self, other_sprite):
        """ Detects collisions between this sprite and another
        """

        collided = False
        distance = dist(other_sprite.get_position(), self.get_position())
        if (distance < other_sprite.get_radius() + self.get_radius()):
            collided = True

        return collided

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang , ang_vel, image, info, sound = None, name = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = list(info.get_center())
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        if name:
            self.name=name
        else:
            self.name="noname"
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        if not self.animated:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            sprite_idx = (self.age % self.image_size[0]) // 1
            self.image_center[0] = self.image_center[0] + self.image_size[0] * sprite_idx
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.angle += self.angle_vel   
        for i in range(2):
            self.pos[i] += self.vel[i]
            self.pos[i] += self.vel[i]

        if (self.pos[0] > WIDTH):
            self.pos[0] -= WIDTH
        if (self.pos[0] < 0):
            self.pos[0] = WIDTH - self.pos[0]
        if (self.pos[1] > HEIGHT):
            self.pos[1] -= HEIGHT
        if (self.pos[1] < 0):
            self.pos[1] = HEIGHT - self.pos[1]

        self.age += 1
        return not (self.age < self.lifespan)

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def collide(self, other_sprite):
        """ Detects collisions between this sprite and another
        """
        collided = False
        distance = dist(other_sprite.get_position(), self.get_position())
        if (distance < other_sprite.get_radius() + self.get_radius()):
            collided = True

        return collided

    def __str__(self):
        return "Name: " + self.name + ";age:" + str(self.age)


def group_collide(sprite, sprite_group):
    """ Detects collision between a sprite and a group of sprites
    """
    sg_copy = set(sprite_group)
    detected = False
    for s in sg_copy:
        if sprite.collide(s):
            explosion = Sprite(s.get_position(),[0,0],0,0,explosion_image,explosion_info, explosion_sound, "explosion")
            explosion_group.add(explosion)
            sprite_group.remove(s)
           
            detected = True

    return detected

def group_group_collide(sprite_group_1, sprite_group_2):

    sg1_copy = set(sprite_group_1)
    num_elements = 0

    for sprite in sg1_copy:
        if (group_collide(sprite, sprite_group_2)):
            num_elements += 1

    return num_elements

def draw_sprite_group(group, canvas):
    """ Draws and updates a group of sprites 
    """
    sg_copy = set(group)
    for sprite in sg_copy:
        sprite.draw(canvas)
        if (sprite.update()):
           
            group.remove(sprite)

def stop_game():
    global missile_group, rock_group, started
    missile_group = set([])
    rock_group = set([])
    started=False
        
def init_game():
    global score, lives, started
    my_ship.set_position([WIDTH/2, HEIGHT/2])
    score = 0
    lives = 3
    started = True
    
def draw(canvas):
    global time
    
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)   

    draw_sprite_group(missile_group, canvas)
    draw_sprite_group(rock_group,canvas)

    # update ship and sprites
    my_ship.update()

    # detect collisions
    global lives
    if group_collide(my_ship, rock_group):
        explosion = Sprite(my_ship.get_position(),[0,0],0,0,explosion_image,explosion_info, explosion_sound, "explosion")
        explosion_group.add(explosion)
        lives -= 1

    global score
    score += group_group_collide(missile_group, rock_group)

    draw_sprite_group(explosion_group, canvas)

    # draw the text on the canvas
    canvas.draw_text("Lives",[40,40],25,"#FFFFFF","monospace")
    canvas.draw_text(str(lives),[40,65],25,"#FFFFFF","monospace")
    
    canvas.draw_text("Score",[WIDTH-100,40], 25, "#FFFFFF","monospace")
    canvas.draw_text(str(score),[WIDTH-100,65],25,"#FFFFFF","monospace")

    global started
    if lives == 0:
        stop_game()

     # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())


# timer handler that spawns a rock    
def rock_spawner():

    # don't to anything if the game is not started
    # or we have enough rocks
    if not started or len(rock_group) == MAX_ROCKS:
        return 

    # spawn the rock at a minimum distance from the ship
    x_pos = random.randrange(WIDTH / 3, WIDTH - WIDTH / 3)
    y_pos = random.randrange(HEIGHT / 3, HEIGHT - HEIGHT / 3)
    rock_position = [x_pos, y_pos]
    if (dist(rock_position, my_ship.get_position()) < MIN_SPAWN_DISTANCE):
        return

    # random velocity
    rock_velocity = [random.randrange(-2,2), random.randrange(-2,2)];
    # random spin velocity and direction
    ang_vel = 0.3 * random.random() * random.choice([-1,1])
    # add the rock to our list
    rock_group.add( Sprite(rock_position, rock_velocity, 0, ang_vel, asteroid_image, asteroid_info, None, "Rock"))

def keydown_handler(key):
    for i in keymaps_down:
        if key == simplegui.KEY_MAP[i]:
            keymaps_down[i]();

def keyup_handler(key):
     for i in keymaps_up:
        if key == simplegui.KEY_MAP[i]:
            keymaps_up[i]();

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        init_game()

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# keyboard mappings
keymaps_down = { "right":my_ship.turn_cw, "left":my_ship.turn_ccw,"up":my_ship.thrust_on, "space":my_ship.shoot }
keymaps_up = { "right":my_ship.stop_turn, "left":my_ship.stop_turn,"up":my_ship.thrust_off }

# register handlers
frame.set_draw_handler(draw)
frame.set_keyup_handler(keyup_handler)
frame.set_keydown_handler(keydown_handler)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

soundtrack.play()

# get things rolling
timer.start()
frame.start()