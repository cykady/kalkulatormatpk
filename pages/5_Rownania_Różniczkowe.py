import streamlit as st
import sympy as sp
import re
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

st.set_page_config(page_title="Kalkulator RR", layout="wide")

# ==========================================
# KONFIGURACJA SYMBOLE I TRANSFORMACJE
# ==========================================
x = sp.Symbol('x')
y_sym = sp.Symbol('y')
yp = sp.Symbol('yp')
ypp = sp.Symbol('ypp')
C1, C2, C = sp.symbols('C_1 C_2 C')
transformations = standard_transformations + (implicit_multiplication_application,)

# ==========================================
# FUNKCJE POMOCNICZE (PARSER I ASYSTENT)
# ==========================================
def sugeruj_zakladke(eq_str):
    if not eq_str:
        return None, "Wpisz równanie, aby asystent mógł je przeanalizować."
    eq_clean = eq_str.split(';')[0].lower().replace(" ", "")
    eq_clean = eq_clean.replace("’", "'").replace("`", "'").replace('"', "''")
    ma_ypp = "y''" in eq_clean or "ypp" in eq_clean
    ma_yp = "y'" in eq_clean or "yp" in eq_clean or "dy/dx" in eq_clean
    
    if ma_ypp:
        czyste_y = eq_clean.replace("y''", "").replace("ypp", "").replace("y'", "").replace("yp", "")
        ma_y = "y" in czyste_y
        ma_x = "x" in eq_clean
        czyste_yp = eq_clean.replace("y''", "").replace("ypp", "")
        ma_yp_samodzielne = "y'" in czyste_yp or "yp" in czyste_yp
        
        # INTELIGENTNA POPRAWKA: Szukamy nieliniowości (potęg, ułamków lub mnożenia zmiennej y)
        ma_nieliniowosc = "^" in eq_clean or "**" in eq_clean or "y*y" in eq_clean or "yy" in eq_clean or "y(" in eq_clean
        
        if not ma_yp_samodzielne and not ma_y:
            return "Typ I: y'' = f(x)", "Użyj zakładki nr 3: **Typ I: y'' = f(x)**"
        elif not ma_y:
            return "Typ II: F(x, y', y'') = 0", "Użyj zakładki nr 4: **Typ II: F(x, y', y'') = 0**"
        elif not ma_x and ma_nieliniowosc:
            # Dopiero gdy nie ma 'x' ORAZ równanie jest nieliniowe, idziemy do Typu III
            return "Typ III: F(y, y', y'') = 0", "Użyj zakładki nr 5: **Typ III: F(y, y', y'') = 0**"
        else:
            # Wszystkie liniowe (nawet te bez 'x' po prawej stronie) wpadają bezpiecznie tutaj
            return "Typ IV: Liniowe 2. Rzędu", "Użyj zakładki nr 6: **Typ IV: Liniowe 2. Rzędu**"
    elif ma_yp:
        ma_potegowanie_y = re.search(r'y\*\*([2-9]|\d+)|y\^([2-9]|\d+)', eq_clean)
        ma_pojedyncze_y = re.search(r'(?<![a-zA-Z])y(?!\^|\*\*)', eq_clean)
        ma_plus_minus = "+" in eq_clean or "-" in eq_clean
        
        if ma_potegowanie_y and ma_pojedyncze_y and ma_plus_minus:
            return "Bernoulliego", "Użyj zakładki nr 7: **Bernoulliego**"
        elif ma_potegowanie_y and not ma_plus_minus:
            return "Zmienne Rozdzielone", "Użyj zakładki nr 1: **Zmienne Rozdzielone**"
        elif ma_plus_minus and not ma_potegowanie_y:
            return "Liniowe 1. Rzędu", "Użyj zakładki nr 2: **Liniowe 1. Rzędu**"
        else:
            return "Zmienne Rozdzielone", "Użyj zakładki nr 1: **Zmienne Rozdzielone**"
    else:
        return "Brak pochodnych", "Asystent nie wykrył pochodnej ($y'$ lub $y''$). Upewnij się, że wpisałeś poprawny symbol."

def preprocess_input(user_input):
    parts = re.split(r'[;\|]', user_input)
    eq_str = parts[0].strip()
    conditions = []
    if len(parts) > 1:
        cond_strs = [p.strip() for p in parts[1:] if p.strip()]
        for c in cond_strs:
            c = c.replace('^', '**')
            t = 'yp' if ("y'" in c or "yp" in c or "y’" in c) else 'y'
            match = re.search(r'\((.*?)\)\s*=\s*(.*)', c)
            if match:
                x_val = parse_expr(match.group(1), local_dict={'e': sp.E, 'pi': sp.pi}, transformations=transformations)
                v_val = parse_expr(match.group(2), local_dict={'e': sp.E, 'pi': sp.pi}, transformations=transformations)
                conditions.append({'type': t, 'x': x_val, 'v': v_val, 'raw': c})
                
    eq_str = eq_str.replace('^', '**').replace("y''", "ypp").replace("y\"", "ypp").replace("y”", "ypp")
    eq_str = eq_str.replace("dy/dx", "yp")
    eq_str = re.sub(r'\bdy\b', 'yp', eq_str)  
    eq_str = re.sub(r'\bdx\b', '1', eq_str)   
    eq_str = eq_str.replace("y'", "yp").replace("y’", "yp")
    return eq_str, conditions

