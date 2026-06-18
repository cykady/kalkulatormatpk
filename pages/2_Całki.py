import streamlit as st
import sympy as sp
import re
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

st.set_page_config(page_title="Kalkulator Całek", layout="wide")

# ==========================================
# KONFIGURACJA SYMBOLE I TRANSFORMACJE
# ==========================================
x = sp.Symbol('x')
transformations = standard_transformations + (implicit_multiplication_application,)

def bezpieczny_parser(f_str):
    """Przetwarza wpisany tekst na wyrażenie SymPy."""
    if not f_str or f_str.strip() == "": return None
    f_str = f_str.replace('^', '**')
    return parse_expr(f_str, local_dict={'e': sp.E, 'pi': sp.pi}, transformations=transformations)

def popraw_logarytmy(latex_str):
    return latex_str.replace(r"\log{\left(x \right)}", r"\ln|x|").replace(r"\log", r"\ln")

# ==========================================
# GŁÓWNY INTERFEJS
# ==========================================
st.title("🧮 Inteligentny Kalkulator Całek")
st.markdown("Kalkulator generujący protokoły rozwiązań w standardzie akademickim (krok po kroku).")
st.caption("💡 Ściąga: ułamek -> a/b | pierwiastek -> sqrt(x) | e^x -> exp(x) | mnożenie -> 6*x*cos(x) | pi -> pi")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["Liniowość (Nieoznaczone)", "Newton-Leibniz (Oznaczone)", "🔥 Przez Części", "🔄 Przez Podstawienie"])

# ==========================================
# TAB 1: CAŁKI NIEOZNACZONE
# ==========================================
with tab1:
    st.header("Rozbijanie całek (Liniowość)")
    col1, col2 = st.columns([4, 1])
    with col1:
        f_input_1 = st.text_input("Wpisz funkcję podcałkową f(x):", "4*x^2 - 3/x + 2*sin(x)", key="in1")
    with col2:
        st.write("")
        btn1 = st.button("🚀 Rozwiąż Krok po Kroku", key="btn1", use_container_width=True)
        
    if btn1 and f_input_1:
        try:
            f_expr = bezpieczny_parser(f_input_1)
            st.markdown("### 📝 Protokół Rozwiązania:")
            lines = []
            
            lines.append(r"\text{1. Zapis wyjściowy:}")
            lines.append(r"\int \left( " + sp.latex(f_expr) + r" \right) dx")
            lines.append(r"")
            
            f_exp = sp.expand(f_expr)
            if f_exp != f_expr:
                lines.append(r"\text{2. Przekształcamy wyrażenie (wymnażamy nawiasy / ułamki):}")
                lines.append(r"= \int \left( " + sp.latex(f_exp) + r" \right) dx")
                lines.append(r"")
            
            lines.append(r"\text{3. Twierdzenie o liniowości (całka sumy, wyłączenie stałej):}")
            terms = f_exp.args if isinstance(f_exp, sp.Add) else [f_exp]
            parts_latex = []
            
            for term in terms:
                coeff, rest = term.as_coeff_Mul()
                if rest == 1: parts_latex.append(sp.latex(coeff) + r" \int 1 \, dx")
                else:
                    if coeff == 1: parts_latex.append(r"\int " + sp.latex(rest) + r" \, dx")
                    elif coeff == -1: parts_latex.append(r"- \int " + sp.latex(rest) + r" \, dx")
                    else: parts_latex.append(sp.latex(coeff) + r" \int " + sp.latex(rest) + r" \, dx")
                        
            sum_latex = " + ".join(parts_latex).replace("+ -", "- ")
            lines.append(r"= " + sum_latex)
            lines.append(r"")
            
            lines.append(r"\text{4. Całkujemy i dodajemy stałą C:}")
            result = sp.integrate(f_exp, x)
            lines.append(r"\underline{= " + popraw_logarytmy(sp.latex(result)) + r" + C }")
            
            st.latex("\\begin{aligned}\n" + " \\\\\n".join(lines) + "\n\\end{aligned}")
        except Exception as e:
            st.error(f"Błąd analizy wyrażenia: {e}")

