import time
import sys
import os
import random
from psychopy import visual,event,core,gui

stimuli = ['red', 'orange', 'yellow', 'green', 'blue']

win = visual.Window([800,600],color="gray", units='pix',checkTiming=False)
placeholder = visual.Rect(win,width=180,height=80, fillColor="lightgray",lineColor="black", lineWidth=6,pos=[0,0])
word_stim = visual.TextStim(win,text="", height=40, color="black",pos=[0,0])
instruction = visual.TextStim(win,text="Press the first letter of the ink color", height=20, color="black",pos=[0,-200])
#add fixation cross
fixation_cross = visual.TextStim(win, text = "+", color = "black", height = 15)

#first letter of color keys
allowed_keys = ['r','o','y','g','b','q']

#add incorrect feedback
incorrect_feedback = visual.TextStim(win, text = "Incorrect", color = "black", height = 30)

#reaction time
RTs = []
react_timer = core.Clock()

key_pressed = False
while True:
    cur_stim = random.choice(stimuli)
    word_stim.setText(cur_stim)
    word_stim.setColor(cur_stim)
    placeholder.draw()
    instruction.autoDraw = True
    #fixation cross 
    fixation_cross.draw()
    win.flip()
    core.wait(0.5)
    # inter-stimulus
    placeholder.draw()
    win.flip()
    core.wait(0.5)
    # stimulus
    placeholder.draw()
    word_stim.draw()
    win.flip()
    # reset time
    react_timer.reset()
    key_pressed = event.waitKeys(keyList=allowed_keys)
    # append rts
    RTs.append(round(react_timer.getTime()*1000,0))
    print(key_pressed[0])
    # display feedback
    if key_pressed[0] == cur_stim[0]:
        continue
    elif key_pressed[0] == 'q':
        break
    else: 
        incorrect_feedback.draw()
        win.flip()
        core.wait(1)

    if key_pressed[0] == 'q':
        break

print(RTs)
