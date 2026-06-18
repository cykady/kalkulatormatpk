import streamlit as st
import sympy as sp
import re
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

st.set_page_config(page_title="Kalkulator RR", layout="centered")

# ==========================================
# KONFIGURACJA SYMBOLI SYM-PY
# ==========================================
x = sp.Symbol('x')
y_sym = sp.Symbol('y')
yp = sp.Symbol('yp')
ypp = sp.Symbol('ypp')
C1, C2, C = sp.symbols('C_1 C_2 C')

transformations = standard_transformations + (implicit_multiplication_application,)

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
                
    # Potężny parser radzący sobie z różniczkami i 'e'
    eq_str = eq_str.replace('^', '**')
    eq_str = eq_str.replace("y''", "ypp").replace("y\"", "ypp").replace("y”", "ypp")
    eq_str = eq_str.replace("dy/dx", "yp")
    eq_str = re.sub(r'\bdy\b', 'yp', eq_str)  # Zastępuje luźne dy na y'
    eq_str = re.sub(r'\bdx\b', '1', eq_str)   # Zastępuje luźne dx na 1 (dzielenie przez dx)
    eq_str = eq_str.replace("y'", "yp").replace("y’", "yp")
    
    return eq_str, conditions

# ==========================================
# SILNIK ZMIENNYCH ROZDZIELONYCH (TYP I)
# ==========================================

def solve_separable(eq, conditions):
    lines = []
    
    # 1. Rozwiązanie równania względem y'
    yp_sols = sp.solve(eq, yp)
    if not yp_sols:
        st.error("Nie udało się wyizolować pochodnej y'. Sprawdź zapis równania.")
        return
        
    # Faktoryzacja: np. x + 2xy -> x(1+2y)
    F = sp.factor(yp_sols[0])
    lines.append(rf"y^{{\prime}} &= {sp.latex(F)} \quad \text{{(izolujemy }} y' \text{{ i grupujemy zmienne)}}")
    
    # 2. Rozdzielenie na funkcję od X i funkcję od Y
    F_x, F_y = F.as_independent(y_sym, as_Add=False)
    
    # 3. Zapis różniczkowy i przenoszenie
    lines.append(rf"\frac{{dy}}{{dx}} &= {sp.latex(F_x)} \cdot \left({sp.latex(F_y)}\right) \quad / \cdot dx \quad / : \left({sp.latex(F_y)}\right)")
    
    left_side = sp.simplify(1/F_y)
    right_side = F_x
    
    lines.append(rf"{sp.latex(left_side)} \, dy &= {sp.latex(right_side)} \, dx \quad / \int")
    
    # 4. Całkowanie
    lines.append(rf"\int \left({sp.latex(left_side)}\right) dy &= \int \left({sp.latex(right_side)}\right) dx")
    
    int_l = sp.integrate(left_side, y_sym)
    int_r = sp.integrate(right_side, x)
    
    int_l_tex = sp.latex(int_l).replace('log', 'ln')
    int_r_tex = sp.latex(int_r).replace('log', 'ln')
    
    lines.append(rf"{int_l_tex} &= {int_r_tex} + C \quad \text{{- COR (postać uwikłana)}}")
    
    # 5. Próba wyznaczenia jawnego y(x)
    y_gen = None
    try:
        sols = sp.solve(sp.Eq(int_l, int_r + C1), y_sym)
        if sols:
            y_gen = sols[-1] # Bierzemy najbardziej rozwinięty wynik
            lines.append(rf"y(x) &= {sp.latex(y_gen).replace('C_1', 'C')} \quad \text{{- COR (postać jawna)}}")
    except:
        pass # Zostajemy przy postaci uwikłanej

    st.latex("\\begin{aligned}\n" + " \\\\\n".join(lines) + "\n\\end{aligned}")
    
    # ==========================
    # 6. WARUNKI BRZEGOWE (CSR)
    # ==========================
    if conditions:
        st.markdown("---")
        cond = conditions[0]
        cond_lines = []
        cond_lines.append(rf"\text{{Podstawiamy warunek początkowy: }} {sp.latex(cond['raw'])}")
        
        # Jeśli mamy jawną postać y(x)
        if y_gen:
            val = sp.simplify(y_gen.subs(x, cond['x']))
            cond_lines.append(rf"{sp.latex(cond['v'])} &= {sp.latex(val)}")
            c_sols = sp.solve(sp.Eq(val, cond['v']), C1)
            if c_sols:
                c_val = sp.simplify(c_sols[0])
                cond_lines.append(rf"C &= {sp.latex(c_val)}")
                y_final = sp.simplify(y_gen.subs(C1, c_val))
                cond_lines.append(rf"\underline{{y(x) = {sp.latex(y_final).replace('log', 'ln')} \quad \text{{- CSR}}}}")
        
        # Jeśli mamy tylko postać uwikłaną (częste przy logarytmach i pierwiastkach)
        else:
            eq_c = sp.Eq(int_l.subs(y_sym, cond['v']), int_r.subs(x, cond['x']) + C)
            cond_lines.append(rf"{sp.latex(int_l.subs(y_sym, cond['v']))} &= {sp.latex(int_r.subs(x, cond['x']))} + C")
            c_sols = sp.solve(eq_c, C)
            if c_sols:
                c_val = sp.simplify(c_sols[0])
                cond_lines.append(rf"C &= {sp.latex(c_val)}")
                cond_lines.append(rf"\underline{{{int_l_tex} = {int_r_tex} + \left({sp.latex(c_val)}\right) \quad \text{{- CSR (uwikłana)}}}}")
                
        if len(cond_lines) > 1:
            st.latex("\\begin{aligned}\n" + " \\\\\n".join(cond_lines) + "\n\\end{aligned}")


# ==========================================
# GŁÓWNY INTERFEJS
# ==========================================

st.title("Rozwiązywanie Równań Różniczkowych")
st.markdown("Wpisz równanie. Kalkulator automatycznie przetworzy pochodne $y'$, $dy/dx$ a nawet luźne różniczki $dx$ i $dy$.")

user_input = st.text_input(
    "Równanie (np. y' - x = 2xy ; y(0)=1):", 
    "y' - x = 2xy ; y(0)=1"
)

if user_input:
    try:
        eq_str, conditions = preprocess_input(user_input)
        
        if '=' not in eq_str:
            st.error("Równanie musi zawierać znak '='.")
            st.stop()
            
        lhs_str, rhs_str = eq_str.split('=', 1)
        # Parse wstrzykuje 'e' jako sp.E, aby rozumieć e^y
        lhs = parse_expr(lhs_str, local_dict={'y': y_sym, 'yp': yp, 'ypp': ypp, 'x': x, 'e': sp.E}, transformations=transformations)
        rhs = parse_expr(rhs_str, local_dict={'y': y_sym, 'yp': yp, 'ypp': ypp, 'x': x, 'e': sp.E}, transformations=transformations)
        
        eq = sp.simplify(lhs - rhs)
        
        st.markdown("---")
        
        if eq.has(yp):
            solve_separable(eq, conditions)
        else:
            st.warning("Nie wykryto pochodnej. Wprowadź równanie zawierające y' lub dy/dx.")

    except Exception as e:
        st.error(f"Błąd analizy. Upewnij się co do zapisu matematycznego. Szczegóły: {e}")