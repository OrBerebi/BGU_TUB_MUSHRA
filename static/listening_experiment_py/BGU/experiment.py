import numpy as np
import os.path
import os
import sys
import scipy.io as scyio
from .. classes.handler import ExperimentHandler
from collections import defaultdict



class Handler(ExperimentHandler):
    def __init__(self, ssr_ids, num_stimuli_per_page, attributes,
                 base_path='listening_experiment', debug=False,
                 do_reset=False, hidden_references=None, groups=None):
        super().__init__(ssr_ids, base_path, debug)

        self.num_stimuli_per_page = num_stimuli_per_page
        self.attributes = attributes
        self.phase = 1  # OLE phase or SAQI phase
        self.switch_phase = False
        self.experiment_complete = False
        self.current_trial = 0
        self.current_attribute = 0
        self.switch_attribute = False
        self.random_vector_phase1 = []
        self.randomized_attributes = list()
        self.current_ssr_cnts = np.array([0, 0])
        self.attribute_has_changed = False
        self.hidden_references = np.array(hidden_references)
        self.groups = groups  # If we want to test stimuli separately in groups, like for example
                              # different rooms, indicate inides of groups here.
                              # Each idx indicates the last ssr idx of the corresponing group
        self.groups_complete = 0
        #self.gifs_paths = gifs_paths
        #self.randomized_gifs_paths = list()

        self._init(do_reset)

    def _randomize(self):
        # randomize stimuli for phase 1
        if self.hidden_references is None:  # shuffle all non-reference ids
            if self.groups is None:
                tmp = np.random.permutation(self.ssr_ids[:, :])
                self.random_vector_phase1     = tmp[:,0]
                self.random_vector_attributes = tmp[:,2]
                del tmp
            else:  # shuffle within groups
                tmp = np.array([], dtype=int)
                cnt = 0
                for g in self.groups:
                    tmp = np.concatenate((tmp, np.random.permutation(self.ssr_ids[cnt:g+1, :])))
                    cnt = g + 1
                self.random_vector_phase1     = tmp[:,0]
                self.random_vector_attributes = tmp[:,2]
                del tmp

        else:  # include the references into the stimuli to be rated
            if self.groups is None:
                pages_dict = defaultdict(list)
                combined_ids = np.concatenate((self.ssr_ids, self.hidden_references), axis=0)
                for row in combined_ids:
                    ssr_id, page, attribute = row
                    pages_dict[page].append((ssr_id, attribute))

                self.random_vector_phase1 = []
                self.random_vector_attributes = []

                for page in sorted(pages_dict.keys()):
                    entries = pages_dict[page]
                    entries = np.array(entries)  # Shape: (N, 2)
                    perm = np.random.permutation(len(entries))

                    shuffled_ssr_ids = entries[perm, 0]
                    shuffled_attributes = entries[perm, 1]

                    self.random_vector_phase1.extend(shuffled_ssr_ids.tolist())
                    self.random_vector_attributes.extend(shuffled_attributes.tolist())

                #tmp = np.concatenate((self.ssr_ids[:, :],self.hidden_references)[:,:])
                #tmp = np.random.permutation(tmp)
                #self.random_vector_phase1     = tmp[:,0]
                #self.random_vector_attributes = tmp[:,2]
                #del tmp
                print("No group, random_vector_phase1: ", self.random_vector_phase1)
                print("No group, random_vector_attributes: ", self.random_vector_attributes)

            else:  # shuffle within groups and assume the first reference belongs to group 1,
                   # the seconds reference to group 2 and so forth
                
                tmp_big = np.empty((0, 3), dtype=int)  # Shape (0,3), matching tmp
                cnt = 0
                for g_idx in range(0, len(self.groups)):
                    tmp = np.concatenate((self.ssr_ids[cnt:self.groups[g_idx]+1, :],
                                          [self.hidden_references[g_idx,:]]))
                    tmp_big = np.concatenate((tmp_big, np.random.permutation(tmp)))
                    cnt = self.groups[g_idx]+1
                self.random_vector_phase1     = tmp_big[:,0]
                self.random_vector_attributes = tmp_big[:,2]
                del tmp
                del tmp_big
                print("Yes group, random_vector_phase1: ", self.random_vector_phase1)
                print("Yes group, random_vector_attributes: ", self.random_vector_attributes)



    def set_participant_infos(self, infos):
        if not self._debug:
            self.participant_infos = {'participant_id': self._overall_id_cnt,
                                      'age': infos[0],
                                      'gender': infos[1],
                                      'ListeningExperimentExperience':
                                          infos[2],
                                      'BinauralExperience': infos[3],
                                      'HealthStatus': infos[4],
                                      'HearingProblems': infos[5]}

            scyio.savemat(f'{self._result_file_name}.mat',
                          {'participant_infos': self.participant_infos,
                           'actual_trial': self.current_trial})

    def reset_ssr_ids(self):
        self.current_ssr_cnts = [0, self.num_stimuli_per_page] 
        # idx of ssr ids in random vector
        self.current_trial = 0
        self.groups_complete = 0
        self.max_trials = np.max(self.ssr_ids[:,1])
        print("max_trials: ",self.max_trials)

    def next_trial(self):
        self.current_trial += 1

        self.current_ssr_cnts[0] = self.current_ssr_cnts[1]
        self.current_ssr_cnts[1] += self.num_stimuli_per_page

        if self.current_trial > self.max_trials:
            self.switch_phase = True
            self.experiment_complete = True
       
        # end of phase 1
        #if self.current_ssr_cnts[1]-1 >= self.random_vector_phase1.shape[0]:
        #    self.current_ssr_cnts[1] = self.random_vector_phase1.shape[0]
        #    self.switch_phase = True
        #    self.current_trial = 0
        #       
        #if self.current_attribute >= len(self.attributes):
        #    self.experiment_complete = True
       
    
    def get_current_ssr_ids(self):
        """_summary_

        Returns:
            _type_: in phase 1, all ssr ids to test are returned (including the reference if desired)
                    in phase 2, reference + all ssr ids to test are returned
        """
        #return self.random_vector_phase1[self.current_ssr_cnts[0]:self.current_ssr_cnts[1]]

        # Extract SSR IDs from stimuli that match the current trial (page id)
        ssr_ids_filtered = self.ssr_ids[self.ssr_ids[:, 1] == self.current_trial]
        
        # Extract SSR ID from hidden references that match the current trial (page id)
        hidden_reference_filtered = self.hidden_references[self.hidden_references[:, 1] == self.current_trial]
        
        # Combine and shuffle
        combined = np.vstack((hidden_reference_filtered, ssr_ids_filtered))
        np.random.shuffle(combined)
        
        # Extract SSR source IDs and attribute IDs separately
        curr_ssr_ids = combined[:, 0].astype(int)
        curr_attribute_ids = combined[:, 2].astype(int)

        """
        # --- set gif path based on current trial ---
        if self.current_trial < len(self.gifs_paths):
            curr_gif_path = self.gifs_paths[self.current_trial]
        else:
            curr_gif_path = None
        """


        if curr_attribute_ids.size > 0:
            atr_id = curr_attribute_ids[0]
            art_sting = self.attributes[atr_id]
        else:
            art_sting = "finish"

        if hidden_reference_filtered.size > 0:
            ref_id = hidden_reference_filtered[0,0]
        else:
            ref_id = np.array([], dtype=int)

        return curr_ssr_ids, art_sting, ref_id

        
        
        


    def write_results(self, values, current_ssr_ids,ref_id):
        trial_dict = {
            'ref_id': ref_id,
            'current_trial': self.current_trial,
            'current_ssr_ids': current_ssr_ids,
            'slider_values': values
        }
        print('Trial: ', trial_dict['current_trial'])
        print('   ref_id: ', ref_id)
        print('   slider values: ', trial_dict['slider_values'])
        print('   ssr ids: ', trial_dict['current_ssr_ids'])
        print(f'{self._result_file_name}_phase{self.phase}_trial{self.current_trial}.mat')
        scyio.savemat(f'{self._result_file_name}_phase{self.phase}'
                      f'_trial{self.current_trial}.mat',
                      trial_dict, appendmat=True)
