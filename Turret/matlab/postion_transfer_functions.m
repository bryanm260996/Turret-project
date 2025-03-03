% Define the transfer functions G(s)
s = zpk('s');
Gsys_yaw_position = 0.85 / (s^2 + 3.846*s);
Gsys_pitch_position = 1.182 / (s^2 + 5.55*s);

% Define simulation time
t = 0:0.01:4; % Time vector from 0 to 4 seconds with 0.01s step size

% Create figure for Step Response
figure;
subplot(2,1,1);
step(Gsys_yaw_position, t); % Step response for 4 seconds
title('Step Response of Gsys\_yaw position (4s)');
grid on;

subplot(2,1,2);
step(Gsys_pitch_position, t); % Step response for 4 seconds
title('Step Response of Gsys\_pitch position (4s)');
grid on;

%going from 0 to 1, 1 being 180 degrees 
