import streamlit as st
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

st.set_page_config(page_title="Równania 2. Rzędu", layout="wide")

st.title("📈 Zadanie 5: Równania Różniczkowe 2. Rzędu")
st.markdown("Automatyczny gotowiec dla równań rzędu drugiego. Zawiera różne metody w zależności od typu równania.")
st.markdown("---")

x = sp.Symbol('x')
r = sp.Symbol('r')
C1, C2 = sp.symbols('C_1 C_2')
transformations = standard_transformations + (implicit_multiplication_application,)

tab1, tab2, tab3 = st.tabs([
    "📌 Postać y'' = f(x)", 
    "📌 Równanie charakterystyczne (COR)",
    "📌 Równanie charakterystyczne + Warunki (CSR)"
])

# ==========================================
# TAB 1: Podwójne całkowanie
# ==========================================
with tab1:
    st.subheader("Wybierz zadanie z listy lub wprowadź własne:")
    
    zadania = {
        "Zadanie 1.1: y'' = 12x^2 | y(1)=2, y'(1)=4": {"f": "12*x**2", "c1_t": "y", "c1_x": "1", "c1_v": "2", "c2_t": "y'", "c2_x": "1", "c2_v": "4"},
        "Zadanie 1.2: y'' = -24x | y(1)=-4, y'(1)=2": {"f": "-24*x", "c1_t": "y", "c1_x": "1", "c1_v": "-4", "c2_t": "y'", "c2_x": "1", "c2_v": "2"},
        "Zadanie 1.3: y'' = -18x | y(0)=6, y'(0)=4": {"f": "-18*x", "c1_t": "y", "c1_x": "0", "c1_v": "6", "c2_t": "y'", "c2_x": "0", "c2_v": "4"},
        "Zadanie 1.4: y'' = 2cos(x) | y(pi/2)=1, y'(pi/2)=6": {"f": "2*cos(x)", "c1_t": "y", "c1_x": "pi/2", "c1_v": "1", "c2_t": "y'", "c2_x": "pi/2", "c2_v": "6"},
        "Zadanie 1.5: y'' = 6sin(2x) | y(0)=2, y(pi)=0": {"f": "6*sin(2*x)", "c1_t": "y", "c1_x": "0", "c1_v": "2", "c2_t": "y", "c2_x": "pi", "c2_v": "0"},
        "Zadanie 1.6: y'' = 12e^(2x) | y(0)=2, y'(0)=4": {"f": "12*exp(2*x)", "c1_t": "y", "c1_x": "0", "c1_v": "2", "c2_t": "y'", "c2_x": "0", "c2_v": "4"},
        "Zadanie 1.7: y'' = -1/x^2 | y(1)=2, y'(1)=4": {"f": "-1/x**2", "c1_t": "y", "c1_x": "1", "c1_v": "2", "c2_t": "y'", "c2_x": "1", "c2_v": "4"},
        "Zadanie 1.8: y'' = 12/x^3 | y(1)=2, y'(1)=4": {"f": "12/x**3", "c1_t": "y", "c1_x": "1", "c1_v": "2", "c2_t": "y'", "c2_x": "1", "c2_v": "4"},
        "Zadanie 1.9: y'' = 1/x | y(1)=2, y'(1)=-4": {"f": "1/x", "c1_t": "y", "c1_x": "1", "c1_v": "2", "c2_t": "y'", "c2_x": "1", "c2_v": "-4"},
        "✨ Własny przykład...": {"f": "WLASNY", "c1_t": "y", "c1_x": "0", "c1_v": "0", "c2_t": "y'", "c2_x": "0", "c2_v": "0"}
    }
    
    wybor = st.selectbox("Zadania ze skanu (Część 1):", list(zadania.keys()), key="sel_tab1")
    data = zadania[wybor]
    
    if data["f"] == "WLASNY":
        f_str = st.text_input("Prawa strona równania y'' = f(x):", "12*x**2")
        st.markdown("**Warunek 1:**")
        col1, col2, col3 = st.columns([1, 2, 2])
        c1_t = col1.selectbox("Typ", ["y", "y'"], key="t1")
        c1_x = col2.text_input("Punkt x0 =", "1", key="x1")
        c1_v = col3.text_input("Wartość =", "2", key="v1")
        
        st.markdown("**Warunek 2:**")
        col4, col5, col6 = st.columns([1, 2, 2])
        c2_t = col4.selectbox("Typ", ["y'", "y"], key="t2")
        c2_x = col5.text_input("Punkt x1 =", "1", key="x2")
        c2_v = col6.text_input("Wartość =", "4", key="v2")
    else:
        f_str = data["f"]
        c1_t, c1_x, c1_v = data["c1_t"], data["c1_x"], data["c1_v"]
        c2_t, c2_x, c2_v = data["c2_t"], data["c2_x"], data["c2_v"]
        st.code(f"y'' = {f_str}  |  {c1_t}({c1_x}) = {c1_v}  |  {c2_t}({c2_x}) = {c2_v}")

    if st.button("📝 Generuj podwójne całkowanie", type="primary", key="btn_tab1"):
        try:
            f_x = parse_expr(f_str.replace('^', '**'), transformations=transformations)
            x0_1 = parse_expr(c1_x.replace('^', '**'), transformations=transformations)
            v0_1 = parse_expr(c1_v.replace('^', '**'), transformations=transformations)
            x0_2 = parse_expr(c2_x.replace('^', '**'), transformations=transformations)
            v0_2 = parse_expr(c2_v.replace('^', '**'), transformations=transformations)
            
            st.markdown("---")
            st.markdown("### 📝 Rozwiązanie krok po kroku:")
            st.latex(rf"y^{{\prime\prime}} = {sp.latex(f_x)}")
            st.markdown("---")
            
            st.markdown("**Krok 1: Pierwsze całkowanie obustronne (wyznaczenie $y'$)**")
            st.latex(rf"y^{{\prime}} = \int y^{{\prime\prime}} \, dx = \int \left({sp.latex(f_x)}\right) dx")
            y_prime_int = sp.integrate(f_x, x)
            y_prime = y_prime_int + C1
            y_prime_latex = sp.latex(y_prime).replace(r"\log", r"\ln")
            st.latex(rf"y^{{\prime}}(x) = {y_prime_latex}")
            st.markdown("---")
            
            st.markdown("**Krok 2: Drugie całkowanie obustronne (wyznaczenie COR)**")
            st.latex(rf"y = \int y^{{\prime}} \, dx = \int \left({y_prime_latex}\right) dx")
            y_int = sp.integrate(y_prime_int, x)
            y_gen = y_int + C1*x + C2
            y_gen_latex = sp.latex(y_gen).replace(r"\log", r"\ln")
            st.latex(rf"y(x) = {y_gen_latex}")
            st.markdown("---")
            
            st.markdown("**Krok 3: Wyznaczenie stałych $C_1$ i $C_2$ z warunków**")
            eqs = []
            eq_latex = []
            
            if c1_t == "y":
                val_sub = y_gen.subs(x, x0_1)
                eqs.append(sp.Eq(val_sub, v0_1))
                eq_latex.append(rf"{sp.latex(v0_1)} = {sp.latex(val_sub)}")
            else:
                val_sub = y_prime.subs(x, x0_1)
                eqs.append(sp.Eq(val_sub, v0_1))
                eq_latex.append(rf"{sp.latex(v0_1)} = {sp.latex(val_sub)}")
                
            if c2_t == "y":
                val_sub = y_gen.subs(x, x0_2)
                eqs.append(sp.Eq(val_sub, v0_2))
                eq_latex.append(rf"{sp.latex(v0_2)} = {sp.latex(val_sub)}")
            else:
                val_sub = y_prime.subs(x, x0_2)
                eqs.append(sp.Eq(val_sub, v0_2))
                eq_latex.append(rf"{sp.latex(v0_2)} = {sp.latex(val_sub)}")
            
            st.latex(rf"\begin{{cases}} {eq_latex[0]} \\ {eq_latex[1]} \end{{cases}}")
            solutions = sp.solve(eqs, (C1, C2))
            
            if solutions:
                c1_val = solutions[C1]
                c2_val = solutions[C2]
                st.latex(rf"C_1 = {sp.latex(c1_val)}, \quad C_2 = {sp.latex(c2_val)}")
                st.markdown("---")
                st.markdown("**Krok 4: Całka Szczególna Równania (Wzór ostateczny)**")
                y_final = y_gen.subs({C1: c1_val, C2: c2_val})
                y_final_latex = sp.latex(y_final).replace(r"\log", r"\ln")
                st.latex(rf"y(x) = {y_final_latex}")
                st.success("✔ Pełne rozwiązanie rzędu drugiego rozpisane!")
            else:
                st.warning("Nie udało się wyznaczyć stałych. Sprawdź warunki.")
        except Exception as e:
            st.error(f"Wystąpił błąd: {e}")

