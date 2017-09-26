# config.py

# configuration for game
game = dict(
    stage_width         = 85.5656967163086, # HALF the stage width of FINAL DESTINATION
    g_time              = 4000, # game time
    t_time              = 4000, # game testing time
    fps                 = 60, # frame per second
    delay               = 20, # terminal update delay
    n_best              = 5, # number of best agents
    n_agents            = 30, # number of agents
)

nnet = dict(
    n_inputs    = 28,
    n_h_neurons = 40,
    n_outputs   = 14,
    n_weights   = (28+1) * (40) + (40+1) * (14), # (inputs + 1) * (h_neurons) + (h_neurons + 1) * (outputs)
)