"""
    Author: Clarke N.

    Date: June 2, 2022

    Description: Sketchy Skies. A rip off of doodle jump (Platformer game)

            v1.0 --> Creating a cloud and implementing the “bouncing” effect with the player
            v2.0 --> Add event handling to be able to control the player left and right.
                     Plus if the user goes out of the boundaries of the screen, they appear on the other side of the screen.
            v3.0 --> Add a random amount of clouds and randomize their location
            v4.0 --> When the player bounces up off of a cloud, make the clouds go down on the screen equal to
                     the magnitude of the jump so that the player is always centered on the screen and never
                     goes too high. This will give the illusion that the player is jumping up.
            v5.0 --> Make the game infinite by always creating clouds outside of the display window and letting them appear into it
            v6.0 --> Add a score keeper that keeps track of the score depending on how high the player reaches.
            v7.0 --> Add the false clouds that will break when the player bounces off of it, and add the moving clouds
            v8.0 --> Add the monsters and black holes that randomly spawn only at certain scores
            v9.0 --> Add jetpacks, propellor hats, and springs that randomly spawn on top of clouds only at certain scores
            v10.0 -> Add background music, sound effects and a background
"""

import pygame, Sprites, time, random

def main():
    '''This function defines the 'mainline logic' for our pyPong game.'''
    # I - Initialize pygame
    pygame.init()
    pygame.mixer.init()

    # D - DISPLAY
    screen = pygame.display.set_mode((480,720))
    pygame.display.set_caption("Sketchy Skies")

    # E - ENTITIES
    background = pygame.Surface(screen.get_size())
    background.fill((135, 206, 235))
    screen.blit(background, (0, 0))

    #Loading the game over message
    gameOver = pygame.image.load('gameOver.png')
    gameOver = gameOver.convert()
    gameOver.set_colorkey((255,255,255))

    cloudGroup = []
    for i in range(9):
        if i == 8:
            cloudGroup.append(Sprites.Cloud(screen,80*i,screen.get_width()//2))
        else:
            cloudGroup.append(Sprites.Cloud(screen,80*i,0))
    springGroup = []
    player = Sprites.Player(screen)
    score = Sprites.ScoreKeeper()
    alien = Sprites.Alien(-50,0,screen)
    jetpack = Sprites.Jetpack(-50,0)
    blackHole = Sprites.BlackHole(-80,0)
    clouds = pygame.sprite.OrderedUpdates(cloudGroup)
    allSprites = pygame.sprite.OrderedUpdates(blackHole, cloudGroup, jetpack, alien, player, score)

    # A - ACTION

    # A - ASSIGN
    clock = pygame.time.Clock()
    keepGoing = True
    #Variable to delete cloud sprites to make the game harder
    delete = -1
    #Variables to make a jetpack and springs and aliens
    makeJetpack = False
    makeSpring = False
    makeAlien = False
    makeBH = False
    # Variable to change player image when it has a jetpack
    animateJet = False

    timer = 0

    # Hide the mouse pointer
    pygame.mouse.set_visible(False)

    # L - LOOP
    while keepGoing:

        # TIME
        clock.tick(30)

        timer += 1

        # E - EVENT HANDLING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            if event.type == pygame.KEYDOWN:
                if animateJet == False:
                    if event.key == pygame.K_RIGHT:
                        player.goRight()
                    elif event.key == pygame.K_LEFT:
                        player.goLeft()
                else:
                    if event.key == pygame.K_RIGHT:
                        player.goRightJet(timer)
                    elif event.key == pygame.K_LEFT:
                        player.goLeftJet(timer)
            elif event.type == pygame.JOYHATMOTION:
                if event.value == (1,0):
                    player.goRight()
                elif event.value == (-1,0):
                    player.goLeft()
            else:
                player.dx = 0

        # Collision detection for all of the sprites
        if pygame.sprite.spritecollide(player, clouds, False) and player.dy >= 8 and (player.rect.bottom <= \
        cloudGroup[cloudGroup.index(pygame.sprite.spritecollide(player, clouds, False)[0])].rect.bottom):
            player.jump()
            if player.image == player.jetAnimationL[0]:
                player.image = player.left_image
            elif player.image == player.jetAnimationR[0]:
                player.image = player.right_image
                animateJet = False
        try:
            if player.rect.colliderect(jetpack):
                jetpack.rect.centery = 760
                temp = score.playerScore
                animateJet = True
                player.dy = 10
                player.gravity = -2
                for c in cloudGroup:
                    c.dy = 15
        except:
            pass
        try:
            if score.playerScore - temp > 500:
                player.gravity = 0.5
        except:
            pass
        try:
            if player.rect.colliderect(spring) and player.dy >= 8 and (player.rect.bottom <= \
            spring.rect.bottom):
                player.dy = -25
        except:
            pass
        if player.rect.colliderect(alien) or player.rect.colliderect(blackHole):
            keepGoing = False
        if player.rect.top > screen.get_height():
            keepGoing = False

        # If the players speed is going up or the players y is
        # less than 260, then everything on the screen moves down
        if player.dy < 0:
            for a in cloudGroup:
                a.dy = 15
            try:
                jetpack.dy = 15
                spring.dy = 15
                alien.dy = 15
                blackHole.dy = 15
            except:
                pass
            score.addScore(cloudGroup[len(cloudGroup)-1].dy)
        elif player.rect.top < 260:
            for a in cloudGroup:
                a.dy = 15
            try:
                jetpack.dy = 15
                spring.dy = 15
                alien.dy = 15
                blackHole.dy = 15
            except:
                pass
            score.addScore(cloudGroup[len(cloudGroup)-1].dy)

        # To ensure the player doesn't go off the top of the screen
        if player.rect.centery < 160:
            player.dy = 0.5

        # Using the score to create sprites at certain amounts
        if score.playerScore % 2010 == 0 and score.playerScore != 0:
            delete = 1
        if score.playerScore % 6000 == 0 and score.playerScore != 0:
            makeJetpack = True
        if score.playerScore % 1500 == 0 and score.playerScore != 0:
            makeSpring = True
        if score.playerScore % 3000 == 0 and score.playerScore != 0:
            makeAlien = True
        if score.playerScore % 4500 == 0 and score.playerScore != 0:
            makeBH = True

        # If the cloud sprite is greater than the screen height, I
        # reset the clouds at the top of the screen outside
        # If I want to make a jetpack, alien, spring or black hole,
        # It resets and positions itself with the cloud outside of view
        for x in cloudGroup:
            if x.rect.top > screen.get_height() and delete > 0:
                cloudGroup.remove(x)
                delete = 0
            elif x.rect.top > screen.get_height():
                x.rect.centerx = random.randint(100,380)
                if len(cloudGroup) == 10:
                    x.rect.top = -100
                elif len(cloudGroup) == 9:
                    x.rect.top = -110
                elif len(cloudGroup) == 8:
                    x.rect.top = -120
                elif len(cloudGroup) == 7:
                    x.rect.top = -130
                elif len(cloudGroup) == 6:
                    x.rect.top = -140
                else:
                    x.rect.top = -150
                if makeJetpack:
                    jetpack.rect.center = (x.rect.centerx, x.rect.top-15)
                    makeJetpack = False
                if makeAlien:
                    alien.rect.center = (x.rect.centerx, x.rect.top-15)
                    makeAlien = False
                if makeBH:
                    blackHole.rect.center = (random.randint(80,400), x.rect.top-random.randint(-150,-30))
                    makeBH = False
                if makeSpring:
                    spring = Sprites.Spring(x.rect.centerx, x.rect.top-5)
                    allSprites.clear(screen, background)
                    allSprites = pygame.sprite.OrderedUpdates(blackHole, cloudGroup, spring, jetpack, alien, player, score)
                    makeSpring = False

        # R - REFRESH SCREEN
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()

    # Unhide the mouse pointer
    pygame.mouse.set_visible(True)
    screen.blit(gameOver, (-35, 150))
    pygame.display.flip()
    time.sleep(2)

    # Close the game window
    pygame.quit()

# Call the main function
main()

