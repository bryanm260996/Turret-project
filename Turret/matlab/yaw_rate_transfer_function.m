% Define the Laplace variable
s = zpk('s');

% Define the transfer function
Gsys_yaw = 314.96 / (s + 5.55);

% Generate time vector
yaw_times = linspace(0, 2.8, 28);

% Simulate step response of the system
[y_model, t_model] = step(Gsys_yaw, yaw_times);



% Define the time array and the data for x and y



time_array = linspace(0, 2.8, 28);
x_values = [ 0.0, ...
            0.0625, 0.0625, 41.375, 50.3125, 44.625, 53.5625, 51.125, 49.625, ...
            50.25, 51.625, 51.3125, 51.75, 49.75, 50.125, 50.5, 50.6875, 50.8125, ...
            51.5625, 50.875, 51.1875, 51.0625, 50.4375, 50.625, 50.5, 51.3125, ...
            48.625, 50.5];
%%

% Smooth the data (example: using a moving average filter for smoothing)
windowSize = 5; % Adjust for different smoothness levels
x_values_smooth = movmean(x_values, windowSize);
y_values_smooth = movmean(y_values, windowSize);

% Select the relevant data for fitting (from 23 to 53)


% Plot the smoothed data
figure;
plot(time_array, x_values, '-o');
hold on;
plot(t_model, y_model)


% Adding labels and title
xlabel('Time');
ylabel('Value');
title('Yaw rate');
legend('Experimental', 'Gsys.yaw')
grid on;




%% Tau

Tau=0.26
a= 3.846
