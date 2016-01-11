w# Implementation of classic arcade game Pong

import simplegui, random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 10
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

R_PAD_DISPLACE = WIDTH - PAD_WIDTH
PAD_MOVE = 5.0
ACCELERATOR = 1.1

paddle1_pos = (HEIGHT / 2) - HALF_PAD_HEIGHT
paddle2_pos = paddle1_pos
paddle1_vel = [0.0, 0.0]
paddle2_vel = [0.0, 0.0]
ball_pos = [0, 0]
ball_vel = [0, 0]
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists

    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [random.randrange(1, 4), random.randrange(1, 3)]
 
    if direction == RIGHT:
        ball_vel[0] = ball_vel[0] 
    else :
        ball_vel[0] = -ball_vel[0]
        
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints

    spawn_ball(random.choice([True, False]))
    score1 = 0
    score2 = 0
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
  
    if (ball_pos[1] <= BALL_RADIUS) or (ball_pos[1] >= HEIGHT - BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
        ball_pos[1] += ball_vel[1]
    else:
        ball_pos[1] += ball_vel[1]
        
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")

    # update paddle's vertical position, keep paddle on the screen
    
    # draw paddles
    #left paddle
    u_left_left = [0, paddle1_pos]
    u_right_left = [PAD_WIDTH, paddle1_pos]
    b_right_left = [PAD_WIDTH, (paddle1_pos + PAD_HEIGHT)]
    b_left_left = [0, (paddle1_pos + PAD_HEIGHT)]

    paddle_left = [u_left_left, u_right_left, b_right_left, b_left_left]

    if (paddle1_pos - PAD_MOVE) <= 0 :        
        paddle1_pos = paddle1_pos + 1
    elif (paddle1_pos + PAD_MOVE) >= (HEIGHT - PAD_HEIGHT): 
        paddle1_pos = paddle1_pos - 1
    else:
        paddle1_pos += paddle1_vel[1]
    
    canvas.draw_polygon(paddle_left, 1, "White", "White")
    
    #right paddle
    u_left_right = [R_PAD_DISPLACE, paddle2_pos] 
    u_right_right = [R_PAD_DISPLACE + PAD_WIDTH, paddle2_pos] 
    b_right_right = [R_PAD_DISPLACE + PAD_WIDTH, (paddle2_pos + PAD_HEIGHT)] 
    b_left_right = [R_PAD_DISPLACE, (paddle2_pos + PAD_HEIGHT)] 

    paddle_right = [u_left_right, u_right_right, b_right_right, b_left_right]

    if (paddle2_pos - PAD_MOVE) <= 0 :        
        paddle2_pos = paddle2_pos + 1
    elif (paddle2_pos + PAD_MOVE) >= (HEIGHT - PAD_HEIGHT): 
        paddle2_pos = paddle2_pos - 1
    else:
        paddle2_pos += paddle2_vel[1]
        
    canvas.draw_polygon(paddle_right, 1, "White", "White")

    # determine whether paddle and ball collide    
    #    check if ball is at gutter and if it is, check to see if it is on the paddle
    #    if so, bounce it back into play. Otherwise increase opponent's score and reset ball
    # right gutter
    if ((ball_pos[0] + BALL_RADIUS) >= (WIDTH - PAD_WIDTH)) : # right gutter
        if (paddle2_pos <= ball_pos[1] <= (paddle2_pos + PAD_HEIGHT)) :
            ball_vel[0] = -ball_vel[0] * ACCELERATOR
            ball_pos[0] += ball_vel[0]  
        else:
            score1 += 1
            spawn_ball(LEFT)
    #left gutter
    elif ((ball_pos[0] - BALL_RADIUS) <= (PAD_WIDTH)) :
        if (paddle1_pos <= ball_pos[1] <= (paddle1_pos + PAD_HEIGHT)) :
            ball_vel[0] = -ball_vel[0] * ACCELERATOR
            ball_pos[0] += ball_vel[0]  
        else:
            score2 += 1
            spawn_ball(RIGHT)
    else :
        ball_pos[0] += ball_vel[0]

# draw scores
    canvas.draw_text(str(score1), [WIDTH / 3, 150], 28, "White", "monospace")
    canvas.draw_text(str(score2), [2 * (WIDTH / 3), 150], 28, "White", "monospace")
    
def keydown(key):
    global paddle1_vel, paddle2_vel

    paddle2_vel[1] = PAD_MOVE if key==simplegui.KEY_MAP["down"] else paddle2_vel[1]
    paddle2_vel[1] = -PAD_MOVE if key==simplegui.KEY_MAP["up"] else paddle2_vel[1]
    paddle1_vel[1] = PAD_MOVE if key==simplegui.KEY_MAP["s"] else paddle1_vel[1]
    paddle1_vel[1] = -PAD_MOVE if key==simplegui.KEY_MAP["w"] else paddle1_vel[1]
    
def keyup(key):
    global paddle1_vel, paddle2_vel

    paddle2_vel[1] = 0 if key==simplegui.KEY_MAP["down"] else paddle2_vel[1]
    paddle2_vel[1] = 0 if key==simplegui.KEY_MAP["up"] else paddle2_vel[1]
    paddle1_vel[1] = 0 if key==simplegui.KEY_MAP["s"] else paddle1_vel[1]
    paddle1_vel[1] = 0 if key==simplegui.KEY_MAP["w"] else paddle1_vel[1]

# create frame
frame = simplegui.create_frame("Python Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("New Game", new_game, 150)

# start frame
new_game()
frame.start()
