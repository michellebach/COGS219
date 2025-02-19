import time
import sys
import os
import random
from psychopy import visual,event,core,gui

stimuli = ['red', 'orange', 'yellow', 'green', 'blue']
stim_type = ['congruent', 'incongruent']
#first letter of color keys
allowed_keys = ['r','o','y','g','b','q']

#wrong colored words
def make_incongruent(color):
    incong_color_set = [stimulus for stimulus in stimuli if stimulus != color] 
    incong_color = random.choice(incong_color_set)
    return incong_color

win = visual.Window([800,600],color="gray", units='pix',checkTiming=False)
placeholder = visual.Rect(win,width=180,height=80, fillColor="lightgray",lineColor="black", lineWidth=6,pos=[0,0])
word_stim = visual.TextStim(win,text="", height=40, color="black",pos=[0,0])
instruction = visual.TextStim(win,text="Press the first letter of the ink color", height=20, color="black",pos=[0,-200], autoDraw = True)
#add fixation cross
fixation_cross = visual.TextStim(win, text = "+", color = "black", height = 15)

#add incorrect feedback
incorrect_feedback = visual.TextStim(win, text = "Incorrect", color = "black", height = 40)
#add slow feedback
slow_feedback = visual.TextStim(win, text = "Too slow", color = "black", height = 40)

#reaction time
RTs = []
react_timer = core.Clock()
#task
key_pressed = False
while True:
    cur_word = random.choice(stimuli)
    stim_type = random.choice(stim_type)
    word_stim.setText(cur_word)
    #set color for word
    if stim_type == 'incongruent':
        cur_color = make_incongruent(cur_word)
    else:
        cur_color = cur_word
    word_stim.setColor(cur_color)
    placeholder.draw()
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
    key_pressed = event.waitKeys(keyList=allowed_keys, maxWait = 2)
    # append rts
    RTs.append(round(react_timer.getTime()*1000,0))
    # time limit + feedback
    if not key_pressed:
        slow_feedback.draw()
        win.flip()
        core.wait(1)
    elif key_pressed[0] == cur_color[0]:
        pass
    elif key_pressed[0] == 'q':
        break
    else:
        incorrect_feedback.draw()
        win.flip()
        core.wait(1)

print(RTs)
