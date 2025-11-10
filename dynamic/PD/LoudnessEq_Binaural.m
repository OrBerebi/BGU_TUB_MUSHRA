function [eqMultValue, optError, optLoud, orgLoud] = LoudnessEq_Binaural(audioDir, optParam, saveFiles, drawGraph)
% LoudnessEq_Binaural_Dir
%
% Equalizes the loudness of all binaural (stereo) WAV files in a directory
% to match the loudness of the quietest signal.
%
% Input:
%   audioDir  - directory containing the binaural wav files
%   optParam  - optimization step size (e.g. 0.01)
%   saveFiles - flag (1/0) to save equalized versions
%   drawGraph - flag (1/0) to plot before/after loudness values
%
% Output:
%   eqMultValue - scaling factor for each file
%   optError    - loudness matching error
%   optLoud     - loudness after equalization
%   orgLoud     - original loudness before equalization
%
% Adapted by ChatGPT from Zamir Ben-Hur’s LoudnessEqOptimize
% October 2025
%

% --- Get all wav files in directory ---
files = dir(fullfile(audioDir, '*.wav'));
if isempty(files)
    error('No .wav files found in directory: %s', audioDir);
end
numOfFiles = length(files);
disp(['Found ' num2str(numOfFiles) ' WAV files in directory.']);

% --- Read and align all files ---
disp('Reading binaural files...');
for i = 1:numOfFiles
    filePath = fullfile(audioDir, files(i).name);
    [tmp, fs] = audioread(filePath);
    
    if size(tmp,2) ~= 2
        error('All WAV files must be stereo (binaural). Problem file: %s', files(i).name);
    end

    % Store data, pad to max length
    if i == 1
        audioData = tmp;
        maxLen = size(tmp,1);
    else
        maxLen = max(maxLen, size(tmp,1));
        audioData(maxLen,2,i) = 0; % preallocate
        tmp(maxLen,2) = 0;         % pad
        audioData(:,:,i) = tmp;
    end
end

if fs ~= 48e3
    error('All signals must have 48 kHz sample rate!');
end

% --- Compute loudness for all signals ---
disp('Computing loudness...');
loudness = zeros(1, numOfFiles);
for i = 1:numOfFiles
    loudness(i) = LoudnessCalc_ITU(audioData(:,:,i));
end
orgLoud = loudness;

% --- Find quietest signal as reference ---
[loudMin, minInd] = min(loudness);
disp(['Reference (quietest) file: ' files(minInd).name]);

% --- Optimize scaling to match loudness ---
disp('Starting loudness optimization...');
multValue = 0.01:optParam:1;
loud = zeros(length(multValue), numOfFiles);

for i = 1:numOfFiles
    if i == minInd
        continue;
    end
    disp(['Optimizing file ' num2str(i) ' of ' num2str(numOfFiles)]);
    for j = 1:length(multValue)
        if ~mod(j,10), fprintf('|'); end
        scaled = multValue(j) * audioData(:,:,i);
        loud(j,i) = LoudnessCalc_ITU(scaled);
    end
    fprintf('\n');
end

% --- Select optimal values ---
eqMultValue = zeros(1, numOfFiles);
optError = zeros(1, numOfFiles);
optLoud = zeros(1, numOfFiles);

for i = 1:numOfFiles
    if i == minInd
        eqMultValue(i) = 1;
        optError(i) = 0;
        optLoud(i) = loudMin;
    else
        [optError(i), idx] = min(abs(loud(:,i) - loudMin));
        optLoud(i) = loud(idx,i);
        eqMultValue(i) = multValue(idx);
    end
end

% --- Apply scaling ---
for i = 1:numOfFiles
    audioData(:,:,i) = eqMultValue(i) * audioData(:,:,i);
end

% --- Save new files if requested ---
if saveFiles
    disp('Saving equalized files...');
    for i = 1:numOfFiles
        [~, name, ext] = fileparts(files(i).name);
        %newFile = fullfile(audioDir, [name '_eqL' ext]);
        newFile = fullfile(audioDir, [name ext]);
        audiowrite(newFile, audioData(:,:,i), fs);
    end
end

% --- Plot loudness before/after ---
if drawGraph
    figure;
    subplot(1,2,1);
    bar(orgLoud);
    title('Original Loudness');
    xlabel('File Index'); ylabel('Loudness [LU]');
    grid on;

    subplot(1,2,2);
    bar(optLoud);
    title('Equalized Loudness');
    xlabel('File Index'); ylabel('Loudness [LU]');
    grid on;
end

disp('Loudness equalization complete.');

% --- Display summary ---
for i = 1:numOfFiles
    fprintf('%s\tMult: %.3f\tOrg: %.2f\tEq: %.2f\n', ...
        files(i).name, eqMultValue(i), orgLoud(i), optLoud(i));
end

end
