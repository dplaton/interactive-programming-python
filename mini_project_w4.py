# Implementation of classic arcade game Pong

import simpleguitk as simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
countdown = 4

paddle1_vel = paddle2_vel = 0


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists    

    ball_pos = [WIDTH/2, HEIGHT/2]
    vel_x = random.randrange(120,240) / 60
    vel_y = random.randrange(60,180) / 60

    if (direction == "RIGHT"):
        ball_vel = [vel_x,-vel_y]
    elif (direction == "LEFT"):
        ball_vel = [-vel_x,-vel_y]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    global countdown

    score1 = score2 = 0

    paddle1_pos = paddle2_pos = HEIGHT/2
    countdown = 4
    timer.start()

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
      
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    if (paddle1_pos <= HALF_PAD_HEIGHT):
        paddle1_pos = HALF_PAD_HEIGHT
    elif (paddle1_pos >= HEIGHT - HALF_PAD_HEIGHT - 1):
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT -1

    paddle2_pos += paddle2_vel
    if (paddle2_pos <= HALF_PAD_HEIGHT):
        paddle2_pos = HALF_PAD_HEIGHT
    elif (paddle2_pos >= HEIGHT - HALF_PAD_HEIGHT - 1):
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT - 1

    # draw paddles
    c.draw_polygon([[0,paddle1_pos - HALF_PAD_HEIGHT], [PAD_WIDTH, paddle1_pos-HALF_PAD_HEIGHT], [PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT],[0, paddle1_pos + HALF_PAD_HEIGHT] ],1,"White","White")
    c.draw_polygon([[WIDTH-PAD_WIDTH,paddle2_pos - HALF_PAD_HEIGHT],[WIDTH,paddle2_pos-HALF_PAD_HEIGHT ], [WIDTH, paddle2_pos + HALF_PAD_HEIGHT], [WIDTH-PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT]],1,"White","White")

    # draw scores
    c.draw_text(str(score1), [WIDTH / 4, 50],24,"White")
    c.draw_text(str(score2), [WIDTH - WIDTH / 4, 50],24,"White")

    # if the timer is still running the game hasn't begun yet
    # show the timer and leave
    if (timer.is_running()):
        c.draw_text(str(countdown), [WIDTH/2-30, HEIGHT/2], 60, "RED")
        return

    # update ball
    # detect collision to upper/bottom walls
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if (ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS) or (ball_pos[1] <= BALL_RADIUS-1):
        ball_vel[1] = -ball_vel[1]

    #detect collision with the left / right gutter and paddles
    if (ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS):
        if (ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT) and (ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT):
            # right paddle collision detected
            ball_vel[0] = -(ball_vel[0] + ball_vel[0] * 0.1)
        else:
            score1 += 1
            spawn_ball("LEFT")
    if (ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH) - 1):
        if (ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT) and (ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT):
            # right paddle collision detected
            ball_vel[0] = -(ball_vel[0] + ball_vel[0] * 0.1)
        else:
            score2 += 1
            spawn_ball("RIGHT")

    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 1, "White","White")      


def keydown(key):
    global paddle1_vel, paddle2_vel
    paddle_acc = 4
    # controls for left paddle
    if (key == simplegui.KEY_MAP["w"]):
        paddle1_vel -= paddle_acc
    elif (key == simplegui.KEY_MAP["s"]):
        paddle1_vel += paddle_acc   

    # controls for right paddle
    if (key == simplegui.KEY_MAP["up"]):
        paddle2_vel -= paddle_acc
    elif (key == simplegui.KEY_MAP["down"]):
        paddle2_vel += paddle_acc  
   
def keyup(key):
    global paddle1_vel, paddle2_vel

    # stop the paddles on key up
    if (key == simplegui.KEY_MAP["w"]) or (key == simplegui.KEY_MAP["s"]):
        paddle1_vel = 0

    if (key == simplegui.KEY_MAP["up"]) or (key == simplegui.KEY_MAP["down"]):
        paddle2_vel = 0

# countdown timer for the start of the game
# when the timer reaches 0 the ball spawns
def timer_countdown():
    global countdown
    countdown -= 1
    if (countdown == 0):
        spawn_ball("RIGHT")
        timer.stop()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button(" Restart ", new_game)
# Add a countdown timer to the beginning of the game
timer = simplegui.create_timer(1000,timer_countdown)
new_game()
# start frame
frame.start()
