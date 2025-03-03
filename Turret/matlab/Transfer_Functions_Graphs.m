% Define the transfer functions G(s)
s = zpk('s');
Gsys_yaw = 0.85 / (s + 3.846);
Gsys_pitch = 1.182 / (s + 5.55);

% Define simulation time
t = 0:0.01:4; % Time vector from 0 to 4 seconds with 0.01s step size

% Create figure for Step Response
figure;
subplot(2,1,1);
step(Gsys_yaw, t); % Step response for 4 seconds
title('Step Response of Gsys\_yaw (4s)');
grid on;

subplot(2,1,2);
step(Gsys_pitch, t); % Step response for 4 seconds
title('Step Response of Gsys\_pitch (4s)');
grid on;
