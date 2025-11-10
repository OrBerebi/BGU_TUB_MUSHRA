% script to create ASD file for BRS renderer

clear
close
clc

restoredefaultpath
root_path = '/Users/orberebi/Documents/GitHub/MUSHRA_2025/SSR_scene/';
addpath(genpath(root_path));

brs = true; % if true generate asd with stimulus, else, generate asd with port

asdFile='test_test.asd';
asdPath = root_path;
masterVolume = -5;
chVolumeBase = 0;
gridWidth = 4;                          % 5 entries on grid width
xMin = -2;
yMin = 1;
gridDelta = 1;

%cd(asdPath);
[stimFile, stimPath]= uigetfile('*.wav', 'Select an anechoic stimulus');
[brirFiles, brirPath] = uigetfile('*.wav', 'Select BRIRs','MultiSelect','on');
%% Equalize loudness
disp('Start equalize loudness...');
optParam = 0.01;
[eqMultValue, optError, optLoud, orgLoud] = LoudnessEqOptimize(brirFiles,brirPath,[stimPath,stimFile],optParam,false,false);
chVolume = chVolumeBase + db(eqMultValue./max(eqMultValue));

%%
fid = fopen([asdPath,asdFile],'w');
% Write the header
fprintf(fid, '<?xml version="1.0" encoding="utf-8"?>\n');
fprintf(fid, '<asdf\n xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n xsi:noNamespaceSchemaLocation="asdf.xsd"\n version="0.1">\n');
fprintf(fid, '\n\n');
fprintf(fid, '<header>\n <name>Example for BRS rendering</name>\n<description>\n This example is best replayed with the BRS renderer.\n </description>\n</header>\n\n\n');

% Scene setup
fprintf(fid,'<scene_setup>\n<volume>%d </volume>\n\n\n',masterVolume);


x = xMin;
y = yMin;

for nn=1:size(brirFiles,2)
    [p1, p2, p3] = fileparts(brirFiles{nn});
    fprintf(fid, '<source name="%s" properties_file="%s" volume="%d" mute="true" id="ID_%d">\n',p2(6:end),strcat(brirPath,brirFiles{nn}),chVolume(nn), nn);
    if brs
        fprintf(fid, '      <file>%s</file>\n',strcat(stimPath,stimFile));
    else
        fprintf(fid, '      <port>1</port>\n');
    end
    fprintf(fid, '      <position x="%.2f" y="%.2f" fixed="true"/>\n',x,y);
    fprintf(fid, '</source>\n\n\n');
    
    x=x+gridDelta;
    
    if x >= (gridWidth/2)*gridDelta
        y = y+gridDelta;
        x = xMin;
    end
end


% Footer
fprintf(fid,'</scene_setup>\n</asdf>\n');

fclose(fid);