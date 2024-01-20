"""
    Author: Clarke N.

    Date: June 2, 2022

    Description: Sprites for Sketchy Skies
"""

import pygame, random

class Cloud(pygame.sprite.Sprite):
    '''This class defines the sprite for a cloud'''
    def __init__(self, screen, y, x):
        '''Initializer method'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        # Creating the image sprite
        self.image = pygame.image.load('cloud.png')
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (100, 25))
        self.image.set_colorkey((255,255,255))

        # Keep track of the screen so we can call get_witdth() and get_height()
        self.window = screen
        self.cy = y
        self.cx = x

        # Define the position of our image using it's rect
        self.rect = self.image.get_rect()

        if self.cx == 240:
            self.rect.center = ((self.cx,self.cy))
        else:
            self.rect.center = ((random.randint(50,430),self.cy))

        self.dy = 0
        self.gravity = 1

    def update(self):
        '''This method will be called automatically to reposition the
        cloud sprite on the screen.'''
        if self.dy != 0:
            self.dy -= self.gravity
        self.rect.centery += self.dy
        if self.dy == 55:
            self.dy = 0

class Player(pygame.sprite.Sprite):
    '''This class defines the sprite for the player'''
    def __init__(self, screen):
        '''Initializer method'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        # Unique instance variables for all of the player images
        self.right_image = pygame.image.load('playerRight.png')
        self.left_image = pygame.image.load('playerLeft.png')

        self.jetAnimationL = [pygame.image.load('playerLeftJet1.png'),pygame.image.load('playerLeftJet2.png'),pygame.image.load('playerLeftJet3.png')]
        self.jetAnimationR = [pygame.image.load('playerRightJet1.png'),pygame.image.load('playerRightJet2.png'),pygame.image.load('playerRightJet3.png')]

        # Creating the image sprite
        # Converting the sprite of a plain surface, then
        # setting the image to the right player model so that
        # there is no white background on the player sprite at the start
        self.image = pygame.Surface((50,50))
        self.image = self.image.convert()
        self.image = self.right_image

        # Keep track of the screen so we can call get_witdth()
        self.window = screen

        # Define the position of our image using it's rect
        self.rect = self.image.get_rect()
        self.rect.center = ((self.window.get_width()//2,(self.window.get_height()//2)+100))
        self.dx = 0
        self.dy = 5
        self.gravity = 0.5

    def jump(self):
        '''This method causes the Player sprite to bounce off a cloud'''
        self.dy = -15

    def goLeft(self):
        '''This method causes the Player sprite to move left'''
        self.image = self.left_image
        self.dx = -8

    def goRight(self):
        '''This method causes the Player sprite to move right'''
        self.image = self.right_image
        self.dx = 8

    def goLeftJet(self,time):
        '''This method causes the Player sprite to move left'''
        self.image = self.jetAnimationL[0]
        self.dx = -10

    def goRightJet(self,time):
        '''This method causes the Player sprite to move right'''
        self.image = self.jetAnimationR[0]
        self.dx = 10

    def update(self):
        '''This method will be called automatically to reposition the
        player sprite on the screen.'''
        self.dy += self.gravity
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        if self.rect.centerx > self.window.get_width() + 18:
            self.rect.centerx = -18
        elif self.rect.centerx < -18:
            self.rect.centerx = self.window.get_width() + 18


class Jetpack(pygame.sprite.Sprite):
    '''This class defines a jetpack sprite'''
    def __init__(self,x,y):
        '''This initializer method loads all of the images
        and sets the position of the jetpack'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('Jetpack.png')
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (45,65))
        self.image.set_colorkey((0,0,0))

        # Define the position of our image using it's rect
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)

        self.dy = 0

    def update(self):
        '''This method will be called automatically to reposition the
        jetpack sprite on the screen.'''
        if self.dy != 0:
            self.dy -= 1
        self.rect.centery += self.dy

class Spring(pygame.sprite.Sprite):
    '''This class defines a spring sprite'''
    def __init__(self,x,y):
        '''This initializer method loads all of the images
        and sets the position of the spring'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('spring.png')
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (50,40))
        self.image.set_colorkey((0,0,0))

        # Define the position of our image using it's rect
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)

        self.dy = 0

    def update(self):
        '''This method will be called automatically to reposition the
        spring sprite on the screen.'''
        if self.dy != 0:
            self.dy -= 1
        self.rect.centery += self.dy

class Alien(pygame.sprite.Sprite):
    '''This class defines an alien sprite'''
    def __init__(self,x,y,screen):
        '''This initializer method loads all of the images
        and sets the position of the spring'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('alien.png')
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (45,60))
        self.image.set_colorkey((0,0,0))

        # Keep track of the screen so we can call get_width()
        self.window = screen

        # Define the position of our image using it's rect
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)

        self.dy = 0
        self.dx = 10
    def update(self):
        '''This method will be called automatically to reposition the
        alien sprite on the screen.'''
        if self.dy != 0:
            self.dy -= 1
        self.rect.centery += self.dy
        self.rect.centerx += self.dx
        if self.rect.centerx >= self.window.get_width() or self.rect.centerx <= 0:
            self.dx = -self.dx

class BlackHole(pygame.sprite.Sprite):
    '''This class defines a black hole sprite'''
    def __init__(self,x,y):
        '''This initializer method loads all of the images
        and sets the position of the black hole'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('blackHole.png')
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (160,160))
        self.image.set_colorkey((0,0,0))

        # Define the position of our image using it's rect
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)

        self.dy = 0
    def update(self):
        '''This method will be called automatically to reposition the
        black hole sprite on the screen.'''
        if self.dy != 0:
            self.dy -= 1
        self.rect.centery += self.dy

class ScoreKeeper(pygame.sprite.Sprite):
    '''This class defines a label sprite to display the score.'''
    def __init__(self):
        '''This initializer loads the system font "Arial", and
        sets the starting score to 0'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        # Load our custom font, and initialize the starting score.
        self.CustomFont = pygame.font.Font("BorderBase.ttf", 50)
        self.playerScore = 0

    def addScore(self, amount):
        self.score = amount
        self.playerScore += self.score

    def update(self):
        '''This method will be called automatically to display
        the current score at the top of the game window.'''
        message = "SCORE:" + str(self.playerScore)
        self.image = self.CustomFont.render(message, 1, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (240, 15)

