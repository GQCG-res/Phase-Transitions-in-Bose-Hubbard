include("3.a. SymmConsDMRG.jl")

using CurveFit

function correlation_function(t::Float64, U::Float64, μ::Float64, L::Int; periodic::Bool=false, sweeps::Int=100, bond_dim::Int=1024, convergence::Float64=1e-4, output::Bool=true)

    Hamiltonian, site_type = boseHubbardHamiltonian(t, U, μ, L; periodic_boundary=periodic)
    state = fill("1", L)
    psi0 = randomMPS(site_type, state)

    # calculate the ground state
    psi = dmrg(Hamiltonian, psi0; nsweeps=sweeps, maxdim=bond_dim, cutoff=1e-15, observer=DMRGObserver(;energy_tol=convergence), outputlevel=output ? 1 : 0)[2]

    # calculate correlation matrix Cij between points i and j
    C = correlation_matrix(psi, "adag", "a")

    if periodic
        cor = C[1, 1:(L ÷ 2 - 1)]
    else
        # get rid of most of the boundary effects by removing 20 sites at each end
        cor = C[20, 20:end-20]
    end
    return cor
end

function density_function(t::Float64, U::Float64, μ::Float64, L::Int; impurity_values::Array{Float64}=[0.0], impurity_sites::Array{Int}=[1], periodic::Bool=false, sweeps::Int=4, output::Bool=true, impurity::Bool=false)

    Hamiltonian, site_type = boseHubbardHamiltonian(t, U, μ, L; impurity_values=impurity_values, impurity_sites=impurity_sites, periodic_boundary=periodic, impurity=impurity)
    state = fill("1", L)
    psi0 = randomMPS(site_type, state)

    bond_dim = [32 * 2^i for i in 1:sweeps]

    psi = dmrg(Hamiltonian, psi0; nsweeps=sweeps, maxdim=bond_dim, cutoff=1e-14, outputlevel=output ? 1 : 0)[2]

    C = correlation_matrix(psi, "adag", "a")

    return [C[i, i] for i in 1:L]
end

# returns how close the power fit is with data points [x, y] and parameter [a]
function power_fit(x, a)
    return x[2] - x[1] ^ a[1]
end

# generally more accurate to fit log(y) = -x/ξ
function exponential_fit(x, a)
    return log(x[2]) + x[1]/a[1]
end

#fit an exponential to the correlation function
function correlation_length(t::Float64, U::Float64, μ::Float64, L::Int; guess::Float64=1.)
    C = correlation_function(t, U, μ, L)

    data = hcat(0:length(C)-1, C)

    return nonlinear_fit(data, exponential_fit, [guess])[1][1]
end