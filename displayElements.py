import pygame
import os.path
import random
import time
import vlc

clock = pygame.time.Clock()

# Images are done at 130% screen shot.

# Colours
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 102, 102)
green = (0, 200, 0)
yellow = (255, 255, 0)
bright_yellow = (255, 255, 102)
bright_red = (255, 153, 153)
bright_green = (0, 255, 0)

overlay = pygame.image.load(os.path.join("img", 'overlay.png'))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def button(gameDisplay, msg, x, y, w, h, ic, ac, clicked, action):
    mouse = pygame.mouse.get_pos()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if clicked and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(TextSurf, TextRect)


def button2(gameDisplay, msg, x, y, w, h, ic, ac, clicked, action):
    mouse = pygame.mouse.get_pos()

    highlightText = pygame.font.Font("freesansbold.ttf", 22)
    smallText = pygame.font.Font("freesansbold.ttf", 20)

    if x + w > mouse[0] > x and y + h > mouse[1] > y:

        # pygame.draw.rect(gameDisplay, ac, (x, y, w, h))

        TextSurf, TextRect = text_objects(msg, highlightText)
        TextRect.center = ((x + (w / 2)), (y + (h / 2)))
        gameDisplay.blit(TextSurf, TextRect)

        if clicked and action != None:
            action()

    # Option to have default colour in  rect

    else:
        TextSurf, TextRect = text_objects(msg, smallText)
        TextRect.center = ((x + (w / 2)), (y + (h / 2)))
        gameDisplay.blit(TextSurf, TextRect)

        #   pygame.draw.rect(gameDisplay, ic, (x, y, w, h))


def message_display(gameDisplay, display_width, display_height, text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)



class Scale:
    def __init__(self, gameDisplay, name, profile_id, button_x, button_y, exit_action):
        self.gameDisplay = gameDisplay
        self.button_x = button_x
        self.button_y = button_y
        self.image = pygame.image.load(os.path.join("profiles", profile_id, name + '.png'))
        self.exit_action = exit_action

    def displayScaleButton(self, clicked):
        button(self.gameDisplay, "", self.button_x, self.button_y, 10, 20, green, bright_green, clicked,
               self.displayScale)

    # Display Scale Items
    def displayScale(self):
        scale_1 = True
        while scale_1:
            clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = True

            # self.gameDisplay.fill(white)
            self.gameDisplay.blit(self.image, (950, 75))
            self.gameDisplay.blit(overlay, (950, 15))
            button(self.gameDisplay, "Return", 950, 25, 80, 20, red, bright_red, clicked, self.exit_action)
            pygame.display.update()
            clock.tick(15)


class Decision:
    def __init__(self, decision, name, button_x, button_y, highlightColor, gameDisplay, decision_action):
        self.name = name
        self.decision = decision
        self.button_x = button_x
        self.button_y = button_y
        self.highlightColor = highlightColor
        self.gameDisplay = gameDisplay
        self.decision_action = decision_action

    def displayDecisionButton(self, clicked):

        mouse = pygame.mouse.get_pos()

        if self.button_x + 100 > mouse[0] > self.button_x and self.button_y + 20 > mouse[1] > self.button_y:
            pygame.draw.rect(self.gameDisplay, self.highlightColor, (self.button_x, self.button_y, 100, 20))
            if clicked:
                self.decision_action(self.decision)
        else:
            pygame.draw.rect(self.gameDisplay, white, (self.button_x, self.button_y, 100, 20))

        smallText = pygame.font.Font("freesansbold.ttf", 14)
        TextSurf, TextRect = text_objects(self.name, smallText)
        TextRect.center = ((self.button_x + (100 / 2)), (self.button_y + (20 / 2)))
        self.gameDisplay.blit(TextSurf, TextRect)


