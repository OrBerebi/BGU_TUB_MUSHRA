function [eqMultValue, optError, optLoud, orgLoud] = LoudnessEqOptimize(BRIRwavFiles,brirPath,StimuliwavFile,optParam,saveFiles,drawGraph)
%
% Optimization of loudness equalization between different signals, equalize
%  the loudness to the minimum loudness signal.
%
% Input: BRIRwavFiles   - cell of names of a BRIR .wav-files on the form: {'name1.wav'; 'name2.wav'}.
%        brirPath       - the path of the brir files
%        StimuliwavFile - name of a stimuli .wav-file on the form: 'name.wav'.
%        optParam       - the parameter for the optimization resolution
%        saveFiles      - flag to save new wav files
%        drawGraph      - flag to show plots
%
% Output: eqMultValue - return a vector of the multiply value that gives the optimize loudness
%         optError    - the optimal error between loudnesses
%         optLoud     - the optimal loudnesses after equalize
%         orgLoud     - the original loudnesses, before equalize
%
% Zamir Ben-Hur
% 30.7.15
%

numOfRIR = length(BRIRwavFiles);

% Reads the audio data
disp('Reading data...')
for i=1:numOfRIR
    [tmp, fs] = audioread([brirPath BRIRwavFiles{i}]);
    % fs_in = fs;
    % fs_target = 48000;
    % tmp = resample(tmp, fs_target, fs_in);
    % fs = fs_target;

    if (i>1) && (size(tmp,1) > size(RIRdata,1))
        RIRdata(end:size(tmp,1),:,:) = 0;
    end
    if (i>1) && (size(tmp,1) < size(RIRdata,1))
        tmp(end:size(RIRdata,1),:) = 0;
    end
    RIRdata(:,:,i) = tmp;
end
[Stimulidata,fs2] = audioread(StimuliwavFile);

% fs_in = fs2;
% fs_target = 48000;
% Stimulidata = resample(Stimulidata, fs_target, fs_in);
% fs2 = fs_target;


% Check the sample rate
if fs~=48e3 | fs2~=48e3
    error('The sample rate must be 48 KHz!')
end

% Convolve the BRIR with the stimuli
RIRdataS = RIRdata(:,1:2,:);
for i=1:numOfRIR
    audioData(:,1,i) = fastConv(RIRdataS(:,1,i),Stimulidata);
    audioData(:,2,i) = fastConv(RIRdataS(:,2,i),Stimulidata);
end

% Compute loudness
loudness = zeros(1,numOfRIR);
for i=1:numOfRIR
    loudness(i) = LoudnessCalc_ITU(audioData(:,:,i));
end
orgLoud = loudness;
[loudMin, minInd] = min(loudness);
RIRdataNoMin = RIRdataS(:,:,[1:minInd-1,minInd+1:end]);

% Optimaize loudness
disp('Starting loudness optimization...')
multValue = 0.01:optParam:1;
loud = zeros(length(multValue),numOfRIR-1);
for i=1:numOfRIR-1
    disp([num2str(i), ' of ',num2str(numOfRIR-1)])
    for j=1:length(multValue)
        if ~mod(j,10)
            fprintf('| ');
        end
        R = multValue(j)*RIRdataNoMin(:,:,i);
        audioDataNew(:,1) = fastConv(R(:,1),Stimulidata);
        audioDataNew(:,2) = fastConv(R(:,2),Stimulidata);
        loud(j,i) = LoudnessCalc_ITU(audioDataNew);
    end
    fprintf('\n\n');
end
loudErr = abs(loud - loudMin);
[optError,Ind] = min(loudErr);
for i=1:length(Ind)
    optLoud(i)=loud(Ind(i),i);
end
optLoud = [optLoud(1:minInd-1),loudMin,optLoud(minInd:end)];
optError = [optError(1:minInd-1),0,optError(minInd:end)];
eqMultValue = multValue(Ind);
eqMultValue = [eqMultValue(1:minInd-1),1,eqMultValue(minInd:end)];

for i=1:numOfRIR
    RIRdata(:,:,i) = eqMultValue(i)*RIRdata(:,:,i);
end

% Save new files
if saveFiles
    disp('Saving files...')
    for i=1:numOfRIR
        newFileName = [BRIRwavFiles{i}(1:end-4), '_eqL.wav'];
        wavwrite(RIRdata(:,:,i), fs, 16, newFileName);
    end
end

% Plots
if drawGraph
    nfft = 2^10;
    fax=linspace(0,fs/2,nfft); % frequency range
    for i=1:numOfRIR
        S(i,:) =  fft(RIRdataS(:,1,i),2*nfft);
        p(i,:) = db(abs(S(i,1:end/2)));
        
        Seq(i,:) =  fft(RIRdata(:,1,i),2*nfft);
        peq(i,:) = db(abs(Seq(i,1:end/2)));
    end
    
    FS = 24;
    FSL = 22;
    LW = 4;
    gr=[0.7 0.7 0.7];
    bl=[0 0 0];
    figure;
    for i = 1:numOfRIR
        subplot(ceil(sqrt(numOfRIR)),ceil(sqrt(numOfRIR)),i)
        semilogx(fax,p(i,:),'-','LineWidth',LW,'color',bl); hold on
        semilogx(fax,peq(i,:),'--','LineWidth',LW,'color',gr); hold off
        grid on;
        h=legend([BRIRwavFiles{i}(1:6),'  '; ...
            BRIRwavFiles{i}(1:6), 'eq'],'Location','Southwest');
        set(h,'FontSize',FSL);
        
        ylim([-60 30]);
        xlim([0 20e3]);
        
        xlabel('Frequency (Hz)','Interpreter','Latex','FontSize',FS);
        ylabel('Magnitude (dB)','Interpreter','Latex','FontSize',FS);
        set(gca,'FontSize',FS);
    end
    
    figure;
    subplot(1,2,1)
    semilogx(fax,p,'-','LineWidth',LW);
    grid on;
    for i=1:numOfRIR
        leg(i,:) = BRIRwavFiles{i}(1:6);
    end
    h=legend(leg,'Location','Southwest');
    set(h,'FontSize',FSL);
    
    ylim([-60 30]);
    xlim([0 20e3]);
    
    xlabel('Frequency (Hz)','Interpreter','Latex','FontSize',FS);
    ylabel('Magnitude (dB)','Interpreter','Latex','FontSize',FS);
    title('Before equalize loudness')
    set(gca,'FontSize',FS);
    
    subplot(1,2,2)
    semilogx(fax,peq,'-','LineWidth',LW);
    grid on;
    h=legend([leg,repmat('eq',numOfRIR,1)],'Location','Southwest');
    set(h,'FontSize',FSL);
    
    ylim([-60 30]);
    xlim([0 20e3]);
    
    xlabel('Frequency (Hz)','Interpreter','Latex','FontSize',FS);
    ylabel('Magnitude (dB)','Interpreter','Latex','FontSize',FS);
    title('After equalize loudness')
    set(gca,'FontSize',FS);
end
end


function ab = fastConv(a,b)
% Internal use only
NFFT = size(a,1)+size(b,1)-1;
A    = fft(a,NFFT);
B    = fft(b,NFFT);
AB   = A.*B;
ab   = ifft(AB);
end