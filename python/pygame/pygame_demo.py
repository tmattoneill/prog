import pygame, sys, os
from pygame.locals import * # This module contains various constants used by Pygame
  
def quit():
	''' Self explanatory '''
	pygame.quit()
	sys.exit(0)
  
def input(events):
	''' Function to handle events, particularly quitting the program '''
	for event in events:
		if event.type == QUIT:
			quit()
		else:
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					quit()
				#else:
				#   print event.key
			else:
				print (event)
  
# Initialize all imported Pygame modules (a.k.a., get things started)
pygame.init()
  
# Set the display's dimensions
screenDimensions = (800, 600)
window = pygame.display.set_mode(screenDimensions)
pygame.display.set_caption('Pygame') # Set the window bar title
screen = pygame.display.get_surface() # This is where images are displayed
  
# Clear the background
background = pygame.Surface(screen.get_size()).convert()
background.fill((255, 255, 255))
screen.blit(background, (0,0))
  
# Draw circle
pygame.draw.circle(screen, (0, 255, 255), (100,100), 75)

def draw_text(screen, text_str, text_size, posx, posy, color=(0,0,0)):
	font = pygame.font.Font('/Library/Fonts/Microsoft/Tw Cen MT.ttf', text_size)
	text = font.render(text_str, 1, color)
	screen.blit(text, (posx, posy))

# Draw a string onto screen
draw_text(screen, "The quick brown fox ran over the lazy dog.", 24, 150, 400, (0,0,255))
pygame.display.flip()
  
# The game loop
while True:
	input(pygame.event.get())