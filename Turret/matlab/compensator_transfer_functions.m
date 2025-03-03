%% Uncompensated Root Locus
% Define the transfer function G(s)
s = tf('s');  % Use tf for the Laplace variable

% Define the open-loop transfer function G(s)
Gsys = 193.95/(s+3.846);

% Plot the root locus of the open-loop transfer function
figure;
rlocus(Gsys);
title('Uncompensated Root Locus');

%% PI-Lead Compensator Setup
% pole for the compensator based on the root locus
p = 4; 

% PI-Lead compensator form: KGc(s) = Kp + Ki/s + Kd * (p / (s + p))

% Choose initial guesses for the gains
Kp = 200;    % Proportional gain
Ki = 150;  % Integral gain
Kd = 0;  % Derivative gain


% Define the compensator transfer function KGc(s)
KGc = Kp + Ki/s + Kd * (s / (s + p))

% Display the compensator transfer function
disp('PI-Lead Compensator Gc(s):');
disp(KGc)


%% Closed-Loop Transfer Functions

% Closed-loop transfer function for output (T_y)
Ty = (KGc * Gsys) / (1 + (KGc * Gsys))

% Closed-loop transfer function for control input (T_u)
Tu = KGc / (1 + (KGc * Gsys));

%% Stepinfo for Settling Time and Overshoot

% Step response for output (T_y)
info_y = stepinfo(Ty);
settling_time_y = info_y.SettlingTime;
overshoot_y = info_y.Overshoot;


disp(['Settling Time (output): ', num2str(settling_time_y)]);
disp(['Overshoot (output): ', num2str(overshoot_y)]);


info_u =stepinfo(Tu)
max_input= info_u.Peak
%% Plot
figure;
step(Ty);  % Plot the step response for the closed-loop system
title('Closed-Loop Step Response');
grid on;