def solve_separable(eq, conditions):
    lines = []
    yp_sols = sp.solve(eq, yp)
    if not yp_sols:
        st.error("Nie udało się wyizolować pochodnej y'. Sprawdź zapis równania.")
        return
        
    F = sp.factor(yp_sols[0])
    lines.append(r"y^{\prime} &= " + sp.latex(F) + r" \quad \text{(izolujemy } y^{\prime} \text{ i grupujemy zmienne)}")
    F_x, F_y = F.as_independent(y_sym, as_Add=False)
    lines.append(r"\frac{dy}{dx} &= " + sp.latex(F_x) + r" \cdot \left(" + sp.latex(F_y) + r"\right) \quad / \cdot dx \quad / : \left(" + sp.latex(F_y) + r"\right)")
    
    left_side = sp.simplify(1/F_y)
    right_side = F_x
    lines.append(sp.latex(left_side) + r" \, dy &= " + sp.latex(right_side) + r" \, dx \quad / \int")
    lines.append(r"\int \left(" + sp.latex(left_side) + r"\right) dy &= \int \left(" + sp.latex(right_side) + r"\right) dx")
    
    int_l = sp.integrate(left_side, y_sym)
    int_r = sp.integrate(right_side, x)
    int_l_tex = sp.latex(int_l).replace('log', 'ln')
    int_r_tex = sp.latex(int_r).replace('log', 'ln')
    lines.append(int_l_tex + r" &= " + int_r_tex + r" + C \quad \text{- COR (postać uwikłana)}")
    
    y_gen = None
    try:
        sols = sp.solve(sp.Eq(int_l, int_r + C1), y_sym)
        if sols:
            y_gen = sols[-1]
            lines.append(r"y(x) &= " + sp.latex(y_gen).replace('C_1', 'C') + r" \quad \text{- COR (postać jawna)}")
    except:
        pass 

    st.latex("\\begin{aligned}\n" + " \\\\\n".join(lines) + "\n\\end{aligned}")
    
    if conditions:
        st.markdown("---")
        cond = conditions[0]
        cond_lines = []
        cond_lines.append(r"\text{Podstawiamy warunek początkowy: } " + sp.latex(cond['raw']))
        
        if y_gen:
            val = sp.simplify(y_gen.subs(x, cond['x']))
            cond_lines.append(sp.latex(cond['v']) + r" &= " + sp.latex(val))
            try:
                c_sols = sp.solve(sp.Eq(val, cond['v']), C1)
                if c_sols:
                    c_val = sp.simplify(c_sols[0])
                    cond_lines.append(r"C &= " + sp.latex(c_val))
                    y_final = sp.simplify(y_gen.subs(C1, c_val))
                    cond_lines.append(r"\underline{y(x) = " + sp.latex(y_final).replace('log', 'ln') + r" \quad \text{- CSR}}")
                else:
                    cond_lines.append(r"\text{Dla } y(" + sp.latex(cond['x']) + r")=" + sp.latex(cond['v']) + r" \text{ układ jest sprzeczny.}")
                    cond_lines.append(r"\implies \text{Rozwiązaniem zadania jest funkcja osobliwa np. } y(x)=0")
            except:
                pass
        else:
            eq_c = sp.Eq(int_l.subs(y_sym, cond['v']), int_r.subs(x, cond['x']) + C)
            cond_lines.append(sp.latex(int_l.subs(y_sym, cond['v'])) + r" &= " + sp.latex(int_r.subs(x, cond['x'])) + r" + C")
            try:
                c_sols = sp.solve(eq_c, C)
                if c_sols:
                    c_val = sp.simplify(c_sols[0])
                    cond_lines.append(r"C &= " + sp.latex(c_val))
                    cond_lines.append(r"\underline{" + int_l_tex + r" = " + int_r_tex + r" + \left(" + sp.latex(c_val) + r"\right) \quad \text{- CSR (uwikłana)}}")
                else:
                    cond_lines.append(r"\text{Dla } y(" + sp.latex(cond['x']) + r")=" + sp.latex(cond['v']) + r" \text{ układ jest sprzeczny.}")
                    cond_lines.append(r"\implies \text{Rozwiązaniem zadania jest funkcja osobliwa np. } y(x)=0")
            except:
                pass
                
        if len(cond_lines) > 1:
            st.latex("\\begin{aligned}\n" + " \\\\\n".join(cond_lines) + "\n\\end{aligned}")


# ==========================================
# INTERFEJS UŻYTKOWNIKA I ASYSTENT
# ==========================================
st.title("🧮 Kalkulator Równań Różniczkowych")
st.markdown("Wybierz odpowiednią zakładkę, wpisz równanie i kliknij **Rozwiąż**.")

st.info("💡 **Inteligentny Asystent Wyboru Modułu**")
col_a, col_b = st.columns([4, 1])
with col_a:
    router_input = st.text_input("Wklej tutaj swoje równanie:", placeholder="np. y'' - 4y' - 12y = 12x + 8", label_visibility="collapsed")
with col_b:
    btn_sprawdz = st.button("🔍 Sprawdź", use_container_width=True, type="primary")

if btn_sprawdz and router_input:
    typ_rownania, rekomendacja = sugeruj_zakladke(router_input)
    if typ_rownania:
        st.success(f"🔍 **Wynik analizy:** Wykryto **{typ_rownania}**")
        st.markdown(f"👉 {rekomendacja}")
        st.markdown("Skopiuj równanie do schowka (ikona w prawym górnym rogu poniższej ramki):")
        st.code(router_input, language="text")
st.markdown("---")

# ==========================================
# ŚCIĄGA DLA INŻYNIERA
# ==========================================
with st.expander("📚 Ściąga: Jak rozpoznać typ równania i wybrać zakładkę? (Kliknij, aby rozwinąć)"):
    st.markdown("""
    ### 🔵 Równania 1. Rzędu (najwyższa pochodna to $y'$)
    * **Zakładka 1: Zmienne Rozdzielone:** Da się łatwo zgrupować wszystkie $y$ po jednej stronie, a $x$ po drugiej poprzez mnożenie/dzielenie. 
        * *Postać:* $y' = f(x) \cdot g(y)$
        * *Przykład:* $y' = 4xy^2$
    * **Zakładka 2: Liniowe 1. Rzędu:** Zmienna $y$ oraz $y'$ występują tylko "luzem" w pierwszej potędze. Nie ma $y^2$ ani $\sin(y)$.
        * *Postać:* $y' + p(x)y = q(x)$
        * *Przykład:* $y' + 2y = 10x^2 + 5$
    * **Zakładka 7: Bernoulliego:** Bardzo podobne do liniowego, ale po prawej stronie zmienna $y$ jest podniesiona do potęgi $n$.
        * *Postać:* $y' + p(x)y = q(x)y^n$
        * *Przykład:* $y' + 2y = x \cdot y^3$

    ### 🔴 Równania 2. Rzędu (najwyższa pochodna to $y''$)
    * **Zakładka 3: Typ I:** Najprostsze. Występuje tylko druga pochodna i jakiś "ogon" z iksami. Wystarczy dwukrotnie obustronnie scałkować.
        * *Postać:* $y'' = f(x)$
        * *Przykład:* $y'' = 4\cos(2x)$
    * **Zakładka 4: Typ II (Brak zmiennej y):** W równaniu brakuje "jawnego" $y$. Są tylko pochodne $y', y''$ oraz zmienna $x$. Stosujemy podstawienie $y' = p(x)$.
        * *Postać:* $F(x, y', y'') = 0$
        * *Przykład:* $y'' - y' = 8x - 2$
    * **Zakładka 5: Typ III (Brak zmiennej x):** W równaniu brakuje "jawnego" $x$. Są tylko pochodne $y', y''$ oraz zmienna $y$. Stosujemy trudniejsze podstawienie $y' = p(y)$.
        * *Postać:* $F(y, y', y'') = 0$
        * *Przykład:* $y \cdot y'' = (y')^2$
    * **Zakładka 6: Typ IV (Liniowe 2. Rzędu):** Klasyk z kolokwium. Pochodne mają stałe liczbowe współczynniki (np. 1, 4, -2). Liczymy z Równania Charakterystycznego (RLJ) i Metody Przewidywań (MP).
        * *Postać:* $ay'' + by' + cy = f(x)$
        * *Przykład:* $y'' - 2y' + y = 4x - 2$
    """)

st.markdown("---")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Zmienne Rozdzielone", "Liniowe 1. Rzędu", "Typ I: y'' = f(x)", 
    "Typ II: F(x, y', y'') = 0", "Typ III: F(y, y', y'') = 0", 
    "Typ IV: Liniowe 2. Rzędu", "Bernoulliego"
])

# ==========================================
# TAB 1: Zmienne Rozdzielone
# ==========================================
with tab1:
    st.header("Metoda zmiennych rozdzielonych")
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input_1 = st.text_input("Równanie:", "y' = 4*x*y^2 ; y(-2)=0", key="in1")
    with col2:
        st.write("")
        btn1 = st.button("🚀 Rozwiąż", key="btn1", use_container_width=True)
    if btn1 and user_input_1:
        try:
            eq_str, conditions = preprocess_input(user_input_1)
            if '=' in eq_str:
                lhs_str, rhs_str = eq_str.split('=', 1)
                lhs = parse_expr(lhs_str, local_dict={'y': y_sym, 'yp': yp, 'x': x, 'e': sp.E}, transformations=transformations)
                rhs = parse_expr(rhs_str, local_dict={'y': y_sym, 'yp': yp, 'x': x, 'e': sp.E}, transformations=transformations)
                eq = sp.simplify(lhs - rhs)
                if eq.has(yp):
                    st.markdown("---")
                    st.markdown("### 📝 Rozwiązanie krok po kroku:")
                    solve_separable(eq, conditions)
                else:
                    st.warning("Nie wykryto pochodnej y'.")
            else:
                st.error("Błąd: Równanie musi zawierać znak '='.")
        except Exception as e:
            st.error(f"Błąd parsowania. Sprawdź zapis. Szczegóły: {e}")

