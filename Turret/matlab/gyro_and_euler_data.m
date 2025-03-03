% Define the time array and the data for x and y
time_array = linspace(0, 5.3, 53);
x_values = [0.0625, 0.0625, 0.0625, -0.0625, -0.125, 0.0625, 0.0, 0.0625, ...
            0.0625, 0.1875, 0.1875, 0.1875, -0.25, -0.0625, 0.125, -0.0625, 0.0, ...
            0.0, -0.125, 0.0625, 0.0625, 0.0, 0.125, 0.0625, -0.0625, 0.0, ...
            0.0625, 0.0625, 41.375, 50.3125, 44.625, 53.5625, 51.125, 49.625, ...
            50.25, 51.625, 51.3125, 51.75, 49.75, 50.125, 50.5, 50.6875, 50.8125, ...
            51.5625, 50.875, 51.1875, 51.0625, 50.4375, 50.625, 50.5, 51.3125, ...
            48.625, 50.5];
y_values = [-0.25, -0.125, -0.3125, 0.0, -0.25, -0.0625, 0.0, 0.0625, 0.0625, ...
            -0.0625, -0.125, -0.0625, 0.0625, 0.0625, -0.0625, -0.125, 0.125, ...
            0.125, -0.0625, 0.0, -0.0625, 0.0625, 0.0625, 0.0, 0.0625, 0.125, ...
            -9.9375, 2.6875, 0.3125, 0.1875, -0.4375, 0.0, 0.1875, -0.0625, ...
            0.25, 0.375, -0.25, 0.0, 0.0, -0.125, 0.0, -0.125, -0.0625, ...
            -0.1875, 0.0, -0.125, -0.125, -0.0625, -0.25, -0.3125, 0.4375, ...
            -0.25, 0.375];

% Smooth the data (example: using a moving average filter for smoothing)
windowSize = 5; % Adjust for different smoothness levels
x_values_smooth = movmean(x_values, windowSize);
y_values_smooth = movmean(y_values, windowSize);

% Select the relevant data for fitting (from 23 to 53)
time_array_plot = time_array(23:53);
x_values_plot = x_values_smooth(23:53);
y_values_plot = y_values_smooth(23:53);

% Plot the smoothed data
figure;
plot(time_array_plot, x_values_plot, '-o');
hold on;


% Adding labels and title
xlabel('Time');
ylabel('Value');
title('Yaw rate');
legend;
grid on;

% Fit a first-order transfer function model to the data
% Define the first-order system model: G(s) = K / (tau*s + 1)
% This is a simple example using system identification toolbox, you could also use
% optimization to fit the model.

% Create data for system identification (using time and output)
data = iddata(y_values_plot', x_values_plot', time_array_plot(2)-time_array_plot(1)); % Assuming sample time is constant

% Estimate the transfer function using system identification
sys = tfest(data, 1); % First-order system estimation

% Display the transfer function
disp('Estimated Transfer Function:');
disp(sys);

% Plot the estimated transfer function response
figure;
bode(sys);
title('Bode Plot of Estimated Transfer Function');
grid on;

%% Tau

Tau=0.26
a= 3.846
