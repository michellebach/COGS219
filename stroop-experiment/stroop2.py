import time
import sys
import os
import random
from psychopy import visual,event,core,gui
from stroop_generate_trials import stroop_generate_trials #stroop_generate_trials doesnt work

stimuli = ['red', 'orange', 'yellow', 'green', 'blue']
valid_response_keys = ['r', 'o', 'y', 'g', 'b','q']
trial_types = ['congruent','incongruent']

def make_incongruent(color):
    possible_incongruent_colors = [stimulus for stimulus in stimuli if stimulus != color]
    incongruent_color = random.choice(possible_incongruent_colors)
    return incongruent_color
    
#runtime variables from helper.py4
def get_runtime_vars(vars_to_get,order,exp_version="stroop_code_from_reference"):
    infoDlg = gui.DlgFromDict(dictionary=vars_to_get, title=exp_version, order=order)
    if infoDlg.OK:
        return vars_to_get
    else: 
        print('User Cancelled')

# import_trials function from helper.py4
def import_trials (trial_filename, col_names=None, separator=','):
    trial_file = open(trial_filename, 'r')
 
    if col_names is None:
        # Assume the first row contains the column names
        col_names = trial_file.readline().rstrip().split(separator)
    trials_list = []
    for cur_trial in trial_file:
        cur_trial = cur_trial.rstrip().split(separator)
        assert len(cur_trial) == len(col_names) # make sure the number of column names = number of columns
        trial_dict = dict(zip(col_names, cur_trial))
        trials_list.append(trial_dict)
    return trials_list

win = visual.Window([800,600],color="gray", units='pix',checkTiming=False)
placeholder = visual.Rect(win,width=180,height=80, fillColor="lightgray",lineColor="black", lineWidth=6,pos=[0,0])
word_stim = visual.TextStim(win,text="", height=40, color="black",pos=[0,0])
instruction = visual.TextStim(win,text="Press the first letter of the ink color", height=20, color="black",pos=[0,-200],autoDraw=True)
#add fixation cross
fixation = visual.TextStim(win,height=40,color="black",text="+")
# add a new feedback TextStim before the while loop
feedback_incorrect = visual.TextStim(win,text="INCORRECT", height=40, color="black",pos=[0,0])
feedback_too_slow = visual.TextStim(win,text="TOO SLOW", height=40, color="black",pos=[0,0])

#get runtime variables from helper.py4
order =  ['subj_code','seed','num_reps']
runtime_vars= get_runtime_vars({'subj_code':'stroop_101','seed': 101, 'num_reps': 25}, order)
print(runtime_vars)

# generate a trial list
generate_trials(runtime_vars['subj_code'],runtime_vars['seed'],runtime_vars['num_reps'])

#read in trials
trial_path = os.path.join(os.getcwd(),'trials',runtime_vars['subj_code']+'_trials.csv')
trial_list = import_trials(trial_path)
print(trial_list)

RTs=[] #set RT list
response_timer = core.Clock() # set response timer clock
key_pressed=False #need to initialize this for later

#open file base code from mental rotation
try:
    os.mkdir('data')
    print('Data directory did not exist. Created data/')
except FileExistsError:
    pass 
separator=","
data_file = open(os.path.join(os.getcwd(),'data',runtime_vars['subj_code']+'_data.csv'),'w')
header = separator.join(["subj_code","seed", 'word','color','trial_type','orientation','trial_num','response','rt', 'is_correct', 'rt'])
data_file.write(header+'\n')

# trial loop
response_timer = core.Clock()
trial_num = 1
for cur_trial in trial_list:

    cur_word = cur_trial['word']
    cur_color = cur_trial['color']
    cur_orient = cur_trial['orientation']
    trial_type = cur_trial['trial_type']

    word_stim.setText(cur_word) #set text
    
    word_stim.setColor(cur_color) #set color
    
    if cur_orient == 'upside_down': 
        word_stim.setOri(180)
    else:
        word_stim.setOri(0)

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
        
    trial_num += 1
print(RTs)

data_file.close()
win.close() 
core.quit()