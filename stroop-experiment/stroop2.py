import time
import sys
import os
import random
from psychopy import visual,event,core,gui

stimuli = ['red', 'orange', 'yellow', 'green', 'blue']
valid_response_keys = ['r', 'o', 'y', 'g', 'b','q']
trial_types = ['congruent','incongruent']

def make_incongruent(color):
    possible_incongruent_colors = [stimulus for stimulus in stimuli if stimulus != color]
    incongruent_color = random.choice(possible_incongruent_colors)
    return incongruent_color
    
#runtime variables
def get_runtime_vars(vars_to_get,order,exp_version="stroop_code_from_reference"):
    infoDlg = gui.DlgFromDict(dictionary=vars_to_get, title=exp_version, order=order)
    if infoDlg.OK:
        return vars_to_get
    else: 
        print('User Cancelled')

win = visual.Window([800,600],color="gray", units='pix',checkTiming=False)
placeholder = visual.Rect(win,width=180,height=80, fillColor="lightgray",lineColor="black", lineWidth=6,pos=[0,0])
word_stim = visual.TextStim(win,text="", height=40, color="black",pos=[0,0])
instruction = visual.TextStim(win,text="Press the first letter of the ink color", height=20, color="black",pos=[0,-200],autoDraw=True)
#add fixation cross
fixation = visual.TextStim(win,height=40,color="black",text="+")
# add a new feedback TextStim before the while loop
feedback_incorrect = visual.TextStim(win,text="INCORRECT", height=40, color="black",pos=[0,0])
feedback_too_slow = visual.TextStim(win,text="TOO SLOW", height=40, color="black",pos=[0,0])

#get runtime variables
order =  ['subj_code','seed','num_reps']
runtime_vars= get_runtime_vars({'subj_code':'stroop_101','seed': 101, 'num_reps': 25]}, order)
print(runtime_vars)

RTs=[] #set RT list
response_timer = core.Clock() # set response timer clock
key_pressed=False #need to initialize this for later
while True:

    cur_word = random.choice(stimuli) #notice the change in variable name now that we have congruent and incongruent trials
    trial_type = random.choice(trial_types) #we're just going to randomly pick the trial type (so it's 50/50 congruent/incongruent)

    word_stim.setText(cur_word) #set text
    if trial_type == 'incongruent':
        cur_color = make_incongruent(cur_word)
    else:
        cur_color = cur_word
    #notice that at this point cur_color is the color we're gonna set the word to. 
    #It's taking into account the trial type 
    word_stim.setColor(cur_color) #set color

    #show fixation
    placeholder.draw()
    fixation.draw()
    win.flip()
    core.wait(.5)

    #short inter stimulus interval
    placeholder.draw()
    win.flip()
    core.wait(.5)

    #draw word stimulus
    placeholder.draw()
    word_stim.draw()
    win.flip()

    #get response
    response_timer.reset() # immediately after win.flip(), reset clock to measure RT
    key_pressed = event.waitKeys(keyList=valid_response_keys,maxWait=2) # maximum wait time of 2 s
    RTs.append(round(response_timer.getTime()*1000,0)) #add an RT to the list, rounded to the nearest millisecond

    # add feedback
    if not key_pressed:
        feedback_too_slow.draw()
        win.flip()
        core.wait(1)
    elif key_pressed[0] == cur_color[0]:
        #correct response
        pass
    elif key_pressed[0] == 'q':
        break
    else:
        feedback_incorrect.draw()
        win.flip()
        core.wait(1)

print(RTs)