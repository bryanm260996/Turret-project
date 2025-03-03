clc; clear; close all;

% Define the original transfer function
G = tf(193, [1 3.846]);

% Define the PI-Lead Controller parameters
Kp = 0.136;
z = 0.77;
lead_zero = 5.13;
lead_pole = 51.3;

% Create the PI-Lead controller
C = Kp * tf([1 z], [1 0]) * tf([1 lead_zero], [1 lead_pole]);

% Open-loop transfer function of the compensated system
L = C * G;

% Closed-loop transfer function of the compensated system
T_compensated = feedback(L, 1);

% Closed-loop transfer function of the original system (unity feedback)
T_original = feedback(G, 1);

% Step response comparison
figure;
step(T_original, 'b', T_compensated, 'r', 5);
grid on;
title('Step Response Comparison');
legend('Original System', 'PI-Lead Compensated System');
xlabel('Time (s)'); ylabel('Amplitude');

% Performance Metrics
S_original = stepinfo(T_original);
S_compensated = stepinfo(T_compensated);

% Display performance metrics
disp('Original System Performance:');
disp(S_original);

disp('Compensated System Performance:');
disp(S_compensated);