# ==========================================
# TAB 2: CAŁKI OZNACZONE
# ==========================================
with tab2:
    st.header("Całki Oznaczone (Wzór Newtona-Leibniza)")
    col_f, col_a, col_b, col_btn = st.columns([3, 1, 1, 1])
    with col_f: f_input_2 = st.text_input("Funkcja podcałkowa f(x):", "3*x^2 + 2x", key="in2")
    with col_a: a_input = st.text_input("Dolna (a):", "1", key="a2")
    with col_b: b_input = st.text_input("Górna (b):", "3", key="b2")
    with col_btn:
        st.write("")
        btn2 = st.button("🚀 Oblicz", key="btn2", use_container_width=True)

    if btn2 and f_input_2 and a_input and b_input:
        try:
            f_expr = bezpieczny_parser(f_input_2)
            a_val, b_val = bezpieczny_parser(a_input), bezpieczny_parser(b_input)
            
            st.markdown("### 📝 Wzór Newtona-Leibniza:")
            lines = []
            
            lines.append(r"\text{1. Całka oznaczona:}")
            lines.append(r"\int_{" + sp.latex(a_val) + r"}^{" + sp.latex(b_val) + r"} \left( " + sp.latex(f_expr) + r" \right) dx")
            lines.append(r"")
            
            lines.append(r"\text{2. Wyznaczamy funkcję pierwotną } F(x):")
            F_expr = sp.integrate(f_expr, x)
            lines.append(r"= \left[ " + popraw_logarytmy(sp.latex(F_expr)) + r" \right]_{" + sp.latex(a_val) + r"}^{" + sp.latex(b_val) + r"}")
            lines.append(r"")
            
            lines.append(r"\text{3. Podstawiamy granice } F(b) - F(a):")
            F_b, F_a = F_expr.subs(x, b_val), F_expr.subs(x, a_val)
            lines.append(r"= \left( " + popraw_logarytmy(sp.latex(F_b)) + r" \right) - \left( " + popraw_logarytmy(sp.latex(F_a)) + r" \right)")
            lines.append(r"")
            
            lines.append(r"\text{4. Wynik końcowy:}")
            final_val = sp.simplify(F_b - F_a)
            lines.append(r"\underline{ = " + sp.latex(final_val) + r" }")
            
            st.latex("\\begin{aligned}\n" + " \\\\\n".join(lines) + "\n\\end{aligned}")
        except Exception as e:
            st.error(f"Wystąpił błąd: {e}")

