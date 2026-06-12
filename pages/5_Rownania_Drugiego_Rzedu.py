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

# DEFINICJA ZAKŁADEK (bez tego wywala błąd!)
tab1, tab2, tab3 = st.tabs([
    "📌 Postać y'' = f(x)", 
    "📌 Równanie charakterystyczne (COR)",
    "📌 Równanie charakterystyczne + Warunki (CSR)"
])

# ==========================================
# TAB 1: Postać y'' = f(x) (Podwójne całkowanie krok po kroku z rozpisaniem algebry)
# ==========================================
with tab1:
    st.subheader("Podwójne całkowanie z pełnym opisem etapów i obliczeń (Zadania nr 1):")
    
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
    
    wybor = st.selectbox("Wybierz zadanie z listy lub opcję własną:", list(zadania.keys()), key="sel_tab1")
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

    if st.button("📝 Generuj szczegółowy protokół kolokwialny (Tab 1)", type="primary", key="btn_tab1"):
        try:
            f_x = parse_expr(f_str.replace('^', '**'), transformations=transformations)
            x0_1 = parse_expr(c1_x.replace('^', '**'), transformations=transformations)
            v0_1 = parse_expr(c1_v.replace('^', '**'), transformations=transformations)
            x0_2 = parse_expr(c2_x.replace('^', '**'), transformations=transformations)
            v0_2 = parse_expr(c2_v.replace('^', '**'), transformations=transformations)
            
            st.markdown("---")
            st.markdown("## 📝 Szczegółowy Protokół Rozwiązania")
            
            # ==========================================
            # WSTĘP
            # ==========================================
            st.markdown("### 🔹 Wstęp")
            st.markdown("Rozpatrujemy równanie różniczkowe zwyczajne rzędu drugiego, w którym druga pochodna poszukiwanej funkcji jest bezpośrednią funkcją zmiennej niezależnej $x$. Zapisujemy równanie w postaci wyjściowej:")
            st.latex(rf"y^{{\prime\prime}} = {sp.latex(f_x)}")
            
            st.markdown("Zadanie obwarowane jest dwoma warunkami granicznymi, które pozwolą na jednoznaczne wyznaczenie stałych całkowania w dalszej części protokołu:")
            st.latex(rf"\begin{{cases}} {c1_t}({sp.latex(x0_1)}) = {sp.latex(v0_1)} \\ {c2_t}({sp.latex(x0_2)}) = {sp.latex(v0_2)} \end{{cases}}")
            
            # ==========================================
            # ETAP 1
            # ==========================================
            st.markdown("### 🔹 ETAP 1: Pierwsze całkowanie (wyznaczenie równania pierwszej pochodnej)")
            st.markdown("Ponieważ druga pochodna to z definicji pochodna z pierwszej pochodnej, czyli $\\frac{d(y')}{dx}$, możemy obniżyć rząd równania poprzez obustronne nałożenie całki nieoznaczonej względem zmiennej $x$:")
            st.latex(rf"y^{{\prime}}(x) = \int y^{{\prime\prime}} \, dx = \int \left({sp.latex(f_x)}\right) dx")
            
            y_prime_int = sp.integrate(f_x, x)
            y_prime = y_prime_int + C1
            y_prime_latex = sp.latex(y_prime).replace(r"\log", r"\ln")
            
            st.markdown("Po obliczeniu całki z funkcji składowej dopisujemy pierwszą niezależną stałą całkowania $C_1$. Otrzymujemy jawną postać równania pierwszej pochodnej:")
            st.latex(rf"y^{{\prime}}(x) = {y_prime_latex}")
            
            # ==========================================
            # ETAP 2
            # ==========================================
            st.markdown("### 🔹 ETAP 2: Drugie całkowanie oraz wyznaczenie stałych strukturalnych")
            st.markdown("Aby przejść od równania pierwszej pochodnej $y'(x) = \\frac{dy}{dx}$ do czystej funkcji $y(x)$, ponownie nakładamy obustronnie całkę nieoznaczoną względem zmiennej $x$:")
            st.latex(rf"y(x) = \int y^{{\prime}}(x) \, dx = \int \left({y_prime_latex}\right) dx")
            
            y_int = sp.integrate(y_prime_int, x)
            y_gen = y_int + C1*x + C2
            y_gen_latex = sp.latex(y_gen).replace(r"\log", r"\ln")
            
            st.markdown("Wykonując całkowanie wyraz po wyrazie i wprowadzając drugą niezależną stałą całkowania $C_2$, uzyskujemy pełną postać Całki Ogólnej Równania (COR):")
            st.latex(rf"y(x) = {y_gen_latex}")
            
            st.markdown("W celu wyznaczenia konkretnych wartości stałych $C_1$ i $C_2$, podstawiamy dane z warunków granicznych do otrzymanych struktur na $y(x)$ oraz $y'(x)$:")
            
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
            
            st.markdown("Konstruujemy układ dwóch równań liniowych z dwiema niewiadomymi:")
            st.latex(rf"\begin{{cases}} {eq_latex[0]} \\ {eq_latex[1]} \end{{cases}}")
            
            # --- ROZPISANIE OBLICZEŃ UKŁADU KROK PO KROKU ---
            solutions = sp.solve(eqs, (C1, C2))
            
            if solutions:
                c1_val = solutions[C1]
                c2_val = solutions[C2]
                
                st.markdown("#### 🧮 Obliczenia algebraiczne stałych (Krok po kroku):")
                
                # Definiujemy zmienne pomocnicze do wykrycia struktury układu
                eq_y_prime = None
                v_y_prime = None
                x_y_prime = None
                eq_y = None
                v_y = None
                x_y = None
                
                if c1_t == "y'":
                    eq_y_prime = y_prime.subs(x, x0_1)
                    v_y_prime = v0_1
                    x_y_prime = x0_1
                    eq_y = y_gen.subs(x, x0_2)
                    v_y = v0_2
                    x_y = x0_2
                elif c2_t == "y'":
                    eq_y_prime = y_prime.subs(x, x0_2)
                    v_y_prime = v0_2
                    x_y_prime = x0_2
                    eq_y = y_gen.subs(x, x0_1)
                    v_y = v0_1
                    x_y = x0_1
                
                if eq_y_prime is not None:
                    # PRZYPADEK CAUCHY'EGO: Jedno z równań ma tylko C1 (pochodzi z pochodnej)
                    st.markdown(f"1. Wybieramy równanie wynikające z warunku dla pierwszej pochodnej ${c1_t if c1_t == 'y' else c2_t}({sp.latex(x_y_prime)}) = {sp.latex(v_y_prime)}$, ponieważ zawiera ono wyłącznie jedną niewiadomą ($C_1$):")
                    st.latex(rf"{sp.latex(v_y_prime)} = {sp.latex(eq_y_prime)}")
                    
                    rest_c1 = sp.simplify(eq_y_prime - C1)
                    st.markdown("Przenosimy znaną wartość całki na lewą stronę, aby wyizolować stałą $C_1$:")
                    st.latex(rf"C_1 = {sp.latex(v_y_prime)} - \left({sp.latex(rest_c1)}\right)")
                    st.latex(rf"C_1 = {sp.latex(c1_val)}")
                    
                    st.markdown(f"2. Podstawiamy obliczoną wartość $C_1 = {sp.latex(c1_val)}$ oraz warunek dla funkcji głównej $y({sp.latex(x_y)}) = {sp.latex(v_y)}$ do drugiego równania układu:")
                    eq_y_substituted = eq_y.subs(C1, c1_val)
                    st.latex(rf"{sp.latex(v_y)} = {sp.latex(eq_y_substituted)}")
                    
                    rest_c2 = sp.simplify(eq_y_substituted - C2)
                    st.markdown("Przerzucamy wszystkie stałe i ułamki na lewą stronę, izolując niewiadomą $C_2$:")
                    st.latex(rf"C_2 = {sp.latex(v_y)} - \left({sp.latex(rest_c2)}\right)")
                    st.latex(rf"C_2 = {sp.latex(c2_val)}")
                
                else:
                    # PRZYPADEK BRZEGOWY: Oba równania zawierają C1 i C2 (np. zadanie 1.5)
                    eq1_full = y_gen.subs(x, x0_1)
                    eq2_full = y_gen.subs(x, x0_2)
                    
                    st.markdown("1. Wyznaczamy stałą $C_2$ z pierwszego równania (przenosząc resztę składników na lewą stronę):")
                    rest_eq1 = sp.simplify(eq1_full - C2)
                    c2_isolated = v0_1 - rest_eq1
                    st.latex(rf"C_2 = {sp.latex(c2_isolated)}")
                    
                    st.markdown("2. Podstawiamy wyznaczone wyrażenie na $C_2$ do drugiego równania strukturalnego układu:")
                    eq2_substituted = eq2_full.subs(C2, c2_isolated)
                    st.latex(rf"{sp.latex(v0_2)} = {sp.latex(eq2_substituted)}")
                    
                    st.markdown("Rozwiązujemy powstałe równanie z jedną niewiadomą, redukując ułamki w celu wyznaczenia $C_1$:")
                    st.latex(rf"C_1 = {sp.latex(c1_val)}")
                    
                    st.markdown(f"3. Wracamy do podstawienia i obliczamy ostateczną wartość liczbową stałej $C_2$ dla $C_1 = {sp.latex(c1_val)}$:")
                    c2_final_calc = c2_isolated.subs(C1, c1_val)
                    st.latex(rf"C_2 = {sp.latex(c2_final_calc)} = {sp.latex(c2_val)}")
                
                st.markdown("---")
                st.markdown("Podstawiamy uzyskane wartości $C_1$ i $C_2$ do wzoru ogólnego z początku Etapu 2. Redukcja ta sprowadza wynik do ostatecznej postaci Całki Szczególnej Równania (CSR):")
                
                y_final = y_gen.subs({C1: c1_val, C2: c2_val})
                y_final_latex = sp.latex(y_final).replace(r"\log", r"\ln")
                st.latex(rf"\text{{CSR:}} \quad y(x) = {y_final_latex}")
                st.success("✔ Pełny proces wyznaczania całki szczególnej (wraz z algebrą) gotowy do przepisania!")
            else:
                st.warning("Układ równań dla podanych warunków granicznych jest sprzeczny.")
        except Exception as e:
            st.error(f"Wystąpił błąd podczas analizy symbolicznej: {e}")

