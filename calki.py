import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import sys

# Włączamy tryb "ładnego drukowania" - ułamki z kreską i prawdziwe symbole matematyczne!
sp.init_printing(use_unicode=True)

# Ustawienia parsera (żeby Python rozumiał "2x" jako "2*x")
transformations = standard_transformations + (implicit_multiplication_application,)
x = sp.Symbol('x')

print("=" * 60)
print("   KALKULATOR CAŁEK: ZAPIS JAK NA KARTCE PAPIERU   ")
print("=" * 60)

# 1. Pobieranie funkcji
str_top = input("Wpisz funkcję GÓRNĄ (np. 5): ")
str_bottom = input("Wpisz funkcję DOLNĄ (np. x^2 - 4x): ")

str_top = str_top.replace('^', '**')
str_bottom = str_bottom.replace('^', '**')

try:
    f_top = parse_expr(str_top, transformations=transformations)
    f_bottom = parse_expr(str_bottom, transformations=transformations)
except:
    print("\n[BŁĄD] Sprawdź zapis funkcji.")
    sys.exit()

# 2. Miejsca zerowe
roots = sp.solve(sp.Eq(f_top, f_bottom), x)
real_roots = [r for r in roots if r.is_real]

if len(real_roots) < 2:
    print("[BŁĄD] Brak zamkniętego pola.")
    sys.exit()

a, b = min(real_roots), max(real_roots)

print("\n" + "=" * 50)
print(" ROZWIĄZANIE KROK PO KROKU")
print("=" * 50)

# KROK 1
print("\nKROK 1: Punkty przecięcia f(x) = g(x)")
sp.pprint(sp.Eq(f_top, f_bottom))
print("Granice całkowania:")
sp.pprint(sp.Eq(sp.Symbol('x_1'), a))
sp.pprint(sp.Eq(sp.Symbol('x_2'), b))

# KROK 2
print("\nKROK 2: Ułożenie całki oznaczonej P = ∫ (Góra - Dół) dx")
integrand = sp.simplify(f_top - f_bottom)
integral_sym = sp.Integral(integrand, (x, a, b))
sp.pprint(sp.Eq(sp.Symbol('P'), integral_sym))

# KROK 3
print("\nKROK 3: Wyznaczenie funkcji pierwotnej F(x)")
F = sp.integrate(integrand, x)
sp.pprint(sp.Eq(sp.Symbol('F(x)'), F))

# KROK 4
print("\nKROK 4: Podstawienie granic (Górna - Dolna)")
F_b = F.subs(x, b)
F_a = F.subs(x, a)
print("Podstawienie za górną granicę:")
sp.pprint(F_b)
print("Odjąć podstawienie za dolną granicę:")
sp.pprint(F_a)

# KROK 5
print("\nKROK 5: Ostateczny wynik")
exact_area = sp.simplify(F_b - F_a)
sp.pprint(sp.Eq(sp.Symbol('P'), exact_area))
print("=" * 50 + "\n")

# ==========================================
# RYSOWANIE WYKRESU
# ==========================================
f_top_np = sp.lambdify(x, f_top, modules=['numpy'])
f_bottom_np = sp.lambdify(x, f_bottom, modules=['numpy'])

a_num, b_num = float(a.evalf()), float(b.evalf())
margin = (b_num - a_num) * 0.5
x_vals = np.linspace(a_num - margin, b_num + margin, 400)

y_top = np.vectorize(f_top_np)(x_vals)
y_bottom = np.vectorize(f_bottom_np)(x_vals)

plt.figure(figsize=(8, 6))
plt.plot(x_vals, y_top, label=f'Góra', color='blue', linewidth=2)
plt.plot(x_vals, y_bottom, label=f'Dół', color='red', linewidth=2)

x_fill = np.linspace(a_num, b_num, 100)
y_top_fill = np.vectorize(f_top_np)(x_fill)
y_bottom_fill = np.vectorize(f_bottom_np)(x_fill)
plt.fill_between(x_fill, y_bottom_fill, y_top_fill, color='indigo', alpha=0.2, label=f'Pole P')

plt.axhline(0, color='black', linewidth=1.5)
plt.axvline(0, color='black', linewidth=1.5)
plt.grid(True, linestyle='--', alpha=0.7)
plt.title('Zadanie - Pole pod krzywą', fontsize=14, fontweight='bold')
plt.xlabel('Oś X', fontsize=12)
plt.ylabel('Oś Y', fontsize=12)
plt.legend(fontsize=11)

plt.show()