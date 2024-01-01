import pygame, time

# Window
window = (600, 600)

#cells
c_size = 4
c_rows = window[1] // c_size
c_cols = window[0] // c_size

#general
max_dt = 0.025 #limit to change per frame for lag spikes. Ensure ant speed * max elapsed time <= cell size to prevent ants skipping squares on check

#ants
ant_sight = 10 #how many cells away gradient is calculated for
num_ants = 5000
ant_speed = 40 #Ensure ant speed * max_dt (delta time) <= cell size to prevent ants skipping squares on checks

#pheromones
p_time = 0.5
p_update_speed = .1 # time in seconds to decrease pheromones on a square
p1_decrease = 1 # amount of decrease per update
p2_decrease = 1
p1_increase = int(50 / c_size**2) # amount cell increased by per ant per update
p2_increase = int(500 / c_size**2)
gradient_update_speed = 1
gradient_timer = gradient_update_speed
pheromone_timer = p_update_speed # time until pheromone disappates by 1

#scene
slotted_box = True

#Debug
debug_show_food = True # f
debug_show_pheromones = True # p
debug_show_grid = False # g key
debug_timed_run = False # For profiling
debug_timed_run_timer = 30.0 # For profiling
debug_show_gradient_colors = False # v key
debug_show_gradient_arrows = False # v key