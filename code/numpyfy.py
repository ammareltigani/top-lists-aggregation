import numpy as np
import filter as F
import sim 
import run_experiments
import collections

sim = sim.Simulation()
# base algorithms 
# deque since indexed access not required
algorithms = collections.deque(sim.funcDict.keys())

# functionality not required for algorithms with epsilon parameters
algorithms.remove("Score-Then-Adjust")
algorithms.remove("Score-Then-Adjust-Relaxed")

algorithmsBaseCopy = tuple(algorithms)

# add combination algorithms
postProcessAlgos = ["Chanas", "Local-Search"]
for postProcessAlgo in postProcessAlgos:
    # Iterate over algorithmsBaseCopy
    for initialAlgorithm in algorithmsBaseCopy:
        if not initialAlgorithm == postProcessAlgo and not initialAlgorithm == "Opt":
            algorithms.append(f"{initialAlgorithm}_{postProcessAlgo}")

f = F.Filter("../Synthetic-Results/")

def convert_to_npArray(filename):
    return np.genfromtxt(filename, delimiter=',', skip_header=1, usecols = (1,2))

def average(array):
    m, _ = np.shape(array)
    return np.sum(array, axis=0) / m



def by(parameter): 
    numAlgorithms = len(algorithms)   
    if parameter == 'n':
        l = run_experiments.ns
    elif parameter == 'N':
        l = run_experiments.Ns
    elif parameter == 'th':
        l = run_experiments.ths
    elif parameter == 'k':
        l = run_experiments.ks_ratio
    else:
        print("Invalid Parameter to filter over!")

    # want to get the average of all algorithms for each value of n,N,th, or k
    # will store in a len(l)xnumAlgorithmsx2 np.array (3 params, 12 algos, each with 2 data 
    # points: time and accuracy)
    out = np.empty((len(l),numAlgorithms,2))

    for j in range(len(l)):
        algs = np.empty((numAlgorithms,2))
        for algo in algorithms:
            _, fname = f.filter_by_param_and_algo(parameter, l[j], algo)
            arr = convert_to_npArray(fname)
            print(f"File name {fname}")
            print(f"File {arr}")
            np.append(algs,average(arr))
            
        out[j] = algs
    return out


if __name__ == '__main__':
    print(by('n'))
    print(by('N'))
    print(by('th'))
    print(by('k'))