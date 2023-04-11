using MPSKit, MPSKitModels, TensorKit, TensorOperations

M = 5 # max number of bosons on a site
a⁺, a⁻ = nonsym_bosonictensors(M) # bosonic operators
n_op = a⁺ * a⁻ # number operator

# define Hamiltonian on L sites
function H_finite(L, t, U)
    H = TensorMap(zeros, ComplexF64, (ℂ^(M+1))^L ← (ℂ^(M+1))^L)
    for i in 1:L-1
        H += mapfoldl(⊗, 1:L-1) do site
            site == i ? t * a⁺ ⊗ a⁻ : id(ℂ^(M+1))
        end
        H += mapfoldl(⊗, 1:L-1) do site
            site == i ? t * a⁻ ⊗ a⁺ : id(ℂ^(M+1))
        end
    end

    for i in 1:L
        H += mapfoldl(⊗, 1:L) do site
            site == i ? -U/2 * n_op * (n_op - id(ℂ^(M+1))) : id(ℂ^(M+1))
        end
    end

    return H
end

# define Hamiltionian for infinite basis with chemical potential
function H_infinite(t, U, μ)
    H_i = TensorMap(zeros, ComplexF64, (ℂ^(M+1))^2 ← (ℂ^(M+1))^2)
    H_i += -t * (a⁺ ⊗ a⁻ + a⁻ ⊗ a⁺) + U/2 * n_op * (n_op - id(ℂ^(M+1))) ⊗ id(ℂ^(M+1))
    H_i += -μ * n_op ⊗ id(ℂ^(M+1))

    return @mpoham sum(H_i{i,i+1} for i in vertices(InfiniteChain(1)))
end

# find groundstate (energy) for a system with L sites using DMRG
function groundstate_finite(L, t, U)
    Ψ = FiniteMPS(rand, ComplexF64, L, ℂ^(M+1), ℂ^20)
    H = H_finite(L, t, U)
    Ψ, envs, δ = find_groundstate(Ψ, H, DMRG())
    E0 = sum(expectation_value(Ψ, H))
    return E0
end

# find groundstate (number of bosons on a site) using VUMPS
function groundstate_infinite(t, U; μ=0)
    Ψ = InfiniteMPS(M+1, 32)
    H_mod = H_infinite(t, U, μ)
    Ψ, envs, δ = find_groundstate(Ψ, H_mod, VUMPS())
    count = sum(expectation_value(Ψ, n_op))
    return count
end