class Profile:
    def __init__(self, ID, gameDisplay, decision_action):
        profile_id = str(ID)

        self.decision = ""

        self.gameDisplay = gameDisplay
        self.decision_action = decision_action
        self.order = []
        self.decisions = []
        self.ID = ID
        self.scales = []

        # Base Import
        # self.backImg = pygame.image.load(os.path.join("img", 'prof.png'))
        self.baseImg = pygame.image.load(os.path.join("profiles", profile_id, 'base.png'))

        # Validity Scales
        xvs = 238
        yvs = 162
        yvs_adj = 28
        self.scales.append(Scale(self.gameDisplay, 'infrequency', profile_id, xvs, yvs, self.display))
        self.scales.append(Scale(self.gameDisplay, 'superlative', profile_id, xvs, yvs + yvs_adj, self.display))
        self.scales.append(Scale(self.gameDisplay, 'lie', profile_id, xvs, yvs + yvs_adj * 2, self.display))
        self.scales.append(Scale(self.gameDisplay, 'defensiveness', profile_id, xvs, yvs + yvs_adj * 3, self.display))

        xcs = 238
        ycs = 362
        ycs_adj = 28
        # Clinical Scales
        self.scales.append(Scale(self.gameDisplay, 'hypochondriasis', profile_id, xcs, ycs, self.display))
        self.scales.append(Scale(self.gameDisplay, 'depression', profile_id, xcs, ycs + ycs_adj, self.display))
        self.scales.append(Scale(self.gameDisplay, 'hysteria', profile_id, xcs, ycs + ycs_adj * 2, self.display))
        self.scales.append(Scale(self.gameDisplay, 'psychopath', profile_id, xcs, ycs + ycs_adj * 3, self.display))
        self.scales.append(Scale(self.gameDisplay, 'paranoia', profile_id, xcs, ycs + ycs_adj * 4, self.display))
        self.scales.append(Scale(self.gameDisplay, 'psychasthenia', profile_id, xcs, ycs + ycs_adj * 5, self.display))
        self.scales.append(Scale(self.gameDisplay, 'schizophrenia', profile_id, xcs, ycs + ycs_adj * 6, self.display))
        self.scales.append(Scale(self.gameDisplay, 'hypomania', profile_id, xcs, ycs + ycs_adj * 7, self.display))
        self.scales.append(Scale(self.gameDisplay, 'introversion', profile_id, xcs, ycs + ycs_adj * 8, self.display))

        xcos = 505
        ycos = 162
        ycos_adj = 28
        # Content Scales
        self.scales.append(Scale(self.gameDisplay, 'ANX', profile_id, xcos, ycos, self.display))
        self.scales.append(Scale(self.gameDisplay, 'FRS', profile_id, xcos, ycos + ycos_adj, self.display))
        self.scales.append(Scale(self.gameDisplay, 'OBS', profile_id, xcos, ycos + ycos_adj * 2, self.display))
        self.scales.append(Scale(self.gameDisplay, 'DEP', profile_id, xcos, ycos + ycos_adj * 3, self.display))
        self.scales.append(Scale(self.gameDisplay, 'HEA', profile_id, xcos, ycos + ycos_adj * 4, self.display))
        self.scales.append(Scale(self.gameDisplay, 'BIZ', profile_id, xcos, ycos + ycos_adj * 5, self.display))
        self.scales.append(Scale(self.gameDisplay, 'ANG', profile_id, xcos, ycos + ycos_adj * 6, self.display))
        self.scales.append(Scale(self.gameDisplay, 'CYN', profile_id, xcos, ycos + ycos_adj * 7, self.display))
        self.scales.append(Scale(self.gameDisplay, 'ASP', profile_id, xcos, ycos + ycos_adj * 8 + 3, self.display))
        self.scales.append(Scale(self.gameDisplay, 'TPA', profile_id, xcos, ycos + ycos_adj * 9 + 3, self.display))
        self.scales.append(Scale(self.gameDisplay, 'LSE', profile_id, xcos, ycos + ycos_adj * 10 + 3, self.display))
        self.scales.append(Scale(self.gameDisplay, 'SOD', profile_id, xcos, ycos + ycos_adj * 11 + 3, self.display))
        self.scales.append(Scale(self.gameDisplay, 'FAM', profile_id, xcos, ycos + ycos_adj * 12 + 3, self.display))
        self.scales.append(Scale(self.gameDisplay, 'WRK', profile_id, xcos, ycos + ycos_adj * 13 + 3, self.display))
        self.scales.append(Scale(self.gameDisplay, 'NT', profile_id, xcos, ycos + ycos_adj * 14 + 3, self.display))

        xsup = 835
        ysup = 162
        ysup_adj = 28
        # Supplementary Scales
        self.scales.append(Scale(self.gameDisplay, 'anxiety', profile_id, xsup, ysup, self.display))
        self.scales.append(Scale(self.gameDisplay, 'macr', profile_id, xsup, ysup + ysup_adj, self.display))
        self.scales.append(Scale(self.gameDisplay, 'aas', profile_id, xsup, ysup + ysup_adj * 2, self.display))
        self.scales.append(Scale(self.gameDisplay, 'aps', profile_id, xsup, ysup + ysup_adj * 3, self.display))
        self.scales.append(Scale(self.gameDisplay, 'aggr', profile_id, xsup, ysup + ysup_adj * 4, self.display))

        xil = xsup
        yil = 360
        yil_adj = 28
        # Item Lists
        self.scales.append(Scale(self.gameDisplay, 'ci', profile_id, xil, yil, self.display))
        self.scales.append(Scale(self.gameDisplay, 'rig', profile_id, xil, yil + yil_adj, self.display))

        xdec = 435
        ydec = 700
        ydec_adj = 26
        self.decisions.append(Decision("A", "Pass", xdec, ydec, bright_green, self.gameDisplay, self.take_decision))
        self.decisions.append(
            Decision("D", "Substance Use", xdec, ydec + ydec_adj, bright_yellow, self.gameDisplay, self.take_decision))
        self.decisions.append(
            Decision("E", "Aggression", xdec, ydec + ydec_adj * 2, bright_yellow, self.gameDisplay, self.take_decision))
        self.decisions.append(
            Decision("F", "Rigidity", xdec, ydec + ydec_adj * 3, bright_yellow, self.gameDisplay, self.take_decision))
        self.decisions.append(
            Decision("G", "Cynicism", xdec, ydec + ydec_adj * 4, bright_yellow, self.gameDisplay, self.take_decision))
        self.decisions.append(
            Decision("H", "Anxiety", xdec, ydec + ydec_adj * 5, bright_yellow, self.gameDisplay, self.take_decision))
        self.decisions.append(
            Decision("C", "Fail", xdec, ydec + ydec_adj * 6, bright_red, self.gameDisplay, self.take_decision))

        self.order.append(profile_id)

    def display(self):
        profile = True
        while profile:
            clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = True

            self.gameDisplay.fill(white)
            self.gameDisplay.blit(self.baseImg, (25, 25))

            ## Validity Scale Buttons
            for scale in self.scales:
                scale.displayScaleButton(clicked)

            # Decision buttons
            for decision in self.decisions:
                decision.displayDecisionButton(clicked)

            font = pygame.font.SysFont(None, 25)
            text = font.render("Complete: " + str(self.order) + "/14", True, black)
            self.gameDisplay.blit(text, (1680 / 2, 5))

            pygame.display.update()
            clock.tick(15)

    def take_decision(self, decision):
        self.decision = decision
        self.decision_action()


