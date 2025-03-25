function soccer_corner_kick_simulation_modified
    % This script simulates a soccer ball trajectory from a corner kick
    % using a simplified model that includes drag and Magnus forces.
    %
    % References:
    % - "Study of soccer ball flight trajectory" (MATEC Web Conf. 145, 01002, 2018).
    % - Cook, B.G. and Goff, J.E., 2006. Parameter space for successful soccer
    %   kicks. European journal of physics, 27(4), p.865.
    %
    % The simulation starts from a corner position and shows the trajectory
    % with detailed football pitch visualization and multiple camera angles.
    
    close all; clear; clc;
    
    %% Parameters
    % Ball properties
    m = 0.45;          % ball mass (kg)
    R = 0.11;          % ball radius (m)
    A = pi * R^2;      % cross-sectional area (m^2)
    g = 9.81;          % gravitational acceleration (m/s^2)
    rho = 1.2;         % air density (kg/m^3)
    
    % Aerodynamic coefficients (typical for spinning soccer ball)
    C_D = 0.33;        % Drag coefficient
    C_L = 0.30;        % Lift (Magnus) coefficient
    
    %% Field parameters
    % Field dimensions (standard)
    field_length = 105; % meters
    field_width = 68;   % meters
    
    % Goal dimensions
    goal_width = 7.32;  % meters
    goal_height = 2.44; % meters
    goal_depth = 2;     % meters
    
    % Penalty area dimensions
    penalty_area_width = 40.2; % meters
    penalty_area_length = 16.5; % meters
    
    % Goal area dimensions
    goal_area_width = 18.3;  % meters
    goal_area_length = 5.5;  % meters
    
    % Penalty mark
    penalty_mark_distance_from_goal = 11; % meters
    
    % Goal position from corner position
    goal_lon_pos = field_length;    % Goal is at the opposite end (x-direction)
    goal_lat_pos = 0;               % Center of the field width (y-direction)
    
    %% Initial conditions for corner kick
    % Ball position [x y z]
    ball_position = [0, -field_width/2, 0];  % Corner position, on the ground
    
    % Ball velocity parameters
    ball_speed = 29.54;     % initial speed (m/s)
    theta = 17.74;          % elevation angle (degrees)
    phi = 15.71;            % horizontal angle (degrees)
    
    % Ball initial velocity components x, y and z
    % For corner kick: need to adjust component calculation to aim toward goal
    % The kick should primarily go in the +y direction (inward) with a small +x component
    vy = ball_speed * cosd(theta) * cosd(phi);    % Primary direction (inward from corner)
    vx = ball_speed * cosd(theta) * sind(phi);    % Secondary direction (slightly forward)
    vz = ball_speed * sind(theta);
    
    % Ball velocity array
    ball_velocity = [vx, vy, vz];
    
    % Angular velocity (spin) - mainly around z-axis for corner kick
    % Negative spin around z-axis creates curve toward goal (inswinger)
    omega = [0; 0; -97.88];  % rad/s (negative for inward curve)
    
    % Initial conditions
    states0 = [ball_position, ball_velocity];
    
    %% Time and video settings
    playback_speed = 2;             % Speed of playback
    tF = 7;                           % Final time [s]
    fR = 30/playback_speed;           % Frame rate [fps]
    dt = 1/fR;                        % Time resolution [s]
    time = linspace(0, tF, tF*fR);    % Time [s]
    
    %% Simulation
    % Event function to stop if ball hits ground or goes beyond field
    options = odeset('Events', @(t,y) ball_floor_or_end(t,y,field_length), 'RelTol', 1e-6);
    
    % Solve the ODE
    [tout, yout] = ode45(@(t,y) ball_dynamics(t,y,m,A,rho,C_D,C_L,g,omega), time, states0, options);
    
    % Retrieving states
    x = yout(:,1);
    y = yout(:,2);
    z = yout(:,3);
    dx = yout(:,4);
    dy = yout(:,5);
    dz = yout(:,6);
    
    %% Animation
    figure
    % set(gcf, 'Position', [50 50 1280 720])  % YouTube: 720p
    % set(gcf, 'Position', [50 50 854 480])   % YouTube: 480p
    set(gcf, 'Position', [50 50 640 640])     % Social
    
    % Create and open video writer object
    % Make sure directory exists for output video
    try
        v = VideoWriter('corner_kick.mp4', 'MPEG-4');
        v.Quality = 100;
        v.FrameRate = fR;  % Set the frame rate explicitly
        open(v);
        videoWriterEnabled = true;
    catch ME
        warning('Could not create video writer. Video will not be saved.');
        fprintf('Error: %s\n', ME.message);
        videoWriterEnabled = false;
    end
    
    for i = 1:length(tout)
        % Main view (perspective view)
        subplot(3, 3, 1:6);
        cla
        hold on; grid on; axis equal
        set(gca, 'FontName', 'Verdana', 'FontSize', 12)
        plot_field_3d([-100, -50, 150], 'full')
        plot3(x(1:i), y(1:i), z(1:i), 'r', 'LineWidth', 2)
        plot3(x(i), y(i), z(i), 'bo', 'MarkerFaceColor', 'b', 'MarkerSize', 4)
        xlabel('x [m]')
        ylabel('y [m]')
        zlabel('z [m]')
        title(strcat('Corner Kick - Time=', num2str(tout(i), '%.3f'), ' s (Playback speed=', num2str(playback_speed), ')'))
        
        % Top view (bird's eye view)
        subplot(3, 3, 7:8);
        cla
        hold on; grid on
        set(gca, 'FontName', 'Verdana', 'FontSize', 12)
        
        % Draw simple field outline for top view
        rectangle('Position', [0, -field_width/2, field_length, field_width], 'EdgeColor', 'k', 'LineWidth', 1);
        
        % Draw center line
        line([field_length/2, field_length/2], [-field_width/2, field_width/2], 'Color', 'k', 'LineWidth', 1);
        
        % Draw center circle
        th = 0:pi/50:2*pi;
        xunit = 9.15 * cos(th) + field_length/2;
        yunit = 9.15 * sin(th);
        plot(xunit, yunit, 'k', 'LineWidth', 1);
        
        % Draw penalty areas
        rectangle('Position', [0, -penalty_area_width/2, penalty_area_length, penalty_area_width], 'EdgeColor', 'k', 'LineWidth', 1);
        rectangle('Position', [field_length-penalty_area_length, -penalty_area_width/2, penalty_area_length, penalty_area_width], 'EdgeColor', 'k', 'LineWidth', 1);
        
        % Draw goals
        rectangle('Position', [-1, -goal_width/2, 1, goal_width], 'EdgeColor', 'r', 'LineWidth', 2);
        rectangle('Position', [field_length, -goal_width/2, 1, goal_width], 'EdgeColor', 'b', 'LineWidth', 2);
        
        % Mark corner kick position
        plot(0, -field_width/2, 'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 5);
        
        % Plot ball trajectory (2D projection)
        plot(x(1:i), y(1:i), 'r', 'LineWidth', 2);
        plot(x(i), y(i), 'bo', 'MarkerFaceColor', 'b', 'MarkerSize', 4);
        
        axis equal
        xlim([-5, field_length+5]);
        ylim([-field_width/2-5, field_width/2+5]);
        xlabel('x [m]')
        ylabel('y [m]')
        title('Top View')
        
        % Goal view (looking from behind the red goal)
        subplot(3, 3, 9);
        cla
        hold on; grid on
        set(gca, 'FontName', 'Verdana', 'FontSize', 12)
        
        % Find trajectory points that are close to the left goal (red goal)
        goal_region_mask = x < 30;
        
        % Draw goal outline for left goal (red)
        rectangle('Position', [-goal_width/2, 0, goal_width, goal_height], 'EdgeColor', 'r', 'LineWidth', 2);
        
        % Plot trajectory points if any are in the goal region
        if any(goal_region_mask)
            % Plot only points that are in the goal region
            y_goal = y(goal_region_mask);
            z_goal = z(goal_region_mask);
            
            % Plot trajectory in goal view (y-z projection)
            plot(y_goal, z_goal, 'r', 'LineWidth', 2);
            
            % Plot current ball position if it's in goal region
            if goal_region_mask(i)
                plot(y(i), z(i), 'bo', 'MarkerFaceColor', 'b', 'MarkerSize', 4);
            end
        end
        
        % Set axis limits for goal view
        axis equal
        xlim([-goal_width/2-2, goal_width/2+2]);
        ylim([0, goal_height+2]);
        xlabel('y [m]')
        ylabel('z [m]')
        title('Goal View')
        
        % Write frame to video
        frame = getframe(gcf);
        if videoWriterEnabled
            try
                writeVideo(v, frame);
            catch
                warning('Could not write video frame.');
                videoWriterEnabled = false;
            end
        end
    end
    % Close video writer
    if exist('v', 'var') && videoWriterEnabled
        try
            close(v);
        catch
            warning('Could not close video writer properly.');
        end
    end
    
    %% Helper functions
    function plot_field_3d(camera_position, view_mode)
        % Draw the football field with all standard markings
        % view_mode: 'full' for complete field, 'goal_only' to show only the target goal
        
        if nargin < 2
            view_mode = 'full'; % Default to full field if not specified
        end
        
        % Set camera position
        set(gca, 'CameraPosition', camera_position)
        
        % Set view limits based on mode
        if strcmp(view_mode, 'goal_only')
            % Expanded view to show goal and trajectory
            set(gca, 'xlim', [field_length-30 field_length+10], 'ylim', [-15 15], 'zlim', [0 8])
        else
            % Full field view
            set(gca, 'xlim', [-5 field_length+10], 'ylim', [-field_width/2-5 field_width/2+5], 'zlim', [0 15])
        end
        
        % Draw elements based on view mode
        if strcmp(view_mode, 'full')
            % Draw field boundary
            plot3([0 field_length field_length 0 0], ...
                  [-field_width/2 -field_width/2 field_width/2 field_width/2 -field_width/2], ...
                  [0 0 0 0 0], 'k', 'LineWidth', 1.5);
            
            % Halfway line
            plot3([field_length/2 field_length/2], [-field_width/2 field_width/2], [0 0], 'k', 'LineWidth', 1);
            
            % Center circle
            theta = linspace(0, 2*pi, 100);
            x_circle = 9.15 * cos(theta) + field_length/2;
            y_circle = 9.15 * sin(theta);
            plot3(x_circle, y_circle, zeros(size(theta)), 'k', 'LineWidth', 1);
            
            % Center spot
            plot3(field_length/2, 0, 0, 'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 2);
        end
        
        % Always draw the right goal (target for corner kick) regardless of view mode
        % Right goal (x=field_length) - main target for corner kick
        plot3([field_length field_length field_length field_length], ...
              [-goal_width/2 -goal_width/2 goal_width/2 goal_width/2], ...
              [0 goal_height goal_height 0], 'b', 'LineWidth', 4);  % Blue goal
        % Add crossbar and goal posts for better visibility
        plot3([field_length field_length], [-goal_width/2 goal_width/2], [goal_height goal_height], 'b', 'LineWidth', 4);
        plot3([field_length field_length], [-goal_width/2 -goal_width/2], [0 goal_height], 'b', 'LineWidth', 4);
        plot3([field_length field_length], [goal_width/2 goal_width/2], [0 goal_height], 'b', 'LineWidth', 4);
        
        % Add goal net visualization (simplified) for the target goal
        % Goal back
        plot3([field_length+goal_depth field_length+goal_depth field_length+goal_depth field_length+goal_depth], ...
              [-goal_width/2 -goal_width/2 goal_width/2 goal_width/2], ...
              [0 goal_height goal_height 0], 'b:', 'LineWidth', 2);
        % Goal top
        plot3([field_length field_length+goal_depth field_length+goal_depth field_length], ...
              [-goal_width/2 -goal_width/2 goal_width/2 goal_width/2], ...
              [goal_height goal_height goal_height goal_height], 'b:', 'LineWidth', 2);
        % Goal sides
        plot3([field_length field_length+goal_depth field_length+goal_depth field_length], ...
              [-goal_width/2 -goal_width/2 -goal_width/2 -goal_width/2], ...
              [0 0 goal_height goal_height], 'b:', 'LineWidth', 2);
        plot3([field_length field_length+goal_depth field_length+goal_depth field_length], ...
              [goal_width/2 goal_width/2 goal_width/2 goal_width/2], ...
              [0 0 goal_height goal_height], 'b:', 'LineWidth', 2);
              
        % Only draw the left goal if in full view mode
        if strcmp(view_mode, 'full')
            % Left goal (x=0)
            plot3([0 0 0 0], ...
                  [-goal_width/2 -goal_width/2 goal_width/2 goal_width/2], ...
                  [0 goal_height goal_height 0], 'r', 'LineWidth', 3);
            % Add crossbar and goal posts for better visibility
            plot3([0 0], [-goal_width/2 goal_width/2], [goal_height goal_height], 'r', 'LineWidth', 3);
            plot3([0 0], [-goal_width/2 -goal_width/2], [0 goal_height], 'r', 'LineWidth', 3);
            plot3([0 0], [goal_width/2 goal_width/2], [0 goal_height], 'r', 'LineWidth', 3);
        end
        
        if strcmp(view_mode, 'full')
            % Only draw these elements in full view mode
            
            % Penalty areas
            % Left penalty area
            plot3([0 penalty_area_length penalty_area_length 0], ...
                  [-penalty_area_width/2 -penalty_area_width/2 penalty_area_width/2 penalty_area_width/2], ...
                  [0 0 0 0], 'k', 'LineWidth', 1);
            
            % Right penalty area
            plot3([field_length field_length-penalty_area_length field_length-penalty_area_length field_length], ...
                  [-penalty_area_width/2 -penalty_area_width/2 penalty_area_width/2 penalty_area_width/2], ...
                  [0 0 0 0], 'k', 'LineWidth', 1);
            
            % Goal areas
            % Left goal area
            plot3([0 goal_area_length goal_area_length 0], ...
                  [-goal_area_width/2 -goal_area_width/2 goal_area_width/2 goal_area_width/2], ...
                  [0 0 0 0], 'k', 'LineWidth', 1);
            
            % Right goal area
            plot3([field_length field_length-goal_area_length field_length-goal_area_length field_length], ...
                  [-goal_area_width/2 -goal_area_width/2 goal_area_width/2 goal_area_width/2], ...
                  [0 0 0 0], 'k', 'LineWidth', 1);
            
            % Penalty marks
            plot3(penalty_mark_distance_from_goal, 0, 0, 'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 2);
            plot3(field_length-penalty_mark_distance_from_goal, 0, 0, 'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 2);
            
            % Penalty arcs
            % Left penalty arc
            theta_amp = acos((penalty_area_length-penalty_mark_distance_from_goal)/9.15);
            theta = linspace(pi-theta_amp, pi+theta_amp, 50);
            x_arc_left = 9.15 * cos(theta) + penalty_mark_distance_from_goal;
            y_arc_left = 9.15 * sin(theta);
            plot3(x_arc_left, y_arc_left, zeros(size(theta)), 'k', 'LineWidth', 1);
            
            % Right penalty arc
            theta = linspace(-theta_amp, theta_amp, 50);
            x_arc_right = 9.15 * cos(theta) + (field_length-penalty_mark_distance_from_goal);
            y_arc_right = 9.15 * sin(theta);
            plot3(x_arc_right, y_arc_right, zeros(size(theta)), 'k', 'LineWidth', 1);
            
            % Corner arcs (1m radius)
            % Bottom left
            theta = linspace(0, pi/2, 20);
            x_corner = 1 * cos(theta);
            y_corner = 1 * sin(theta) - field_width/2;
            plot3(x_corner, y_corner, zeros(size(theta)), 'k', 'LineWidth', 1);
            
            % Top left
            theta = linspace(pi/2, pi, 20);
            x_corner = 1 * cos(theta);
            y_corner = 1 * sin(theta) + field_width/2 - 1;
            plot3(x_corner, y_corner, zeros(size(theta)), 'k', 'LineWidth', 1);
            
            % Bottom right
            theta = linspace(-pi/2, 0, 20);
            x_corner = 1 * cos(theta) + field_length - 1;
            y_corner = 1 * sin(theta) - field_width/2 + 1;
            plot3(x_corner, y_corner, zeros(size(theta)), 'k', 'LineWidth', 1);
            
            % Top right
            theta = linspace(pi, 3*pi/2, 20);
            x_corner = 1 * cos(theta) + field_length;
            y_corner = 1 * sin(theta) + field_width/2;
            plot3(x_corner, y_corner, zeros(size(theta)), 'k', 'LineWidth', 1);
            
            % Corner kick position marker (ball initial position)
            plot3(0, -field_width/2, 0, 'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 3);
        else
            % In goal_only mode, add a small field section near the goal for reference
            plot3([field_length-30 field_length field_length field_length-30], ...
                  [-15 -15 15 15], ...
                  [0 0 0 0], 'k:', 'LineWidth', 0.5);
                  
            % Add a field marking to show where the ball is relative to the goal
            plot3([field_length-20 field_length-20], [-15 15], [0 0], 'k:', 'LineWidth', 0.5);
        end
    end
    
    function dstates = ball_dynamics(~, states, m, A, rho, C_D, C_L, g, omega)
        % Ball dynamics considering drag and Magnus forces
        % states = [x y z vx vy vz]
        
        % Extract velocity components
        dx = states(4);
        dy = states(5);
        dz = states(6);
        
        % Calculate speed
        v = sqrt(dx^2 + dy^2 + dz^2);   % Speed [m/s]
        
        % Calculate forces
        if v > 0
            % Drag force (Prandtl)
            F_drag = -0.5 * rho * A * C_D * v^2 * [dx/v; dy/v; dz/v];
            
            % Magnus force (spin effect)
            cross_val = cross([dx; dy; dz], omega);
            if norm(cross_val) > 0
                F_magnus = 0.5 * rho * A * C_L * v^2 * (cross_val / norm(cross_val));
            else
                F_magnus = [0; 0; 0];
            end
        else
            F_drag = [0; 0; 0];
            F_magnus = [0; 0; 0];
        end
        
        % Gravity force
        F_gravity = [0; 0; -m*g];
        
        % Sum forces and calculate acceleration
        F_total = F_drag + F_magnus + F_gravity;
        a = F_total / m;
        
        % Return state derivatives
        dstates = [dx; dy; dz; a];
    end
    
    function [position, isterminal, direction] = ball_floor_or_end(~, y, field_length)
        % Terminate simulation when ball touches the floor or goes beyond the field
        
        % Extract current position
        x_pos = y(1);
        y_pos = y(2);
        z_pos = y(3);
        
        % Check if ball has hit the ground (z=0)
        position = z_pos;
        
        % Also terminate if ball has gone too far beyond the field
        if x_pos > field_length + 10 || x_pos < -10 || ...
           abs(y_pos) > field_width/2 + 10
            position = 0;
        end
        
        isterminal = 1;  % Stop integration when event occurs
        direction = -1;  % Trigger only when ball is descending
    end
end