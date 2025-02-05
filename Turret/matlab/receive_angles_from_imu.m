% Create serial port connection
turret_angles = serialport('COM6', 9600);

rx_msg = readline(turret_angles);
dat_str_array = split(rx_msg,',');
yaw = str2double(dat_str_array(1));
pitch = str2double(dat_str_array(2));

fprintf(yaw,pitch)

