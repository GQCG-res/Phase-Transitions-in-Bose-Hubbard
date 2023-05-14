using MPSKit, MPSKitModels, TensorOperations

function BoseHubbardHamiltonian(eltype=Float64, symmetry=U₁;
    cutoff=5, t=1.0, U=1.0, mu=0.0, n::Int=0, L::Int=128)
    
    lattice=FiniteChain(L)
    # Open boundary conditions.
    BHHamiltonian = bose_hubbard_model(eltype, symmetry, lattice; cutoff, t, U, mu, n)
    charges = fill(1, L)
    MPOHamiltonian = MPSKit.add_physical_charge(BHHamiltonian, charges)

    return MPOHamiltonian
end

function optimize(eltype=Float64, symmetry=U₁;
    cutoff=5, t=1.0, U=1.0, mu=0.0, n::Int=0, L::Int=128)

    H = BoseHubbardHamiltonian(eltype, symmetry;cutoff, t, U, mu, n, L)
    print("test")
    state = FiniteMPS(rand, Float64, 12, ℝ^(5+1), ℝ^10)

    (groundstate,_) = find_groundstate(state, H, DMRG2(tol=1e-10, maxiter=1000))

    return groundstate
end