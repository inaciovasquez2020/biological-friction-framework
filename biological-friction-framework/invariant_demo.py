import numpy as np

def invariant(alpha=0.5, beta=1.0, gamma=1.0, kappa=1.5, n=20000):
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    gradS = np.sin(t)
    dgradS = np.cos(t)
    delta = np.arctan(1.0/gamma)
    m = (beta/np.sqrt(gamma**2 + 1.0)) * np.sin(t - delta)
    phi = alpha*gradS + kappa*m
    I = np.trapz(phi * dgradS, t)
    return I

if __name__ == "__main__":
    for g in [10.0, 1.0, 0.1]:
        I = invariant(gamma=g)
        print(f"gamma={g:>4}  I={I:.6f}")
