import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

# Ustawienia strony
st.set_page_config(page_title="Gotowiec - Objętość", layout="wide", initial_sidebar_state="expanded")
st.sidebar.title("🧭 Nawigacja")
st.sidebar.markdown("---")

st.title("🎓 Gotowiec: Objętość bryły obrotowej (V_ox)")
st.markdown("Ten moduł oblicza objętość bryły powstałej przez obrót funkcji wokół osi $OX$ w przedziale $[a, b]$.")
st.markdown("---")

transformations = standard_transformations + (implicit_multiplication_application,)
x = sp.Symbol('x')

col_input, col_output = st.columns([1, 2], gap="large")

with col_input:
    st.subheader("Wprowadź dane z zadania")
    str_f = st.text_input("Funkcja f(x):", "1/2 * x^2")
    
    col_a, col_b = st.columns(2)
    with col_a:
        str_a = st.text_input("Dolna granica a:", "0")
    with col_b:
        str_b = st.text_input("Górna granica b:", "4")
        
    st.info("💡 Wzór podstawowy: $V_{ox} = \pi \int_{a}^{b} [f(x)]^2 dx$")
    generuj = st.button("📝 Generuj rozwiązanie", type="primary", use_container_width=True)

with col_output:
    if generuj:
        try:
            f = parse_expr(str_f.replace('^', '**'), transformations=transformations)
            a = parse_expr(str_a, transformations=transformations)
            b = parse_expr(str_b, transformations=transformations)
            
            # --- START KARTKI Z ROZWIĄZANIEM ---
            st.subheader("Rozwiązanie do przepisania:")
            st.markdown("**Polecenie:** Oblicz objętość bryły powstałej przez obrót wokół osi $OX$ krzywej:")
            st.latex(rf"f(x) = {sp.latex(f)} \quad \text{{dla}} \quad x \in [{sp.latex(a)}, {sp.latex(b)}]")
            st.markdown("---")
            
            # KROK 1
            st.markdown("**Krok 1: Wyznaczenie kwadratu funkcji $[f(x)]^2$**")
            f_sq = sp.simplify(f**2)
            st.latex(rf"[f(x)]^2 = \left( {sp.latex(f)} \right)^2 = {sp.latex(f_sq)}")
            
            # KROK 2
            st.markdown("**Krok 2: Ułożenie całki na objętość $V_{ox}$**")
            integral_sym = sp.Integral(f_sq, (x, a, b))
            st.latex(rf"V_{{ox}} = \pi \int_{{{sp.latex(a)}}}^{{{sp.latex(b)}}} {sp.latex(f_sq)} dx")
            
            # KROK 3
            st.markdown("**Krok 3: Wyznaczenie funkcji pierwotnej**")
            F = sp.integrate(f_sq, x)
            st.latex(rf"F(x) = \int {sp.latex(f_sq)} dx = {sp.latex(F)}")
            
            # KROK 4
            st.markdown("**Krok 4: Podstawienie granic (Wzór Newtona-Leibniza)**")
            st.latex(rf"V_{{ox}} = \pi \cdot \left[ {sp.latex(F)} \right]_{{{sp.latex(a)}}}^{{{sp.latex(b)}}}")
            
            F_b_exp = F.subs(x, sp.Symbol(f'({sp.latex(b)})'))
            F_a_exp = F.subs(x, sp.Symbol(f'({sp.latex(a)})'))
            st.latex(rf"V_{{ox}} = \pi \cdot \left[ \left( {sp.latex(F_b_exp)} \right) - \left( {sp.latex(F_a_exp)} \right) \right]")
            
            F_b_val = sp.simplify(F.subs(x, b))
            F_a_val = sp.simplify(F.subs(x, a))
            st.latex(rf"V_{{ox}} = \pi \cdot \left( {sp.latex(F_b_val)} - {sp.latex(F_a_val)} \right)")
            
            # KROK 5
            st.markdown("**Krok 5: Wynik końcowy**")
            final_integral = sp.simplify(F_b_val - F_a_val)
            final_v = final_integral * sp.pi
            
            st.latex(rf"V_{{ox}} = {sp.latex(final_v)}")
            
            v_numeric = float(final_v.evalf())
            st.write(f"Przybliżenie dziesiętne: $V \approx {v_numeric:.4f} \ [j^3]$")
            st.markdown("---")
            
            # KROK 6: Zaktualizowany wykres z pionowymi granicami
            st.markdown("**Szkic przekroju bryły obrotowej z zaznaczonymi granicami cięcia:**")
            f_np = sp.lambdify(x, f, modules=['numpy'])
            
            a_n, b_n = float(a.evalf()), float(b.evalf())
            
            # Dodajemy szerokie marginesy, żeby było widać zachowanie funkcji poza granicami
            margin = max((b_n - a_n) * 0.25, 1.0)
            x_plot = np.linspace(a_n - margin, b_n + margin, 400)
            y_plot = np.vectorize(f_np)(x_plot)
            
            fig, ax = plt.subplots(figsize=(8, 4.5))
            
            # Rysujemy funkcję i jej odbicie w szerszym zakresie
            ax.plot(x_plot, y_plot, color='#2563eb', linewidth=2, label='Krzywa f(x)')
            ax.plot(x_plot, -y_plot, color='#2563eb', linestyle='--', linewidth=1.5, alpha=0.4, label='Odbicie (obrót)')
            
            # ZAZNACZENIE GRANIC (Pionowe linie)
            ax.axvline(a_n, color='#d97706', linestyle='-.', linewidth=2.5, label=f'Granica a = {a_n}')
            ax.axvline(b_n, color='#d97706', linestyle='-.', linewidth=2.5, label=f'Granica b = {b_n}')
            
            # Wypełniamy tylko pole MIĘDZY granicami (nasza wyliczona bryła)
            x_fill = np.linspace(a_n, b_n, 200)
            y_fill = np.vectorize(f_np)(x_fill)
            ax.fill_between(x_fill, y_fill, -y_fill, color='#818cf8', alpha=0.25, label='Objętość bryły')
            
            ax.axhline(0, color='black', linewidth=1)
            ax.axvline(0, color='black', linewidth=1)
            ax.set_title("Wizualizacja cięcia bryły obrotowej", fontweight='bold')
            ax.grid(True, linestyle=':', alpha=0.6)
            
            # Przesunięcie legendy, żeby nie zasłaniała bryły
            ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
            
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"Błąd przetwarzania: {e}")