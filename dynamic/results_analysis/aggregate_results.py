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
        if mat_variable.dtype.kind == 'U':
            return str(mat_variable[0])
        if mat_variable.size == 1:
            return mat_variable.item()
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

def aggregate_mat_results(results_folder, output_filename='aggregated_results_v2.csv'):
    """
    Finds 'results_subj*.mat' files, aggregates them by subject,
    and writes a CSV file with paired (id, rating) columns.
    
    Args:
        results_folder (str): The path to the directory containing the .mat files.
        output_filename (str): The name for the output CSV file.
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
    
    static_info_fields = [
        'subject_id', 'participant_id', 'age', 'gender',
        'ListeningExperimentExperience', 'BinauralExperience',
        'HealthStatus', 'HearingProblems'
    ]
    all_fieldnames.update(static_info_fields)

    for subj_id in sorted(subjects_files.keys(), key=int):
        print(f"Processing subject {subj_id}...")
        row = {'subject_id': subj_id}
        file_group = subjects_files[subj_id]
        
        if file_group['info']:
            try:
                data = scipy.io.loadmat(file_group['info'])
                infos = data['participant_infos'][0, 0]
                
                for field in infos.dtype.names:
                    if field in static_info_fields:
                        row[field] = get_mat_value(infos[field])
                        
            except Exception as e:
                print(f"  ERROR: Could not read info file {file_group['info']}: {e}")
        
        sorted_trials = sorted(
            file_group['trials'], 
            key=lambda f: int(re.search(r'_trial(\d+)\.mat', os.path.basename(f)).group(1))
        )
        
        for trial_file in sorted_trials:
            try:
                trial_num_match = re.search(r'_trial(\d+)\.mat', os.path.basename(trial_file))
                if not trial_num_match:
                    print(f"  Warning: Skipping file with unexpected name: {trial_file}")
                    continue
                
                trial_num = trial_num_match.group(1)
                t_data = scipy.io.loadmat(trial_file)
                
                
                # 1. Get the values and IDs
                slider_vals = get_mat_value(t_data['slider_values'])
                ssr_ids = get_mat_value(t_data['current_ssr_ids'])

                # 2. Ensure they are lists, even if single values
                if not isinstance(slider_vals, list):
                    slider_vals = [slider_vals]
                if not isinstance(ssr_ids, list):
                    ssr_ids = [ssr_ids]

                # 3. Check for mismatches
                if len(slider_vals) != len(ssr_ids):
                    print(f"  Warning: Mismatch in slider_values ({len(slider_vals)}) "
                          f"and ssr_ids ({len(ssr_ids)}) in file {trial_file}. Skipping trial.")
                    continue
                
                # 4. Zip, sort by ID, and add to row
                #    We cast ssr_id to int to get clean headers like '..._id_7' not '..._id_7.0'
                
                # Create (id, value) pairs
                paired_data = zip(ssr_ids, slider_vals)
                
                # Sort pairs by the ssr_id (the first item in the tuple)
                sorted_pairs = sorted(paired_data, key=lambda pair: pair[0])

                # 5. Add to the row dictionary
                for ssr_id, slider_val in sorted_pairs:
                    key = f'trial_{trial_num}_id_{int(ssr_id)}'
                    row[key] = slider_val
                    all_fieldnames.add(key) # Add new header to our master set
                                
            except Exception as e:
                print(f"  ERROR: Could not read trial file {trial_file}: {e}")
        
        all_data_rows.append(row)

    if not all_data_rows:
        print("No data processed. Exiting.")
        return

    # Use the custom sort key to order dynamic fields
    dynamic_fields = sorted(
        [f for f in all_fieldnames if f not in static_info_fields],
        key=sort_key_for_trial_cols
    )
    final_headers = static_info_fields + dynamic_fields

    try:
        with open(output_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=final_headers, restval='NA')
            writer.writeheader()
            writer.writerows(all_data_rows)
        print(f"\nSuccess! Aggregated data written to {output_filename}")
    except Exception as e:
        print(f"\nERROR: Could not write CSV file: {e}")

# --- To run the script ---
if __name__ == "__main__":
    
    # Use the current directory
    path_to_data = '../bgu_results/results/' 
    
    print(f"--- Running aggregation for folder: {os.path.abspath(path_to_data)} ---")
    aggregate_mat_results(path_to_data, output_filename='aggregated_results.csv')