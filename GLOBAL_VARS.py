
# Preset functions
functions_dict = {"Quadratic": "x**2",
                  "Mixed": "(np.sin(1/2 * x) + 2 * np.cos(1/2 * x)) * x**2"
                  }

# Basic args
basic_args = {
    "jac": None,
    "hess": None,
    "hessp": None,
    "bounds": None,
    "constraints": (),
    "tol": None,
    "callback": None,
    "options": None
}

# Preset Methods
methods_options_dict = {
    "SLSQP": {"ftol": ["float", None],
                "eps": ["float", None],
                #"disp": ["bool", False],
                "maxiter": ["int", None],
                "finite_diff_rel_step": ["array", None]},
    "COBYLA": {"rhobeg": ["float", None],
                "tol": ["float", None],
                #"disp": ["bool", False],
                "maxiter": ["int", None],
                "catol": ["float", None]},
    "Nelder-Mead": {},
    "Powell": {},
    "CG": {},
    "BFGS": {},
    "Newton-CG": {},
    "CG": {},
    "L-BFGS-B": {},
    "TNC": {},
    "trust-constr": {},
    "dogleg": {},
    "trust-ncg": {},
    "trust-exact": {},
    "trust-krylov": {}
}