# ==========================================
# TAB 3: CAŁKOWANIE PRZEZ CZĘŚCI
# ==========================================
with tab3:
    st.header("Całkowanie przez części (z tabelką)")
    st.markdown(r"**Wzór:** $\int u \cdot v' dx = u \cdot v - \int u' \cdot v dx$")
    
    col_u, col_v = st.columns(2)
    with col_u: u_in = st.text_input("Wpisz u(x) [np. 6*x]:", "6*x")
    with col_v: dv_in = st.text_input("Wpisz v'(x) [np. cos(x)]:", "cos(x)")
        
    st.markdown("**(Opcjonalnie) Granice całkowania:** *Jeśli zostawisz puste, policzy całkę nieoznaczoną.*")
    col_a3, col_b3, col_btn3 = st.columns([1, 1, 2])
    with col_a3: a_in3 = st.text_input("Dolna granica a:", "0")
    with col_b3: b_in3 = st.text_input("Górna granica b:", "pi/2")
    with col_btn3:
        st.write("")
        btn3 = st.button("🚀 Rozwiąż przez części", type="primary", use_container_width=True)
        
    if btn3 and u_in and dv_in:
        try:
            u_expr = bezpieczny_parser(u_in)
            dv_expr = bezpieczny_parser(dv_in)
            a_val = bezpieczny_parser(a_in3)
            b_val = bezpieczny_parser(b_in3)
            
            # Wyliczanie pochodnej i całki do tabelki
            du_expr = sp.diff(u_expr, x)
            v_expr = sp.integrate(dv_expr, x)
            
            # Pełna funkcja f(x) = u * v'
            f_full = u_expr * dv_expr
            
            st.markdown("---")
            st.markdown("### 📝 Rozwiązanie krok po kroku:")
            lines = []
            
            is_def = (a_val is not None) and (b_val is not None)
            
            if is_def:
                lines.append(r"\text{1. Zapis wyjściowy:}")
                lines.append(r"I = \int_{" + sp.latex(a_val) + r"}^{" + sp.latex(b_val) + r"} " + sp.latex(f_full) + r" \, dx")
            else:
                lines.append(r"\text{1. Zapis wyjściowy:}")
                lines.append(r"I = \int " + sp.latex(f_full) + r" \, dx")
            
            lines.append(r"")
            lines.append(r"\text{2. Tabelka podstawień:}")
            lines.append(r"\begin{vmatrix}")
            lines.append(r"u = " + sp.latex(u_expr) + r" & v^{\prime} = " + sp.latex(dv_expr) + r" \\")
            lines.append(r"u^{\prime} = " + sp.latex(du_expr) + r" & v = " + sp.latex(v_expr))
            lines.append(r"\end{vmatrix}")
            lines.append(r"")
            
            uv = u_expr * v_expr
            int_udv = du_expr * v_expr
            
            lines.append(r"\text{3. Stosujemy wzór na całkowanie przez części:}")
            if is_def:
                lines.append(r"I = \left[ " + sp.latex(uv) + r" \right]_{" + sp.latex(a_val) + r"}^{" + sp.latex(b_val) + r"} - \int_{" + sp.latex(a_val) + r"}^{" + sp.latex(b_val) + r"} \left(" + sp.latex(int_udv) + r"\right) \, dx")
                lines.append(r"")
                
                lines.append(r"\text{4. Obliczamy drugą całkę z wzoru:}")
                second_integral = sp.integrate(int_udv, x)
                lines.append(r"I = \left[ " + sp.latex(uv) + r" \right]_{" + sp.latex(a_val) + r"}^{" + sp.latex(b_val) + r"} - \left[ " + sp.latex(second_integral) + r" \right]_{" + sp.latex(a_val) + r"}^{" + sp.latex(b_val) + r"}")
                lines.append(r"I = \left[ " + sp.latex(uv - second_integral) + r" \right]_{" + sp.latex(a_val) + r"}^{" + sp.latex(b_val) + r"}")
                lines.append(r"")
                
                lines.append(r"\text{5. Podstawiamy granice Newtonem-Leibnizem:}")
                F_expr = uv - second_integral
                F_b = F_expr.subs(x, b_val)
                F_a = F_expr.subs(x, a_val)
                lines.append(r"I = \left( " + sp.latex(F_b) + r" \right) - \left( " + sp.latex(F_a) + r" \right)")
                
                final_val = sp.simplify(F_b - F_a)
                lines.append(r"\underline{ I = " + sp.latex(final_val) + r" }")
                
            else:
                lines.append(r"I = " + sp.latex(uv) + r" - \int \left(" + sp.latex(int_udv) + r"\right) \, dx")
                lines.append(r"")
                
                lines.append(r"\text{4. Rozwiązujemy drugą całkę i dodajemy stałą C:}")
                second_integral = sp.integrate(int_udv, x)
                final_expr = uv - second_integral
                lines.append(r"I = " + sp.latex(uv) + r" - \left(" + sp.latex(second_integral) + r"\right) + C")
                lines.append(r"\underline{ I = " + popraw_logarytmy(sp.latex(final_expr)) + r" + C }")

            st.latex("\\begin{aligned}\n" + " \\\\\n".join(lines) + "\n\\end{aligned}")
            
        except Exception as e:
            st.error(f"Wystąpił błąd. Szczegóły: {e}")
            # ==========================================
