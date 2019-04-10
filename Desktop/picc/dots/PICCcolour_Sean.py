# -*- coding: utf-8 -*-
"""
code to display colored dot stimuli
author: David Levari, david.levari@gmail.com
last updated: 17 October 2018

based on studies found in:
Levari, D. E., Gilbert, D. T., Wilson, T. D., Sievers, B., Amodio, D. M.,
& Wheatley, T. (2018). Prevalence-induced concept change in human judgment.
Science, 360(6396), 1465-1467.

Edit log by Sean Devine, seandamiandevine@gmail.com:
    "blue" and "not blue" in instructions switched for "a" and "l" respectively
"""

from psychopy import visual, core, gui, event, monitors
from psychopy.visual import ShapeStim, ImageStim
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np
import pandas as pd
import random
import pyglet
import csv
import os

#Set directory
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

#Define functions
def addOutput(file, output):
    with open(file, 'a') as data:
        writer = csv.writer(data)
        writer.writerow(output)

def stimRandomizer(block,colorfreq,numtrials):
    """Generates stimuli"""
    reds = range(100)
    greens = [0] * 100
    blues = range(155,255)[::-1]
    colors = []
    for i in range(100):
        colors.append(list([reds[i],greens[i],blues[i]]))
    colorsignals = colors[0:50] #blue spectrum
    colornoise = colors[50:100] #purple spectrum
    colorsignals = random.sample(colorsignals,len(colorsignals))[:int(round(numtrials*colorfreq))]
    colornoise = random.sample(colornoise,len(colornoise))[:int(round(numtrials*(1-colorfreq)))]
    colorstim = random.sample(colorsignals+colornoise,numtrials)
    return(colorstim)

