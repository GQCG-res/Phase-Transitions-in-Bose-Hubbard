import numpy as np
from scipy.special import binom
import scipy.sparse as sparse
import Helper as h


class AdjacencyMatrix:

    def __init__ (self, number_of_sites: int):
        L = number_of_sites - 1
        A = np.zeros((number_of_sites, number_of_sites))
        super_diag = np.diag([1] * L, 1)
        sub_diag = np.diag([1] * L, -1)

        self.L = L
        self.adjacency = A + super_diag + sub_diag

    def withPeriodicBoundaryConditions(self):
        A = self.adjacency
        A[0, self.L] = 1
        A[self.L, 0] = 1
        self.adjacency = A
        return self.adjacency

    def withoutPeriodicBoundaryConditions(self):
        if self.adjacency[0, self.L] == 1 and self.adjacency[self.L, 0] == 1:
            self.adjacency[0, self.L] = 0
            self.adjacency[self.L, 0] = 0
        return self.adjacency


class BoseHubbardHamiltonian:

    def __init__(self, number_of_sites: int, number_of_bosons: int, hopping: float, on_site_repulsion: float, on_site_potentials: list, boundary_conditions: bool):
        # Dimensions of the model.
        self.sites = number_of_sites
        self.bosons = number_of_bosons

        # Hamiltonian preparation in site basis.
        # Set up the adjacency matrix.
        if boundary_conditions:
            adjacency_matrix = AdjacencyMatrix(self.sites).withPeriodicBoundaryConditions()
        else:
            adjacency_matrix = AdjacencyMatrix(self.sites).withoutPeriodicBoundaryConditions()

        if len(on_site_potentials) > number_of_sites or len(on_site_potentials) < number_of_sites:
            raise "The number of specified on-site potentials has to be equal to the number of sites."

        self.site_potentials = on_site_potentials
        self.hopping_matrix = hopping * adjacency_matrix
        self.U = on_site_repulsion


class ONVBasis:

    def __init__(self, number_of_sites:int, number_of_bosons: int):
        self.sites = number_of_sites
        self.bosons = number_of_bosons

        # Number of possible ONVs is defined as a binomial expansion.
        self.size = int(binom( self.bosons+ self.sites-1,  self.bosons))
        states = np.zeros((self.size,  self.sites), dtype=int)

        states[0, 0] =  self.bosons
        ni = 0  # initial value
        for i in range(1, states.shape[0]):

            # See algorithm in http://iopscience.iop.org/article/10.1088/0143-0807/31/3/016
            states[i, : self.sites-1] = states[i-1, : self.sites-1]
            states[i, ni] -= 1
            states[i, ni+1] += 1 + states[i-1,  self.sites-1]

            if ni >=  self.sites-2:
                if np.any(states[i, : self.sites-1]):
                    ni = np.nonzero(states[i, : self.sites-1])[0][-1]
            else:
                ni += 1

        self.ONVs = states


    def _stateIndex(self, state):
        key = h.hash(state)
        hashes =h.hash(self.ONVs)
        sorter = np.argsort(hashes, 0, 'quicksort')

        return sorter[np.searchsorted(hashes, key, sorter=sorter)]


    def evaluateHamiltonian(self, H: BoseHubbardHamiltonian):
        # evaluate the onsite part of the Hamiltonian.
        # We do minus U/2 since otherwise the evaluation of U in the basis counts certain elemnts double. (U * n_i(n_i - 1))
        onsite = self.ONVs.dot(np.array(H.site_potentials) - H.U/2)

        # evaluate the on-site repulsion part of the Hamiltonian.
        onsite_repulsion = np.sum(H.U/2*self.ONVs**2, axis=1)

        # The diagonal indices need to be stored as well, since we work in a sparse representation.
        H_ii = np.arange(self.size)

        # Evaluate the Hopping part of the Hamiltonian.
        # Since we construct a sparse Hamiltonian, we need the indices as well as the values.
        Ht_i, Ht_j, Ht_values = [], [], []

        for i in range(H.hopping_matrix.shape[0]):
            js = np.nonzero(self.ONVs[:, i])[0]  # affected states
            nj = len(js)

            ls = np.nonzero(H.hopping_matrix[i, :])[0]  # relevant hoppings
            nl = len(ls)

            ks = np.zeros((nj*nl,))  # storing result states
            vs = np.zeros((nj*nl,))  # storing result states

            for k, l in enumerate(ls):
                nstates = self.ONVs[js, :]
                nstates[:, i] -= 1  # remove one element
                nstates[:, l] += 1  # add it here

                ks[k*nj:(k+1)*nj] = self._stateIndex(nstates)  # the new states
                vs[k*nj:(k+1)*nj] = H.hopping_matrix[i, l]*np.sqrt(self.ONVs[js, i]*(self.ONVs[js, l] + 1))

            Ht_i += np.tile(js, nl).tolist()
            Ht_j += ks.tolist()
            Ht_values += vs.tolist()

        return sparse.coo_matrix((Ht_values, (Ht_i, Ht_j)), shape=(self.size, self.size)).tocsr() + sparse.coo_matrix((onsite+onsite_repulsion, (H_ii, H_ii)), shape=(self.size, self.size)).tocsr()

    def evaluateDiagonalOperator(self, operator, sparse_representation=True):
        # Any diagonal operator can be evaluated the same way as the on-site part of the Hamiltonian.
        diagonal = np.diag(operator)
        evaluated_operator = self.ONVs.dot(diagonal)
        diagonal_indices = np.arange(self.size)
        if sparse_representation:
            return sparse.coo_matrix((evaluated_operator, (diagonal_indices, diagonal_indices)), shape=(self.size, self.size)).tocsr()
        else:
            return sparse.coo_matrix((evaluated_operator, (diagonal_indices, diagonal_indices)), shape=(self.size, self.size)).tocsr().toarray()


class BoseHubbardModel:
    def __init__(self, energy, expansion_coefficients):
        self.energy = energy
        self.C = expansion_coefficients

    def singleParticleDensityMatrix(self):
        return np.outer(self.C, self.C.T)

    def calculateExpectationValue(self, operator):
        return np.einsum("pq, pq->", self.singleParticleDensityMatrix(), operator)


class BoseHubbardSolver:

    def __init__(self, evaluated_hamiltonian: sparse):

        # diagonalize the Hamiltonian matrix.
        val, C = sparse.linalg.eigs(evaluated_hamiltonian)

        self.energies = np.sort(val)
        self.expansion_coefficients = C

    def groundState(self):
        return BoseHubbardModel(self.energies[0], self.expansion_coefficients[:, 0])

    def excitedState(self, index):
        return BoseHubbardModel(self.energies[index], self.expansion_coefficients[:, index])