# ==========================================
# TAB 2: Równanie charakterystyczne (Bez warunków)
# ==========================================
with tab2:
    st.subheader("Rozwiązywanie równań jednorodnych (Postać ogólna COR):")
    
    zadania_2 = {
        "Zadanie 2.1: y'' + 4y' + 4y = 0": {"a": "1", "b": "4", "c": "4"},
        "Zadanie 2.2: y'' - 16y' + 64y = 0": {"a": "1", "b": "-16", "c": "64"},
        "Zadanie 2.3: y'' + 2√2y' + 2y = 0": {"a": "1", "b": "2*sqrt(2)", "c": "2"},
        "Zadanie 2.4: y'' - y' - 12y = 0": {"a": "1", "b": "-1", "c": "-12"},
        "Zadanie 2.5: y'' - 3y' = 0": {"a": "1", "b": "-3", "c": "0"},
        "Zadanie 2.6: y'' - 4y' - 12y = 0": {"a": "1", "b": "-4", "c": "-12"},
        "Zadanie 2.7: y'' + y' - 2y = 0": {"a": "1", "b": "1", "c": "-2"},
        "Zadanie 2.8: y'' - 2√3y' + 3y = 0": {"a": "1", "b": "-2*sqrt(3)", "c": "3"},
        "Zadanie 2.9: y'' + 2y' - 8y = 0": {"a": "1", "b": "2", "c": "-8"},
        "✨ Własny przykład...": {"a": "1", "b": "0", "c": "1"}
    }
    
    wybor_2 = st.selectbox("Zadania ze skanu (Część 2):", list(zadania_2.keys()), key="sel_tab2")
    data_2 = zadania_2[wybor_2]
    
    if wybor_2 == "✨ Własny przykład...":
        st.markdown("Wprowadź współczynniki dla równania postaci $ay'' + by' + cy = 0$")
        col_a, col_b, col_c = st.columns(3)
        a_str = col_a.text_input("a =", "1")
        b_str = col_b.text_input("b =", "2")
        c_str = col_c.text_input("c =", "1")
    else:
        a_str, b_str, c_str = data_2["a"], data_2["b"], data_2["c"]
        b_znak = "+" if not b_str.startswith("-") else ""
        c_znak = "+" if not c_str.startswith("-") else ""
        eq_preview = f"{a_str}y'' {b_znak} {b_str}y' {c_znak} {c_str}y = 0".replace("1y", "y").replace("+ -", "- ")
        st.code(f"Rozwiązujemy: {eq_preview}")

    if st.button("📝 Generuj COR", type="primary", key="btn_tab2"):
        try:
            a_val = parse_expr(a_str, transformations=transformations)
            b_val = parse_expr(b_str, transformations=transformations)
            c_val = parse_expr(c_str, transformations=transformations)
            
            st.markdown("---")
            st.markdown("### 📝 Rozwiązanie krok po kroku:")
            
            st.markdown("**Krok 1: Układamy równanie charakterystyczne**")
            char_eq = a_val*r**2 + b_val*r + c_val
            st.latex(rf"{sp.latex(char_eq)} = 0")
            
            st.markdown("**Krok 2: Obliczamy wyróżnik (Deltę)**")
            delta = sp.simplify(b_val**2 - 4*a_val*c_val)
            
            b_tex = f"({sp.latex(b_val)})" if b_val < 0 or "sqrt" in b_str else sp.latex(b_val)
            a_tex = f"({sp.latex(a_val)})" if a_val < 0 else sp.latex(a_val)
            c_tex = f"({sp.latex(c_val)})" if c_val < 0 else sp.latex(c_val)
            
            st.latex(rf"\Delta = {b_tex}^2 - 4 \cdot {a_tex} \cdot {c_tex} = {sp.latex(delta)}")
            delta_val = float(delta)
            
            st.markdown("**Krok 3: Wyznaczamy pierwiastki i zapisujemy Całkę Ogólną Równania (COR)**")
            
            if delta_val > 0:
                r1 = sp.simplify((-b_val - sp.sqrt(delta))/(2*a_val))
                r2 = sp.simplify((-b_val + sp.sqrt(delta))/(2*a_val))
                st.latex(rf"r_1 = {sp.latex(r1)}, \quad r_2 = {sp.latex(r2)}")
                y_gen = C1*sp.exp(r1*x) + C2*sp.exp(r2*x)
                st.latex(rf"\text{{COR:}} \quad y(x) = {sp.latex(y_gen)}")
            elif delta_val == 0:
                r0 = sp.simplify(-b_val/(2*a_val))
                st.latex(rf"r_0 = {sp.latex(r0)}")
                y_gen = (C1 + C2*x)*sp.exp(r0*x)
                st.latex(rf"\text{{COR:}} \quad y(x) = {sp.latex(y_gen)}")
            else:
                alpha = sp.simplify(-b_val/(2*a_val))
                beta = sp.simplify(sp.sqrt(-delta)/(2*a_val))
                st.latex(rf"\alpha = {sp.latex(alpha)}, \quad \beta = {sp.latex(beta)}")
                st.latex(rf"r_{{1,2}} = {sp.latex(alpha)} \pm {sp.latex(beta)} i")
                y_gen = sp.exp(alpha*x)*(C1*sp.cos(beta*x) + C2*sp.sin(beta*x))
                st.latex(rf"\text{{COR:}} \quad y(x) = {sp.latex(y_gen)}")
                
            st.success("✔ Równanie charakterystyczne rozwiązane!")
        except Exception as e:
            st.error(f"Wystąpił błąd: {e}")

