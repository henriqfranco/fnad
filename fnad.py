import pygame
import cv2
from moviepy.editor import VideoFileClip
import os
import glob
import datetime
import random

currentres = (1280,720)
currentfull = False
while True:
    print("---Five Nights At Deovas': O Dopaganger---\n")
    print(f"Resolução atual: {currentres}")
    print(f"Tela Cheia: {currentfull}")
    print("1 - Alterar Resolução")
    print("2 - Ativar/desativar tela cheia")
    print("3 - Jogar")
    #uinput = input("> ")
    uinput = "3"
    match uinput:
        case "1":
            print("Selecione resolução: ")
            print("1 - (1280, 720)")
            print("2 - (1920, 1080)")
            print("3 - (2560, 1440)")
            print("4 - Resolução customizada (Cuidado! Resoluções personalizadas podem não funcionar corretamente)")
            uinput = input("> ")
            match uinput:
                case "1":
                    currentres = (1280,720)
                case "2":
                    currentres = (1920,1080)
                case "3":
                    currentres = (2560,1440)
                case "4":
                    print("Insira a resolução personalizada (largura, altura)")
                    try:
                        uinput = tuple(map(int,(input("> ")[1:-1].split(","))))
                        currentres = uinput
                    except:
                        print("Erro ao definir resolução personalizada")
                case _:
                    print("Seleção inválida")
        case "2":
            currentfull = not currentfull
        case "3":
            break
        case _:
            print("Seleção inválida")

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
pygame.font.init()
screensize = currentres
fps = 60
if currentfull:
    screen = pygame.display.set_mode(screensize, pygame.DOUBLEBUF|pygame.FULLSCREEN) #|pygame.FULLSCREEN
else:
    screen = pygame.display.set_mode(screensize, pygame.DOUBLEBUF)
clock = pygame.time.Clock()
vhsfont = pygame.font.Font("assets/fonts/VCR_OSD_MONO_1.001.ttf", int(screensize[0]*0.031))
loading = vhsfont.render("Loading", True, (255,255,255))
screen.blit(loading, (0,0))
pygame.display.flip()
pygame.display.set_caption("Five Nights At Deovas': O Dopaganger")