# ==========================================
# TAB 2: Liniowe 1. Rzędu
# ==========================================
with tab2:
    st.header("Równania liniowe 1. rzędu")
    st.markdown("**Postać ogólna:** $y' + p(x)y = q(x)$")
    col1, col2 = st.columns([4, 1])
    with col1:
        eq_input_2 = st.text_input("Wprowadź równanie:", "y' + y/x = 9 - x^2 ; y(1)=2", key="input_t2")
    with col2:
        st.write("")
        btn_2 = st.button("🚀 Rozwiąż Liniowe", key="btn_t2", use_container_width=True)
    if btn_2 and eq_input_2:
        try:
            parts = eq_input_2.split(';')
            eq_str = parts[0].strip().replace('^', '**').replace("y'", "yp").replace("y’", "yp")
            conds = []
            if len(parts) > 1:
                for c in parts[1].split(','):
                    match = re.search(r'\((.*?)\)\s*=\s*(.*)', c.strip().replace('^', '**'))
                    if match:
                        conds.append({'x_val': sp.sympify(match.group(1), locals={'pi': sp.pi, 'e': sp.E}), 'y_val': sp.sympify(match.group(2), locals={'pi': sp.pi, 'e': sp.E})})
            if '=' not in eq_str:
                st.error("Błąd: Równanie musi zawierać znak '='.")
            else:
                lhs_str, rhs_str = eq_str.split('=', 1)
                lhs_expr = parse_expr(lhs_str, local_dict={'y': y_sym, 'yp': yp, 'x': x, 'e': sp.E}, transformations=transformations)
                rhs_expr = parse_expr(rhs_str, local_dict={'y': y_sym, 'yp': yp, 'x': x, 'e': sp.E}, transformations=transformations)
                eq = sp.simplify(lhs_expr - rhs_expr)
                yp_sols = sp.solve(eq, yp)
                if not yp_sols:
                    st.error("Nie można wyizolować pochodnej y'.")
                else:
                    yp_expr = sp.simplify(yp_sols[0])
                    poly = sp.expand(yp_expr)
                    p_x = sp.simplify(-poly.coeff(y_sym, 1))
                    q_x = sp.simplify(poly + p_x * y_sym)
                    if q_x.has(y_sym):
                        st.warning("To równanie zawiera potęgi y. Przejdź do zakładki 'Bernoulliego'.")
                    else:
                        st.markdown("---")
                        st.markdown("### 📝 Rozwiązanie krok po kroku:")
                        lines = []
                        lines.append(rf"y^{{\prime}} + \left({sp.latex(p_x)}\right)y = {sp.latex(q_x)}")
                        lines.append(r"")
                        lines.append(r"\text{1. Równanie Liniowe Jednorodne (RLJ):}")
                        lines.append(rf"y^{{\prime}} + \left({sp.latex(p_x)}\right)y = 0 \quad / : y \quad / \cdot dx")
                        lines.append(rf"\frac{{dy}}{{y}} = {sp.latex(-p_x)} dx \quad / \int")
                        int_p = sp.integrate(-p_x, x)
                        int_p_tex = sp.latex(int_p).replace('log', 'ln')
                        lines.append(rf"\ln|y| = {int_p_tex} + C_1 \quad / e^{{(\dots)}}")
                        lines.append(rf"y_0 = C \cdot e^{{{int_p_tex}}} \quad \text{{- CORJ}}")
                        lines.append(r"")
                        lines.append(r"\text{2. Metoda uzmienniania stałej (RLN):}")
                        lines.append(rf"y = C(x) \cdot e^{{{int_p_tex}}}")
                        y_deriv = sp.simplify(sp.diff(sp.exp(int_p), x))
                        lines.append(rf"y^{{\prime}} = C^{{\prime}}(x) e^{{{int_p_tex}}} + C(x) \left({sp.latex(y_deriv)}\right)")
                        lines.append(rf"C^{{\prime}}(x) e^{{{int_p_tex}}} = {sp.latex(q_x)}")
                        c_prime = sp.simplify(q_x / sp.exp(int_p))
                        lines.append(rf"C^{{\prime}}(x) = {sp.latex(c_prime)} \quad / \int")
                        c_int = sp.integrate(c_prime, x)
                        c_int_tex = sp.latex(c_int).replace('log', 'ln')
                        lines.append(rf"C(x) = {c_int_tex} + C_1")
                        y_final = sp.simplify((c_int + C1) * sp.exp(int_p))
                        lines.append(rf"\text{{Odp:}} \quad \underline{{y = \left({c_int_tex} + C_1\right) e^{{{int_p_tex}}} \quad \text{{- CORN}}}}")
                        if conds:
                            st.markdown("---")
                            zp_lines = []
                            c_data = conds[0]
                            zp_lines.append(rf"\text{{Z.P.}} \quad y({sp.latex(c_data['x_val'])}) = {sp.latex(c_data['y_val'])}")
                            val_expr = y_final.subs(x, c_data['x_val'])
                            zp_lines.append(rf"{sp.latex(c_data['y_val'])} = {sp.latex(val_expr).replace('log', 'ln')}")
                            sols = sp.solve(sp.Eq(val_expr, c_data['y_val']), C1)
                            if sols:
                                zp_lines.append(rf"C_1 = {sp.latex(sols[0])}")
                                y_s = y_final.subs(C1, sols[0])
                                zp_lines.append(rf"\text{{Odp:}} \quad \underline{{ y_s = {sp.latex(y_s).replace('log', 'ln')} \quad \text{{- CSR}} }}")
                            lines.extend(zp_lines)
                        st.latex("\\begin{aligned}\n" + " \\\\\n".join(lines) + "\n\\end{aligned}")
        except Exception as e:
            st.error(f"Błąd analizy równania. Szczegóły: {e}")

