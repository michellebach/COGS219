def generate_trials(subj_code, seed,num_repetitions=25):
    '''
    Writes a file named {subj_code_}trials.csv, one line per trial. Creates a trials subdirectory if one does not exist
    subj_code: a string corresponding to a participant's unique subject code
    seed: an integer specifying the random seed
    num_repetitions: integer specifying total times that combinations of trial type 
    (congruent vs. incongruent) and orientation (upright vs. upside_down) should repeat (total number of trials = 4 * num_repetitions)
    '''
    import os
    import random
    
    # define general parameters and functions here
    separator=","
    trial_type = ['congruent', 'incongruent']
    orientation = ['upright', 'upside_down']
    num_repetitions = int(num_repetitions)
    act_colors = ['red', 'orange', 'yellow', 'green', 'blue']
    
    # create a trials folder if it doesn't already exist
    try:
        os.mkdir('trials')
    except FileExistsError:
        print('Trials directory exists; proceeding to open file')
    f= open(f"trials/{subj_code}_trials.csv","w")

    #write header
    header = separator.join(["subj_code","seed","word", 'color','trial_type','orientation'])
    f.write(header+'\n')
    
    # write code to loop through creating and adding trials to the file here
    trials = []
    for i in range(num_repetitions):
        for cur_trial_type in trial_type:
            for cur_orientation in orientation: 
                cur_word = random.choice(act_colors)
                if cur_trial_type == 'incongruent':
                    cur_color = make_incongruent(cur_word, colors)
                else:
                    cur_color = cur_word
                trials.append([subj_code, seed, cur_word, cur_color, cur_trial_type, cur_orientation])
    
    #shuffle
    random.shuffle(trials)
    
    #write into file
    for cur_trial in trials:
        trial_file.write(separator.join(map(str,cur_trial))+'\n')


    #close the file
    f.close()