# ==========================================
# TAB 2: Równanie charakterystyczne (Format z notatek - układ bazowy i CORLJ)
# ==========================================
with tab2:
    st.subheader("Rozwiązywanie równań jednorodnych (Dokładny format z zajęć):")
    
    zadania_2 = {
        "Zadanie z notatek: y'' - 4y' + 3y = 0": {"a": "1", "b": "-4", "c": "3"},
        "Zadanie z notatek: y'' + 4y' + 13y = 0": {"a": "1", "b": "4", "c": "13"},
        "Zadanie z notatek: y'' + 4y = 0": {"a": "1", "b": "0", "c": "4"},
        "Zadanie 2.1: y'' + 4y' + 4y = 0": {"a": "1", "b": "4", "c": "4"},
        "Zadanie 2.2: y'' - 16y' + 64y = 0": {"a": "1", "b": "-16", "c": "64"},
        "Zadanie 2.3: y'' + 2√2y' + 2y = 0": {"a": "1", "b": "2*sqrt(2)", "c": "2"},
        "✨ Własny przykład...": {"a": "1", "b": "0", "c": "1"}
    }
    
    wybor_2 = st.selectbox("Wybierz zadanie:", list(zadania_2.keys()), key="sel_tab2")
    data_2 = zadania_2[wybor_2]
    
    if wybor_2 == "✨ Własny przykład...":
        col_a, col_b, col_c = st.columns(3)
        a_str = col_a.text_input("a =", "1")
        b_str = col_b.text_input("b =", "-4")
        c_str = col_c.text_input("c =", "3")
    else:
        a_str, b_str, c_str = data_2["a"], data_2["b"], data_2["c"]

    if st.button("📝 Generuj rozwiązanie w formacie z zajęć", type="primary", key="btn_tab2"):
        try:
            a_v = parse_expr(a_str, transformations=transformations)
            b_v = parse_expr(b_str, transformations=transformations)
            c_v = parse_expr(c_str, transformations=transformations)
            
            st.markdown("---")
            st.markdown("### Rozwiązanie:")
            
            # Budowanie estetycznego zapisu równania początkowego
            b_p = f"+ {sp.latex(b_v)}" if b_v > 0 else f"{sp.latex(b_v)}"
            c_p = f"+ {sp.latex(c_v)}" if c_v > 0 else f"{sp.latex(c_v)}"
            st.latex(rf"{sp.latex(a_v)}y'' {b_p if b_v != 0 else ''}y' {c_p if c_v != 0 else ''}y = 0")
            
            # KROK 1: Podstawienie
            st.latex(r"\begin{aligned} \text{podst:} \quad & y = e^{rx} \longrightarrow 1 \\ & y' = r e^{rx} \longrightarrow r \\ & y'' = r^2 e^{rx} \longrightarrow r^2 \end{aligned}")
            
            # KROK 2: Równanie charakterystyczne
            char_eq = a_v*r**2 + b_v*r + c_v
            st.latex(rf"{sp.latex(char_eq)} = 0 \quad \text{{- równanie charakterystyczne}}")
            
            # KROK 3: Delta
            delta = sp.simplify(b_v**2 - 4*a_v*c_v)
            st.latex(r"\Delta = b^2 - 4ac")
            
            b_tex = f"({sp.latex(b_v)})" if b_v < 0 or "sqrt" in b_str else sp.latex(b_v)
            a_tex = f"({sp.latex(a_v)})" if a_v < 0 else sp.latex(a_v)
            c_tex = f"({sp.latex(c_v)})" if c_v < 0 else sp.latex(c_v)
            
            d_val = float(delta)
            
            if d_val > 0:
                st.latex(rf"\Delta = {b_tex}^2 - 4 \cdot {a_tex} \cdot {c_tex} = {sp.latex(delta)} > 0")
                st.latex(rf"\sqrt{{\Delta}} = {sp.latex(sp.sqrt(delta))}")
                
                r1 = sp.simplify((-b_v - sp.sqrt(delta))/(2*a_v))
                r2 = sp.simplify((-b_v + sp.sqrt(delta))/(2*a_v))
                
                # POPRAWIONE: minus przeniesiony bezpiecznie do wewnątrz funkcji sp.latex
                st.latex(rf"r_1 = \frac{{{sp.latex(-b_v)} - {sp.latex(sp.sqrt(delta))}}}{{2 \cdot {a_tex}}} = {sp.latex(r1)} \quad ; \quad r_2 = \frac{{{sp.latex(-b_v)} + {sp.latex(sp.sqrt(delta))}}}{{2 \cdot {a_tex}}} = {sp.latex(r2)}")
                
                st.markdown("**wtedy**")
                y1 = sp.exp(r1*x)
                y2 = sp.exp(r2*x)
                st.latex(rf"y_1 = e^{{{sp.latex(r1)}x}} \quad ; \quad y_2 = e^{{{sp.latex(r2)}x}} \quad \longrightarrow \text{{układ bazowy}}")
                
                st.markdown("**tw.** \quad $y_0 = C_1 y_1 + C_2 y_2$")
                st.markdown("**czyli**")
                st.latex(rf"\underline{{y_0 = C_1 e^{{{sp.latex(r1)}x}} + C_2 e^{{{sp.latex(r2)}x}} \quad \text{{- CORLJ}}}}")
                
            elif d_val == 0:
                st.latex(rf"\Delta = {b_tex}^2 - 4 \cdot {a_tex} \cdot {c_tex} = 0")
                
                r0 = sp.simplify(-b_v/(2*a_v))
                # POPRAWIONE: sp.latex(-b_v) zamiast negowania stringa
                st.latex(rf"r_0 = \frac{{-b}}{{2a}} = \frac{{{sp.latex(-b_v)}}}{{2 \cdot {a_tex}}} = {sp.latex(r0)}")
                
                st.markdown("**to**")
                y1 = sp.exp(r0*x)
                y2 = x * sp.exp(r0*x)
                st.latex(rf"y_1 = e^{{{sp.latex(r0)}x}} \quad ; \quad y_2 = x e^{{{sp.latex(r0)}x}} \quad \longrightarrow \text{{układ bazowy}}")
                
                st.markdown("**tw.** \quad $y_0 = C_1 y_1 + C_2 y_2$")
                st.markdown("**czyli**")
                st.latex(rf"\underline{{y_0 = C_1 e^{{{sp.latex(r0)}x}} + C_2 x e^{{{sp.latex(r0)}x}} \quad \text{{- CORLJ}}}}")
                
            else:
                st.latex(rf"\Delta = {b_tex}^2 - 4 \cdot {a_tex} \cdot {c_tex} = {sp.latex(delta)} < 0")
                
                alpha = sp.simplify(-b_v/(2*a_v))
                beta = sp.simplify(sp.sqrt(-delta)/(2*a_v))
                
                st.markdown("**wtedy** \quad $r_{1,2} = \alpha \pm \beta i \quad \text{gdzie:}$")
                # POPRAWIONE: bezpieczne parsowanie -b_v wewnątrz obiektów SymPy
                st.latex(rf"\alpha = \frac{{-b}}{{2a}} = {sp.latex(alpha)} \quad ; \quad \beta = \frac{{\sqrt{{-\Delta}}}}{{2a}} = \frac{{\sqrt{{{sp.latex(-delta)}}}}}{{2 \cdot {a_tex}}} = {sp.latex(beta)}")
                
                st.markdown("**to**")
                
                if alpha == 0:
                    st.latex(rf"y_1 = \cos({sp.latex(beta)}x) \quad ; \quad y_2 = \sin({sp.latex(beta)}x) \quad \longrightarrow \text{{układ bazowy}}")
                    st.markdown("**tw.** \quad $y_0 = C_1 y_1 + C_2 y_2$")
                    st.markdown("**czyli**")
                    st.latex(rf"\underline{{y_0 = C_1 \cos({sp.latex(beta)}x) + C_2 \sin({sp.latex(beta)}x) \quad \text{{- CORLJ}}}}")
                else:
                    st.latex(rf"y_1 = e^{{{sp.latex(alpha)}x}} \cos({sp.latex(beta)}x) \quad ; \quad y_2 = e^{{{sp.latex(alpha)}x}} \sin({sp.latex(beta)}x) \quad \longrightarrow \text{{układ bazowy}}")
                    st.markdown("**tw.** \quad $y_0 = C_1 y_1 + C_2 y_2$")
                    st.markdown("**czyli**")
                    st.latex(rf"\underline{{y_0 = C_1 e^{{{sp.latex(alpha)}x}} \cos({sp.latex(beta)}x) + C_2 e^{{{sp.latex(alpha)}x}} \sin({sp.latex(beta)}x) \quad \text{{- CORLJ}}}}")
                
        except Exception as e:
            st.error(f"Błąd podczas generowania: {e}")