# ==========================================
# TAB 3: Typ I: y'' = f(x)
# ==========================================
with tab3:
    st.header("Typ I: Równania sprowadzalne do rzędu I")
    st.markdown("**Postać:** $y'' = f(x)$")
    col1, col2 = st.columns([4, 1])
    with col1:
        eq_input_3 = st.text_input("Wprowadź równanie:", "y'' = 4*cos(2x) ; y(0)=0, y'(0)=0", key="input_t3")
    with col2:
        st.write("")
        btn_3 = st.button("🚀 Rozwiąż Typ I", key="btn_t3", use_container_width=True)
    if btn_3 and eq_input_3:
        try:
            parts = eq_input_3.split(';')
            eq_str = parts[0].strip().replace('^', '**').replace("y''", "ypp").replace('y"', 'ypp').replace("y”", "ypp")
            conds = []
            if len(parts) > 1:
                for c in parts[1].strip().split(','):
                    c = c.strip().replace('^', '**')
                    t = 'yp' if "'" in c or "yp" in c else 'y'
                    match = re.search(r'\((.*?)\)\s*=\s*(.*)', c)
                    if match:
                        conds.append({'type': t, 'x_val': sp.sympify(match.group(1), locals={'pi': sp.pi, 'e': sp.E}), 'y_val': sp.sympify(match.group(2), locals={'pi': sp.pi, 'e': sp.E})})
            if '=' not in eq_str:
                st.error("Błąd: Równanie musi zawierać znak '='.")
            else:
                lhs_str, rhs_str = eq_str.split('=', 1)
                f_x = parse_expr(rhs_str, local_dict={'x': x, 'e': sp.E, 'pi': sp.pi}, transformations=transformations)
                st.markdown("---")
                st.markdown("### 📝 Rozwiązanie krok po kroku:")
                lines = []
                lines.append(rf"y^{{\prime\prime}} &= {sp.latex(f_x)} \quad \rightarrow \text{{Typ I: }} y^{{\prime\prime}} = f(x)")
                lines.append(r"\bullet \text{ dwukrotnie całkujemy:}")
                int_1 = sp.integrate(f_x, x)
                int_1_tex = sp.latex(int_1).replace('log', 'ln')
                lines.append(rf"y^{{\prime}} &= \int \left({sp.latex(f_x)}\right) dx = {int_1_tex} + C_1")
                int_2 = sp.integrate(int_1, x)
                int_2_tex = sp.latex(int_2).replace('log', 'ln')
                if int_1 == 0:
                     lines.append(rf"y &= \int (C_1) dx = C_1 x + C_2")
                     y_gen = C1*x + C2
                else:
                     lines.append(rf"y &= \int \left({int_1_tex} + C_1\right) dx = {int_2_tex} + C_1 x + C_2")
                     y_gen = int_2 + C1*x + C2
                lines.append(rf"\text{{czyli:}}")
                lines.append(rf"&\underline{{y = {sp.latex(y_gen).replace('log', 'ln')} \quad \text{{- COR}}}}")
                st.latex("\\begin{aligned}\n" + " \\\\\n".join(lines) + "\n\\end{aligned}")
                if conds:
                    st.markdown("---")
                    zp_lines = []
                    eq_yp = int_1 + C1
                    eq_y = y_gen
                    cases_str = rf"y = {sp.latex(eq_y).replace('log', 'ln')} \\ "
                    for c in conds:
                        if c['type'] == 'y': cases_str += rf"y({sp.latex(c['x_val'])}) = {sp.latex(c['y_val'])} \\ "
                        else: cases_str += rf"y^{{\prime}}({sp.latex(c['x_val'])}) = {sp.latex(c['y_val'])} \\ "
                    zp_lines.append(rf"\text{{Z.P.}} \quad \begin{{cases}} {cases_str} \end{{cases}}")
                    system_eqs = []
                    subst_lines = []
                    for c in conds:
                        if c['type'] == 'y':
                            val_expr = eq_y.subs(x, c['x_val'])
                            system_eqs.append(sp.Eq(val_expr, c['y_val']))
                            subst_lines.append(rf"{sp.latex(c['y_val'])} = {sp.latex(val_expr).replace('log', 'ln')}")
                        else:
                            val_expr = eq_yp.subs(x, c['x_val'])
                            system_eqs.append(sp.Eq(val_expr, c['y_val']))
                            subst_lines.append(rf"{sp.latex(c['y_val'])} = {sp.latex(val_expr).replace('log', 'ln')}")
                    for sl in subst_lines: zp_lines.append(sl)
                    sols = sp.solve(system_eqs, (C1, C2))
                    if sols:
                        if isinstance(sols, dict):
                            c1_ans, c2_ans = sols.get(C1, C1), sols.get(C2, C2)
                        else:
                            c1_ans, c2_ans = sols[0][0], sols[0][1]
                        zp_lines.append(rf"C_1 = {sp.latex(c1_ans)} \quad , \quad C_2 = {sp.latex(c2_ans)}")
                        y_s = eq_y.subs({C1: c1_ans, C2: c2_ans})
                        zp_lines.append(rf"\text{{Odp:}} \quad \underline{{ y_s = {sp.latex(y_s).replace('log', 'ln')} \quad \text{{- CSR}} }}")
                    else:
                        zp_lines.append(rf"\text{{Brak rozwiązań dla podanych warunków.}}")
                    st.latex("\\begin{aligned}\n" + " \\\\\n".join(zp_lines) + "\n\\end{aligned}")
        except Exception as e:
            st.error(f"Błąd analizy równania. Szczegóły: {e}")

