% Data (already smoothed and time array defined)
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

% Select the data for analysis (from index 23 to 53)
time_array_plot = time_array(23:53);
x_values_plot = x_values(23:53);
y_values_plot = y_values(23:53);

% Estimate the steady-state gain K (final value of y / final value of x)
K = y_values_plot(end) / x_values_plot(end); % Assume steady-state values are reached
disp(['Estimated Steady-State Gain (K): ', num2str(K)]);

% Estimate the time constant Ts by fitting a first-order model to the data
% First-order model: y(t) = K * (1 - exp(-t/Ts))

% Define the objective function for curve fitting
first_order_model = @(params, t) params(1) * (1 - exp(-t / params(2))); % K * (1 - exp(-t/Ts))
initial_guess = [K, 1]; % Initial guess for K and Ts

% Fit the model to the data (y_values vs time_array)
opts = fitoptions('Method', 'NonlinearLeastSquares', 'StartPoint', initial_guess);
ft = fittype(first_order_model, 'options', opts);
fit_result = fit(time_array_plot(:), y_values_plot(:), ft);

% Extract the estimated parameters
K_estimated = fit_result(1); % Estimated gain
Ts_estimated = fit_result(2); % Estimated time constant

% Display the results
disp(['Estimated Gain (K): ', num2str(K_estimated)]);
disp(['Estimated Time Constant (Ts): ', num2str(Ts_estimated)]);

% Plot the data and the fitted curve
figure;
plot(time_array_plot, y_values_plot, 'o', 'DisplayName', 'Measured Data');
hold on;
plot(time_array_plot, first_order_model([K_estimated, Ts_estimated], time_array_plot), '-', 'DisplayName', 'Fitted First-Order Model');
xlabel('Time');
ylabel('Output (y)');
title('First-Order System Estimation');
legend;
grid on;

