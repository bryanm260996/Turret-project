% Define the Laplace variable
s = zpk('s');

% Define the transfer function
Gsys_pitch = 314.96 / (s + 5.55);

% Generate time vector
pitch_times = linspace(0, 1.9, 19);

% Simulate step response of the system
[y_model, t_model] = step(Gsys_pitch, pitch_times);

% Given experimental data
y_exp = [ 0.0, 1.8125, 55.6875, 55.625, ...
         60.0625, 57.0625, 56.5, 55.0, 57.4375, 57.6875, 57.4375, 55.0625, ...
         54.8125, 56.375, 57.1875, 56.4375, 56.75, 56.1875, 56.25]; 

% Plot results
figure;
plot(pitch_times, y_exp, 'ro-', 'LineWidth', 1.5); % Experimental data (red circles)
hold on;
plot(t_model, y_model, 'b-', 'LineWidth', 1.5); % Model step response (blue line)
xlabel('Time (s)');
ylabel('Pitch Response');
legend('Experimental Data', 'Model Step Response');
title('Comparison of Experimental and Model Response');
grid on;
