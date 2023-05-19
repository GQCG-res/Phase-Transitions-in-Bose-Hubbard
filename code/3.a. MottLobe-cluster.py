# Generate Mott-Lobe
import prototypes.BoseHubbardModel as bh
import numpy as np
import pandas as pd
import scipy.optimize as opt
import time
import argparse

# Setup the argument parses in order to select the task.
parser = argparse.ArgumentParser(description='mott-lobe generation')
parser.add_argument("PBS_ARRAYID", type=int, help="PBS task id")
args = parser.parse_args()

# Required functions.
def chemicalPotential(sites, bosons, boson_limit, t, U, site_potentials, boundary_conditions):
    H_n = bh.BoseHubbardHamiltonian(sites, bosons, t, U, [site_potentials]*sites, boundary_conditions)
    basis_n = bh.ONVBasis(sites, bosons, boson_limit)
    H_n_eval = basis_n.evaluateHamiltonian(H_n)

    H_n_plus_1 = bh.BoseHubbardHamiltonian(sites, bosons+1, t, U, [site_potentials]*sites, boundary_conditions)
    basis_n_plus_1 = bh.ONVBasis(sites, bosons+1, boson_limit)
    H_n_plus_1_eval = basis_n_plus_1.evaluateHamiltonian(H_n_plus_1)

    H_n_min_1 = bh.BoseHubbardHamiltonian(sites, bosons-1, t, U, [site_potentials]*sites, boundary_conditions)
    basis_n_min_1 = bh.ONVBasis(sites, bosons-1, boson_limit)
    H_n_min_1_eval = basis_n_min_1.evaluateHamiltonian(H_n_min_1)

    E_n = bh.BoseHubbardSolver(H_n_eval).groundState().energy
    E_n_plus_1 = bh.BoseHubbardSolver(H_n_plus_1_eval).groundState().energy
    E_n_min_1 = bh.BoseHubbardSolver(H_n_min_1_eval).groundState().energy

    return E_n_plus_1 - E_n, E_n - E_n_min_1

def chemicalPotential_H_eval(H_n_eval, H_n_plus_1_eval, H_n_min_1_eval):

    E_n = bh.BoseHubbardSolver(H_n_eval, True).groundState().energy
    E_n_plus_1 = bh.BoseHubbardSolver(H_n_plus_1_eval, True).groundState().energy
    E_n_min_1 = bh.BoseHubbardSolver(H_n_min_1_eval, True).groundState().energy

    return E_n_plus_1 - E_n, E_n - E_n_min_1

def generate_H(sites, bosons, boson_limit, U, site_potentials, boundary_conditions):
    H_diag = bh.BoseHubbardHamiltonian(sites, bosons, 0, U, [site_potentials]*sites, boundary_conditions)
    H_hop = bh.BoseHubbardHamiltonian(sites, bosons, 1, 0, [0]*sites, boundary_conditions)
    basis = bh.ONVBasis(sites, bosons, boson_limit)
    H_diag_eval = basis.evaluateHamiltonian(H_diag)
    H_hop_eval = basis.evaluateHamiltonian(H_hop)

    return H_diag_eval, H_hop_eval

# Define some variables.
t_range = np.arange(0.0, 2.0, 0.1)
U = 2
mott_lobe = 1
sites = 14
bosons = 14
boson_limit = None

# The actual calculation.
H_n_eval_diag, H_n_eval_hop = generate_H(sites, bosons, boson_limit, U, 0, True)
H_n_plus_1_eval_diag, H_n_plus_1_eval_hop = generate_H(sites, bosons + 1, boson_limit, U, 0, True)
H_n_min_1_eval_diag, H_n_min_1_eval_hop = generate_H(sites, bosons - 1, boson_limit, U, 0, True)

chemical_potentials_upper = []
chemical_potentials_lower = []
t_U_values = []

output_df = pd.DataFrame(columns=["t/U", "mu_upper/U", "mu_lower/U"])

t = t_range[args.PBS_ARRAYID]
H_n_eval = H_n_eval_diag + H_n_eval_hop * t
H_n_plus_1_eval = H_n_plus_1_eval_diag + H_n_plus_1_eval_hop * t
H_n_min_1_eval = H_n_min_1_eval_diag + H_n_min_1_eval_hop * t
mu_upper, mu_lower = chemicalPotential_H_eval(H_n_eval, H_n_plus_1_eval, H_n_min_1_eval)

output_df.loc[0, "t/U"] = t/U
output_df.loc[0, "mu_upper/U"] = mu_upper/U
output_df.loc[0, "mu_lower/U"] = mu_lower/U

# Save the dataframe as a json file.
path = "./Mott-Lobe-1/mott-lobe-1-t-value" + str(args.PBS_ARRAYID) + ".json"

output_df.to_json(path, orient="columns")
