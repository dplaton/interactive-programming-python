# Spaceship - Python mini-project for week 7

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
FRICTION = 0.02
score = 0
lives = 3
time = 0.5

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
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
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

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
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
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
    
    # draw the text on the canvas
    canvas.draw_text("Lives",[40,40],25,"#FFFFFF","monospace")
    canvas.draw_text(str(lives),[40,65],25,"#FFFFFF","monospace")
    
    canvas.draw_text("Score",[WIDTH-100,40], 25, "#FFFFFF","monospace")
    canvas.draw_text(str(score),[WIDTH-100,65],25,"#FFFFFF","monospace")
            
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    # make the rocks spawn closer to the ship
    rock_position = [random.randrange(WIDTH / 4, WIDTH - WIDTH/4),random.randrange(HEIGHT / 4, HEIGHT - HEIGHT/4)];
    # random velocity
    rock_velocity = [random.randrange(-3,3), random.randrange(-3,3)];
    # random spin velocity and direction
    ang_vel = 0.3 * random.random() * random.choice([-1,1])
    a_rock = Sprite(rock_position, rock_velocity, 0, ang_vel, asteroid_image, asteroid_info)
    
def keydown_handler(key):
    for i in keymaps_down:
        if key == simplegui.KEY_MAP[i]:
            keymaps_down[i]();

def keyup_handler(key):
     for i in keymaps_up:
        if key == simplegui.KEY_MAP[i]:
            keymaps_up[i]();

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0.08, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# keyboard mappings
keymaps_down = { "right":my_ship.turn_cw, "left":my_ship.turn_ccw,"up":my_ship.thrust_on, "space":my_ship.shoot }
keymaps_up = { "right":my_ship.stop_turn, "left":my_ship.stop_turn,"up":my_ship.thrust_off }


# register handlers
frame.set_draw_handler(draw)
frame.set_keyup_handler(keyup_handler)
frame.set_keydown_handler(keydown_handler)
timer = simplegui.create_timer(1000.0, rock_spawner)

soundtrack.play()

# get things rolling
timer.start()
frame.start()
