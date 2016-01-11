# program template for Spaceship
import simplegui
import math
import random
from user16_DmDJwXW1dy0Sw1u import rgba

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
rock_speed = 10
rock_spawn_speed = 1000	# in miliseconds
thrust_vol = 80
started = False

COF = 0.07				# Friction coefficient
TURN_INC = 0.05			# Turning amount in radians
MISS_ACC = 10			# Missile velocity accelerator
UP_IN_RAD = -1.5708		# Ship pointing up angle in radians
ACC_FACTOR = 0.5		# Accelerator factor
MAX_ROCKS = 5			# Maximum number of asteroids
RIGHT = 1
LEFT = -1
SCORE_INC = 10

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
nebula_image = simplegui.load_image("https://dl.dropboxusercontent.com/u/21868561/images/14424_star_wars_death_star.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 41.5], [90, 83], 35)
ship_image = simplegui.load_image("https://dl.dropboxusercontent.com/u/21868561/images/x-wing_double.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("https://dl.dropboxusercontent.com/u/21868561/images/photon.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://www.sa-matra.net/sounds/starwars/XWing-Laser.wav")
ship_thrust_sound = simplegui.load_sound("http://www.sa-matra.net/sounds/starwars/XWing-Fly3.wav")
explosion_sound = simplegui.load_sound("https://dl.dropboxusercontent.com/u/21868561/sfx/torpedo-hit.mp3")
explode_asteroid = simplegui.load_sound("https://dl.dropboxusercontent.com/u/21868561/sfx/d-charge-short.mp3")
# helper functions to handle transformations
def angle_to_vector(ang):
				return [math.cos(ang), math.sin(ang)]

def dist(p,q):
				return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group(canvas, group):
				sprite_set = set(group)
				
				for sprite in sprite_set:
								sprite.draw(canvas)
								result = sprite.update()
								if result:
												group.remove(sprite)
								
def group_collision(group, other_obj):
				collide_set = set()
				collision = False
				for item in group:
								if item.collision(other_obj):
												collide_set.add(item)
												collision = True
				group.difference_update(collide_set)

				return collision

def group_group_collide(group_1, group_2):
				temp_group = set(group_1)
				hit_list = []
				for item in temp_group:
								if group_collision(group_2, item):
												explode_asteroid.rewind()
												explode_asteroid.play()
												group_1.remove(item)
												hit_list.append(item)            
				return len(hit_list)
		
def start(pos):
		global started, my_ship, asteroids, score, lives
		started = True
		lives = 3
		score = 0
		soundtrack.rewind()
		soundtrack.play()
		my_ship.pos = [WIDTH/2, HEIGHT/2]
		soundtrack.pause()
		for item in asteroids:
				asteroids.remove(item)
				
def game_state(lives):
		global started, my_ship, asteroids, score
		explosion_sound.play()
		ship_thrust_sound.rewind()
		my_ship.pos = [WIDTH / 2, HEIGHT / 2]
		my_ship.angle = UP_IN_RAD
		my_ship.vel = [0,0]
		my_ship.angle_vel = 0.0
		my_ship.thrust = False    
		if lives > 0:
				return True
		else:
				lives = 3
				score = 0
				soundtrack.pause()
				for item in asteroids:
						asteroids.remove(item)
				return False
				
# Ship class
class Ship:
				def __init__(self, pos, vel, angle, image, info):
								self.pos = [pos[0],pos[1]]
								self.vel = [vel[0],vel[1]]
								self.thrust = False
								self.angle = angle
								self.angle_vel = 0.0
								self.image = image
								self.image_center = info.get_center()
								self.image_size = info.get_size()
								self.radius = info.get_radius()
								
				def get_pos(self):
								return self.pos
				
				def get_radius(self):
								return self.radius
				
				def get_center(self):
								return self.image_center
				
				def draw(self,canvas):
								ship_center = [self.image_center[0] + self.image_size[0], self.image_center[1]] if self.thrust else self.image_center
								canvas.draw_image(self.image, ship_center , self.image_size, self.pos, self.image_size, self.angle)

				def thrusting(self):
								self.thrust = True
								ship_thrust_sound.rewind()
								ship_thrust_sound.set_volume(thrust_vol * .01)
								ship_thrust_sound.play()
								
				def turn(self, direction):
								self.angle_vel = TURN_INC * (RIGHT if direction == "right" else LEFT)

				def stop(self, what):
								if what == "turn":
												self.angle_vel = 0
								elif what == "thrust":
												my_ship.thrust = False
												ship_thrust_sound.pause()

				def dies(self, canvas):
								global lives, started
								lives -= 1
								started = game_state(lives)
								
				def shoot(self):
								global missiles
								m_dir = angle_to_vector(self.angle)
								m_pos = [self.pos[0] + self.radius * m_dir[0],
																 self.pos[1] + self.radius * m_dir[1]]
								m_vel = [self.vel[0] + MISS_ACC * m_dir[0], 
																 self.vel[1] + MISS_ACC * m_dir[1]]
								missiles.add(Sprite(m_pos, m_vel, self.angle, 0, missile_image, missile_info, missile_sound))
				
				def update(self):
								#accelerate the ship
								if self.thrust:
												acc_vector = angle_to_vector(self.angle)
												self.vel[0] += acc_vector[0] * ACC_FACTOR
												self.vel[1] += acc_vector[1] * ACC_FACTOR
												
								self.vel[0] *= 1 - COF
								self.vel[1] *= 1 - COF

								self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
								self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

								#turn the ship
								self.angle += self.angle_vel
				
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
												
				def get_pos(self):
								return self.pos
				
				def get_radius(self):
								return self.radius
				
				def get_center(self):
								return self.image_center
				
				def get_age(self):
								return self.age
				
				def __str__(self):
								ret_str = ""
								sprite_attribs = {"Pos: ":self.pos, 
																										"Vel: ": self.vel, 
																										"Ang: ": self.angle,
																										"Img: ": self.image,
																										"Imc.s: ": self.image_center,
																										"Img.c: ": self.image_center,
																										"Rad: ": self.radius,
																										"Lif: ": self.lifespan,
																										"Age: ":self.age}
								for attrib in sprite_attribs:
												ret_str += str(attrib) + str(sprite_attribs[attrib]) + '\n'
								return ret_str
												
				def draw(self, canvas):
								canvas.draw_image(self.image, self.image_center, self.image_size,
																										self.pos, self.image_size, self.angle)

				def collision(self, other_obj):        
								if dist(self.pos, other_obj.get_pos()) < (self.radius + other_obj.get_radius()):
												print other_obj
												return True
								else:
												return False
																
				def update(self):
								# update angle
								self.angle += self.angle_vel
								
								# update position
								self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
								self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
								self.age += 1
								if self.age >= self.lifespan:
												return True
								else:
												return False
										 
def draw(canvas):
				global time, score
				
				# animiate background
				time += 1
				wtime = (time / 4) % WIDTH
				center = debris_info.get_center()
				size = debris_info.get_size()
				canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
				canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
				canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

				# User Interface & Feedback
				canvas.draw_text("Lives: %d"%lives, [100,100], 24, rgba(255,255,255,.5), "monospace")
				canvas.draw_text("Score: %d"%score, [600,100], 24, rgba(255,255,255,.5), "monospace")
				# draw ship and sprites
				my_ship.draw(canvas)
				process_sprite_group(canvas, missiles)
				process_sprite_group(canvas, asteroids)
				
				# update ship and sprites
				my_ship.update()
				if not started:
						canvas.draw_image(splash_image, splash_info.get_center(),
															splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
															splash_info.get_size())
						timer.stop()
				else:
						timer.start()
				
				score += group_group_collide(missiles, asteroids) * SCORE_INC
				my_ship.dies(canvas) if group_collision(asteroids, my_ship) else None
								

def keydown(key):
				global started
				
				if started:
						if key==simplegui.KEY_MAP["left"]:
										my_ship.turn("left")
						elif key==simplegui.KEY_MAP["right"]:
										my_ship.turn("right")
						elif key==simplegui.KEY_MAP["up"]:
										my_ship.thrusting()
						elif key==simplegui.KEY_MAP["space"]:
										my_ship.shoot()
				else:
						started = True
				

def keyup(key):
				if key==simplegui.KEY_MAP["left"]:
								my_ship.stop("turn")
				elif key==simplegui.KEY_MAP["right"]:
								my_ship.stop("turn")
				elif key==simplegui.KEY_MAP["up"]:
								my_ship.stop("thrust")



# timer handler that spawns a rock    
def rock_spawner():
				global asteroids
				vel = [0, 0]
				pos = random.randrange(0, WIDTH), random.randrange(0, HEIGHT)
				
				while dist(my_ship.get_pos(), pos) < my_ship.get_radius()*2:
								pos = random.randrange(0, WIDTH), random.randrange(0, HEIGHT)
								print "Too close; respawn:"
								
				if not len(asteroids) >= MAX_ROCKS:
								#vel = [random.random() * 1.0 - .5, random.random() * 1.0 - .5]
								vel[0] = random.random() * (score / 100)
								vel[1] = random.random() * (score / 100)
								ang = random.randrange(-6, 7)
								ang_vel = random.random() * .2 - .1
								asteroids.add(Sprite(pos, vel, ang, ang_vel, asteroid_image, asteroid_info))

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship, asteroid set and missile set
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], UP_IN_RAD, ship_image, ship_info)
asteroids = set()
missiles = set()

# register handlers
frame.set_mouseclick_handler(start)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
timer = simplegui.create_timer(rock_spawn_speed, rock_spawner)
frame.set_draw_handler(draw)
# get things rolling
timer.start()
frame.start()
