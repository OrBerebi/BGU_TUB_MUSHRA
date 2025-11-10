clc
clear
close all

name = "Ref_median.wav";
[sig_in,fs] = audioread(name);
[N,ch] = size(sig_in);
sig_L = sig_in(:,1);
sig_R = sig_in(:,2);

[pathstr, name, ext] = fileparts(name);

name_L = name + "_L" + ext;
name_R = name + "_R" + ext;
audiowrite(name_L,sig_L,fs);
audiowrite(name_R,sig_R,fs);