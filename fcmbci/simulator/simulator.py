import pandas as pd
import numpy as np
from simulation_functions import *

class FcmSimulator(self, init):
    
    self.results = pd.DataFrame(self.init, index=[0])

    def simulate(self, initial_state, weights, iterations, inference = 'mk', 
                 transform = 's', l = 1, thresh = 0.001):
        
        """ Runs simulations over the passed FCM.
        
        Parameters
        ----------
        initial_state : dict,
                        A dictionary of Concepts as keys and their initial states. ---> {'C1': 0.5, 'C2' : 0.4}.
                        The initial states take only values in the range of [-1,1].

        weights : Data frame with the causal weights.

        iterations : int,
                        Number of itterations to run in case if the system doesn't converge.
        inference : str,
                    default --> 'mk' -> modified kosko; available options: 'k' -> Kosko, 'r' -> Rescale.
                    Method of inference.
                    
        transform : str,
                    default --> 's' -> sigmoid; available options: 'h' -> hyperbolic tangent; 'b' -> bivalent; 't' trivalent. 
                    transfer function.
        l : int,
            A parameter that determines the steepness of the sigmoid and hyperbolic tangent function at values around 0. 
        
        thresh : float,
                    default -->  0.001,
                    a thershold for convergence of the values.

        Return
        ----------
        y : dataframe,
            dataframe with the results of the simulation steps.
        """


        initial_state = self.init
        step_count = 0
        stop = thresh
        
        state_vector = list(initial_state.values())
        
        while stop >= thresh and step_count <= iterations:
            res = weights.mul(state_vector, axis=0).sum()+state_vector
            if transform == 's':
                state_vector = [sig(i, l) for i in res]
            elif transform == 'h':
                state_vector = [np.tanh(l * i) for i in res]
            elif transform == 'b':
                state_vector = [bi(i) for i in res]
            elif transform == 't':
                state_vector = [tri(i) for i in res]
            else:
                raise ValueError('Unrecognized transfer function!')

            self.results.loc[len(self.results)] = state_vector
            step_count +=1
            stop = max(self.results.loc[len(self.results)-1] - self.results.loc[len(self.results) - 2])
        print(f'The values converged in the {step_count+1} state (e <= {tresh})')
        return self.results