%% Proposed Model
clc; clear all;close all;
% Parameters
n=0.01;              %per minute
Hb=5.8/(10^6);
tD =40;
AG = 0.8;
% G0 = 50;
Gb = 90;
% Ib =565;
% EGP0=0.8471; 
VG = 0.16 *70;
KP2 = .0007;
KA1= 0.006;
KA2=0.06;
KA3= 0.03;
S1T=0.00512;
S1D=.00082;
SIE=.052;
KB1=KA1*S1T;
KB2=KA2*S1D;
KB3=SIE*KA3;
% KP2=0.0035;
 VG = 0.16*70;
% UII=1.09; %% 18*(0.0097/VG) to convert into mg/dl/min
K12=0.066;
Ke=0.138;
VI=0.12*70;
TmaxI=55;
u0=12.9127;
s10=u0*TmaxI;
s20=s10;
% ubasal = 10.9127;
%  UI0=s20/TmaxI;
I0 = (u0)/(70*.01656);
% I0=UI0/(Ke*VI);
% x10=(KB1/KA1)*I0;
% x20=(KB2/KA1)*I0;
% x30=(KB3/KA3)*I0;
% x10 = (.30898*u0)/70;
% x20= (.04951*u0)/70;
% x30 = (3.2206*u0)/70;
x10 = (.30898*u0)/70;
x20= (.04951*u0)/70;
x30 = (3.2206*u0)/70;
G10 = 90;
% G20 = (18/VG)*((-0.2292*70)+(4.5307*u0));
 G20 = 70;
% G20= 68.23;
Ggnb = .495 ;        %mg/dL/min
K6GP = 0.034;        %/min