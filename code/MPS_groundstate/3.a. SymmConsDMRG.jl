using ITensors, TensorKit, TensorOperations

function boseHubbardHamiltonian(t::Float64, U::Float64, μ::Float64, L::Int; impurity_values::Array{Float64}=[0.0], impurity_sites::Array{Int}=[0], periodic_boundary::Bool=true, impurity::Bool=false)
    # Define the type of sites needed for the calculation.
    sites = siteinds("Qudit",L; dim=5,  conserve_qns=true, conserve_number=true)

    H = OpSum()
    for i in (1:L-1)
        H += -μ - U/2, "n", i
        H += U/2, "n", i, "n", i
        H += -t, "a", i, "adag", i+1
        H += -t, "adag", i, "a", i+1
    end
    # Add the on-site terms that couldn't be added in the loop (due to i+1).
    H += -μ - U/2, "n", L
    H += U/2, "n", L, "n", L

    # Add periodic boundary conditions.
    if periodic_boundary
        H += -t, "a", 1, "adag", L
        H += -t, "adag", 1, "a", L
    end

    if impurity
        for (value, site) in zip(impurity_values, impurity_sites) 
            H += -value, "n", site
        end
    end
    
    # Transform to an MPO Hamiltonian.
    Ham = MPO(H, sites)

    return Ham, sites
end


function energyZero(t::Float64, U::Float64, μ::Float64, L::Int, lobe::Int)

    Hamiltonian, site_type = boseHubbardHamiltonian(t, U, μ, L)
    
    # The lobe (lb) defines the density within the lobe.
    # We create an initial state that adheres to the wanted particle number symmetry.
    lb = string(lobe)
    state = [isodd(n) ? lb : lb for n=1:L]
    psi0 = randomMPS(site_type, state)
    
    # Define the DMRG variables.
    nsweeps = 10
    maxdim = [40, 80, 400, 400, 800, 800, 1000, 1000, 1000, 1000]
    cutoff = [1e-12]
    
    # perform the DMRG calculation and check the quantum number.
    energy, psi = dmrg(Hamiltonian, psi0; nsweeps, maxdim, cutoff)
    @show flux(psi)

    return energy
end

function energyPlusOne(t::Float64, U::Float64, μ::Float64, L::Int, lobe::Int)

    Hamiltonian, site_type = boseHubbardHamiltonian(t, U, μ, L)
    
    # The lobe (lb) defines the density within the lobe.
    # We create an initial state that adheres to the wanted particle number symmetry.
    lb = string(lobe)
    state_p = [isodd(n) ? lb : lb for n=1:L]
    state_p[1] = string(lobe+1)
    psi0_p = randomMPS(site_type,state_p)

    # Define the DMRG variables.
    nsweeps = 10
    maxdim = [40, 80, 400, 400, 800, 800, 1000, 1000, 1000, 1000]
    cutoff = [1e-12]
    
    # perform the DMRG calculation and check the quantum number.
    energy_p, psi_p = dmrg(Hamiltonian, psi0_p; nsweeps, maxdim, cutoff)
    @show flux(psi_p)

    return energy_p
end


function energyMinusOne(t::Float64, U::Float64, μ::Float64, L::Int, lobe::Int)

    Hamiltonian, site_type = boseHubbardHamiltonian(t, U, μ, L)
    
    # The lobe (lb) defines the density within the lobe.
    # We create an initial state that adheres to the wanted particle number symmetry.
    lb = string(lobe)
    state_m = [isodd(n) ? lb : lb for n=1:L]
    state_m[1] = string(lobe-1)
    psi0_m = randomMPS(site_type,state_m)

    # Define the DMRG variables.
    nsweeps = 10
    maxdim = [40, 80, 400, 400, 800, 800, 1000, 1000, 1000, 1000]
    cutoff = [1e-12]
    
    # perform the DMRG calculation and check the quantum number.
    energy_m, psi_m = dmrg(Hamiltonian, psi0_m; nsweeps, maxdim, cutoff)
    @show flux(psi_m)

    return energy_m
end
