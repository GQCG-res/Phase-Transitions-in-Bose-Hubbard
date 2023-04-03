import time
import numpy as np


def bisection_algorithm(objective_function, target_value, bracket=None, maximum_iterations=10000, tolerance=1e-4, log=False):
    # Timling for the calculation.
    start = time.time()

    # dictionary containing information about the optimization.
    infodict = {}

    # Number of iterations
    iter = 1

    # Unpack the bracket.
    if bracket is None:
        raise Exception("You need to specify a bracket")

    a, b = bracket[0], bracket[1]
    if (lower := objective_function(a)) > (upper := objective_function(b)):
        a, b = b, a
        lower, upper = upper, lower

    assert target_value >= lower - 1e-5, f"y is smaller than the lower bound. {target_value} < {lower}"
    assert target_value <= upper + 1e-5, f"y is larger than the upper bound. {target_value} > {upper}"

    # Time the optimization loops.
    loop_time = 0
  
    # Optimization loop.
    while iter <= maximum_iterations:
        loop_start = time.time()
        # Take the middle point of the bracket
        c = (a + b) / 2
        # If the function value of this point - the target value < the threshold, the algorithm finishes.
        if abs((y_c := objective_function(c)) - target_value) < tolerance:
            loop_end = time.time()
            loop_time += (loop_end-loop_start)
            average_loop_time = (loop_time / iter)
            end = time.time()
            infodict["number of iterations"] = iter
            infodict["average loop time (s)"] = average_loop_time
            infodict["total computation time (s)"] = (end-start)
            infodict['Optimized result'] = c

            # print the infodict if log is true.
            if log:
                print("************************")
                for key, value in infodict.items():
                    print(key, ' : ', value)
                print("************************")
            return c
        # If the target value < function value of the middle point, repeat the process in the half bracket up to the function value.
        elif target_value < y_c:
            b, upper = c, y_c
            loop_end = time.time()
            loop_time += (loop_end - loop_start)
        # Otherwise, start the new bracket at the function value. 
        else:
            a, lower = c, y_c
            loop_end = time.time()
            loop_time += (loop_end - loop_start)
        
        # increase the number of iterations.
        iter += 1