# ==========================================
# TAB 4: Typ II (brak y)
# ==========================================
with tab4:
    st.header("Typ II: Równania niezawierające zmiennej y")
    st.markdown("**Postać ogólna:** $F(x, y', y'') = 0$")
    st.markdown("**Podstawienie:** $y' = p(x)$ oraz $y'' = p'(x)$")
    col1, col2 = st.columns([4, 1])
    with col1:
        eq_input_4 = st.text_input("Wprowadź równanie:", "y'' - y' = 8x - 2", key="input_t4")
    with col2:
        st.write("")
        btn_4 = st.button("🚀 Rozwiąż Typ II", key="btn_t4", use_container_width=True)
    if btn_4 and eq_input_4:
        try:
            parts = eq_input_4.split(';')
            eq_str = parts[0].strip().replace('^', '**').replace("y''", "ypp").replace('y"', 'ypp').replace("y”", "ypp").replace("y'", "yp")
            conds = []
            if len(parts) > 1:
                for c in parts[1].split(','):
                    t = 'yp' if "'" in c or "yp" in c else 'y'
                    match = re.search(r'\((.*?)\)\s*=\s*(.*)', c.strip().replace('^', '**'))
                    if match:
                        conds.append({'type': t, 'x_val': sp.sympify(match.group(1), locals={'pi': sp.pi, 'e': sp.E}), 'y_val': sp.sympify(match.group(2), locals={'pi': sp.pi, 'e': sp.E})})
            if '=' not in eq_str:
                st.error("Błąd: Równanie musi zawierać znak '='.")
            else:
                lhs_str, rhs_str = eq_str.split('=', 1)
                lhs_expr = parse_expr(lhs_str, local_dict={'y': y_sym, 'yp': yp, 'ypp': ypp, 'x': x}, transformations=transformations)
                rhs_expr = parse_expr(rhs_str, local_dict={'x': x, 'e': sp.E, 'pi': sp.pi}, transformations=transformations)
                eq = sp.simplify(lhs_expr - rhs_expr)
                
                if eq.has(y_sym):
                    st.warning("Równanie zawiera zmienną 'y'. To nie jest Typ II! Sprawdź Typ III lub IV.")
                elif not eq.has(ypp):
                    st.warning("Brak drugiej pochodnej y''.")
                else:
                    st.markdown("---")
                    st.markdown("### 📝 Rozwiązanie krok po kroku:")
                    lines = []
                    disp_eq = sp.Eq(lhs_expr, rhs_expr)
                    lines.append(r"\text{Równanie wyjściowe: } " + sp.latex(disp_eq).replace('ypp', r'{y^{\prime\prime}}').replace('yp', r'{y^{\prime}}'))
                    lines.append("")
                    lines.append(r"\text{1. Podstawienie obniżające rząd:}")
                    lines.append(r"y^{\prime} = p(x) \implies y^{\prime\prime} = p^{\prime}(x)")
                    
                    p_func = sp.Function('p')(x)
                    eq_p = eq.subs({ypp: p_func.diff(x), yp: p_func, y_sym: 0})
                    p_sym = sp.Symbol('p')
                    pp_sym = sp.Symbol(r'{p^{\prime}}')
                    eq_p_disp = eq.subs({ypp: pp_sym, yp: p_sym})
                    lines.append(r"\text{Równanie I rzędu dla zmiennej } p: \quad " + sp.latex(eq_p_disp) + " = 0")
                    
                    sol_p = sp.dsolve(eq_p, p_func)
                    if isinstance(sol_p, list): sol_p = sol_p[-1]
                    p_rhs = sol_p.rhs
                    
                    lines.append("")
                    lines.append(r"\text{2. Rozwiązujemy równanie dla } p(x):")
                    lines.append(r"p(x) = " + sp.latex(p_rhs))
                    lines.append("")
                    lines.append(r"\text{3. Wracamy do podstawienia i całkujemy:}")
                    lines.append(r"y^{\prime} = p(x) = " + sp.latex(p_rhs))
                    lines.append(r"y = \int \left( " + sp.latex(p_rhs) + r" \right) dx")
                    
                    final_y = sp.simplify(sp.integrate(p_rhs, x) + C2)
                    lines.append(r"\text{Całkujemy:}")
                    lines.append(r"\underline{ y(x) = " + sp.latex(final_y) + r" \quad \text{- COR} }")
                    
                    if conds:
                        lines.append("")
                        lines.append(r"\underline{\textbf{etap III}} \quad \text{Zagadnienie Początkowe (Z.P.)}")
                        y_prime_eq = sp.simplify(sp.diff(final_y, x))
                        cases_str = r"y = " + sp.latex(final_y) + r" \\ "
                        for c_d in conds:
                            if c_d['type'] == 'y': cases_str += r"y(" + sp.latex(c_d['x_val']) + r") = " + sp.latex(c_d['y_val']) + r" \\ "
                            else: cases_str += r"y^{\prime}(" + sp.latex(c_d['x_val']) + r") = " + sp.latex(c_d['y_val']) + r" \\ "
                        lines.append(r"\text{Z.P.} \quad \begin{cases} " + cases_str + r" \end{cases}")
                        lines.append(r"y^{\prime} = " + sp.latex(y_prime_eq))
                        sys_eqs = []
                        for c_d in conds:
                            if c_d['type'] == 'y':
                                val = sp.simplify(final_y.subs(x, c_d['x_val']))
                                sys_eqs.append(sp.Eq(val, c_d['y_val']))
                            else:
                                val = sp.simplify(y_prime_eq.subs(x, c_d['x_val']))
                                sys_eqs.append(sp.Eq(val, c_d['y_val']))
                        try:
                            sols = sp.solve(sys_eqs, (C1, C2), dict=True)
                            if sols and len(sols) > 0:
                                c1_ans, c2_ans = sols[0].get(C1, C1), sols[0].get(C2, C2)
                                lines.append(r"C_1 = " + sp.latex(c1_ans) + r" \quad , \quad C_2 = " + sp.latex(c2_ans))
                                y_s_final = sp.simplify(final_y.subs({C1: c1_ans, C2: c2_ans}))
                                lines.append(r"\text{Odp:} \quad \underline{ y_s = " + sp.latex(y_s_final) + r" \quad \text{- CSR} }")
                            else:
                                lines.append(r"\text{Brak jednoznacznych rozwiązań dla podanych warunków.}")
                        except: pass
                    st.latex("\\begin{aligned}\n" + " \\\\\n".join(lines) + "\n\\end{aligned}")
        except Exception as e:
            st.error(f"Błąd analizy równania. Szczegóły: {e}")

# ==========================================
# TAB 5: Typ III (brak x)
# ==========================================
with tab5:
    st.header("Typ III: Równania niezawierające zmiennej x")
    st.markdown("**Postać ogólna:** $F(y, y', y'') = 0$")
    st.markdown(r"**Podstawienie:** $y' = p(y)$ oraz $y'' = p \cdot \frac{dp}{dy}$")
    col1, col2 = st.columns([4, 1])
    with col1:
        eq_input_5 = st.text_input("Wprowadź równanie:", "y*y'' = (y')^2 ; y(1)=1, y'(1)=2", key="input_t5")
    with col2:
        st.write("")
        btn_5 = st.button("🚀 Rozwiąż Typ III", key="btn_t5", use_container_width=True)
    if btn_5 and eq_input_5:
        try:
            parts = eq_input_5.split(';')
            eq_str = parts[0].strip().replace('^', '**').replace("y''", "ypp").replace('y"', 'ypp').replace("y”", "ypp").replace("y'", "yp")
            conds = []
            if len(parts) > 1:
                for c in parts[1].split(','):
                    t = 'yp' if "'" in c or "yp" in c else 'y'
                    match = re.search(r'\((.*?)\)\s*=\s*(.*)', c.strip().replace('^', '**'))
                    if match:
                        conds.append({'type': t, 'x_val': sp.sympify(match.group(1), locals={'pi': sp.pi, 'e': sp.E}), 'y_val': sp.sympify(match.group(2), locals={'pi': sp.pi, 'e': sp.E})})
            if '=' not in eq_str:
                st.error("Błąd: Równanie musi zawierać znak '='.")
            else:
                lhs_str, rhs_str = eq_str.split('=', 1)
                lhs_expr = parse_expr(lhs_str, local_dict={'y': y_sym, 'yp': yp, 'ypp': ypp, 'x': x}, transformations=transformations)
                rhs_expr = parse_expr(rhs_str, local_dict={'y': y_sym, 'yp': yp, 'ypp': ypp, 'x': x}, transformations=transformations)
                eq = sp.simplify(lhs_expr - rhs_expr)
                if eq.has(x):
                    st.warning("Równanie zawiera jawną zmienną 'x'. To nie jest Typ III! Sprawdź Typ II lub IV.")
                elif not eq.has(ypp):
                    st.warning("Brak drugiej pochodnej y''.")
                else:
                    st.markdown("---")
                    st.markdown("### 📝 Rozwiązanie krok po kroku:")
                    lines = []
                    disp_eq = sp.Eq(lhs_expr, rhs_expr)
                    lines.append(r"\text{Równanie wyjściowe: } " + sp.latex(disp_eq).replace('ypp', r'{y^{\prime\prime}}').replace('yp', r'{y^{\prime}}'))
                    lines.append("")
                    lines.append(r"\text{1. Podstawienie obniżające rząd (zmienną niezależną staje się } y \text{):}")
                    lines.append(r"y^{\prime} = p(y) \implies y^{\prime\prime} = p \cdot \frac{dp}{dy}")
                    
                    p_func = sp.Function('p')(y_sym)
                    eq_p = eq.subs({ypp: p_func * p_func.diff(y_sym), yp: p_func})
                    p_sym = sp.Symbol('p')
                    dp_dy = sp.Symbol(r'\frac{dp}{dy}')
                    eq_p_disp = eq.subs({ypp: p_sym * dp_dy, yp: p_sym})
                    lines.append(r"\text{Równanie I rzędu: } \quad " + sp.latex(eq_p_disp) + " = 0")
                    
                    try: eq_p_clean = sp.simplify(eq_p / p_func)
                    except: eq_p_clean = eq_p
                    sol_p = sp.dsolve(eq_p_clean, p_func)
                    if isinstance(sol_p, list): sol_p = sol_p[-1]
                    p_rhs = sol_p.rhs
                    
                    lines.append("")
                    lines.append(r"\text{2. Rozwiązujemy to równanie dla zmiennej } p:")
                    lines.append(r"p(y) = " + sp.latex(p_rhs))
                    lines.append("")
                    lines.append(r"\text{3. Wracamy do podstawienia } y^{\prime} = p(y):")
                    lines.append(r"y^{\prime} = " + sp.latex(p_rhs))
                    
                    y_func = sp.Function('y')(x)
                    eq_y = sp.Eq(y_func.diff(x), p_rhs.subs(y_sym, y_func))
                    sol_y = sp.dsolve(eq_y, y_func)
                    if isinstance(sol_y, list): sol_y = sol_y[-1]
                    final_y = sol_y.rhs
                    
                    lines.append("")
                    lines.append(r"\text{4. Całka Ogólna Równania:}")
                    lines.append(r"\underline{ y(x) = " + sp.latex(final_y) + r" \quad \text{- COR} }")
                    
                    if conds:
                        lines.append("")
                        lines.append(r"\underline{\textbf{etap III}} \quad \text{Zagadnienie Początkowe (Z.P.)}")
                        y_prime_eq = sp.simplify(sp.diff(final_y, x))
                        cases_str = r"y = " + sp.latex(final_y) + r" \\ "
                        for c_d in conds:
                            if c_d['type'] == 'y': cases_str += r"y(" + sp.latex(c_d['x_val']) + r") = " + sp.latex(c_d['y_val']) + r" \\ "
                            else: cases_str += r"y^{\prime}(" + sp.latex(c_d['x_val']) + r") = " + sp.latex(c_d['y_val']) + r" \\ "
                        lines.append(r"\text{Z.P.} \quad \begin{cases} " + cases_str + r" \end{cases}")
                        sys_eqs = []
                        for c_d in conds:
                            if c_d['type'] == 'y':
                                val = sp.simplify(final_y.subs(x, c_d['x_val']))
                                sys_eqs.append(sp.Eq(val, c_d['y_val']))
                            else:
                                val = sp.simplify(y_prime_eq.subs(x, c_d['x_val']))
                                sys_eqs.append(sp.Eq(val, c_d['y_val']))
                        try:
                            sols = sp.solve(sys_eqs, (C1, C2), dict=True)
                            if sols and len(sols) > 0:
                                c1_ans, c2_ans = sols[0].get(C1, C1), sols[0].get(C2, C2)
                                lines.append(r"C_1 = " + sp.latex(c1_ans) + r" \quad , \quad C_2 = " + sp.latex(c2_ans))
                                y_s_final = sp.simplify(final_y.subs({C1: c1_ans, C2: c2_ans}))
                                lines.append(r"\text{Odp:} \quad \underline{ y_s = " + sp.latex(y_s_final) + r" \quad \text{- CSR} }")
                        except: pass
                    st.latex("\\begin{aligned}\n" + " \\\\\n".join(lines) + "\n\\end{aligned}")
        except Exception as e:
            st.error(f"Błąd analizy równania. Szczegóły: {e}")

