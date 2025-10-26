from golden_math.butusov_phi import to_phi_base_integer, from_phi_base
import sys
if __name__ == "__main__":
    n = int(sys.argv[1])
    s = to_phi_base_integer(n)
    print(f"{n} -> {s}")
    print(f"back ≈ {float(from_phi_base(s))}")
