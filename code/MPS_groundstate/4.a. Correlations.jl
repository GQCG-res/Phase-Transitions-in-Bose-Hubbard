include("3.a. SymmConsDMRG.jl")

using CurveFit

function correlation_function(t::Float64, U::Float64, μ::Float64, L::Int; ρ::Float64=1., periodic::Bool=false, sweeps::Int=100, bond_dim::Int=128, convergence::Float64=1e-6, output::Bool=true)

    Hamiltonian, site_type = boseHubbardHamiltonian(t, U, μ, L; periodic_boundary=periodic)
    state = [i%(1/ρ) < 1 ? "1" : "0" for i in 0:L-1]
    psi0 = randomMPS(site_type, state)

    # calculate the ground state
    psi = dmrg(Hamiltonian, psi0; nsweeps=sweeps, maxdim=bond_dim, cutoff=1e-15, observer=DMRGObserver(;energy_tol=convergence), outputlevel=output ? 1 : 0)[2]

    # calculate correlation matrix Cij between points i and j
    C = correlation_matrix(psi, "adag", "a")

    return [sum(C[L ÷ 2 - r ÷ 2 + i, L ÷ 2 - r ÷ 2 + r + i] for i in -15:16)/32 for r in 0:(L-40)]
end

function density_function(t::Float64, U::Float64, μ::Float64, L::Int; ρ::Float64=1., periodic::Bool=false, sweeps::Int=100, bond_dim::Int=128, convergence::Float64=1e-4, output::Bool=true,
                          impurity_values::Array{Float64}=[0.0], impurity_sites::Array{Int}=[1], impurity::Bool=false)

    Hamiltonian, site_type = boseHubbardHamiltonian(t, U, μ, L; impurity_values=impurity_values, impurity_sites=impurity_sites, periodic_boundary=periodic, impurity=impurity)
    state = [i%(1/ρ) < 1 ? "1" : "0" for i in 0:L-1]
    psi0 = randomMPS(site_type, state)

    psi = dmrg(Hamiltonian, psi0; nsweeps=sweeps, maxdim=bond_dim, cutoff=1e-15, observer=DMRGObserver(;energy_tol=convergence), outputlevel=output ? 1 : 0)[2]

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
function correlation_length(t::Float64, U::Float64, μ::Float64, L::Int)
    C = correlation_function(t, U, μ, L; convergence=1e-10, output=false)

    data = hcat(4:length(C)-1, C[5:end])
    l = 0
    
    for guess in 0.1:0.1:10
        l = nonlinear_fit(data, exponential_fit, [guess])[1][1]
        if !isnan(l)
            break
        end
    end

    return C, l
end