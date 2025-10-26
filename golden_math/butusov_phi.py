from __future__ import annotations
from decimal import Decimal, getcontext

# Настраиваем точность для стабильной математики φ
getcontext().prec = 80

sqrt5 = Decimal(5).sqrt()
phi: Decimal = (Decimal(1) + sqrt5) / Decimal(2)  # ϕ

__all__ = ["phi", "log_phi", "from_phi_base", "to_phi_base_integer"]

def log_phi(x: Decimal | float | int | str) -> Decimal:
    """log base φ: ln(x)/ln(φ). Принимает Decimal/float/int/str."""
    x_dec = Decimal(str(x))
    return x_dec.ln() / phi.ln()

def from_phi_base(s: str) -> Decimal:
    """
    Декодирует строку в «базе φ» (только 0/1 и опциональная точка) в Decimal.
    Пример: '1010.01' → ~6.23606797749979
    """
    s = s.strip()
    if not s or s.count('.') > 1 or any(ch not in '01.' for ch in s):
        raise ValueError("phi string must match ^[01]+(\\.[01]+)?$")
    intp, fracp = (s.split('.', 1) + [''])[:2]

    total = Decimal(0)
    # integer part: левый разряд — φ^(len(intp)-1)
    for i, ch in enumerate(intp):
        if ch == '1':
            exp = len(intp) - 1 - i
            total += phi ** exp
    # fractional part: первый разряд после точки — φ^-1, дальше φ^-2 и т.д.
    for i, ch in enumerate(fracp, start=1):
        if ch == '1':
            total += phi ** (-i)
    return total

def to_phi_base_integer(n: int) -> str:
    """
    Гридди-кодирование целого n в «базе φ» без подряд идущих '1' в целой части.
    Возвращает ТОЛЬКО целую часть (без дробного хвоста).
    Пример: 1973 → '1010001000100000'
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return "0"

    # находим максимальную степень k: φ^k <= n
    k = 0
    while (phi ** k) <= n:
        k += 1
    k -= 1

    digits = []
    remain = Decimal(n)
    prev_one = False

    while k >= 0:
        pk = phi ** k
        if (not prev_one) and pk <= remain + Decimal('1e-30'):
            digits.append('1')
            remain -= pk
            prev_one = True
        else:
            digits.append('0')
            prev_one = False
        k -= 1

    s = ''.join(digits).lstrip('0')
    return s or '0'