# ==========================================
# TAB 3: Równanie charakterystyczne + Warunki (Pełny format z zajęć + Algebra na piechotę)
# ==========================================
with tab3:
    st.subheader("Wyznaczanie Całki Szczególnej (Format z zajęć + obliczenia na piechotę):")
    
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
    
    # NAPRAWIONY WARUNEK: Teraz poprawnie sprawdza nazwę wyboru z listy selectboxa
    if wybor_3 == "✨ Własny przykład...":
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

    if st.button("📝 Generuj pełną procedurę CSR", type="primary", key="btn_tab3"):
        try:
            a_val = parse_expr(a_str, transformations=transformations)
            b_val = parse_expr(b_str, transformations=transformations)
            c_val = parse_expr(c_str, transformations=transformations)
            
            x0_1 = parse_expr(c1_x.replace('^', '**'), transformations=transformations)
            v0_1 = parse_expr(c1_v.replace('^', '**'), transformations=transformations)
            x0_2 = parse_expr(c2_x.replace('^', '**'), transformations=transformations)
            v0_2 = parse_expr(c2_v.replace('^', '**'), transformations=transformations)
            
            st.markdown("---")
            st.markdown("### Rozwiązanie:")
            
            # 1. Zapis równania wyjściowego
            b_p = f"+ {sp.latex(b_val)}" if b_val > 0 else f"{sp.latex(b_val)}"
            c_p = f"+ {sp.latex(c_val)}" if c_val > 0 else f"{sp.latex(c_val)}"
            st.latex(rf"{sp.latex(a_val)}y'' {b_p if b_val != 0 else ''}y' {c_p if c_val != 0 else ''}y = 0")
            
            # 2. Blok podstawienia (Format z notatek)
            st.latex(r"\begin{aligned} \text{podst:} \quad & y = e^{rx} \longrightarrow 1 \\ & y' = r e^{rx} \longrightarrow r \\ & y'' = r^2 e^{rx} \longrightarrow r^2 \end{aligned}")
            
            # 3. Równanie charakterystyczne
            char_eq = a_val*r**2 + b_val*r + c_val
            st.latex(rf"{sp.latex(char_eq)} = 0 \quad \text{{- równanie charakterystyczne}}")
            
            # 4. Delta
            delta = sp.simplify(b_val**2 - 4*a_val*c_val)
            st.latex(r"\Delta = b^2 - 4ac")
            
            b_tex = f"({sp.latex(b_val)})" if b_val < 0 or "sqrt" in b_str else sp.latex(b_val)
            a_tex = f"({sp.latex(a_val)})" if a_val < 0 else sp.latex(a_val)
            c_tex = f"({sp.latex(c_val)})" if c_val < 0 else sp.latex(c_val)
            
            delta_val = float(delta)
            
            # Wyznaczenie CORLJ w zależności od delty (Zgodnie z formatem z notatek)
            if delta_val > 0:
                st.latex(rf"\Delta = {b_tex}^2 - 4 \cdot {a_tex} \cdot {c_tex} = {sp.latex(delta)} > 0")
                st.latex(rf"\sqrt{{\Delta}} = {sp.latex(sp.sqrt(delta))}")
                
                r1 = sp.simplify((-b_val - sp.sqrt(delta))/(2*a_val))
                r2 = sp.simplify((-b_val + sp.sqrt(delta))/(2*a_val))
                st.latex(rf"r_1 = \frac{{{sp.latex(-b_val)} - {sp.latex(sp.sqrt(delta))}}}{{2 \cdot {a_tex}}} = {sp.latex(r1)} \quad ; \quad r_2 = \frac{{{sp.latex(-b_val)} + {sp.latex(sp.sqrt(delta))}}}{{2 \cdot {a_tex}}} = {sp.latex(r2)}")
                
                st.markdown("**wtedy**")
                y_gen = C1*sp.exp(r1*x) + C2*sp.exp(r2*x)
                st.latex(rf"y_1 = e^{{{sp.latex(r1)}x}} \quad ; \quad y_2 = e^{{{sp.latex(r2)}x}} \quad \longrightarrow \text{{układ bazowy}}")
                
            elif delta_val == 0:
                st.latex(rf"\Delta = {b_tex}^2 - 4 \cdot {a_tex} \cdot {c_tex} = 0")
                r0 = sp.simplify(-b_val/(2*a_val))
                st.latex(rf"r_0 = \frac{{-b}}{{2a}} = \frac{{{sp.latex(-b_val)}}}{{2 \cdot {a_tex}}} = {sp.latex(r0)}")
                
                st.markdown("**to**")
                y_gen = (C1 + C2*x)*sp.exp(r0*x)
                st.latex(rf"y_1 = e^{{{sp.latex(r0)}x}} \quad ; \quad y_2 = x e^{{{sp.latex(r0)}x}} \quad \longrightarrow \text{{układ bazowy}}")
                
            else:
                st.latex(rf"\Delta = {b_tex}^2 - 4 \cdot {a_tex} \cdot {c_tex} = {sp.latex(delta)} < 0")
                alpha = sp.simplify(-b_val/(2*a_val))
                beta = sp.simplify(sp.sqrt(-delta)/(2*a_val))
                
                st.markdown("**wtedy** \quad $r_{1,2} = \alpha \pm \beta i \quad \text{gdzie:}$")
                st.latex(rf"\alpha = \frac{{-b}}{{2a}} = {sp.latex(alpha)} \quad ; \quad \beta = \frac{{\sqrt{{-\Delta}}}}{{2a}} = \frac{{\sqrt{{{sp.latex(-delta)}}}}}{{2 \cdot {a_tex}}} = {sp.latex(beta)}")
                
                st.markdown("**to**")
                if alpha == 0:
                    y_gen = C1*sp.cos(beta*x) + C2*sp.sin(beta*x)
                    st.latex(rf"y_1 = \cos({sp.latex(beta)}x) \quad ; \quad y_2 = \sin({sp.latex(beta)}x) \quad \longrightarrow \text{{układ bazowy}}")
                else:
                    y_gen = sp.exp(alpha*x)*(C1*sp.cos(beta*x) + C2*sp.sin(beta*x))
                    st.latex(rf"y_1 = e^{{{sp.latex(alpha)}x}} \cos({sp.latex(beta)}x) \quad ; \quad y_2 = e^{{{sp.latex(alpha)}x}} \sin({sp.latex(beta)}x) \quad \longrightarrow \text{{układ bazowy}}")
            
            st.markdown("**tw.** \quad $y_0 = C_1 y_1 + C_2 y_2$")
            st.markdown("**czyli**")
            st.latex(rf"y_0 = {sp.latex(y_gen)} \quad \text{{- CORLJ}}")
            st.markdown("---")
            
            # KROK 5: Pochodna do warunku Cauchy'ego
            st.markdown("**Wyznaczenie pochodnej pierwszego stopnia funkcji $y_0(x)$:**")
            y_prime = sp.diff(y_gen, x)
            st.latex(rf"y_0^{{\prime}}(x) = {sp.latex(y_prime)}")
            st.markdown("---")
            
            # KROK 6: Układ równań z warunków
            st.markdown("**Budujemy układ równań na podstawie zadanych warunków granicznych:**")
            eqs = []
            eq_latex = []
            
            if c1_t == "y":
                val_sub1 = sp.simplify(y_gen.subs(x, x0_1))
            else:
                val_sub1 = sp.simplify(y_prime.subs(x, x0_1))
            eqs.append(sp.Eq(val_sub1, v0_1))
            eq_latex.append(rf"{sp.latex(v0_1)} = {sp.latex(val_sub1)}")
                
            if c2_t == "y":
                val_sub2 = sp.simplify(y_gen.subs(x, x0_2))
            else:
                val_sub2 = sp.simplify(y_prime.subs(x, x0_2))
            eqs.append(sp.Eq(val_sub2, v0_2))
            eq_latex.append(rf"{sp.latex(v0_2)} = {sp.latex(val_sub2)}")
            
            st.latex(rf"\begin{{cases}} {eq_latex[0]} \\ {eq_latex[1]} \end{{cases}}")
            
            # KROK 7: Algebra na piechotę
            solutions = sp.solve(eqs, (C1, C2))
            
            if solutions:
                c1_val = sp.simplify(solutions[C1])
                c2_val = sp.simplify(solutions[C2])
                
                st.markdown("#### 🧮 Obliczenia algebraiczne układu na piechotę:")
                
                has_c1_eq1 = val_sub1.has(C1)
                has_c2_eq1 = val_sub1.has(C2)
                
                if has_c1_eq1 and not has_c2_eq1:
                    c1_iso = sp.solve(sp.Eq(val_sub1, v0_1), C1)[0]
                    st.markdown("Z pierwszego równania (dzięki wyzerowaniu się jednego ze składników trygonometrycznych lub wykładniczych) wyznaczamy bezpośrednio stałą $C_1$:")
                    st.latex(rf"C_1 = {sp.latex(c1_iso)}")
                    st.markdown("Podstawiamy obliczoną wartość $C_1$ do drugiego równania strukturalnego:")
                    eq2_sub = sp.simplify(val_sub2.subs(C1, c1_iso))
                    st.latex(rf"{sp.latex(v0_2)} = {sp.latex(eq2_sub)} \implies C_2 = {sp.latex(c2_val)}")
                    
                elif has_c2_eq1 and not has_c1_eq1:
                    c2_iso = sp.solve(sp.Eq(val_sub1, v0_1), C2)[0]
                    st.markdown("Z pierwszego równania wyznaczamy bezpośrednio stałą $C_2$:")
                    st.latex(rf"C_2 = {sp.latex(c2_iso)}")
                    st.markdown("Podstawiamy obliczoną wartość $C_2$ do drugiego równania strukturalnego:")
                    eq2_sub = sp.simplify(val_sub2.subs(C2, c2_iso))
                    st.latex(rf"{sp.latex(v0_2)} = {sp.latex(eq2_sub)} \implies C_1 = {sp.latex(c1_val)}")
                    
                else:
                    st.markdown("Metodą podstawiania wyznaczamy zależność dla stałej $C_1$ z pierwszego równania:")
                    c1_iso = sp.solve(sp.Eq(val_sub1, v0_1), C1)[0]
                    st.latex(rf"C_1 = {sp.latex(c1_iso)}")
                    st.markdown("Wstawiamy wyznaczone wyrażenie do drugiego równania w celu redukcji do jednej niewiadomej:")
                    eq2_sub = sp.simplify(val_sub2.subs(C1, c1_iso))
                    st.latex(rf"{sp.latex(v0_2)} = {sp.latex(eq2_sub)}")
                    st.markdown("Sprowadzamy ułamki do wspólnego mianownika i izolujemy ostateczną wartość liczbową dla $C_2$:")
                    st.latex(rf"C_2 = {sp.latex(c2_val)}")
                    st.markdown("Wracamy do pierwszego podstawienia, aby domknąć obliczenia dla stałej $C_1$:")
                    st.latex(rf"C_1 = {sp.latex(c1_val)}")

                st.markdown("---")
                # KROK 8: Podkreślony wynik końcowy Całki Szczególnej (CSR)
                st.markdown("**Ostateczna Całka Szczególna Równania (CSR):**")
                y_final = sp.simplify(y_gen.subs({C1: c1_val, C2: c2_val}))
                st.latex(rf"\underline{{y(x) = {sp.latex(y_final)} \quad \text{{- CSR}}}}")
                st.success("✔ Całe zagadnienie Cauchy'ego / brzegowe rozpisane pomyślnie!")
            else:
                st.warning("Układ równań dla podanych warunków granicznych jest sprzeczny.")
                
        except Exception as e:
            st.error(f"Wystąpił błąd podczas obliczeń: {e}")