# ==========================================
# TAB 3: Równanie charakterystyczne z warunkami (CSR)
# ==========================================
with tab3:
    st.subheader("Wyznaczanie Całki Szczególnej (Zagadnienie Cauchy'ego / Brzegowe):")
    
    zadania_3 = {
        "Zadanie 3.1: y'' + 4y = 0 | y(pi/2)=2, y'(pi/2)=-2": {"a":"1", "b":"0", "c":"4", "c1_t":"y", "c1_x":"pi/2", "c1_v":"2", "c2_t":"y'", "c2_x":"pi/2", "c2_v":"-2"},
        "Zadanie 3.2: y'' + 36y = 0 | y(pi/12)=4, y'(pi/12)=0": {"a":"1", "b":"0", "c":"36", "c1_t":"y", "c1_x":"pi/12", "c1_v":"4", "c2_t":"y'", "c2_x":"pi/12", "c2_v":"0"},
        "Zadanie 3.3: y'' + 100y = 0 | y(pi/20)=-6, y'(pi/20)=2": {"a":"1", "b":"0", "c":"100", "c1_t":"y", "c1_x":"pi/20", "c1_v":"-6", "c2_t":"y'", "c2_x":"pi/20", "c2_v":"2"},
        "Zadanie 3.4: y'' + y = 0 | y(pi/2)=4, y'(pi/2)=-2": {"a":"1", "b":"0", "c":"1", "c1_t":"y", "c1_x":"pi/2", "c1_v":"4", "c2_t":"y'", "c2_x":"pi/2", "c2_v":"-2"},
        "Zadanie 3.5: y'' + 2y' = 0 | y(0)=2, y'(0)=6": {"a":"1", "b":"2", "c":"0", "c1_t":"y", "c1_x":"0", "c1_v":"2", "c2_t":"y'", "c2_x":"0", "c2_v":"6"},
        "Zadanie 3.6: y'' - 5y' = 0 | y(0)=2, y(2)=-4": {"a":"1", "b":"-5", "c":"0", "c1_t":"y", "c1_x":"0", "c1_v":"2", "c2_t":"y", "c2_x":"2", "c2_v":"-4"},
        "Zadanie 3.7: y'' + pi^2*y = 0 | y(1)=2, y'(1)=6": {"a":"1", "b":"0", "c":"pi**2", "c1_t":"y", "c1_x":"1", "c1_v":"2", "c2_t":"y'", "c2_x":"1", "c2_v":"6"},
        "Zadanie 3.8: y'' + y = 0 | y(pi/2)=0, y'(pi/2)=2": {"a":"1", "b":"0", "c":"1", "c1_t":"y", "c1_x":"pi/2", "c1_v":"0", "c2_t":"y'", "c2_x":"pi/2", "c2_v":"2"},
        "Zadanie 3.9: y'' + 7y = 0 | y(pi/√7)=0, y(pi/2√7)=4": {"a":"1", "b":"0", "c":"7", "c1_t":"y", "c1_x":"pi/sqrt(7)", "c1_v":"0", "c2_t":"y", "c2_x":"pi/(2*sqrt(7))", "c2_v":"4"},
        "✨ Własny przykład...": {"a":"1", "b":"0", "c":"1", "c1_t":"y", "c1_x":"0", "c1_v":"0", "c2_t":"y'", "c2_x":"0", "c2_v":"0"}
    }
    
    wybor_3 = st.selectbox("Zadania ze skanu (Część 3):", list(zadania_3.keys()), key="sel_tab3")
    data_3 = zadania_3[wybor_3]
    
    if data_3["a"] == "WLASNY":
        st.markdown("**Współczynniki równania $ay'' + by' + cy = 0$:**")
        col_a, col_b, col_c = st.columns(3)
        a_str = col_a.text_input("a =", "1", key="a3")
        b_str = col_b.text_input("b =", "0", key="b3")
        c_str = col_c.text_input("c =", "1", key="c3")
        
        st.markdown("**Warunek 1:**")
        col1, col2, col3 = st.columns([1, 2, 2])
        c1_t = col1.selectbox("Typ", ["y", "y'"], key="t1_3")
        c1_x = col2.text_input("Punkt x0 =", "0", key="x1_3")
        c1_v = col3.text_input("Wartość =", "1", key="v1_3")
        
        st.markdown("**Warunek 2:**")
        col4, col5, col6 = st.columns([1, 2, 2])
        c2_t = col4.selectbox("Typ", ["y'", "y"], key="t2_3")
        c2_x = col5.text_input("Punkt x1 =", "0", key="x2_3")
        c2_v = col6.text_input("Wartość =", "0", key="v2_3")
    else:
        a_str, b_str, c_str = data_3["a"], data_3["b"], data_3["c"]
        c1_t, c1_x, c1_v = data_3["c1_t"], data_3["c1_x"], data_3["c1_v"]
        c2_t, c2_x, c2_v = data_3["c2_t"], data_3["c2_x"], data_3["c2_v"]
        
        b_znak = "+" if not b_str.startswith("-") else ""
        c_znak = "+" if not c_str.startswith("-") else ""
        eq_preview = f"{a_str}y'' {b_znak} {b_str}y' {c_znak} {c_str}y = 0".replace("1y", "y").replace("+ -", "- ")
        st.code(f"Rozwiązujemy: {eq_preview}  |  {c1_t}({c1_x}) = {c1_v}  |  {c2_t}({c2_x}) = {c2_v}")

    if st.button("📝 Generuj CSR", type="primary", key="btn_tab3"):
        try:
            a_val = parse_expr(a_str, transformations=transformations)
            b_val = parse_expr(b_str, transformations=transformations)
            c_val = parse_expr(c_str, transformations=transformations)
            
            x0_1 = parse_expr(c1_x.replace('^', '**'), transformations=transformations)
            v0_1 = parse_expr(c1_v.replace('^', '**'), transformations=transformations)
            x0_2 = parse_expr(c2_x.replace('^', '**'), transformations=transformations)
            v0_2 = parse_expr(c2_v.replace('^', '**'), transformations=transformations)
            
            st.markdown("---")
            st.markdown("### 📝 Rozwiązanie krok po kroku:")
            
            # KROK 1 i 2 (Wspólne z COR)
            st.markdown("**Krok 1: Równanie charakterystyczne i wyznaczenie wzoru ogólnego**")
            char_eq = a_val*r**2 + b_val*r + c_val
            delta = sp.simplify(b_val**2 - 4*a_val*c_val)
            delta_val = float(delta)
            
            if delta_val > 0:
                r1 = sp.simplify((-b_val - sp.sqrt(delta))/(2*a_val))
                r2 = sp.simplify((-b_val + sp.sqrt(delta))/(2*a_val))
                y_gen = C1*sp.exp(r1*x) + C2*sp.exp(r2*x)
            elif delta_val == 0:
                r0 = sp.simplify(-b_val/(2*a_val))
                y_gen = (C1 + C2*x)*sp.exp(r0*x)
            else:
                alpha = sp.simplify(-b_val/(2*a_val))
                beta = sp.simplify(sp.sqrt(-delta)/(2*a_val))
                y_gen = sp.exp(alpha*x)*(C1*sp.cos(beta*x) + C2*sp.sin(beta*x))
            
            st.latex(rf"\text{{Otrzymujemy COR:}} \quad y(x) = {sp.latex(y_gen)}")
            
            # KROK 3: Pochodna COR (Zawsze warto ją policzyć dla bezpieczeństwa)
            st.markdown("**Krok 2: Obliczamy pochodną $y'(x)$ ze wzoru ogólnego**")
            y_prime = sp.diff(y_gen, x)
            st.latex(rf"y^{{\prime}}(x) = {sp.latex(y_prime)}")
            
            # KROK 4: Budowa układu równań
            st.markdown("**Krok 3: Układamy układ równań z warunków początkowych/brzegowych**")
            eqs = []
            eq_latex = []
            
            if c1_t == "y":
                val_sub = sp.simplify(y_gen.subs(x, x0_1))
                eqs.append(sp.Eq(val_sub, v0_1))
                eq_latex.append(rf"{sp.latex(v0_1)} = {sp.latex(val_sub)}")
            else:
                val_sub = sp.simplify(y_prime.subs(x, x0_1))
                eqs.append(sp.Eq(val_sub, v0_1))
                eq_latex.append(rf"{sp.latex(v0_1)} = {sp.latex(val_sub)}")
                
            if c2_t == "y":
                val_sub = sp.simplify(y_gen.subs(x, x0_2))
                eqs.append(sp.Eq(val_sub, v0_2))
                eq_latex.append(rf"{sp.latex(v0_2)} = {sp.latex(val_sub)}")
            else:
                val_sub = sp.simplify(y_prime.subs(x, x0_2))
                eqs.append(sp.Eq(val_sub, v0_2))
                eq_latex.append(rf"{sp.latex(v0_2)} = {sp.latex(val_sub)}")
            
            st.latex(rf"\begin{{cases}} {eq_latex[0]} \\ {eq_latex[1]} \end{{cases}}")
            
            # KROK 5: Wyliczenie stałych i wynik ostateczny
            solutions = sp.solve(eqs, (C1, C2))
            
            if solutions:
                c1_val = sp.simplify(solutions[C1])
                c2_val = sp.simplify(solutions[C2])
                st.markdown("Rozwiązując ten układ równań wyznaczamy stałe:")
                st.latex(rf"C_1 = {sp.latex(c1_val)}, \quad C_2 = {sp.latex(c2_val)}")
                
                st.markdown("---")
                st.markdown("**Krok 4: Całka Szczególna Równania (CSR)**")
                y_final = sp.simplify(y_gen.subs({C1: c1_val, C2: c2_val}))
                st.latex(rf"y(x) = {sp.latex(y_final)}")
                st.success("✔ Zagadnienie dla równania o stałych współczynnikach rozpisane pomyślnie!")
            else:
                st.warning("Nie udało się rozwiązać układu dla podanych warunków.")
                
        except Exception as e:
            st.error(f"Wystąpił błąd podczas podstawiania: {e}")