include("3.a. SymmConsDMRG.jl")

enrgs_0 = zeros(0)

for t in range(0.45, 0.8, step=0.05)
    # U=2.0, μ=0.0, L=128, lobe=1
    E = energyZero(t, 2.0, 0.0, 128, 1)
    append!(enrgs_0, E)
end

println(enrgs_0)