# ==========================================
# TAB 6: Typ IV (Liniowe 2. Rzędu stałe wpół.)
# ==========================================
with tab6:
    st.header("Typ IV: Liniowe 2. rzędu o stałych współczynnikach")
    st.markdown("**Postać ogólna:** $y'' + py' + qy = f(x)$")
    col1, col2 = st.columns([4, 1])
    with col1:
        eq_input_6 = st.text_input("Wprowadź równanie:", "y'' + 9*y = 0 ; y(pi/2)=2, y(pi/3)=6", key="input_t6")
    with col2:
        st.write("")
        btn_6 = st.button("🚀 Rozwiąż Typ IV", key="btn_t6", use_container_width=True)
    if btn_6 and eq_input_6:
        try:
            parts = eq_input_6.split(';')
            eq_str = parts[0].strip().replace('^', '**').replace("y''", "ypp").replace('y"', 'ypp').replace("y”", "ypp").replace("y'", "yp")
            conds = []
            if len(parts) > 1:
                for c in parts[1].split(','):
                    c = c.strip().replace('^', '**')
                    t = 'yp' if "'" in c or "yp" in c else 'y'
                    match = re.search(r'\((.*?)\)\s*=\s*(.*)', c)
                    if match:
                        conds.append({'type': t, 'x_val': sp.sympify(match.group(1), locals={'pi': sp.pi, 'e': sp.E}), 'y_val': sp.sympify(match.group(2), locals={'pi': sp.pi, 'e': sp.E})})
            if '=' not in eq_str:
                st.error("Błąd: Równanie musi zawierać znak '='.")
            else:
                lhs_str, rhs_str = eq_str.split('=', 1)
                r = sp.Symbol('r')
                lhs_expr = parse_expr(lhs_str, local_dict={'y': y_sym, 'yp': yp, 'ypp': ypp, 'x': x}, transformations=transformations)
                rhs_expr = parse_expr(rhs_str, local_dict={'x': x, 'e': sp.E, 'pi': sp.pi}, transformations=transformations)
                eq = sp.simplify(lhs_expr - rhs_expr)
                a = eq.coeff(ypp)
                b = eq.coeff(yp)
                c = eq.coeff(y_sym)
                f_x = sp.simplify(-(eq - (a*ypp + b*yp + c*y_sym)))
                
                st.markdown("---")
                st.markdown("### 📝 Rozwiązanie krok po kroku:")
                lines = []
                disp_lhs = sp.latex(a*ypp + b*yp + c*y_sym).replace('ypp', r'y^{\prime\prime}').replace('yp', r'y^{\prime}')
                lines.append(rf"{disp_lhs} = {sp.latex(f_x)}")
                lines.append(r"")
                lines.append(r"\underline{\textbf{etap I}} \quad \text{RLJ}")
                lines.append(rf"{disp_lhs} = 0")
                char_eq = a*r**2 + b*r + c
                lines.append(rf"{sp.latex(char_eq)} = 0 \quad \text{{- r. charakterystyczne}}")
                delta = sp.simplify(b**2 - 4*a*c)
                lines.append(rf"\Delta = {sp.latex(delta)}")
                
                d_val = float(delta)
                y_0 = 0
                C1, C2 = sp.symbols('C1 C2')
                if d_val > 0:
                    r1 = sp.simplify((-b - sp.sqrt(delta))/(2*a))
                    r2 = sp.simplify((-b + sp.sqrt(delta))/(2*a))
                    lines.append(rf"r_1 = {sp.latex(r1)} \quad ; \quad r_2 = {sp.latex(r2)}")
                    lines.append(rf"\begin{{cases}} y_1 = e^{{{sp.latex(r1)}x}} \\ y_2 = e^{{{sp.latex(r2)}x}} \end{{cases}} \quad \text{{- układ fundamentalny}}")
                    y_0 = C1*sp.exp(r1*x) + C2*sp.exp(r2*x)
                elif d_val == 0:
                    r0 = sp.simplify(-b/(2*a))
                    lines.append(rf"r_0 = {sp.latex(r0)}")
                    lines.append(rf"\begin{{cases}} y_1 = e^{{{sp.latex(r0)}x}} \\ y_2 = x e^{{{sp.latex(r0)}x}} \end{{cases}} \quad \text{{- układ fundamentalny}}")
                    y_0 = (C1 + C2*x)*sp.exp(r0*x)
                else:
                    alpha = sp.simplify(-b/(2*a))
                    beta = sp.simplify(sp.sqrt(-delta)/(2*a))
                    lines.append(rf"\alpha = {sp.latex(alpha)} \quad ; \quad \beta = {sp.latex(beta)}")
                    lines.append(rf"\begin{{cases}} y_1 = e^{{{sp.latex(alpha)}x}} \cos({sp.latex(beta)}x) \\ y_2 = e^{{{sp.latex(alpha)}x}} \sin({sp.latex(beta)}x) \end{{cases}} \quad \text{{- układ fundamentalny}}")
                    y_0 = sp.simplify(sp.exp(alpha*x)*(C1*sp.cos(beta*x) + C2*sp.sin(beta*x)))
                    
                lines.append(rf"\text{{tw. \quad }} y_0 = C_1 y_1 + C_2 y_2")
                lines.append(rf"\underline{{y_0 = {sp.latex(y_0)} \quad \text{{- CORLJ}}}}")
                
                final_y = y_0
                if f_x != 0:
                    lines.append(r"")
                    lines.append(r"\underline{\textbf{etap II}} \quad \text{MP}")
                    lines.append(rf"f(x) = {sp.latex(f_x)}")
                    try:
                        if f_x.is_polynomial(x):
                            deg = sp.degree(f_x, x)
                            k = 0
                            root_msg = r"\text{Liczba } r=0 \text{ nie jest pierw. r.ch.}"
                            if float(c) == 0 and float(b) != 0:
                                k = 1
                                root_msg = r"\text{Liczba } r=0 \text{ jest pierw. jednokrotnym}"
                            elif float(c) == 0 and float(b) == 0:
                                k = 2
                                root_msg = r"\text{Liczba } r=0 \text{ jest pierw. dwukrotnym}"
                                
                            lines.append(rf"{root_msg} \rightarrow \text{{mnożymy przez }} x^{k}")
                            letters = sp.symbols('A B C D E F')
                            poly_base = sum(letters[i] * x**(deg-i) for i in range(deg+1))
                            y_s = sp.expand((x**k) * poly_base)
                            lines.append(rf"\text{{CSRLN:}} \quad y_s = x^{k} ({sp.latex(poly_base)}) = {sp.latex(y_s)}")
                            y_s_p = sp.diff(y_s, x)
                            y_s_pp = sp.diff(y_s_p, x)
                            lines.append(r"\text{podstawiamy do RLN:}")
                            subst_eq = sp.expand(a*y_s_pp + b*y_s_p + c*y_s)
                            lines.append(rf"{sp.latex(subst_eq)} = {sp.latex(f_x)}")
                            
                            eqs_to_solve = []
                            syms_to_solve = [letters[i] for i in range(deg+1)]
                            for p_pow in range(deg + k, -1, -1):
                                lhs_coeff = subst_eq.coeff(x, p_pow)
                                rhs_coeff = f_x.coeff(x, p_pow)
                                if lhs_coeff != 0 or rhs_coeff != 0:
                                    eqs_to_solve.append(sp.Eq(lhs_coeff, rhs_coeff))
                            
                            sols = sp.solve(eqs_to_solve, syms_to_solve)
                            if sols:
                                final_y_s = y_s.subs(sols)
                                final_y = y_0 + final_y_s
                                lines.append(rf"\text{{tw. }} \quad y = y_0 + y_s")
                                lines.append(rf"\underline{{y(x) = {sp.latex(final_y)} \quad \text{{- CORLN}}}}")
                            else:
                                lines.append(r"\text{Błąd przy wyliczaniu stałych.}")
                        else:
                            lines.append(r"\text{(Funkcja } f(x) \text{ wymaga rozszerzonego modułu)}")
                    except: pass
                else:
                    lines.append(r"")
                    lines.append(r"\text{Ponieważ } f(x) = 0\text{, pomijamy etap II (równanie jednorodne).}")
                    lines.append(rf"\underline{{y(x) = {sp.latex(final_y)} \quad \text{{- CORLJ}}}}")
                    
                # POPRAWIONY ETAP III (Bezwzględny brak skrótów myślowych)
                if conds:
                    lines.append(r"")
                    lines.append(r"\underline{\textbf{etap III}} \quad \text{Zagadnienie Początkowe (Z.P.)}")
                    y_prime_eq = sp.simplify(sp.diff(final_y, x))
                    cases_str = rf"y = {sp.latex(final_y)} \\ "
                    for c_d in conds:
                        if c_d['type'] == 'y': cases_str += rf"y({sp.latex(c_d['x_val'])}) = {sp.latex(c_d['y_val'])} \\ "
                        else: cases_str += rf"y^{{\prime}}({sp.latex(c_d['x_val'])}) = {sp.latex(c_d['y_val'])} \\ "
                    lines.append(rf"\text{{Z.P.}} \quad \begin{{cases}} {cases_str} \end{{cases}}")
                    
                    lines.append(r"")
                    lines.append(r"\text{Podstawiamy warunki brzegowe (krok po kroku):}")
                    sys_eqs = []
                    
                    for c_d in conds:
                        x_val_latex = sp.latex(c_d['x_val'])
                        y_val_latex = sp.latex(c_d['y_val'])
                        
                        # Tworzymy atrapę zmiennej x, żeby zablokować natychmiastowe obliczanie trygonometrii
                        dummy_x = sp.Symbol(rf"\left({x_val_latex}\right)")
                        
                        if c_d['type'] == 'y':
                            lines.append(rf"\text{{Dla }} x = {x_val_latex}, \quad y = {y_val_latex}:")
                            # 1. Podstawienie "surowe" (tylko zamiana znaków)
                            raw_subbed = final_y.subs(x, dummy_x)
                            # 2. Pełne matematyczne wyliczenie (znikające zera itp.)
                            eval_subbed = sp.simplify(final_y.subs(x, c_d['x_val']))
                        else:
                            lines.append(rf"\text{{Dla }} x = {x_val_latex}, \quad y' = {y_val_latex}:")
                            raw_subbed = y_prime_eq.subs(x, dummy_x)
                            eval_subbed = sp.simplify(y_prime_eq.subs(x, c_d['x_val']))
                            
                        # Drukujemy linię przed uproszczeniem
                        lines.append(rf"{y_val_latex} = {sp.latex(raw_subbed)}")
                        
                        # Jeśli uproszczona wersja różni się od surowej, pokazujemy wynik uproszczenia z implikacją
                        if sp.latex(raw_subbed) != sp.latex(eval_subbed):
                            lines.append(rf"\implies {y_val_latex} = {sp.latex(eval_subbed)}")
                            
                        lines.append(r"") # Odstęp
                        sys_eqs.append(sp.Eq(eval_subbed, c_d['y_val']))
                            
                    sols = sp.solve(sys_eqs, (C1, C2))
                    
                    if sols:
                        if isinstance(sols, dict):
                            c1_ans, c2_ans = sols.get(C1, C1), sols.get(C2, C2)
                        else:
                            c1_ans, c2_ans = sols[0][0], sols[0][1]
                        lines.append(rf"C_1 = {sp.latex(c1_ans)} \quad , \quad C_2 = {sp.latex(c2_ans)}")
                        y_s_final = sp.simplify(final_y.subs({C1: c1_ans, C2: c2_ans}))
                        lines.append(rf"\text{{Odp:}} \quad \underline{{ y_s = {sp.latex(y_s_final)} \quad \text{{- CSR}} }}")
                    else:
                        lines.append(r"\textbf{Wniosek:} \text{ Otrzymano układ sprzeczny.}")
                        lines.append(r"\text{Brak rozwiązania dla podanych warunków brzegowych.}")
                        
                st.latex("\\begin{aligned}\n" + " \\\\\n".join(lines) + "\n\\end{aligned}")
        except Exception as e:
            st.error(f"Błąd analizy równania. Szczegóły: {e}")

