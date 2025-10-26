from golden_math.butusov_phi import to_phi_base_integer, from_phi_base
def recon(n):
    s = to_phi_base_integer(n)
    back = float(from_phi_base(s))
    assert abs(back - n) < 1e-3
def test_sample():
    for n in [0,1,2,3,5,8,10,21,34,55,1973,9999]:
        recon(n)
