import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

# Ustawienia strony
st.set_page_config(page_title="Gotowiec - Pole", layout="wide", initial_sidebar_state="expanded")
st.sidebar.title("🧭 Nawigacja")
st.sidebar.markdown("---")

st.title("🎓 Gotowiec na Kolokwium: Pole pod krzywą")
st.markdown("Ten moduł generuje pełne, szczegółowe rozwiązanie wraz z rozpisaniem obliczeń granic. Posiada wbudowany **Auto-Sort**, który sam ustala, co jest górą, a co dołem.")
st.markdown("---")

transformations = standard_transformations + (implicit_multiplication_application,)
x = sp.Symbol('x')

col_input, col_output = st.columns([1, 2], gap="large")

with col_input:
    st.subheader("Wprowadź dane z zadania")
    str_1 = st.text_input("Pierwsza funkcja f(x):", "5")
    str_2 = st.text_input("Druga funkcja g(x):", "x^2 - 4x")
    
    st.info("💡 Wskazówka: Program sam sprawdzi, która funkcja leży wyżej na wykresie i odpowiednio ułoży całkę.")
    generuj = st.button("📝 Generuj pełnego gotowca", type="primary", use_container_width=True)

with col_output:
    if generuj:
        try:
            expr_1 = parse_expr(str_1.replace('^', '**'), transformations=transformations)
            expr_2 = parse_expr(str_2.replace('^', '**'), transformations=transformations)
            
            # 1. Znalezienie pierwiastków
            roots = sp.solve(sp.Eq(expr_1, expr_2), x)
            real_roots = [r for r in roots if r.is_real]
            
            if len(real_roots) < 2:
                st.error("Funkcje nie domykają obszaru (brak dwóch punktów przecięcia).")
                st.stop()
                
            a, b = min(real_roots), max(real_roots)
            
            # ==========================================
            # AUTO-DETEKCJA GÓRA / DÓŁ
            # ==========================================
            midpoint = (a + b) / 2
            val1 = expr_1.subs(x, midpoint)
            val2 = expr_2.subs(x, midpoint)
            
            if val1 >= val2:
                f_top, f_bottom = expr_1, expr_2
                name_top, name_bottom = "f(x)", "g(x)"
            else:
                f_top, f_bottom = expr_2, expr_1
                name_top, name_bottom = "g(x)", "f(x)"
                st.success(f"🔄 **Auto-Korekta:** Wykryto, że w przedziale od {sp.latex(a)} do {sp.latex(b)} to funkcja **{name_top}** leży wyżej. Zmieniono kolejność w układaniu całki!")

            # --- START KARTKI Z ROZWIĄZANIEM ---
            st.subheader("Rozwiązanie do przepisania:")
            st.markdown("**Polecenie:** Oblicz pole obszaru ograniczonego krzywymi:")
            st.latex(rf"f(x) = {sp.latex(expr_1)} \quad \text{{oraz}} \quad g(x) = {sp.latex(expr_2)}")
            st.markdown("---")
            
            # KROK 1: SZCZEGÓŁOWE OBLICZENIA GRANIC
            st.markdown("**Krok 1: Wyznaczenie granic całkowania (punkty przecięcia)**")
            st.markdown("Przyrównujemy obie funkcje do siebie:")
            st.latex(rf"{sp.latex(expr_1)} = {sp.latex(expr_2)}")
            
            eq_diff = expr_1 - expr_2
            st.latex(rf"{sp.latex(eq_diff)} = 0")
            
            eq_simplified = sp.simplify(eq_diff)
            st.markdown("Po uporządkowaniu otrzymujemy:")
            st.latex(rf"{sp.latex(eq_simplified)} = 0")
            
            # Rozpisanie Delty
            is_quadratic = False
            try:
                poly = sp.Poly(eq_simplified, x)
                if poly.degree() == 2:
                    is_quadratic = True
                    coeffs = poly.all_coeffs()
                    A, B, C = coeffs[0], coeffs[1], coeffs[2]
                    
                    st.markdown("*Równanie kwadratowe:*")
                    st.latex(rf"A = {sp.latex(A)}, \quad B = {sp.latex(B)}, \quad C = {sp.latex(C)}")
                    
                    delta_val = B**2 - 4*A*C
                    st.latex(rf"\Delta = B^2 - 4AC = ({sp.latex(B)})^2 - 4 \cdot ({sp.latex(A)}) \cdot ({sp.latex(C)}) = {sp.latex(delta_val)}")
                    
                    if delta_val > 0:
                        sqrt_delta = sp.sqrt(delta_val)
                        st.latex(rf"\sqrt{{\Delta}} = {sp.latex(sqrt_delta)}")
                        x1_step = (-B - sqrt_delta) / (2*A)
                        x2_step = (-B + sqrt_delta) / (2*A)
                        st.latex(rf"x_1 = \frac{{-B - \sqrt{{\Delta}}}}{{2A}} = \frac{{-({sp.latex(B)}) - {sp.latex(sqrt_delta)}}}{{2 \cdot ({sp.latex(A)})}} = {sp.latex(sp.simplify(x1_step))}")
                        st.latex(rf"x_2 = \frac{{-B + \sqrt{{\Delta}}}}{{2A}} = \frac{{-({sp.latex(B)}) + {sp.latex(sqrt_delta)}}}{{2 \cdot ({sp.latex(A)})}} = {sp.latex(sp.simplify(x2_step))}")
                    elif delta_val == 0:
                        x0_step = -B / (2*A)
                        st.latex(rf"x_0 = \frac{{-B}}{{2A}} = {sp.latex(sp.simplify(x0_step))}")
            except:
                pass
            
            if not is_quadratic:
                st.markdown("*Rozwiązaniem równania są:*")
                st.latex(rf"x_1 = {sp.latex(a)}, \quad x_2 = {sp.latex(b)}")
                
            st.markdown("Granice całkowania: **$a = {} \ \ \text{{oraz}} \ \ b = {}$**".format(sp.latex(a), sp.latex(b)))
            st.markdown("---")
            
            # KROK 2: CAŁKA Z UWZGLĘDNIENIEM AUTO-DETEKCJI
            st.markdown(f"**Krok 2: Ułożenie całki oznaczonej (Góra - Dół)**")
            st.markdown(f"*Z wykresu/analizy widać, że funkcja {name_top} ogranicza obszar od góry.*")
            integrand = sp.simplify(f_top - f_bottom)
            integral_sym = sp.Integral(integrand, (x, a, b))
            st.latex(rf"P = \int_{{{sp.latex(a)}}}^{{{sp.latex(b)}}} \left[ {sp.latex(f_top)} - \left({sp.latex(f_bottom)}\right) \right] dx = {sp.latex(integral_sym)}")
            
            # KROK 3: FUNKCJA PIERWOTNA
            st.markdown("**Krok 3: Wyznaczenie funkcji pierwotnej**")
            F = sp.integrate(integrand, x)
            st.latex(rf"F(x) = \int \left({sp.latex(integrand)}\right) dx = {sp.latex(F)}")
            
            # KROK 4: NOWE, JAWDNE PODSTAWIENIE GRANIC (ZAMIAST F(b) - F(a))
            st.markdown("**Krok 4: Podstawienie granic (Wzór Newtona-Leibniza)**")
            st.markdown("Zgodnie ze wzorem podstawiamy granice całkowania do uzyskanej funkcji pierwotnej $F(x)$:")
            st.latex(rf"P = \left[ {sp.latex(F)} \right]_{{{sp.latex(a)}}}^{{{sp.latex(b)}}}")
            
            # Tworzenie jawnego podstawienia znak po znaku za pomocą zamiany zmiennej na stringa z nawiasem liczbym
            # Dla górnej granicy (b)
            F_b_expanded = F.subs(x, sp.Symbol(f'({sp.latex(b)})'))
            # Dla dolnej granicy (a)
            F_a_expanded = F.subs(x, sp.Symbol(f'({sp.latex(a)})'))
            
            st.markdown("Podstawiamy najpierw granicę górną, a następnie odejmujemy podstawienie granicy dolnej:")
            st.latex(rf"P = \left( {sp.latex(F_b_expanded)} \right) - \left( {sp.latex(F_a_expanded)} \right)")
            
            # Obliczenie wartości liczbowych dla każdego nawiasu oddzielnie
            F_b_computed = sp.simplify(F.subs(x, b))
            F_a_computed = sp.simplify(F.subs(x, a))
            st.markdown("Po wyliczeniu wartości poszczególnych nawiasów otrzymujemy:")
            st.latex(rf"P = \left( {sp.latex(F_b_computed)} \right) - \left( {sp.latex(F_a_computed)} \right)")
            
            # KROK 5: WYNIK KOŃCOWY
            st.markdown("**Krok 5: Wynik końcowy**")
            exact_area = sp.simplify(F_b_computed - F_a_computed)
            st.latex(rf"P = {sp.latex(exact_area)}")
            st.markdown("---")
            
            # KROK 6: WYKRES
            st.markdown("**Szkic pomocniczy obszaru:**")
            f_top_np = sp.lambdify(x, f_top, modules=['numpy'])
            f_bottom_np = sp.lambdify(x, f_bottom, modules=['numpy'])
            
            a_num, b_num = float(a.evalf()), float(b.evalf())
            margin = max((b_num - a_num) * 0.4, 1.0)
            x_vals = np.linspace(a_num - margin, b_num + margin, 400)
            
            fig, ax = plt.subplots(figsize=(7, 3.5))
            ax.plot(x_vals, np.vectorize(f_top_np)(x_vals), color='#2563eb', label=f'Góra: {name_top}')
            ax.plot(x_vals, np.vectorize(f_bottom_np)(x_vals), color='#dc2626', label=f'Dół: {name_bottom}')
            
            x_fill = np.linspace(a_num, b_num, 100)
            ax.fill_between(x_fill, np.vectorize(f_bottom_np)(x_fill), np.vectorize(f_top_np)(x_fill), color='#818cf8', alpha=0.3, label=f'P = {exact_area}')
            
            ax.axhline(0, color='black', linewidth=1)
            ax.axvline(0, color='black', linewidth=1)
            ax.grid(True, linestyle='--', alpha=0.4)
            ax.legend()
            
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"Błąd w zapisie matematycznym. Szczegóły: {e}")