# ==========================================
# TAB 7: Bernoulliego
# ==========================================
with tab7:
    st.header("Równania Bernoulliego")
    st.markdown("**Postać ogólna:** $y' + p(x)y = q(x)y^n$")
    col1, col2 = st.columns([4, 1])
    with col1:
        eq_input_7 = st.text_input("Wprowadź równanie:", "y' = y^2 * sin(2x) ; y(pi/2)=-4", key="input_t7")
    with col2:
        st.write("")
        btn_7 = st.button("🚀 Rozwiąż Bernoulliego", key="btn_t7", use_container_width=True)
    if btn_7 and eq_input_7:
        try:
            parts = eq_input_7.split(';')
            eq_str = parts[0].strip().replace('^', '**').replace("y'", "yp").replace("y’", "yp")
            conds = []
            if len(parts) > 1:
                for c in parts[1].split(','):
                    match = re.search(r'\((.*?)\)\s*=\s*(.*)', c.strip().replace('^', '**'))
                    if match:
                        conds.append({'x_val': sp.sympify(match.group(1), locals={'pi': sp.pi, 'e': sp.E}), 'y_val': sp.sympify(match.group(2), locals={'pi': sp.pi, 'e': sp.E})})
            if '=' not in eq_str:
                st.error("Błąd: Równanie musi zawierać znak '='.")
            else:
                lhs_str, rhs_str = eq_str.split('=', 1)
                lhs_expr = parse_expr(lhs_str, local_dict={'y': y_sym, 'yp': yp, 'x': x, 'e': sp.E}, transformations=transformations)
                rhs_expr = parse_expr(rhs_str, local_dict={'y': y_sym, 'yp': yp, 'x': x, 'e': sp.E}, transformations=transformations)
                eq = sp.simplify(lhs_expr - rhs_expr)
                yp_sols = sp.solve(eq, yp)
                if not yp_sols:
                    st.error("Nie można wyizolować pochodnej y'.")
                else:
                    yp_expr = sp.simplify(yp_sols[0])
                    poly = sp.expand(yp_expr)
                    p_x = sp.simplify(-poly.coeff(y_sym, 1))
                    remainder = sp.simplify(poly + p_x * y_sym)
                    if not remainder.has(y_sym):
                        st.warning("To jest zwykłe równanie liniowe. Przejdź do zakładki 'Liniowe 1. Rzędu'.")
                    else:
                        q_x, y_part = remainder.as_independent(y_sym, as_Add=False)
                        base, n = y_part.as_base_exp()
                        if base == y_sym:
                            st.markdown("---")
                            st.markdown("### 📝 Rozwiązanie krok po kroku:")
                            lines = []
                            lines.append(rf"y^{{\prime}} + \left({sp.latex(p_x)}\right)y = {sp.latex(q_x)} y^{{{sp.latex(n)}}}")
                            lines.append(r"")
                            lines.append(rf"\text{{1. Dzielimy przez }} y^{{{sp.latex(n)}}}:")
                            lines.append(rf"y^{{{sp.latex(-n)}}} y^{{\prime}} + \left({sp.latex(p_x)}\right) y^{{{sp.latex(1-n)}}} = {sp.latex(q_x)}")
                            u_sub = sp.simplify(1 - n)
                            lines.append(r"")
                            lines.append(r"\text{2. Podstawienie:}")
                            lines.append(rf"u = y^{{{sp.latex(u_sub)}}} \implies u^{{\prime}} = {sp.latex(u_sub)} y^{{{sp.latex(-n)}}} y^{{\prime}} \implies y^{{{sp.latex(-n)}}} y^{{\prime}} = \frac{{u^{{\prime}}}}{{{sp.latex(u_sub)}}}")
                            p_u = sp.simplify(u_sub * p_x)
                            q_u = sp.simplify(u_sub * q_x)
                            lines.append(r"")
                            lines.append(r"\text{3. Równanie liniowe dla zmiennej } u:")
                            lines.append(rf"\frac{{u^{{\prime}}}}{{{sp.latex(u_sub)}}} + \left({sp.latex(p_x)}\right) u = {sp.latex(q_x)} \quad / \cdot ({sp.latex(u_sub)})")
                            lines.append(rf"u^{{\prime}} + \left({sp.latex(p_u)}\right) u = {sp.latex(q_u)}")
                            
                            lines.append(r"")
                            lines.append(r"\text{4. Rozwiązanie RLJ dla } u:")
                            lines.append(rf"\frac{{du}}{{u}} = {sp.latex(-p_u)} dx \quad / \int")
                            int_pu = sp.integrate(-p_u, x)
                            int_pu_tex = sp.latex(int_pu).replace('log', 'ln')
                            lines.append(rf"u_0 = C \cdot e^{{{int_pu_tex}}}")
                            
                            lines.append(r"")
                            lines.append(r"\text{5. Metoda uzmienniania stałej dla } u:")
                            lines.append(rf"u^{{\prime}} = C^{{\prime}}(x) e^{{{int_pu_tex}}} + C(x)(\dots)")
                            lines.append(rf"C^{{\prime}}(x) e^{{{int_pu_tex}}} = {sp.latex(q_u)}")
                            cu_prime = sp.simplify(q_u / sp.exp(int_pu))
                            lines.append(rf"C^{{\prime}}(x) = {sp.latex(cu_prime)}")
                            cu_int = sp.integrate(cu_prime, x)
                            cu_int_tex = sp.latex(cu_int).replace('log', 'ln')
                            lines.append(rf"C(x) = {cu_int_tex} + C_1")
                            
                            u_final = sp.simplify((cu_int + C1) * sp.exp(int_pu))
                            lines.append(rf"u = \left({cu_int_tex} + C_1\right) e^{{{int_pu_tex}}}")
                            lines.append(r"")
                            lines.append(r"\text{6. Wracamy do podstawienia (postać uwikłana):}")
                            lines.append(rf"\text{{Odp:}} \quad \underline{{y^{{{sp.latex(u_sub)}}} = \left({cu_int_tex} + C_1\right) e^{{{int_pu_tex}}} \quad \text{{- COR}}}}")
                            
                            if conds:
                                st.markdown("---")
                                zp_lines = []
                                c_data = conds[0]
                                zp_lines.append(rf"\text{{Z.P.}} \quad y({sp.latex(c_data['x_val'])}) = {sp.latex(c_data['y_val'])}")
                                y_pow_val = c_data['y_val']**u_sub
                                val_expr = u_final.subs(x, c_data['x_val'])
                                zp_lines.append(rf"{sp.latex(c_data['y_val'])}^{{{sp.latex(u_sub)}}} = {sp.latex(val_expr).replace('log', 'ln')}")
                                sols = sp.solve(sp.Eq(y_pow_val, val_expr), C1)
                                if sols:
                                    zp_lines.append(rf"C_1 = {sp.latex(sols[0])}")
                                    u_s = u_final.subs(C1, sols[0])
                                    zp_lines.append(rf"\text{{Odp:}} \quad \underline{{ y_s^{{{sp.latex(u_sub)}}} = {sp.latex(u_s).replace('log', 'ln')} \quad \text{{- CSR}} }}")
                                lines.extend(zp_lines)
                            st.latex("\\begin{aligned}\n" + " \\\\\n".join(lines) + "\n\\end{aligned}")
                        else:
                            st.error("Nie udało się rozpoznać struktury Bernoulliego.")
        except Exception as e:
            st.error(f"Błąd analizy równania. Szczegóły: {e}")