#dialogue box
expName = 'Ethics Task'
expInfo = {'participant': '', 'condition': ''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel'

#setup datafile
id = expInfo['participant']
cn = expInfo['condition']
filename = _thisDir + os.sep + 'data/PICCcolor_' + id+'.csv'
with open(filename, 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(['id', 'condition', 'block', 'trialinblock', 'trial', 'tstart', 'tend', 'trialstim', 'trialintensity', 'response', 'RT', 'trialtype', 'colourfreq'])

#Window setup
win = visual.Window(
    size=[1920, 1080], fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='cm')

#set constants
textCol = [1, 1, 1]
numtrials = 50
numpractrials = 10
numblocks = 16
trials = range(numtrials)
blocks = range(numblocks)
praccolorfreq = .5

postblocktime = 10
stimtime = .5
poststimtime = .5
postinsttime = 3

advance = ['space']
signalKey = "a"
noiseKey = "l"
acceptedKeys = ["a","l"]
fontH = 1


if cn == '0': #stable prevalence
    colorfreqs = [.5] * numblocks
elif cn == '1': #decreasing prevalence
    colorfreqs = [.5,.5,.5,.5,.4,.28,.14,.06,.06,.06,.06,.06,.06,.06,.06,.06]
elif cn == '2': #increasing prevalence
    colorfreqs =  [.5,.5,.5,.5,.6,.72,.86,.94,.94,.94,.94,.94,.94,.94,.94,.94]

#randomize stim for each trial in each block
practiceStim = stimRandomizer(1,praccolorfreq,numpractrials)
alltrials = []
for i in range(numblocks):
    alltrials.append(stimRandomizer(blocks[i],colorfreqs[i],numtrials))

print(alltrials)

#initialize instructions 
pressSpace = visual.TextStim(win=win, name='pressSpace',
    text="Press SPACE to continue.",
    font='Arial',
    pos=(0, -10), height=fontH, wrapWidth=30, ori=0,
    color='white', colorSpace='rgb');
    
i1 = visual.TextStim(win=win, name='i1',
    text="Welcome to this study! We are interested in studying how people \
perceive and identify colors.",
    font='Arial',
    pos=(0, 0), height=fontH, wrapWidth=30, ori=0,
    color='white', colorSpace='rgb');

i2 = visual.TextStim(win=win, name='i2',
    text='In this task, you will see a series of colored dots. \
The dots will be presented on the screen one at a time. \
Your tasks in this study will be to identify blue dots.',
    font='Arial',
    pos=(0, 0), height=fontH, wrapWidth=30, ori=0,
    color='white', colorSpace='rgb');

i3 = visual.TextStim(win=win, name='i3',
    text='When you see a blue dot on the screen, press \
the "A" key. For all other dots, press the "L" key.',
    font='Arial',
    pos=[0, 0], height=fontH, wrapWidth=30, ori=0,
    color='white', colorSpace='rgb');

i4 = visual.TextStim(win=win, name='i5',
    text='The dots will be presented in series with breaks in between. \
This means that you will see a series of dots, have a short break, and \
then another series of dots, until you have seen 16 series.',
    font='Arial',
    pos=(0, 0), height=fontH, wrapWidth=30, ori=0,
    color='white', colorSpace='rgb');

i5 = visual.TextStim(win=win, name='i5',
    text="Some of the series you see may have a lot of blue dots, and \
others may have only a few.",
    font='Arial',
    pos=(0, 0), height=fontH, wrapWidth=30, ori=0,
    color='white', colorSpace='rgb');

i6 = visual.TextStim(win=win, name='i6',
    text="You should do your best to answer quickly and accurately during \
the study. However, if you make a mistake and hit the wrong button at \
any point, don't worry -- just keep going.",
    font='Arial',
    pos=(0, 0), height=fontH, wrapWidth=30, ori=0,
    color='white', colorSpace='rgb');

i7 = visual.TextStim(win=win, name='i8',
    text='Now you will complete a brief practice series so you can see how \
the task works.',
    font='Arial',
    pos=(0, 0), height=fontH, wrapWidth=30, ori=0,
    color='white', colorSpace='rgb');

instsA = [i1, i2, i3, i4, i5, i6, i7]

i8 = visual.TextStim(win, text="You have now completed the practice \
series. If you have any questions, you can ask the \
experimenter now. Otherwise, you're ready to begin the \
study.",
    height=fontH, color=textCol, pos=[0, 0], wrapWidth=30);

#initialize trial components
trialClock = core.Clock()

blockTxt = visual.TextStim(win, text="", height=fontH, color=textCol, pos=[0, 0]);

fix = visual.TextStim(win, text="?", height=3*fontH, color=textCol, pos=[0, 0]);

dot = visual.Circle(win, radius = 200, edges = 1048, units = 'pix', 
    pos=[0, 0],fillColor = [1,1,1], #will change each trial
    fillColorSpace='rgb255',
    lineColor = None)

end = visual.TextStim(win, pos=[0, 0], text="Thanks for your participation\
! Please go get the experimenter.", height=fontH, alignHoriz = 'center')

#--------------------------------------Start Task-----------------------------------------
#display instructions 
for i in instsA: 
    i.draw()
    win.flip()
    #core.wait(postinsttime)
    i.draw()
    pressSpace.draw()
    win.flip()
    event.waitKeys(keyList = advance)


#practice sessions
blockTxt.text = 'Practice Block'
blockTxt.draw()
win.flip()
core.wait(postinsttime)
blockTxt.draw()
pressSpace.draw()
win.flip()
event.waitKeys(keyList = advance)
trialClock.reset()
for s in range(len(practiceStim)):
    startTime = trialClock.getTime()
    dot.fillColor = practiceStim[s]
    dot.draw()
    win.flip()
    core.wait(stimtime)
    fix.draw()
    win.flip()
    response = event.waitKeys(keyList = acceptedKeys, timeStamped = True)
    endTime = trialClock.getTime()
    win.flip()
    core.wait(poststimtime)
    addOutput(filename, [id, cn, 'Practice', s+1, 'NA', startTime, endTime, practiceStim[s], practiceStim[s][2], response[0][0], response[0][1]*10, 'colour', praccolorfreq])

#end practice 
i8.draw()
win.flip()
core.wait(postinsttime)
i8.draw()
pressSpace.draw()
win.flip()
event.waitKeys(keyList = advance)

#trials 
trialClock.reset()
tCount = 0
for block in range(len(alltrials)):
    blockTxt.text = 'Block {}'.format(str(block+1))
    blockTxt.draw()
    win.flip()
    core.wait(postinsttime)
    blockTxt.draw()
    pressSpace.draw()
    win.flip()
    event.waitKeys(keyList=advance)
    for s in range(len(alltrials[block])): 
        tCount += 1
        startTime = trialClock.getTime()
        dot.fillColor = alltrials[block][s]
        dot.draw()
        win.flip()
        core.wait(stimtime)
        fix.draw()
        win.flip()
        response = event.waitKeys(keyList = acceptedKeys, timeStamped = True)
        endTime = trialClock.getTime()
        win.flip()
        core.wait(poststimtime)
        addOutput(filename, [id, cn, block+1, s+1, tCount, startTime, endTime, alltrials[block][s], alltrials[block][s][2], response[0][0], response[0][1]*10, 'colour', colorfreqs[block]])

end.draw()
win.flip()
event.waitKeys(keyList = advance)