class Experiment:
    def __init__(self, gameDisplay, exit_action):
        self.exit_action = exit_action
        self.profiles = []
        self.times_from_start = []
        self.start_time = 0
        self.current_profile = 0

        for i in range(1, 15):
            self.profiles.append(Profile(i, gameDisplay, self.next_profile))

    def profile_order(self):
        return self.profiles

    def resetAndDisplay(self):

        random.shuffle(self.profiles)
        for i in range(0, len(self.profiles)):
            self.profiles[i].order = i + 1
        self.current_profile = 0
        self.start_time = time.time()
        del self.times_from_start[:]
        ###
        self.times_from_start = [0] * 14
        self.profile_order = []
        self.profiles[0].display()

    def next_profile(self):
        self.times_from_start[self.current_profile] = time.time() - self.start_time
        self.current_profile += 1
        if self.current_profile == len(self.profiles):
            self.exit_action()
        else:
            self.profiles[self.current_profile].display()

    def list_decisions(self):
        decisions = [profile.decision for profile in self.profiles]
        return decisions

    def list_order(self):
        order = [profile.order for profile in self.profiles]
        return order

    def list_times_from_start(self):
        return self.times_from_start

    def list_times_to_decide(self):
        times_to_decide = ([self.times_from_start[0]]
                           + [self.times_from_start[i] - self.times_from_start[i - 1] for i in
                              range(1, len(self.times_from_start))])
        return times_to_decide


class Practice:
    def __init__(self, gameDisplay, exit_action):
        self.exit_action = exit_action
        self.profiles = []
        self.current_profile = 0

        for i in range(20, 21):
            self.profiles.append(Profile(i, gameDisplay, self.next_profile))

    def resetAndDisplay(self):
        random.shuffle(self.profiles)

        for i in range(0, len(self.profiles)):
            self.profiles[i].order = i + 1
        self.current_profile = 0
        self.profiles[0].display()

    def next_profile(self):
        self.current_profile += 1
        if self.current_profile == len(self.profiles):
            self.exit_action()
        else:
            self.profiles[self.current_profile].display()

