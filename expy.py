import pygame
import time
import random
import os.path
import pandas as pd
from displayElements import *
from pygame import movie
from Tkinter import *
import vlc

#### Participant Name
participant = 'max'

#Colours
black = (0,0,0)
white = (255,255,255)
red = (255, 102, 102)
green = (0,200,0)
yellow = (255,255,0)
bright_yellow = (255,255,102)
bright_red = (255, 153, 153)
bright_green = (0,255,0)
orange = (204,204,0)

#Display Settings
pygame.init()
display_width = 1680
display_height = 1050


gameDisplay = pygame.display.set_mode((display_width, display_height), pygame.FULLSCREEN)
pygame.display.set_caption('Assessment Experiment')
clock = pygame.time.Clock()
startImg = pygame.image.load(os.path.join("img", 'start.png'))


times_from_start = []
times_to_decide = []
order = []

# Next Steps

'''
At start, before starting the first profile, enter demographics, time starts once demographics are entered.
1. Enter a new name upon starting experiment, change the csv. output files to name entered in a single csv file
2. Add a survey where the user inputs values or strings to questions
3. Play Video instead of showing images for brief function, loop to main menu, make the brief no  longer able to
be selected
4. Host the file online so users can log in at scheduled times to complete the experiment.
'''

def start_brief():

    FPS = 60


    pygame.display.get_wm_info()
    movie = os.path.expanduser('Tutorial_1.mpg')
    vlcInstance = vlc.Instance()
    media = vlcInstance.media_new(movie)
    player = vlcInstance.media_player_new()
    player.set_media(media)
    pygame.mixer.quit()

    player.play()






def start_experiment():
    experiment.resetAndDisplay()

def start_practice():
    practice.resetAndDisplay()

def end_experiment():
    times_from_start = experiment.list_times_from_start()
    times_to_decide = experiment.list_times_to_decide()
    responses = experiment.list_decisions()

    order = [experiment.profiles[0].ID, experiment.profiles[1].ID, experiment.profiles[2].ID,experiment.profiles[3].ID]

    #,
    #experiment.profiles[4].ID, experiment.profiles[5].ID]

   # ,experiment.profiles[6].ID, experiment.profiles[7].ID,
   # experiment.profiles[8].ID, experiment.profiles[9].ID, experiment.profiles[10].ID,
   # experiment.profiles[11].ID, experiment.profiles[12].ID, experiment.profiles[13].ID


    #print(times_from_start)
    data1 = pd.DataFrame(times_to_decide)
    data2 = pd.DataFrame(responses)
    data3 = pd.DataFrame(order)

    data1.columns = ['Time']
    data2.columns = ['Response']
    data3.columns = ['Order']

    pd.DataFrame.to_csv(data1, participant + ' time.csv', )
    pd.DataFrame.to_csv(data2, participant + ' response.csv', )
    pd.DataFrame.to_csv(data3, participant + ' order.csv', )

    quitExperiment()





def quitExperiment():
    pygame.quit()
    quit()

def experiment_Title():
    intro = True

    while intro:
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True


        gameDisplay.fill(white)

        gameDisplay.blit(startImg, (0, 0))
        #pygame.draw.rect(gameDisplay, orange, ((display_width/2)-325,(display_height/2)-100, 600, 200))

        largeText = pygame.font.Font('freesansbold.ttf', 34)
        largeText2 = pygame.font.Font('freesansbold.ttf', 24)
        TextSurf, TextRect = text_objects("Psychological Assessment Task", largeText)
        TextRect.center = (320, 190)
        gameDisplay.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects("-Correctional Officer Recruitment-", largeText2)
        TextRect.center = (305, 250)
        gameDisplay.blit(TextSurf, TextRect)

        y1 = 300
        button2(gameDisplay, "Brief     ", 60, y1, 100, 35, white, bright_green, clicked, start_brief)
        button2(gameDisplay, "Practice", 60, y1+40, 100, 35, white, bright_green, clicked, start_practice)
        button2(gameDisplay, "Start      ", 60, y1+(40*2), 100, 35, white, bright_green, clicked, start_experiment)
        button2(gameDisplay, "Quit       ", 60, y1+(40*3), 100, 35, white, bright_red, clicked, quitExperiment)

        pygame.display.update()
        clock.tick(15)

    pygame.display.update()
    clock.tick(15)

experiment = Experiment(gameDisplay, end_experiment)
practice = Practice(gameDisplay, experiment_Title)
experiment_Title()