# ==========================================
# TAB 4: CAŁKOWANIE PRZEZ PODSTAWIENIE
# ==========================================
with tab4:
    st.header("Całkowanie przez podstawienie")
    st.markdown(r"**Zasada:** Wprowadzamy nową zmienną $t = g(x)$, liczymy różniczkę $dt = g'(x)dx$ i podmieniamy w całce.")
    
    col_f, col_t = st.columns(2)
    with col_f: 
        f_in4 = st.text_input("Cała funkcja podcałkowa f(x):", "9*x^2*(3*x^3+6)^2", key="f_in4")
    with col_t: 
        t_in4 = st.text_input("Zdefiniuj podstawienie t =", "3*x^3+6", key="t_in4")
        
    st.markdown("**(Opcjonalnie) Granice całkowania:** *Zostaw puste dla całki nieoznaczonej.*")
    col_a4, col_b4, col_btn4 = st.columns([1, 1, 2])
    with col_a4: a_in4 = st.text_input("Dolna granica a:", "0", key="a4")
    with col_b4: b_in4 = st.text_input("Górna granica b:", "1", key="b4")
    with col_btn4:
        st.write("")
        btn4 = st.button("🚀 Rozwiąż przez podstawienie", type="primary", use_container_width=True, key="btn4")

    if btn4 and f_in4 and t_in4:
        try:
            f_expr = bezpieczny_parser(f_in4)
            t_expr = bezpieczny_parser(t_in4)
            a_val = bezpieczny_parser(a_in4) if a_in4 else None
            b_val = bezpieczny_parser(b_in4) if b_in4 else None
            
            t_sym = sp.Symbol('t')
            
            # Liczymy pochodną dt/dx
            dt_dx = sp.diff(t_expr, x)
            
            # POPRAWKA BŁĘDU: Delikatne podstawienie bez agresywnego wymnażania!
            # 1. Zwykłe dzielenie (utnie 9x^2)
            f_bez_dx = f_expr / dt_dx
            # 2. Twarde podstawienie 't' dokładnie w miejsce nawiasu
            f_t_expr = f_bez_dx.subs(t_expr, t_sym)
            # 3. Dopiero teraz ewentualnie sprzątamy stałe
            f_t_expr = sp.simplify(f_t_expr)
            
            st.markdown("---")
            st.markdown("### 📝 Rozwiązanie krok po kroku:")
            lines = []
            
            is_def = (a_val is not None) and (b_val is not None)
            
            if is_def:
                lines.append(r"\text{1. Zapis wyjściowy:}")
                lines.append(r"I = \int_{" + sp.latex(a_val) + r"}^{" + sp.latex(b_val) + r"} \left(" + sp.latex(f_expr) + r"\right) \, dx")
            else:
                lines.append(r"\text{1. Zapis wyjściowy:}")
                lines.append(r"I = \int \left(" + sp.latex(f_expr) + r"\right) \, dx")
                
            lines.append(r"")
            lines.append(r"\text{2. Tabelka podstawień (oraz różniczkowanie):}")
            
            if is_def:
                t_a = sp.simplify(t_expr.subs(x, a_val))
                t_b = sp.simplify(t_expr.subs(x, b_val))
                lines.append(r"\begin{vmatrix}")
                lines.append(r"t = " + sp.latex(t_expr) + r" & \Rightarrow \text{dla } x = " + sp.latex(a_val) + r" \rightarrow t = " + sp.latex(t_a) + r"\\")
                lines.append(r"dt = " + sp.latex(dt_dx) + r" \, dx" + r" & \Rightarrow \text{dla } x = " + sp.latex(b_val) + r" \rightarrow t = " + sp.latex(t_b) + r"\\")
                lines.append(r"\end{vmatrix}")
            else:
                lines.append(r"\begin{vmatrix}")
                lines.append(r"t = " + sp.latex(t_expr) + r" \\")
                lines.append(r"dt = \left(" + sp.latex(dt_dx) + r"\right) dx \implies dx = \frac{dt}{" + sp.latex(dt_dx) + r"}")
                lines.append(r"\end{vmatrix}")

            if f_t_expr.has(x):
                st.warning("UWAGA: Po zastosowaniu podstawienia, zmienna 'x' w pełni się nie skróciła. To podstawienie może być nieodpowiednie, ale poniżej pokazuję próbę kalkulacji.")
            
            lines.append(r"")
            lines.append(r"\text{3. Wstawiamy zmienną } t \text{ do całki:}")
            if is_def:
                lines.append(r"I = \int_{" + sp.latex(t_a) + r"}^{" + sp.latex(t_b) + r"} \left(" + sp.latex(f_t_expr) + r"\right) \, dt")
            else:
                lines.append(r"I = \int \left(" + sp.latex(f_t_expr) + r"\right) \, dt")
                
            result_t = sp.integrate(f_t_expr, t_sym)
            lines.append(r"")
            lines.append(r"\text{4. Całkujemy po zmiennej } t:")
            
            if is_def:
                lines.append(r"I = \left[ " + popraw_logarytmy(sp.latex(result_t)) + r" \right]_{" + sp.latex(t_a) + r"}^{" + sp.latex(t_b) + r"}")
                lines.append(r"")
                lines.append(r"\text{5. Podstawiamy przeliczone granice (Newton-Leibniz):}")
                res_b = result_t.subs(t_sym, t_b)
                res_a = result_t.subs(t_sym, t_a)
                lines.append(r"I = \left(" + popraw_logarytmy(sp.latex(res_b)) + r"\right) - \left(" + popraw_logarytmy(sp.latex(res_a)) + r"\right)")
                final_res = sp.simplify(res_b - res_a)
                lines.append(r"\underline{ I = " + sp.latex(final_res) + r" }")
            else:
                lines.append(r"I = " + popraw_logarytmy(sp.latex(result_t)) + r" + C")
                lines.append(r"")
                lines.append(r"\text{5. Wracamy z podstawienia (podmieniamy } t \text{ na } x \text{):}")
                result_x = result_t.subs(t_sym, t_expr)
                lines.append(r"\underline{ I = " + popraw_logarytmy(sp.latex(result_x)) + r" + C }")

            st.latex("\\begin{aligned}\n" + " \\\\\n".join(lines) + "\n\\end{aligned}")
            
        except Exception as e:
            st.error(f"Wystąpił błąd parsowania. Upewnij się, że wpisałeś poprawnie obie funkcje. Szczegóły: {e}")