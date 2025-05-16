import pygame
import cv2
from moviepy.editor import VideoFileClip
import os
import glob
import datetime
import random
import string
import json
import os
import pygame_textinput
import time

currentres = (1280,720)
currentfull = False
while True:
    time.sleep(0.1)
    os.system("cls")
    print("---Five Nights At Deovas': O Dopaganger---\n")
    print(f"Resolução atual: {currentres}")
    print(f"Tela Cheia: {currentfull}")
    print("1 - Alterar Resolução")
    print("2 - Ativar/desativar tela cheia")
    print("3 - Jogar")
    uinput = input("> ")
    match uinput:
        case "1":
            print("\nSelecione resolução: ")
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

if glob.glob("saves/save.json"):
    with open("saves/save.json","r") as savefile:
        save = json.load(savefile)
else:
    with open("saves/save.json","w"):
        pass
    save = {"currentnight": 1,
            "gameseed": random.randint(99999,999999)}

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
        self.currentframe = False
        self.video.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'X264'))
        self.framecount = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
        self.baseres = (self.video.get(cv2.CAP_PROP_FRAME_WIDTH),self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if self.audio and not glob.glob(f"tmp.{self.file.split('/')[-1].split('.')[0]}.mp3"):
            VideoFileClip(self.file).audio.write_audiofile(f"tmp.{self.file.split('/')[-1].split('.')[0]}.mp3")
    def frame(self):
        success, img = self.video.read()
        self.currentframe = self.video.get(cv2.CAP_PROP_POS_FRAMES)
        if self.currentframe == 1.0 and self.audio:
            videoaudio = pygame.mixer.Sound(f"tmp.{self.file.split('/')[-1].split('.')[0]}.mp3")
            pygame.mixer.find_channel().play(videoaudio)

        if self.currentframe == self.framecount:
            if self.loop:
                self.video = cv2.VideoCapture(self.file)
            else:
                self.ended = True
        return pygame.image.frombuffer(img.tobytes(), img.shape[1::-1], "BGR")
    def randomizeframe(self):
        self.video.set(cv2.CAP_PROP_POS_FRAMES, random.randint(1, int(self.framecount) - 1))

def deovasmovement(pos, difficulty):
    global cantcam
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
        cantcam = random.randint(30,60)
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
def resetigv(cellphone):
    global ingamevars
    ingamevars = {"battery": 100000,
                "action": "normal",
                "cellphonenow": cellphone,
                "audiosleft": 3,
                "backdoor": False,
                "fan": False,
                "heat": 0,
                "time": 0,
                "cam": 2,
                "deovaspos": 2,
                "lurgapos":0,
                "difficulty": [0,0],
                "computerstage": 0,
                "computerdone": False}
resetigv("")
#menu assets and vars        
menuvideo = pgvideo("assets/videos/menu.mp4",loop=True,audio=False)
deovavideo = pgvideo("assets/videos/deovamenu.mp4",loop=True,audio=False)
testvideo = pgvideo("assets/videos/test.mp4",loop=True,audio=True)
vhsfont = pygame.font.Font("assets/fonts/VCR_OSD_MONO_1.001.ttf", int(screensize[0]*0.031))
vhsfontbig = pygame.font.Font("assets/fonts/VCR_OSD_MONO_1.001.ttf", int(screensize[0]*0.039))
dtime = vhsfont.render(f"{datetime.datetime.now().strftime('%H:%M')}", True, (255,255,255))
ddate = vhsfont.render(f"{datetime.datetime.now().strftime('%b.%d %Y')}", True, (255,255,255))
title = vhsfontbig.render(f"FIVE NIGHTS AT DEOVAS'", True, (255,255,255))
play = vhsfont.render(f"JOGAR", True, (255,255,255))
currentnight = vhsfont.render(f"Segunda-Feira", True, (110,110,110))
exit = vhsfont.render(f"SAIR", True, (255,255,255))

#game assets and vars
grabcell = pygame.image.load("assets/sprites/switch/grabcell.png").convert_alpha()
grabcell = pygame.transform.scale(grabcell, (screensize[0]*0.5,screensize[1]*0.08))
grabcell.set_alpha(80)

heat = vhsfont.render(f"Calor", True, (100,10,10))
heatturn = 0
heatcolor = (120,10,10)

phonefont = pygame.font.Font(None, int(screensize[0]*0.02))
gametime = phonefont.render(f"H: 0{int(ingamevars['time']*0.0002362)}", True, (255,255,255))
battery = phonefont.render(f"B: {int(ingamevars['battery'])}%", True, (255,255,255))
nightdisplay = phonefont.render("Segunda-Feira", True, (0,0,0))
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
audiodelay = 1

fan = pygame.image.load("assets/sprites/fan/fan.png").convert_alpha()
fan = pygame.transform.scale(fan,(screensize[0]*0.176,screensize[1]*0.43))
fan.set_alpha(0)

fanblades = pygame.image.load("assets/sprites/fan/fanblades.png").convert_alpha()
fanblades = pygame.transform.scale(fanblades,(screensize[0]*0.107,screensize[0]*0.107))
fanblades_ = fanblades
fanbladesrotation = 0
fanbladesoff = 100
fanontimer = 0

frontimage1deovas = pygame.image.load("assets/images/frontimage/frontimage1-deovas.png").convert_alpha()
frontimage1deovas = pygame.transform.scale(frontimage1deovas, (screensize[0]*1.5,screensize[1]))
frontimage1 = pygame.image.load("assets/images/frontimage/frontimage1.png").convert_alpha()
frontimage1 = pygame.transform.scale(frontimage1, (screensize[0]*1.5,screensize[1]))
frontimage1.set_alpha(0)
scenariospeed = 0
scenarioX = 0
deovasdiscovered = False
seedeovas = pygame.mixer.Sound("assets/audios/seedeovas/seedeovas.mp3")

godumpingroom = pygame.image.load("assets/sprites/switch/godumpingroom.png").convert_alpha()
godumpingroom = pygame.transform.scale(godumpingroom, (screensize[0]*0.065,screensize[1]*0.7))
godumpingroom.set_alpha(80)
stepsound = pygame.mixer.Sound("assets/audios/inoutdumping/step.mp3")
dooropen = pygame.mixer.Sound("assets/audios/inoutdumping/dooropen.mp3")
doorclose = pygame.mixer.Sound("assets/audios/inoutdumping/doorclose.mp3")

backimage1open = pygame.image.load("assets/images/backimage/backimage1-open.png").convert_alpha()
backimage1open = pygame.transform.scale(backimage1open, screensize)
backimage1open.set_alpha(0)

backimage1closed = pygame.image.load("assets/images/backimage/backimage1-closed.png").convert_alpha()
backimage1closed = pygame.transform.scale(backimage1closed, screensize)
backimage1closed.set_alpha(0)

backimage2deova = pygame.image.load("assets/images/backimage/backimage2-deova.png").convert_alpha()
backimage2deova = pygame.transform.scale(backimage2deova, (screensize[0],screensize[1]*1.5))
backimage2 = pygame.image.load("assets/images/backimage/backimage2.png").convert_alpha()
backimage2 = pygame.transform.scale(backimage2, (screensize[0],screensize[1]*1.5))
backimage2.set_alpha(0)
scenariospeed = 0
scenarioY = -0.5

faintimage = pygame.image.load("assets/images/faintimage.png").convert_alpha()
faintimage = pygame.transform.scale(faintimage, screensize)
faintimage.set_alpha(0)
faintkill = 0

computerimage = pygame.image.load("assets/images/computer/computerimage.png").convert_alpha()
computerimage = pygame.transform.scale(computerimage,screensize)
computerimage.set_alpha(0)
computerimagebrowser = []

for computerimagei in range(1,6):
    computerimagebrowser.append(pygame.image.load(f"assets/images/computer/computerimagebrowser{computerimagei}.png").convert_alpha())
    computerimagebrowser[-1] = pygame.transform.scale(computerimagebrowser[-1],screensize)
computerfont = pygame.font.Font("assets/fonts/LUCON.TTF", int(screensize[0]*0.03))
computerbrowserstage = computerimage

random.seed(save["gameseed"])
temppass ="".join([random.choice(string.ascii_letters+"".join(list(map(str,list((range(10))))))) for char in "xxxxxxxx"])
random.seed()
temppassdisplay = computerfont.render(temppass, True, (0,0,0))
textinput0 = pygame_textinput.TextInputVisualizer()
textinput1 = pygame_textinput.TextInputVisualizer()

chargingtimer = 900

currentcamnumber = phonefont.render(f"{ingamevars['cam']}", True, (255,255,255))
camdelay = 0
camdeovasin = []
camdeovasout = []
cantcam = 0

for cam in range(5):
    camdeovasin.append(pygame.image.load(f"assets/sprites/cellphone/cams/deovasin/cellphone-cam{cam}.png").convert_alpha())
    camdeovasin[-1] = pygame.transform.scale(camdeovasin[-1], (screensize[0]*0.66,screensize[1]*1.15))
    camdeovasout.append(pygame.image.load(f"assets/sprites/cellphone/cams/deovasout/cellphone-cam{cam}.png").convert_alpha())
    camdeovasout[-1] = pygame.transform.scale(camdeovasout[-1], (screensize[0]*0.66,screensize[1]*1.15))

moveloop = 300

debugfont = pygame.font.Font("assets/fonts/LUCON.TTF", int(screensize[0]*0.012))

pygame.mixer_music.load(f"assets/audios/ambience/ambience{random.randint(0,8)}.mp3")
jumpscarelurgavideo = pgvideo("assets/videos/jumpscarelurga.mp4",loop=False,audio=False)
jumpscarelurgaudio = pygame.mixer.Sound("assets/audios/jumpscare/jumpscarelurga.mp3")
jumpscaredeovasvideo = pgvideo("assets/videos/jumpscaredeovas.mp4",loop=False,audio=False)
jumpscaredeovasaudio = jumpscarelurgaudio
jumpscared = False

goodmorning = pgvideo("assets/videos/goodmorning.mp4",loop=False,audio=True)
firstvideo = pgvideo(f"assets/videos/first.mp4",loop=False,audio=False)
entryvideo = pgvideo("assets/videos/night1.mp4",loop=False,audio=True)

occasionaldeovas = pygame.mixer.Sound("assets/audios/occasionaldeovas/deoba0.mp3")

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
            play = vhsfont.render(f"JOGAR", True, (255,255,255))
            exit = vhsfont.render(f"SAIR", True, (255,255,255))
            if save["currentnight"] == 1:
                currentnight = vhsfont.render(f"Segunda-Feira", True, (110,110,110))
            elif save["currentnight"] == 2:
                currentnight = vhsfont.render(f"Terça-Feira", True, (110,110,110))
            elif save["currentnight"] == 3:
                currentnight = vhsfont.render(f"Quarta-Feira", True, (110,110,110))
            elif save["currentnight"] == 4:
                currentnight = vhsfont.render(f"Quinta-Feira", True, (110,110,110))
            elif save["currentnight"] == 5:
                currentnight = vhsfont.render(f"Sexta-Feira", True, (110,110,110))
            elif save["currentnight"] == 6:
                currentnight = vhsfont.render(f"Sábado", True, (110,110,110))
            currentnight.set_alpha(0)
            currentnight = pygame.transform.scale_by(currentnight,0.5)
            if not pygame.mixer_music.get_busy():
                pygame.mixer_music.load("assets/audios/menusong.mp3")
                pygame.mixer_music.play()
                pygame.mixer_music.set_volume(0.8)
            if pygame.mouse.get_pos()[0] > screensize[0]*0.45 and pygame.mouse.get_pos()[0] < screensize[0]*0.45+play.get_rect()[2] and \
                pygame.mouse.get_pos()[1] > screensize[1]*0.4 and pygame.mouse.get_pos()[1] < screensize[1]*0.4+play.get_rect()[3]:
                    if not pygame.mouse.get_pressed()[0]:
                        play = vhsfont.render(f"JOGAR", True, (0,0,255))
                        currentnight.set_alpha(255)
                    else:
                        state = "game"
                        section = "first"
                        entryvideo = pgvideo(f"assets/videos/night{save['currentnight']}.mp4",loop=False,audio=True)
                        firstvideo = pgvideo(f"assets/videos/first.mp4",loop=False,audio=False)
                        pygame.mixer_music.stop()
                        init = False
                        resetigv(cellphonehome)
                        fanontimer = 0
                        jumpscared = False
                        jumpscarelurgavideo = pgvideo("assets/videos/jumpscarelurga.mp4",loop=False,audio=False)
                        jumpscaredeovasvideo = pgvideo("assets/videos/jumpscaredeovas.mp4",loop=False,audio=False)
                        goodmorning = pgvideo("assets/videos/goodmorning.mp4",loop=False,audio=True)
                        heat.set_alpha(255)
                        cellphoneY = 1.05
                        scenarioX = 0
                        scenarioY = -0.5
                        scenariospeed = 0
                        chargingtimer = 900
                        faintkill = 0
                        faintimage.set_alpha(9)
            if pygame.mouse.get_pos()[0] > screensize[0]*0.46 and pygame.mouse.get_pos()[0] < screensize[0]*0.46+exit.get_rect()[2] and \
                pygame.mouse.get_pos()[1] > screensize[1]*0.6 and pygame.mouse.get_pos()[1] < screensize[1]*0.6+exit.get_rect()[3]:
                    if not pygame.mouse.get_pressed()[0]:
                        exit = vhsfont.render(f"SAIR", True, (255,0,0))
                    else:
                        running = False

            screen.blit(pygame.transform.scale(deovavideo.frame(),screensize), (0, 0))
            if random.randint(0,29) == 0 and deovavideo.currentframe != False:
                deovavideo.randomizeframe()
            screen.blit(dtime, (screensize[0]*0.1,screensize[1]*0.766))
            screen.blit(ddate, (screensize[0]*0.1,screensize[1]*0.833))
            screen.blit(title, (screensize[0]*0.248,screensize[1]*0.1))
            aligntext = (play.get_rect()[2]-currentnight.get_rect()[2])*0.5
            screen.blit(currentnight, ((screensize[0]*0.45)+aligntext,(screensize[1]*0.4)+play.get_rect()[3]))
            screen.blit(play, (screensize[0]*0.45,screensize[1]*0.4))
            screen.blit(exit, (screensize[0]*0.46,screensize[1]*0.6))
            if realframe == 2: # game/video fps difference fix
                oldframe = pygame.transform.scale(menuvideo.frame(), screensize)
                oldframe.set_alpha(50)
            screen.blit(oldframe, (0, 0))

        if section == "test":
            if realframe == 2: # game/video fps difference fix
                oldframe = pygame.transform.scale(testvideo.frame(), screensize)
            screen.blit(oldframe, (0, 0))

    #game section
    if state == "game":
        if section == "first":
            if save["currentnight"] == 1:
                if not firstvideo.currentframe:
                    screen.fill((0,0,0))
                    pygame.display.flip()
                    time.sleep(1)
                if not firstvideo.ended:
                    screen.blit(pygame.transform.scale(firstvideo.frame(), screensize),(0,0))
                else:
                    section = "loading"
            else:
                section = "loading"
        if section == "loading":
            if not entryvideo.currentframe:
                screen.fill((0,0,0))
                pygame.display.flip()
                time.sleep(1)
            if not entryvideo.ended:
                screen.blit(pygame.transform.scale(entryvideo.frame(), screensize),(0,0))
            else:
                section = f"night{save['currentnight']}"
        if section not in ["first", "loading"]:
            screen.fill((0,0,0))
            #game globals
            #ambience
            if not pygame.mixer_music.get_busy():
                pygame.mixer_music.load(f"assets/audios/ambience/ambience{random.randint(0,8)}.mp3")
                pygame.mixer_music.play()
                pygame.mixer_music.set_volume(0.05)
            #time
            ingamevars["time"]+=1
            if ingamevars["time"] >= 29635:
                if ingamevars["computerdone"] and not jumpscared:
                    if ingamevars["time"] == 29635:
                        if save["currentnight"] < 5:
                            save["currentnight"] += 1
                        ingamevars["action"] = None
                        godumpingroom.set_alpha(0)
                        grabcell.set_alpha(0)
                        heat.set_alpha(0)
                        ingamevars["heat"] = 0
                        faintimage.set_alpha(0)
                        pygame.mixer_music.set_volume(0.0)
                        pygame.mixer.stop()
                    if not goodmorning.ended:
                        screen.blit(pygame.transform.scale(goodmorning.frame(),screensize),(0,0))
                    else:
                        pygame.mixer_music.stop()
                        state = "menu"
                        section = "main"
                else:
                    pygame.mixer_music.set_volume(0.0)
                    pygame.mixer.stop()
                    state = "menu"
                    section = "main"
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
                faintkill+=3
            elif faintkill>=0:
                faintkill-=2
            if faintkill >= 540:
                if not jumpscared:
                    pygame.mixer.find_channel().play(jumpscaredeovasaudio)
                    jumpscared = True
                    fanontimer = 1201
                    moveloop = -1
                    ingamevars[random.choice(["deovaspos","lurgapos"])] = 20
                    ingamevars["time"] = 0
            #fan
            if ingamevars["fan"]:
                fanbladesrotation += 100
                if fanbladesoff == 100:
                    fansoundo = pygame.mixer.Sound(f"assets/audios/fanon.mp3")
                    pygame.mixer.find_channel().play(fansoundo,-1)
                    fansoundo.set_volume(0.5)
                fanbladesoff -= 2
                fanontimer += 1
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
                if ingamevars["deovaspos"] not in [20,12] or ingamevars["cellphonenow"] != cellphoneflash:
                    screen.blit(frontimage1,(screensize[0]*scenarioX,0))
                else:
                    if not deovasdiscovered:
                        scenarioX = -0.5
                        pygame.mixer.find_channel().play(seedeovas)
                        deovasdiscovered = True
                    screen.blit(frontimage1deovas,(screensize[0]*scenarioX,0))
                screen.blit(fan,(screensize[0]*scenarioX+(screensize[0]*0.8),screensize[1]*0.2))
                screen.blit(fanblades_,(screensize[0]*scenarioX+(screensize[0]*0.888)-int(fanblades_.get_width()/2),screensize[1]*0.34-int(fanblades_.get_height()/2)))
                if cellphoneY < 1.05:
                    screen.blit(ingamevars["cellphonenow"],(screensize[0]*0.25,screensize[1]*cellphoneY))
                    if ingamevars["cellphonenow"] == cellphonecams and cantcam <= 0:
                        if ingamevars["deovaspos"] == ingamevars["cam"]:
                            screen.blit(camdeovasin[ingamevars["cam"]],(screensize[0]*0.25,screensize[1]*cellphoneY))
                        else:
                            screen.blit(camdeovasout[ingamevars["cam"]],(screensize[0]*0.25,screensize[1]*cellphoneY))
            if ingamevars["action"] == "computerdesktop":
                screen.blit(computerimage,(0,0))
            if ingamevars["action"] == "computerbrowser":
                if ingamevars["computerstage"] == 0:
                    screen.blit(computerimagebrowser[int(section[-1])-1],(0,0))
                else:
                    screen.blit(computerbrowserstage,(0,0))
                if section == "night2" and ingamevars["computerstage"] == 1:
                    screen.blit(temppassdisplay,(screensize[0]*0.435,screensize[1]*0.5))
                if section == "night3":
                    screen.blit(textinput0.surface,(screensize[0]*0.357,screensize[1]*0.532))
                if section == "night4":
                    screen.blit(textinput0.surface,(screensize[0]*0.410,screensize[1]*0.490))
                    screen.blit(textinput1.surface,(screensize[0]*0.410,screensize[1]*0.556))
                if section == "night5" and not ingamevars["computerdone"]:
                    screen.blit(textinput0.surface,(screensize[0]*0.357,screensize[1]*0.532))
                    screen.blit(textinput1.surface,(screensize[0]*0.426,screensize[1]*0.716))
            if ingamevars["action"] == "outdumpingroom":
                if not ingamevars["backdoor"]:
                    screen.blit(backimage1open,(0,0))
                else:
                    screen.blit(backimage1closed,(0,0))
            if ingamevars["action"] == "indumpingroom":
                if ingamevars["deovaspos"] != 11:
                    screen.blit(backimage2,(0,screensize[1]*scenarioY))
                else:
                    if not deovasdiscovered:
                        if backimage2.get_alpha() ==200 or scenarioY >= -0.20:
                            scenarioY = 0
                            pygame.mixer.find_channel().play(seedeovas)
                            deovasdiscovered = True
                    screen.blit(backimage2deova,(0,screensize[1]*scenarioY))

            if ingamevars["action"] == "cellphone" and ingamevars["battery"] > 0:
                if ingamevars["cellphonenow"] != cellphonecams:
                    screen.blit(battery, (screensize[0]*0.558,screensize[1]*cellphoneY*3.1))
                    screen.blit(gametime, (screensize[0]*0.517,screensize[1]*cellphoneY*3.1))
                    screen.blit(nightdisplay, (screensize[0]*0.4,screensize[1]*cellphoneY*3.1))
                else:
                    screen.blit(battery, (screensize[0]*0.62,screensize[1]*cellphoneY*-0.3))
                    screen.blit(gametime, (screensize[0]*0.569,screensize[1]*cellphoneY*-0.3))
                    screen.blit(nightdisplay, (screensize[0]*0.34,screensize[1]*cellphoneY*-0.3))
                    screen.blit(currentcamnumber, (screensize[0]*0.64,screensize[1]*0.685))
                if ingamevars["cellphonenow"] == cellphoneaudio:
                    for lockaudio in range(3-ingamevars["audiosleft"]):
                        screen.blit(lock,(screensize[0]*0.394,screensize[1]*cellphoneY*5.8+(1.3*lockaudio*lock.get_height())))

            if faintimage.get_alpha() > 0:
                screen.blit(faintimage,(0,0))
            if godumpingroom.get_alpha() != 0:   
                screen.blit(godumpingroom, (screensize[0]*scenarioX+(screensize[0]*0.01),screensize[1]*0.1))
            if grabcell.get_alpha() != 0:
                screen.blit(grabcell, (screensize[0]*0.25,screensize[1]*0.9))
            screen.blit(heat,(screensize[0]*0.02,screensize[1]*0.02))
            if ingamevars["action"] != None:
                screen.fill((50,50,50),(screensize[0]*0.021,screensize[1]*0.071,heat.get_width()*1,int(screensize[0]*0.015)))
                screen.fill(heatcolor,(screensize[0]*0.02,screensize[1]*0.07,ingamevars["heat"]*heat.get_width()*0.00082,int(screensize[0]*0.014)))
            if debug:
                info = debugfont.render(f"fps: {round(clock.get_fps(),1)} frametime(raw):{clock.get_time()}({clock.get_rawtime()}) time: {ingamevars['time']}/29635 battery:{ingamevars['battery']} heat:{ingamevars['heat']} deovaspos: {ingamevars['deovaspos']} lurgapos: {ingamevars['lurgapos']}", False, (255,255,255))
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
                        fansoundo.set_volume(0.5)
                else:
                    stepsound.stop()
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
                    gametime = phonefont.render(f"H: 0{int(ingamevars['time']*0.0002363)}", True, (0,0,0))
                    if ingamevars["cellphonenow"] == cellphonecams:
                        gametime = pygame.transform.scale_by(gametime,1.277)

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
                            cantcam = 10
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
                            ingamevars["action"] = "computerdesktop"

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
                        fansoundo.set_volume(0.3)
                elif backimage1closed.get_alpha() != 255 and ingamevars["backdoor"]:
                    fan.set_alpha(fan.get_alpha()-10)
                    fanblades_.set_alpha(fan.get_alpha())
                    frontimage1.set_alpha(frontimage1.get_alpha()-10)
                    backimage1closed.set_alpha(backimage1closed.get_alpha()+10)
                    grabcell.set_alpha(0)
                    if ingamevars["fan"]:
                        fansoundo.set_volume(0.3)
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
                            pygame.mixer.find_channel().play(doorclose)
                            backimage1open.set_alpha(0)
                        else:
                            ingamevars["backdoor"] = False
                            pygame.mixer.find_channel().play(dooropen)
                            backimage1open.set_alpha(0)
                            backimage1closed.set_alpha(0)
                    if not ingamevars["backdoor"] and\
                        pygame.mouse.get_pos()[0] < screensize[0]*0.7 and pygame.mouse.get_pos()[0] > screensize[0]*0.2 and\
                        pygame.mouse.get_pressed()[0]:
                        ingamevars["action"] = "indumpingroom"
                        pygame.mixer.find_channel().play(stepsound)
                        scenarioY = -0.5

            #in dumping room
            if ingamevars["action"]  == "indumpingroom":
                if backimage2.get_alpha() != 255:
                    scenariospeed = 0
                    backimage2.set_alpha(backimage2.get_alpha()+10)
                    backimage1open.set_alpha(backimage1open.get_alpha()-10)
                    backimage1closed.set_alpha(backimage1closed.get_alpha()-10)
                else:
                    stepsound.stop()
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
                        pygame.mixer.find_channel().play(stepsound)
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
            
            #computer
            if ingamevars["action"] == "computerdesktop":
                if computerimage.get_alpha() != 255:
                    computerimage.set_alpha(computerimage.get_alpha()+10)
                    frontimage1.set_alpha(frontimage1.get_alpha()-10)
                else:
                    if pygame.mouse.get_pos()[0] > screensize[0]*0.880 and pygame.mouse.get_pos()[0] < screensize[0]*0.908 and\
                        pygame.mouse.get_pos()[1] > screensize[1]*0.115 and pygame.mouse.get_pos()[1] < screensize[1]*0.189 and\
                        pygame.mouse.get_pressed()[0]:
                            ingamevars["action"] = "normal"
                    if pygame.mouse.get_pos()[0] > screensize[0]*0.095 and pygame.mouse.get_pos()[0] < screensize[0]*0.155 and\
                        pygame.mouse.get_pos()[1] > screensize[1]*0.115 and pygame.mouse.get_pos()[1] < screensize[1]*0.189 and\
                        pygame.mouse.get_pressed()[0]:
                            ingamevars["action"] = "computerbrowser"
            if ingamevars["action"] == "computerbrowser":
                if pygame.mouse.get_pos()[0] > screensize[0]*0.083 and pygame.mouse.get_pos()[0] < screensize[0]*0.166 and\
                    pygame.mouse.get_pos()[1] > screensize[1]*0.785 and pygame.mouse.get_pos()[1] < screensize[1]*0.832 and\
                    pygame.mouse.get_pressed()[0]:
                        ingamevars["action"] = "computerdesktop"
            #lurga ai
            if fanontimer >= 1200:
                if fanontimer == 1200:
                    oldlurgapos = ingamevars["lurgapos"]
                    ingamevars["lurgapos"] = lurgamovement(ingamevars["lurgapos"], ingamevars["difficulty"][1])
                if ingamevars["lurgapos"] == 20:
                    if not jumpscared:
                        pygame.mixer.find_channel().play(jumpscarelurgaudio)
                        jumpscared = True
                elif ingamevars["lurgapos"] == 1 and oldlurgapos != ingamevars["lurgapos"]:
                    lurgaudio = pygame.mixer.Sound(f"assets/audios/lurganear{random.randint(0,2)}.mp3")
                    pygame.mixer.find_channel().play(lurgaudio)
                    fanontimer = 0

                if jumpscared and ingamevars["lurgapos"] in [20,21]:
                    if not jumpscarelurgavideo.ended:
                        jumpscarelurgaframe = pygame.transform.scale(jumpscarelurgavideo.frame(),screensize)
                        jumpscarelurgaframe.set_colorkey((232,0,1))
                        screen.blit(jumpscarelurgaframe,(0,0))
                    else:
                        time.sleep(1.2)
                        state = "menu"
                        section = "main"
                        pygame.mixer.stop()
                        pygame.mixer_music.stop()
            #deovas ai
            moveloop -= 1
            cantcam -=1
            if moveloop <= 0:
                if moveloop == 0:
                    olddeovaspos = ingamevars["deovaspos"]
                    ingamevars["deovaspos"] = deovasmovement(ingamevars["deovaspos"],ingamevars["difficulty"][0])
                    if random.randint(0,4) == 0:
                        occasionaldeovas = pygame.mixer.Sound(f"assets/audios/occasionaldeovas/deoba{random.randint(0,1)}.mp3")
                        pygame.mixer.find_channel().play(occasionaldeovas)
                        occasionaldeovas.set_volume(0.1)
                if ingamevars["deovaspos"] not in [11,12,20,21]:
                    deovasdiscovered = False
                if ingamevars["deovaspos"] == 20:
                    if not ingamevars["backdoor"]:
                        if not jumpscared:
                            pygame.mixer.find_channel().play(jumpscaredeovasaudio)
                            jumpscared = True
                    elif not jumpscared:
                        ingamevars["deovaspos"] = random.choices([2,11],[60,30])[0]
                if ingamevars["deovaspos"] == 21:
                    if ingamevars["cellphonenow"] != cellphoneflash:
                        if not jumpscared:
                            pygame.mixer.find_channel().play(jumpscaredeovasaudio)
                            jumpscared = True
                    elif not jumpscared:
                        ingamevars["deovaspos"] = random.choices([2,12],[70,30])[0]
                if jumpscared and ingamevars["deovaspos"] in [20,21]:
                    if not jumpscaredeovasvideo.ended:
                        jumpscaredeovasframe = pygame.transform.scale(jumpscaredeovasvideo.frame(),screensize)
                        jumpscaredeovasframe.set_colorkey((232,0,1))
                        screen.blit(jumpscaredeovasframe,(0,0))
                    else:
                        time.sleep(1.2)
                        state = "menu"
                        section = "main"
                        pygame.mixer.stop()
                        pygame.mixer_music.stop()
                if ingamevars["deovaspos"] not in [20,21]:
                    moveloop = 300
            #noite 1 vc tenta logar e clica pra recuperar a senha
            #noite 2 vc pega a senha no email
            #noite 3 vc loga com a senha provisoria
            #noite 4 vc redefine a senha
            #noite 5 vc coloca o captcha pra confirmar
            if section == "night1":
                if not init:
                    textinput0.value = ""
                    textinput1.value = ""
                    ingamevars["difficulty"] = [9,12]
                    init = True
                else:
                    nightdisplay = phonefont.render("Segunda-Feira", True, (0,0,0))
                    if ingamevars["cellphonenow"] == cellphonecams:
                        nightdisplay = pygame.transform.scale_by(nightdisplay,1.277)
                    if pygame.mouse.get_pos()[0] > screensize[0]*0.451 and pygame.mouse.get_pos()[0] < screensize[0]*0.540 and\
                        pygame.mouse.get_pos()[1] > screensize[1]*0.590 and pygame.mouse.get_pos()[1] < screensize[1]*0.642 and\
                        pygame.mouse.get_pressed()[0] and ingamevars["computerstage"] == 0:
                            ingamevars["computerstage"] = 1
                            computerbrowserstage = pygame.image.load(f"assets/images/computer/nightstages/{section[-1]}-{ingamevars['computerstage']}.png").convert_alpha()
                            computerbrowserstage = pygame.transform.scale(computerbrowserstage,screensize)
                    if pygame.mouse.get_pos()[0] > screensize[0]*0.447 and pygame.mouse.get_pos()[0] < screensize[0]*0.550 and\
                        pygame.mouse.get_pos()[1] > screensize[1]*0.658 and pygame.mouse.get_pos()[1] < screensize[1]*0.730 and\
                        pygame.mouse.get_pressed()[0] and ingamevars["computerstage"] == 1:
                            ingamevars["computerstage"] = 2
                            computerbrowserstage = pygame.image.load(f"assets/images/computer/nightstages/{section[-1]}-{ingamevars['computerstage']}.png").convert_alpha()
                            computerbrowserstage = pygame.transform.scale(computerbrowserstage,screensize)
                            ingamevars["computerdone"] = True

            if section == "night2":
                if not init:
                    textinput0.value = ""
                    textinput1.value = ""
                    ingamevars["difficulty"] = [13,16]
                    init = True
                else:
                    nightdisplay = phonefont.render("Terça-Feira", True, (0,0,0))
                    if ingamevars["cellphonenow"] == cellphonecams:
                        nightdisplay = pygame.transform.scale_by(nightdisplay,1.277)
                    if pygame.mouse.get_pos()[0] > screensize[0]*0.140 and pygame.mouse.get_pos()[0] < screensize[0]*0.792 and\
                        pygame.mouse.get_pos()[1] > screensize[1]*0.329 and pygame.mouse.get_pos()[1] < screensize[1]*0.376 and\
                        pygame.mouse.get_pressed()[0] and ingamevars["computerstage"] == 0:
                            ingamevars["computerstage"] = 1
                            computerbrowserstage = pygame.image.load(f"assets/images/computer/nightstages/{section[-1]}-{ingamevars['computerstage']}.png").convert_alpha()
                            computerbrowserstage = pygame.transform.scale(computerbrowserstage,screensize)
                            ingamevars["computerdone"] = True

            if section == "night3":
                if not init:
                    textinput0.value = ""
                    textinput1.value = ""
                    ingamevars["difficulty"] = [17,20]
                    init = True
                else:
                    nightdisplay = phonefont.render("Quarta-Feira", True, (0,0,0))
                    if ingamevars["cellphonenow"] == cellphonecams:
                        nightdisplay = pygame.transform.scale_by(nightdisplay,1.277)
                    if ingamevars["computerstage"] in [0,-1]:
                        textinput0.update(events)
                        if pygame.mouse.get_pos()[0] > screensize[0]*0.451 and pygame.mouse.get_pos()[0] < screensize[0]*0.540 and\
                            pygame.mouse.get_pos()[1] > screensize[1]*0.590 and pygame.mouse.get_pos()[1] < screensize[1]*0.642 and\
                            pygame.mouse.get_pressed()[0]:
                                if textinput0.value == temppass:
                                    ingamevars["computerstage"] = 1
                                    computerbrowserstage = pygame.image.load(f"assets/images/computer/nightstages/{section[-1]}-{ingamevars['computerstage']}.png").convert_alpha()
                                    computerbrowserstage = pygame.transform.scale(computerbrowserstage,screensize)
                                    ingamevars["computerdone"] = True
                                else:
                                    ingamevars["computerstage"] = -1
                                    computerbrowserstage = pygame.image.load(f"assets/images/computer/nightstages/{section[-1]}-{ingamevars['computerstage']}.png").convert_alpha()
                                    computerbrowserstage = pygame.transform.scale(computerbrowserstage,screensize)
                    if ingamevars["computerdone"]:
                        textinput0.value = "********"
            if section == "night4":
                if not init:
                    textinput0.value = ""
                    textinput1.value = ""
                    inputfocus = textinput0
                    ingamevars["difficulty"] = [21,24]
                    init = True
                else:
                    nightdisplay = phonefont.render("Quinta-Feira", True, (0,0,0))
                    if ingamevars["cellphonenow"] == cellphonecams:
                        nightdisplay = pygame.transform.scale_by(nightdisplay,1.277)
                    if pygame.mouse.get_pos()[0] > screensize[0]*0.137 and pygame.mouse.get_pos()[0] < screensize[0]*0.242 and\
                        pygame.mouse.get_pos()[1] > screensize[1]*0.431 and pygame.mouse.get_pos()[1] < screensize[1]*0.452 and\
                        pygame.mouse.get_pressed()[0] and ingamevars["computerstage"] == 0:
                            ingamevars["computerstage"] = 1
                            computerbrowserstage = pygame.image.load(f"assets/images/computer/nightstages/{section[-1]}-{ingamevars['computerstage']}.png").convert_alpha()
                            computerbrowserstage = pygame.transform.scale(computerbrowserstage,screensize)
                    if pygame.mouse.get_pos()[0] > screensize[0]*0.477 and pygame.mouse.get_pos()[0] < screensize[0]*0.576 and\
                        pygame.mouse.get_pos()[1] > screensize[1]*0.648 and pygame.mouse.get_pos()[1] < screensize[1]*0.710 and\
                        pygame.mouse.get_pressed()[0] and ingamevars["computerstage"] in [1,-1]:
                            if textinput0.value == temppass and textinput1.value == "Pesca1797200769AB_O1":
                                ingamevars["computerstage"] = 2
                                computerbrowserstage = pygame.image.load(f"assets/images/computer/nightstages/{section[-1]}-{ingamevars['computerstage']}.png").convert_alpha()
                                computerbrowserstage = pygame.transform.scale(computerbrowserstage,screensize)
                                ingamevars["computerdone"] = True
                            else:
                                ingamevars["computerstage"] = -1
                                computerbrowserstage = pygame.image.load(f"assets/images/computer/nightstages/{section[-1]}-{ingamevars['computerstage']}.png").convert_alpha()
                                computerbrowserstage = pygame.transform.scale(computerbrowserstage,screensize)
                    if ingamevars["computerstage"] in [1,-1]:
                        if inputfocus == textinput0:
                            textinput0.update(events)
                        else:
                            textinput1.update(events)
                    if len(inputfocus.value) != 0 and ord(inputfocus.value[-1]) == 9:
                        inputfocus.value = inputfocus.value[:-1]
            if section == "night5":
                if not init:
                    textinput0.value = ""
                    textinput1.value = ""
                    inputfocus = textinput0
                    ingamevars["difficulty"] = [25,28]
                    init = True
                else:
                    nightdisplay = phonefont.render("Sexta-Feira", True, (0,0,0))
                    if ingamevars["cellphonenow"] == cellphonecams:
                        nightdisplay = pygame.transform.scale_by(nightdisplay,1.277)
                    if pygame.mouse.get_pos()[0] > screensize[0]*0.451 and pygame.mouse.get_pos()[0] < screensize[0]*0.540 and\
                        pygame.mouse.get_pos()[1] > screensize[1]*0.769 and pygame.mouse.get_pos()[1] < screensize[1]*0.821 and\
                        pygame.mouse.get_pressed()[0] and ingamevars["computerstage"] in [0,-1]:
                            if textinput0.value == "Pesca21797200769AB_O1" and textinput1.value.lower().replace(" ", "") == "fish,ball,cat":
                                ingamevars["computerstage"] = 1
                                computerbrowserstage = pygame.image.load(f"assets/images/computer/nightstages/{section[-1]}-{ingamevars['computerstage']}.png").convert_alpha()
                                computerbrowserstage = pygame.transform.scale(computerbrowserstage,screensize)
                                ingamevars["computerdone"] = True
                            else:
                                ingamevars["computerstage"] = -1
                                computerbrowserstage = pygame.image.load(f"assets/images/computer/nightstages/{section[-1]}-{ingamevars['computerstage']}.png").convert_alpha()
                                computerbrowserstage = pygame.transform.scale(computerbrowserstage,screensize)

                    if ingamevars["computerstage"] in [0,-1]:
                        if inputfocus == textinput0:
                            textinput0.update(events)
                        else:
                            textinput1.update(events)
                    if len(inputfocus.value) != 0 and ord(inputfocus.value[-1]) == 9:
                        inputfocus.value = inputfocus.value[:-1]
            if section == "night6":
                if not init:
                    ingamevars["difficulty"] = [0.1,0]
                    init = True
                else:
                    moveloop = 1
                    pygame.mixer.set_num_channels(999)

    if realframe == 2:
        realframe = 0
    pygame.display.flip()
    clock.tick(fps)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                debug = not debug
            elif event.key == pygame.K_TAB and section in ["night4","night5"]:
                if inputfocus == textinput0:
                    inputfocus = textinput1
                else:
                    inputfocus = textinput0
            elif event.key == pygame.K_RETURN and section == "first":
                section = "loading"
        if event.type == pygame.QUIT:
            running = False

for file in glob.glob('tmp.*.mp3'):
    os.remove(file)
with open("saves/save.json", 'w') as savefile:
    json.dump(save, savefile)