class pgvideo:
    def __init__(self, file:str, loop:bool, audio:bool):
        self.file = file
        self.loop = loop
        self.audio = audio
        self.ended = False
        self.video = cv2.VideoCapture(self.file)
        self.framecount = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
        self.baseres = (self.video.get(cv2.CAP_PROP_FRAME_WIDTH),self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if self.audio:
            VideoFileClip(self.file).audio.write_audiofile(f"assets/tmp/{self.file.split('/')[-1].split('.')[0]}.mp3")

    def frame(self):
        success, img = self.video.read()
        self.currentframe = self.video.get(cv2.CAP_PROP_POS_FRAMES)
        if self.currentframe == 1.0 and self.audio:
            videoaudio = pygame.mixer.Sound(f"assets/tmp/{self.file.split('/')[-1].split('.')[0]}.mp3")
            pygame.mixer.find_channel().play(videoaudio)

        if self.currentframe == self.framecount:
            if self.loop:
                self.video = cv2.VideoCapture(self.file)
            else:
                self.ended = True
        return pygame.image.frombuffer(img.tobytes(), img.shape[1::-1], "BGR")

def deovasmovement(pos, difficulty):
    if random.randint(0,50) < difficulty:
        if pos == 0:
            newpos = 3
        elif pos == 1:
            newpos = random.choice([4,10,12])
        elif pos == 2:
            newpos = random.choice([1,3])
        elif pos == 3:
            newpos = random.choice([0,1])
        elif pos == 4:
            newpos = 1
        elif pos == 10:
            newpos = 11
        elif pos == 11:
            newpos = 20
        elif pos == 12:
            newpos = 21
    else:
        newpos = pos
    return newpos

def lurgamovement(pos, difficulty):
    if random.randint(0,50) < difficulty:
        if pos == 0:
            newpos = 1
        elif pos == 1:
            newpos = 20
    else:
        newpos = pos
    return newpos

#general assets and vars
debug = False
realframe = 1
state = "menu" # game, menu
section = "main" # menu = opening, main, settings / game = first, loading, night1, night2, night3, night4, night5
ingamevars = {"battery": 100000,
              "action": "normal",
              "cellphonenow": "",
              "audiosleft": 3,
              "backdoor": False,
              "fan": False,
              "heat": 0,
              "time": 0,
              "cam": 0,
              "deovaspos": 2,
              "lurgapos":0,
              "difficulty": [0,0]}

#menu assets and vars        
menuvideo = pgvideo("assets/videos/menu.mp4",loop=True,audio=False)
testvideo = pgvideo("assets/videos/test.mp4",loop=True,audio=True)
vhsfont = pygame.font.Font("assets/fonts/VCR_OSD_MONO_1.001.ttf", int(screensize[0]*0.031))
vhsfontbig = pygame.font.Font("assets/fonts/VCR_OSD_MONO_1.001.ttf", int(screensize[0]*0.039))
dtime = vhsfont.render(f"{datetime.datetime.now().strftime('%H:%M')}", True, (255,255,255))
ddate = vhsfont.render(f"{datetime.datetime.now().strftime('%b.%d %Y')}", True, (255,255,255))
title = vhsfontbig.render(f"FIVE NIGHTS AT DEOVAS'", True, (255,255,255))
play = vhsfont.render(f"JOGAR", True, (255,255,255))
exit = vhsfont.render(f"SAIR", True, (255,255,255))

#game assets and vars
grabcell = pygame.image.load("assets/sprites/switch/grabcell.png").convert_alpha()
grabcell = pygame.transform.scale(grabcell, (screensize[0]*0.5,screensize[1]*0.08))
grabcell.set_alpha(80)

heat = vhsfont.render(f"Calor", True, (100,10,10))
heatturn = 0
heatcolor = (120,10,10)

phonefont = pygame.font.Font(None, int(screensize[0]*0.02))
time = phonefont.render(f"H: 0{int(ingamevars['time']*0.00024)}", True, (255,255,255))
battery = phonefont.render(f"B: {int(ingamevars['battery'])}%", True, (255,255,255))
cellphonespeed = 0
cellphoneY = 1.05

cellphoneflash = pygame.image.load("assets/sprites/cellphone/cellphone-flash.png").convert_alpha()
cellphoneflash = pygame.transform.scale(cellphoneflash, (screensize[0]*0.5,screensize[1]*0.9))
cellphoneaudio = pygame.image.load("assets/sprites/cellphone/cellphone-audio.png").convert_alpha()
cellphoneaudio = pygame.transform.scale(cellphoneaudio, (screensize[0]*0.5,screensize[1]*0.9))
lock = pygame.image.load("assets/sprites/cellphone/lock2.png").convert_alpha()
lock = pygame.transform.scale(lock, (screensize[0]*0.025,screensize[1]*0.05))
cellphonecams = pygame.image.load("assets/sprites/cellphone/cellphone-cams.png").convert_alpha()
cellphonecams = pygame.transform.scale(cellphonecams, (screensize[0]*0.66,screensize[1]*1.15))
cellphonebattery = pygame.image.load("assets/sprites/cellphone/cellphone-battery.png").convert_alpha()
cellphonebattery = pygame.transform.scale(cellphonebattery, (screensize[0]*0.5,screensize[1]*0.9))
cellphonehome = pygame.image.load("assets/sprites/cellphone/cellphone-home.png").convert_alpha()
cellphonehome = pygame.transform.scale(cellphonehome, (screensize[0]*0.5,screensize[1]*0.9))
ingamevars["cellphonenow"] = cellphonehome
audiodelay = 1

fan = pygame.image.load("assets/sprites/fan/fan.png").convert_alpha()
fan = pygame.transform.scale(fan,(screensize[0]*0.176,screensize[1]*0.43))
fan.set_alpha(0)

fanblades = pygame.image.load("assets/sprites/fan/fanblades.png").convert_alpha()
fanblades = pygame.transform.scale(fanblades,(screensize[0]*0.107,screensize[0]*0.107))
fanblades_ = fanblades
fanbladesrotation = 0
fanbladesoff = 100

frontimage1deovas = pygame.image.load("assets/images/frontimage1-deovas.png").convert_alpha()
frontimage1deovas = pygame.transform.scale(frontimage1deovas, (screensize[0]*1.5,screensize[1]))
frontimage1 = pygame.image.load("assets/images/frontimage1.png").convert_alpha()
frontimage1 = pygame.transform.scale(frontimage1, (screensize[0]*1.5,screensize[1]))
frontimage1.set_alpha(0)
scenariospeed = 0
scenarioX = 0

godumpingroom = pygame.image.load("assets/sprites/switch/godumpingroom.png").convert_alpha()
godumpingroom = pygame.transform.scale(godumpingroom, (screensize[0]*0.065,screensize[1]*0.7))
godumpingroom.set_alpha(80)

backimage1open = pygame.image.load("assets/images/backimage1-open.png").convert_alpha()
backimage1open = pygame.transform.scale(backimage1open, screensize)
backimage1open.set_alpha(0)

backimage1closed = pygame.image.load("assets/images/backimage1-closed.png").convert_alpha()
backimage1closed = pygame.transform.scale(backimage1closed, screensize)
backimage1closed.set_alpha(0)

backimage2deova = pygame.image.load("assets/images/backimage2-deova.png").convert_alpha()
backimage2deova = pygame.transform.scale(backimage2deova, (screensize[0],screensize[1]*1.5))
backimage2 = pygame.image.load("assets/images/backimage2.png").convert_alpha()
backimage2 = pygame.transform.scale(backimage2, (screensize[0],screensize[1]*1.5))
backimage2.set_alpha(0)
scenariospeed = 0
scenarioY = -0.5

faintimage = pygame.image.load("assets/images/faintimage.png").convert_alpha()
faintimage = pygame.transform.scale(faintimage, screensize)
faintimage.set_alpha(0)

computerimage = pygame.image.load("assets/images/computerimage.png").convert_alpha()
computerimage = pygame.transform.scale(computerimage,screensize)
computerimage.set_alpha(0)

chargingtimer = 900

debugfont = pygame.font.Font("assets/fonts/LUCON.TTF", int(screensize[0]*0.012))

currentcamnumber = phonefont.render(f"{ingamevars['cam']}", True, (255,255,255))
camdelay = 0
camdeovasin = []
camdeovasout = []

for cam in range(5):
    camdeovasin.append(pygame.image.load(f"assets/sprites/cellphone/cams/deovasin/cellphone-cam{cam}.png").convert_alpha())
    camdeovasin[-1] = pygame.transform.scale(camdeovasin[-1], (screensize[0]*0.66,screensize[1]*1.15))
    camdeovasout.append(pygame.image.load(f"assets/sprites/cellphone/cams/deovasout/cellphone-cam{cam}.png").convert_alpha())
    camdeovasout[-1] = pygame.transform.scale(camdeovasout[-1], (screensize[0]*0.66,screensize[1]*1.15))

moveloop = 300

#start
running = True
while running:
    realframe += 1
    #menu section
    if state == "menu":
        screen.fill((0,0,0))
        if section == "main":
            dtime = vhsfont.render(f"{datetime.datetime.now().strftime('%H:%M')}", True, (255,255,255))
            ddate = vhsfont.render(f"{datetime.datetime.now().strftime('%b.%d %Y')}", True, (255,255,255))
            title = vhsfontbig.render(f"FIVE NIGHTS AT DEOVAS'", True, (255,255,255))
            play = vhsfont.render(f"JOGAR", True, (255,255,255))
            exit = vhsfont.render(f"SAIR", True, (255,255,255))

            if pygame.mouse.get_pos()[0] > screensize[0]*0.45 and pygame.mouse.get_pos()[0] < screensize[0]*0.45+play.get_rect()[2] and \
                pygame.mouse.get_pos()[1] > screensize[1]*0.4 and pygame.mouse.get_pos()[1] < screensize[1]*0.4+play.get_rect()[3]:
                    if not pygame.mouse.get_pressed()[0]:
                        play = vhsfont.render(f"JOGAR", True, (0,0,255))
                    else:
                        state = "game"
                        section = "night5"
                        init = False
            if pygame.mouse.get_pos()[0] > screensize[0]*0.46 and pygame.mouse.get_pos()[0] < screensize[0]*0.46+exit.get_rect()[2] and \
                pygame.mouse.get_pos()[1] > screensize[1]*0.6 and pygame.mouse.get_pos()[1] < screensize[1]*0.6+exit.get_rect()[3]:
                    if not pygame.mouse.get_pressed()[0]:
                        exit = vhsfont.render(f"SAIR", True, (255,0,0))
                    else:
                        pygame.quit()


            screen.blit(dtime, (screensize[0]*0.1,screensize[1]*0.766))
            screen.blit(ddate, (screensize[0]*0.1,screensize[1]*0.833))
            screen.blit(title, (screensize[0]*0.248,screensize[1]*0.1))
            screen.blit(play, (screensize[0]*0.45,screensize[1]*0.4))
            screen.blit(exit, (screensize[0]*0.46,screensize[1]*0.6))
            if realframe == 2: # game/video fps difference fix
                oldframe = pygame.transform.scale(menuvideo.frame(), screensize)
                oldframe.set_alpha(120)
            screen.blit(oldframe, (0, 0))

        if section == "test":
            if realframe == 2: # game/video fps difference fix
                oldframe = pygame.transform.scale(testvideo.frame(), screensize)
            screen.blit(oldframe, (0, 0))

    #game section
    if state == "game":
        screen.fill((0,0,0))
        if section not in ["first", "loading"]:
            #game globals
            #time
            ingamevars["time"]+=1
            #battery
            if ingamevars["cellphonenow"] in [cellphonehome,cellphoneaudio]:
                ingamevars['battery']-=11
            elif ingamevars["cellphonenow"] == cellphoneflash:
                ingamevars['battery']-=17
            elif ingamevars["cellphonenow"] == cellphonecams:
                ingamevars['battery']-=18
            #heat
            heatturn += 1
            if heatturn == 10:
                if ingamevars["heat"] > 600:
                    if heatcolor == (120,10,10):
                        heatcolor = (200,200,200)
                    else:
                        heatcolor = (120,10,10)
                else:
                    heatcolor = (120,10,10)
                heatturn = 0

            if ingamevars["backdoor"]:
                if not ingamevars["fan"] and ingamevars["heat"] < 1200:
                    ingamevars["heat"] += 2
            elif ingamevars["heat"] > 0:
                ingamevars["heat"] -=1

            #faint
            if ingamevars["time"] % 2 == 0:
                if ingamevars["heat"] >= 1200:
                    faintimage.set_alpha(faintimage.get_alpha()+1)
                else:
                    faintimage.set_alpha(faintimage.get_alpha()-1)
            if faintimage.get_alpha() == 255:
                #jumpscare
                print("dead")

            #fan
            if ingamevars["fan"]:
                fanbladesrotation += 100
                if fanbladesoff == 100:
                    fansoundo = pygame.mixer.Sound(f"assets/audios/fanon.mp3")
                    pygame.mixer.find_channel().play(fansoundo,-1)
                fanbladesoff -= 2
            else:
                if fanbladesoff < 0:
                    fanbladesoff = 0
                    fansoundo.stop()
                    fansoundse = pygame.mixer.Sound(f"assets/audios/fanend.mp3")
                    pygame.mixer.find_channel().play(fansoundse)
                if fanbladesoff < 100:
                    fanbladesoff += 2
                fanbladesrotation += 100-fanbladesoff
            
            if ingamevars["action"] in ["normal","cellphone"]:
                if ingamevars["deovaspos"] != 12 or ingamevars["cellphonenow"] != cellphoneflash:
                    screen.blit(frontimage1,(screensize[0]*scenarioX,0))
                else:
                    screen.blit(frontimage1deovas,(screensize[0]*scenarioX,0))
                screen.blit(fan,(screensize[0]*scenarioX+(screensize[0]*0.8),screensize[1]*0.2))
                screen.blit(fanblades_,(screensize[0]*scenarioX+(screensize[0]*0.888)-int(fanblades_.get_width()/2),screensize[1]*0.34-int(fanblades_.get_height()/2)))
                if cellphoneY < 1.05:
                    screen.blit(ingamevars["cellphonenow"],(screensize[0]*0.25,screensize[1]*cellphoneY))
                    if ingamevars["cellphonenow"] == cellphonecams:
                        if ingamevars["deovaspos"] == ingamevars["cam"]:
                            screen.blit(camdeovasin[ingamevars["cam"]],(screensize[0]*0.25,screensize[1]*cellphoneY))
                        else:
                            screen.blit(camdeovasout[ingamevars["cam"]],(screensize[0]*0.25,screensize[1]*cellphoneY))
            if ingamevars["action"] == "computer":
                screen.blit(computerimage,(0,0))

            if ingamevars["action"] == "outdumpingroom":
                if not ingamevars["backdoor"]:
                    screen.blit(backimage1open,(0,0))
                else:
                    screen.blit(backimage1closed,(0,0))
            if ingamevars["action"] == "indumpingroom":
                if ingamevars["deovaspos"] != 11:
                    screen.blit(backimage2,(0,screensize[1]*scenarioY))
                else:
                    screen.blit(backimage2deova,(0,screensize[1]*scenarioY))
            if ingamevars["action"] == "cellphone" and ingamevars["battery"] > 0:
                if ingamevars["cellphonenow"] != cellphonecams:
                    screen.blit(battery, (screensize[0]*0.558,screensize[1]*cellphoneY*3.1))
                    screen.blit(time, (screensize[0]*0.517,screensize[1]*cellphoneY*3.1))
                    screen.blit(nightdisplay, (screensize[0]*0.4,screensize[1]*cellphoneY*3.1))
                else:
                    screen.blit(battery, (screensize[0]*0.62,screensize[1]*cellphoneY*-0.3))
                    screen.blit(time, (screensize[0]*0.569,screensize[1]*cellphoneY*-0.3))
                    screen.blit(nightdisplay, (screensize[0]*0.34,screensize[1]*cellphoneY*-0.3))
                    screen.blit(currentcamnumber, (screensize[0]*0.64,screensize[1]*0.685))
                if ingamevars["cellphonenow"] == cellphoneaudio:
                    for lockaudio in range(3-ingamevars["audiosleft"]):
                        screen.blit(lock,(screensize[0]*0.394,screensize[1]*cellphoneY*5.8+(1.3*lockaudio*lock.get_height())))
                # if ingamevars["cellphonenow"] == cellphoneflash:
                #     pass

            if faintimage.get_alpha() > 0:
                screen.blit(faintimage,(0,0))
            if godumpingroom.get_alpha() != 0:   
                screen.blit(godumpingroom, (screensize[0]*scenarioX+(screensize[0]*0.01),screensize[1]*0.1))
            if grabcell.get_alpha() != 0:
                screen.blit(grabcell, (screensize[0]*0.25,screensize[1]*0.9))
            screen.blit(heat,(screensize[0]*0.02,screensize[1]*0.02))
            screen.fill((0,0,0),(screensize[0]*0.021,screensize[1]*0.071,heat.get_width()*1,int(screensize[0]*0.015)))
            screen.fill(heatcolor,(screensize[0]*0.02,screensize[1]*0.07,ingamevars["heat"]*heat.get_width()*0.00082,int(screensize[0]*0.014)))
            if debug:
                info = debugfont.render(f"fps: {round(clock.get_fps(),1)} frametime(raw):{clock.get_time()}({clock.get_rawtime()}) time: {ingamevars['time']}/29635 battery:{ingamevars['battery']} heat:{ingamevars['heat']} deovaspos: {ingamevars['deovaspos']} lurgapos: {ingamevars['lurgapos']}", False, (126,126,126))
                screen.blit(info, (0,0))
            if ingamevars["action"] in ["normal", "cellphone"]:
                if frontimage1.get_alpha() != 255:
                    fanblades_ = pygame.transform.rotate(fanblades,fanbladesrotation).convert_alpha()
                    fan.set_alpha(fan.get_alpha()+10)
                    fanblades_.set_alpha(fan.get_alpha())
                    frontimage1.set_alpha(frontimage1.get_alpha()+10)
                    backimage1open.set_alpha(backimage1open.get_alpha()-10)
                    backimage1closed.set_alpha(backimage1closed.get_alpha()-10)
                    backimage2.set_alpha(backimage2.get_alpha()-10)
                    computerimage.set_alpha(computerimage.get_alpha()-10)
                    grabcell.set_alpha(80)
                    if ingamevars["fan"]:
                        fansoundo.set_volume(1)
                else:
                    fanblades_ = pygame.transform.rotate(fanblades,fanbladesrotation).convert_alpha()

                    #scenario move
                    if scenarioX == -0.5 and scenariospeed == -0.01:
                        scenariospeed = 0
                    if scenarioX == 0 and scenariospeed == 0.01:
                        scenariospeed = 0
                    scenarioX += scenariospeed
                    scenarioX = round(scenarioX,2)
                    if ingamevars["action"] == "normal" and pygame.mouse.get_pos()[0] < screensize[0]*0.1:
                        scenariospeed = 0.01
                    elif scenariospeed == 0.01:
                        scenariospeed = 0
                    if ingamevars["action"] == "normal" and pygame.mouse.get_pos()[0] > screensize[0]*0.9:
                        scenariospeed = -0.01
                    elif scenariospeed == -0.01:
                        scenariospeed = 0

                    # cellphone grab and store
                    if ingamevars["cellphonenow"] != cellphonecams and (cellphoneY == 0.05 and (cellphonespeed in [0.01,-0.1])):
                        cellphonespeed = 0
                    if cellphoneY >= 1.05 and (cellphonespeed in [0.01,0.1]):
                        cellphonespeed = 0
                        cellphoneY = 1.05
                    cellphoneY += cellphonespeed
                    cellphoneY = round(cellphoneY,2)
                    if pygame.mouse.get_pos()[1] > screensize[1]*0.94 and\
                        pygame.mouse.get_pos()[0] > screensize[0]*0.25 and pygame.mouse.get_pos()[0] < screensize[0]*0.75 and\
                        ingamevars["action"] == "normal" and grabcell.get_alpha() != 0:
                            ingamevars["action"] = "cellphone"
                            grabcell.set_alpha(0)
                            godumpingroom.set_alpha(0)
                            cellphonespeed = -0.1
                    if pygame.mouse.get_pos()[1] > screensize[1]*0.94 and\
                        pygame.mouse.get_pos()[0] > screensize[0]*0.25 and pygame.mouse.get_pos()[0] < screensize[0]*0.75 and\
                        ingamevars["action"] == "cellphone" and grabcell.get_alpha() != 0:
                            ingamevars["action"] = "normal"
                            grabcell.set_alpha(0)
                            godumpingroom.set_alpha(80)
                            cellphonespeed = 0.1
                    if pygame.mouse.get_pos()[1] < screensize[1]*0.9 and grabcell.get_alpha() == 0:
                        grabcell.set_alpha(80)

                    # cellphone battery
                    if ingamevars["battery"] < 0 and ingamevars["action"] == "cellphone" and cellphoneY <= 0.05:
                        ingamevars["cellphonenow"] = cellphonebattery
                        cellnobattery = pygame.mixer.Sound(f"assets/audios/nobattery.mp3")
                        pygame.mixer.find_channel().play(cellnobattery)
                        ingamevars["action"] = "normal"
                        cellphonespeed = 0.1

                    if ingamevars["battery"] < 33333:
                        battery = phonefont.render(f"B: {int(ingamevars['battery']*0.001)}%", True, (155,0,0))
                    elif ingamevars["battery"] < 66666:
                        battery = phonefont.render(f"B: {int(ingamevars['battery']*0.001)}%", True, (155,155,0))
                    else:
                        battery = phonefont.render(f"B: {int(ingamevars['battery']*0.001)}%", True, (0,155,0))
                    if ingamevars["cellphonenow"] == cellphonecams:
                        battery = pygame.transform.scale_by(battery,1.277)

                    #cellphone time
                    time = phonefont.render(f"H: 0{int(ingamevars['time']*0.00024)}", True, (0,0,0))
                    if ingamevars["cellphonenow"] == cellphonecams:
                        time = pygame.transform.scale_by(time,1.277)

                    #cellphone audio
                    if ingamevars["action"] == "cellphone" and ingamevars["cellphonenow"] == cellphoneaudio and \
                        pygame.mouse.get_pos()[0] > screensize[0]*0.39 and pygame.mouse.get_pos()[0] < screensize[0]*0.61 and\
                        pygame.mouse.get_pos()[1] > screensize[1]*0.28 and pygame.mouse.get_pos()[1] < screensize[1]*0.48 and\
                        pygame.mouse.get_pressed()[0] and audiodelay <= 0:
                        if ingamevars["audiosleft"] > 0:
                            audioapp = pygame.mixer.Sound(f"assets/audios/deovaudio{ingamevars['audiosleft']}.mp3")
                            pygame.mixer.find_channel().play(audioapp)
                            ingamevars["audiosleft"] -= 1
                            audiodelay = 300
                        else:
                            audioapp = pygame.mixer.Sound(f"assets/audios/audioerror.mp3")
                            pygame.mixer.find_channel().play(audioapp)
                            audiodelay = 80
                    audiodelay -=1
                    if audiodelay == 81 and ingamevars["lurgapos"] == 1:
                        ingamevars["lurgapos"] = 0
                        lurgaudio = pygame.mixer.Sound(f"assets/audios/lurgscared{random.randint(0,5)}.mp3")
                        pygame.mixer.find_channel().play(lurgaudio)

                    #cellphone cams
                    if cellphoneY <= -0.10 and (cellphonespeed in [-0.01,-0.1]):
                        cellphonespeed = 0
                        cellphoneY = -0.10
                    if ingamevars["action"] == "cellphone" and ingamevars["cellphonenow"] == cellphonecams and \
                        pygame.mouse.get_pos()[0] > screensize[0]*0.43 and pygame.mouse.get_pos()[0] < screensize[0]*0.57 and\
                        pygame.mouse.get_pos()[1] > screensize[1]*0.82 and pygame.mouse.get_pos()[1] < screensize[1]*0.9 and\
                        pygame.mouse.get_pressed()[0]:
                            cellphonespeed = 0.01
                            ingamevars["cellphonenow"] = cellphonehome
                    currentcamnumber = phonefont.render(f"{ingamevars['cam']}", True, (255,255,255))
                    currentcamnumber = pygame.transform.scale_by(currentcamnumber,1.5)
                    camdelay -=1
                    if ingamevars["action"] == "cellphone" and ingamevars["cellphonenow"] == cellphonecams and \
                        pygame.mouse.get_pos()[0] > screensize[0]*0.627 and pygame.mouse.get_pos()[0] < screensize[0]*0.664 and \
                        pygame.mouse.get_pressed()[0] and\
                            camdelay <=0:
                            if pygame.mouse.get_pos()[1] > screensize[1]*0.595 and pygame.mouse.get_pos()[1] < screensize[1]*0.67 and\
                                ingamevars["cam"] < 4:
                                    ingamevars["cam"] +=1
                                    camdelay = 30
                            elif pygame.mouse.get_pos()[1] > screensize[1]*0.73 and pygame.mouse.get_pos()[1] < screensize[1]*0.805 and\
                                ingamevars["cam"] > 0:
                                    ingamevars["cam"] -=1
                                    camdelay = 30

                    #cellphone home
                    if ingamevars["action"] == "cellphone" and ingamevars["cellphonenow"] not in [cellphonehome,cellphonecams] and \
                        pygame.mouse.get_pos()[0] > screensize[0]*0.47 and pygame.mouse.get_pos()[0] < screensize[0]*0.53 and\
                        pygame.mouse.get_pos()[1] > screensize[1]*0.77 and pygame.mouse.get_pos()[1] < screensize[1]*0.833 and\
                        pygame.mouse.get_pressed()[0]:
                        ingamevars["cellphonenow"] = cellphonehome

                    if ingamevars["action"] == "cellphone" and ingamevars["cellphonenow"] == cellphonehome and \
                        pygame.mouse.get_pos()[0] > screensize[0]*0.405 and pygame.mouse.get_pos()[0] < screensize[0]*0.455 and \
                        pygame.mouse.get_pressed()[0]:
                        if pygame.mouse.get_pos()[1] > screensize[1]*0.37 and pygame.mouse.get_pos()[1] < screensize[1]*0.5:
                            ingamevars["cellphonenow"] = cellphoneflash
                        elif pygame.mouse.get_pos()[1] > screensize[1]*0.24 and pygame.mouse.get_pos()[1] < screensize[1]*0.36:
                            ingamevars["cellphonenow"] = cellphonecams
                            cellphoneY -= 0.01
                            cellphonespeed -=0.01
                    elif ingamevars["action"] == "cellphone" and ingamevars["cellphonenow"] == cellphonehome and \
                        pygame.mouse.get_pos()[0] > screensize[0]*0.477 and pygame.mouse.get_pos()[0] < screensize[0]*0.527 and \
                        pygame.mouse.get_pos()[1] > screensize[1]*0.37 and pygame.mouse.get_pos()[1] < screensize[1]*0.5 and \
                        pygame.mouse.get_pressed()[0]:
                        ingamevars["cellphonenow"] = cellphoneaudio
                        audiodelay = 80

                    #fan
                    if pygame.mouse.get_pos()[0] > screensize[0]*scenarioX+(screensize[0]*0.83) and pygame.mouse.get_pos()[0] < screensize[0]*scenarioX+(screensize[0]*0.94) and \
                        pygame.mouse.get_pos()[1] > screensize[1]*0.51 and  pygame.mouse.get_pos()[1] < screensize[1]*0.61 and \
                        pygame.mouse.get_pressed()[0]:
                            if ingamevars["fan"]:
                                if fanbladesoff < -100:
                                    ingamevars["fan"] = False
                            else:
                                if fanbladesoff == 100:
                                    ingamevars["fan"] = True

                    #computer
                    if pygame.mouse.get_pos()[0] > screensize[0]*scenarioX+(screensize[0]*0.1937) and pygame.mouse.get_pos()[0] < screensize[0]*scenarioX+(screensize[0]*0.571) and\
                        pygame.mouse.get_pos()[1] > screensize[1]*0.03 and pygame.mouse.get_pos()[1] < screensize[1]*0.406 and\
                        ingamevars["action"] == "normal" and pygame.mouse.get_pressed()[0]:
                            grabcell.set_alpha(0)
                            godumpingroom.set_alpha(0)
                            ingamevars["action"] = "computer"

                    # goto dumping room
                    if ingamevars["action"] == "normal" and \
                        scenarioX != 0 and \
                        pygame.mouse.get_pos()[0] < screensize[0]*0.04 and \
                        pygame.mouse.get_pos()[1] > screensize[1]*0.1 and pygame.mouse.get_pos()[1] < screensize[1]*0.8 and \
                        godumpingroom.get_alpha() != 0:
                        godumpingroom.set_alpha(0)

                    if ingamevars["action"] == "normal" and \
                        scenarioX == 0 and \
                        pygame.mouse.get_pos()[0] < screensize[0]*0.04 and \
                        pygame.mouse.get_pos()[1] > screensize[1]*0.1 and pygame.mouse.get_pos()[1] < screensize[1]*0.8 and \
                        godumpingroom.get_alpha() != 0:
                        ingamevars["action"] = "outdumpingroom"
                        godumpingroom.set_alpha(0)
                    if pygame.mouse.get_pos()[0] > screensize[0]*0.0742 and ingamevars["action"] == "normal" and godumpingroom.get_alpha() == 0:
                        godumpingroom.set_alpha(80)
                    
                    
            #door of dumping room
            if ingamevars["action"]  == "outdumpingroom":
                if backimage1open.get_alpha() != 255 and not ingamevars["backdoor"]:
                    fan.set_alpha(fan.get_alpha()-10)
                    fanblades_.set_alpha(fan.get_alpha())
                    frontimage1.set_alpha(frontimage1.get_alpha()-10)
                    backimage1open.set_alpha(backimage1open.get_alpha()+10)
                    grabcell.set_alpha(0)
                    if ingamevars["fan"]:
                        fansoundo.set_volume(0.6)
                elif backimage1closed.get_alpha() != 255 and ingamevars["backdoor"]:
                    fan.set_alpha(fan.get_alpha()-10)
                    fanblades_.set_alpha(fan.get_alpha())
                    frontimage1.set_alpha(frontimage1.get_alpha()-10)
                    backimage1closed.set_alpha(backimage1closed.get_alpha()+10)
                    grabcell.set_alpha(0)
                    if ingamevars["fan"]:
                        fansoundo.set_volume(0.6)
                else:
                    if pygame.mouse.get_pos()[0] < screensize[0]*0.04 and \
                        pygame.mouse.get_pos()[1] > screensize[1]*0.1 and pygame.mouse.get_pos()[1] < screensize[1]*0.8 and \
                        godumpingroom.get_alpha() != 0:
                        ingamevars["action"] = "normal"
                        godumpingroom.set_alpha(0)
                    if pygame.mouse.get_pos()[0] > screensize[0]*0.0742 and godumpingroom.get_alpha() == 0:
                        godumpingroom.set_alpha(80)
                    if pygame.mouse.get_pos()[0] > screensize[0]*0.7 and pygame.mouse.get_pressed()[0]:
                        if not ingamevars["backdoor"]:
                            ingamevars["backdoor"] = True
                            backimage1open.set_alpha(0)
                        else:
                            ingamevars["backdoor"] = False
                            backimage1open.set_alpha(0)
                            backimage1closed.set_alpha(0)
                    if not ingamevars["backdoor"] and\
                        pygame.mouse.get_pos()[0] < screensize[0]*0.7 and pygame.mouse.get_pos()[0] > screensize[0]*0.2 and\
                        pygame.mouse.get_pressed()[0]:
                        ingamevars["action"] = "indumpingroom"
                        scenarioY = -0.5

            #in dumping room
            if ingamevars["action"]  == "indumpingroom":
                if backimage2.get_alpha() != 255:
                    scenariospeed = 0
                    backimage2.set_alpha(backimage2.get_alpha()+10)
                    backimage1open.set_alpha(backimage1open.get_alpha()-10)
                    backimage1closed.set_alpha(backimage1closed.get_alpha()-10)
                else:
                    if scenarioY == -0.5 and scenariospeed == -0.01:
                        scenariospeed = 0
                    if scenarioY == 0 and scenariospeed == 0.01:
                        scenariospeed = 0
                    scenarioY += scenariospeed
                    scenarioY = round(scenarioY,2)
                    if ingamevars["action"] == "indumpingroom" and pygame.mouse.get_pos()[1] < screensize[1]*0.07:
                        scenariospeed = 0.01
                    elif scenariospeed == 0.01:
                        scenariospeed = 0
                    if ingamevars["action"] == "indumpingroom" and pygame.mouse.get_pos()[1] > screensize[1]*0.93:
                        scenariospeed = -0.01
                    elif scenariospeed == -0.01:
                        scenariospeed = 0
                    if pygame.mouse.get_pos()[0] < screensize[0]*0.04 and \
                        pygame.mouse.get_pos()[1] > screensize[1]*0.1 and pygame.mouse.get_pos()[1] < screensize[1]*0.8 and \
                        godumpingroom.get_alpha() != 0 and chargingtimer == 900:
                        ingamevars["action"] = "normal"
                        godumpingroom.set_alpha(0)
                    if pygame.mouse.get_pos()[0] > screensize[0]*0.4 and pygame.mouse.get_pos()[0] < screensize[0]*0.49 and \
                        pygame.mouse.get_pos()[1] > screensize[1]*scenarioY+(screensize[0]*0.76) and pygame.mouse.get_pos()[1] < screensize[1]*scenarioY+(screensize[0]*0.81) and \
                        pygame.mouse.get_pressed()[0] and chargingtimer == 900:
                            chargingtimer = 1
                            godumpingroom.set_alpha(0)
                            ingamevars["battery"] = 109901
                            ingamevars["cellphonenow"] = cellphonehome
                    if chargingtimer > 0 and chargingtimer != 900:
                        chargingtimer+= 1
                        screen.fill((0,0,200),(screensize[0]*0.01,screensize[1]-screensize[1]*0.03,chargingtimer*(screensize[0]*0.00109),screensize[1]*0.02))
                    else:
                        godumpingroom.set_alpha(80)

            if ingamevars["action"] == "computer":
                if computerimage.get_alpha() != 255:
                    computerimage.set_alpha(computerimage.get_alpha()+10)
                    frontimage1.set_alpha(frontimage1.get_alpha()-10)
                else:
                    if pygame.mouse.get_pos()[0] > screensize[0]*0.880 and pygame.mouse.get_pos()[0] < screensize[0]*0.908 and\
                        pygame.mouse.get_pos()[1] > screensize[1]*0.115 and pygame.mouse.get_pos()[1] < screensize[1]*0.189 and\
                        pygame.mouse.get_pressed()[0]:
                            ingamevars["action"] = "normal"

            #lurga ai
            if fanbladesoff < -100 and abs(fanbladesoff) % 2400 == 0:
                oldlurgapos = ingamevars["lurgapos"]
                ingamevars["lurgapos"] = lurgamovement(ingamevars["lurgapos"], ingamevars["difficulty"][1])
                if ingamevars["lurgapos"] == 20:
                    #jumpscare
                    print("dead")
                elif ingamevars["lurgapos"] == 1 and oldlurgapos != ingamevars["lurgapos"]:
                    lurgaudio = pygame.mixer.Sound(f"assets/audios/lurganear.mp3")
                    pygame.mixer.find_channel().play(lurgaudio)
            
            #deovas ai
            moveloop -= 1
            if moveloop <= 0:
                ingamevars["deovaspos"] = deovasmovement(ingamevars["deovaspos"],ingamevars["difficulty"][0])
                if ingamevars["deovaspos"] == 20:
                    if not ingamevars["backdoor"]:
                        #jumpscare
                        print("dead")
                    else:
                        ingamevars["deovaspos"] = random.choice([2,11])

                if ingamevars["deovaspos"] == 21:
                    if ingamevars["cellphonenow"] != cellphoneflash:
                        #jumpscare
                        print("dead")
                    else:
                        ingamevars["deovaspos"] = random.choice([2,12])
                moveloop = 300

            if section == "night5":
                if not init:
                    ingamevars["difficulty"] = [25,28]
                    init = True
                else:
                    nightdisplay = phonefont.render("Sexta-Feira", True, (0,0,0))
                    if ingamevars["cellphonenow"] == cellphonecams:
                        nightdisplay = pygame.transform.scale_by(nightdisplay,1.277)
                    
                        
    if realframe == 2:
        realframe = 0
    pygame.display.flip()
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                if not debug:
                    debug = True
                else:
                    debug = False
        if event.type == pygame.QUIT:
            for file in glob.glob('assets/tmp/*'):
                os.remove(file)
            running = False