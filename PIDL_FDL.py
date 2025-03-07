import numpy
import tensorflow as tf

def mse(state1, state2):
    #should be the l2 distance function between 2 states
    return 1

def zerostate(state):
    #should be a state with all zero locations of the same size as state
    return 0

def physical_model():
    return 0
    #some pde related stuff
def loss_function(predicted_states, target_states, aux_states, physics_model, model_params, alpha = 1, beta = 1):
    data_disc = 0
    physical_disc = 0
    for i in range(len(predicted_states)):
        data_disc += mse(predicted_states[i], target_states[i])
    for i in range(len(aux_states)):
        physical_disc += mse(physics_model(aux_states[i], model_params), zerostate(aux_states[i]))
    return alpha * (data_disc / len(predicted_states)) + beta * (physical_disc / len(aux_states))





