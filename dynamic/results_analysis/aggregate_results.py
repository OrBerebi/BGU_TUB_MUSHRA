import glob
import re
import csv
import scipy.io
import numpy as np
import os
from collections import defaultdict

def get_mat_value(mat_variable):
    """
    Helper function to extract a clean Python value from a
    scipy.io.loadmat-loaded variable, which are often
    nested in arrays.
    """
    if isinstance(mat_variable, np.ndarray):
        # Handle empty arrays (e.g. empty optional text fields)
        if mat_variable.size == 0:
            return ""
        
        # Handle strings
        if mat_variable.dtype.kind in {'U', 'S'}:
            # If it's a scalar string wrapped in array
            if mat_variable.size == 1:
                val = mat_variable.item()
                # Sometimes scipy returns it as a string, sometimes as a generic object
                return str(val) if val is not None else ""
            # If it's an array of characters
            return "".join(str(c) for c in mat_variable.flatten())
            
        # Handle scalar numbers
        if mat_variable.size == 1:
            return mat_variable.item()
            
        # Handle lists/arrays
        return mat_variable.flatten().tolist()
    
    return mat_variable

def sort_key_for_trial_cols(col_name):
    """
    A custom sort key function to properly sort headers like
    'trial_1_id_9' and 'trial_10_id_7'.
    It sorts by trial number first, then by id number.
    """
    match = re.search(r'trial_(\d+)_id_(\d+)', col_name)
    if match:
        trial_num = int(match.group(1))
        id_num = int(match.group(2))
        # Return a tuple for sorting (sort by trial, then by id)
        return (trial_num, id_num)
    else:
        # If it doesn't match, put it at the end
        return (float('inf'), col_name)

def aggregate_mat_results(results_folder, output_filename='aggregated_results.csv'):
    """
    Finds 'results_subj*.mat' files, aggregates them by subject,
    and writes a CSV file with paired (id, rating) columns.
    """
    print(f"Starting aggregation in folder: {results_folder}")
    
    search_path = os.path.join(results_folder, 'results_subj*.mat')
    all_mat_files = glob.glob(search_path)
    
    if not all_mat_files:
        print(f"Warning: No 'results_subj*.mat' files found in {results_folder}")
        return

    subjects_files = defaultdict(lambda: {'info': None, 'trials': []})
    
    info_pattern = re.compile(r'results_subj(\d+)\.mat$')
    trial_pattern = re.compile(r'results_subj(\d+)_phase\d+_trial\d+\.mat$')

    for f in all_mat_files:
        filename = os.path.basename(f)
        info_match = info_pattern.search(filename)
        trial_match = trial_pattern.search(filename)
        
        if info_match and not trial_match:
            subj_id = info_match.group(1)
            subjects_files[subj_id]['info'] = f
        elif trial_match:
            subj_id = trial_match.group(1)
            subjects_files[subj_id]['trials'].append(f)

    print(f"Found data for {len(subjects_files)} subjects.")

    all_data_rows = []
    all_fieldnames = set()
    
    # --- UPDATED FIELD LIST ---
    # This matches the keys we created in main_window.py -> finish_login()
    static_info_fields = [
        'subject_id', 
        'participant_id', 
        'subject_code', 
        'gender', 
        'year_born', 
        'native_language', 
        'german_proficiency', 
        'education', 
        'hearing_impairment', 
        'acoustics_profession', 
        'acoustics_years', 
        'music_profession', 
        'music_years', 
        'musical_instrument', 
        'instrument_years', 
        'prior_experiment', 
        'num_studies', 
        'listening_hours_daily', 
        'matriculation_number'
    ]
    all_fieldnames.update(static_info_fields)

    for subj_id in sorted(subjects_files.keys(), key=int):
        print(f"Processing subject {subj_id}...")
        row = {'subject_id': subj_id}
        file_group = subjects_files[subj_id]
        
        if file_group['info']:
            try:
                data = scipy.io.loadmat(file_group['info'])
                
                # Check if 'participant_infos' exists
                if 'participant_infos' in data:
                    # Depending on how it was saved, it might be a struct array
                    # Extract the structured array
                    infos_struct = data['participant_infos']
                    
                    # If it's 2D [[(values)]], get to the void scalar
                    if infos_struct.shape == (1, 1):
                        infos = infos_struct[0, 0]
                        
                        # Check which fields from our list exist in the .mat file
                        for field in static_info_fields:
                            # skip subject_id as it comes from filename
                            if field == 'subject_id': 
                                continue
                                
                            # Numpy structured arrays access fields by name
                            if field in infos.dtype.names:
                                raw_val = infos[field]
                                row[field] = get_mat_value(raw_val)
                            else:
                                # If field is missing in .mat (e.g. old file), leave blank
                                row[field] = ""
                    else:
                        print(f"  Warning: 'participant_infos' has unexpected shape {infos_struct.shape}")
                else:
                    print(f"  Warning: 'participant_infos' key not found in {file_group['info']}")

            except Exception as e:
                print(f"  ERROR: Could not read info file {file_group['info']}: {e}")
        
        # Process Trial Files
        sorted_trials = sorted(
            file_group['trials'], 
            key=lambda f: int(re.search(r'_trial(\d+)\.mat', os.path.basename(f)).group(1))
        )
        
        for trial_file in sorted_trials:
            try:
                trial_num_match = re.search(r'_trial(\d+)\.mat', os.path.basename(trial_file))
                if not trial_num_match:
                    continue
                
                trial_num = trial_num_match.group(1)
                t_data = scipy.io.loadmat(trial_file)
                
                slider_vals = get_mat_value(t_data['slider_values'])
                ssr_ids = get_mat_value(t_data['current_ssr_ids'])

                if not isinstance(slider_vals, list):
                    slider_vals = [slider_vals]
                if not isinstance(ssr_ids, list):
                    ssr_ids = [ssr_ids]

                if len(slider_vals) != len(ssr_ids):
                    print(f"  Warning: Mismatch in trial {trial_num}. Skipping.")
                    continue
                
                paired_data = zip(ssr_ids, slider_vals)
                sorted_pairs = sorted(paired_data, key=lambda pair: pair[0])

                for ssr_id, slider_val in sorted_pairs:
                    key = f'trial_{trial_num}_id_{int(ssr_id)}'
                    row[key] = slider_val
                    all_fieldnames.add(key)
                                
            except Exception as e:
                print(f"  ERROR: Could not read trial file {trial_file}: {e}")
        
        all_data_rows.append(row)

    if not all_data_rows:
        print("No data processed. Exiting.")
        return

    # Sort dynamic trial columns
    dynamic_fields = sorted(
        [f for f in all_fieldnames if f not in static_info_fields],
        key=sort_key_for_trial_cols
    )
    final_headers = static_info_fields + dynamic_fields

    try:
        with open(output_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=final_headers, restval='')
            writer.writeheader()
            writer.writerows(all_data_rows)
        print(f"\nSuccess! Aggregated data written to {output_filename}")
    except Exception as e:
        print(f"\nERROR: Could not write CSV file: {e}")

if __name__ == "__main__":
    path_to_data = '../bgu_results/results/' 
    aggregate_mat_results(path_to_data, output_filename='aggregated_results.csv')