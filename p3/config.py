# config.py

# configuration for game
game = dict(
    stage_width         = 85.5656967163086, # HALF the stage width of FINAL DESTINATION
    g_time              = 4000, # game time
    t_time              = 4000, # game testing time
    fps                 = 60, # frame per second
    delay               = 20, # terminal update delay
    n_best              = 5, # number of best agents
    n_agents            = 12, # number of agents
)

nnet = dict(
    n_inputs    = 6,
    n_h_neurons = 6,
    n_outputs   = 28,
    n_weights   = (6+1) * (6) + (6+1) * (28), # (inputs + bias) * (h_neurons) + (h_neurons + bias) * (outputs)
)