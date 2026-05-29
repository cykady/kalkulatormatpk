import streamlit as st
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

st.set_page_config(page_title="CSR - Zagadnienie Cauchyego", layout="wide", initial_sidebar_state="expanded")
st.sidebar.title("🧭 Nawigacja")
st.sidebar.markdown("---")

st.title("🎓 Wyznaczanie Całki Szczególnej (CSR) - Arkusz PD-7")
st.write("Wybierz zadanie z warunkiem początkowym, aby wyznaczyć stałą C.")

# SŁOWNIK ZADAŃ (Typ 2 i 4 z każdego zestawu)
zadania_csr = {
    "Zad 1.2: y' = 2xy^2, y(0)=2": {"eq": "2*x*y**2", "x0": "0", "y0": "2"},
    "Zad 1.4: y' + 2y = 6x + 2, y(0)=-4": {"eq": "-2*y + 6*x + 2", "x0": "0", "y0": "-4"},
    "Zad 2.2: y' = y^2 / (2*sqrt(x)), y(1)=3": {"eq": "y**2 / (2*sqrt(x))", "x0": "1", "y0": "3"},
    "Zad 2.4: x*y' - 2y = 2x, y(1)=2": {"eq": "(2*y + 2*x)/x", "x0": "1", "y0": "2"},
    "Zad 3.2: y' = y / (x*ln(x)), y(e)=2": {"eq": "y / (x*ln(x))", "x0": "exp(1)", "y0": "2"},
    "Zad 3.4: y' + 2y/x = 6x + 12, y(1)=-6": {"eq": "-2*y/x + 6*x + 12", "x0": "1", "y0": "-6"},
    "Zad 4.2: y' = 2x(y-1), y(0)=4": {"eq": "2*x*(y-1)", "x0": "0", "y0": "4"},
    "Zad 4.4: y' + 8y = 16x - 16, y(0)=-2": {"eq": "-8*y + 16*x - 16", "x0": "0", "y0": "-2"},
    "Zad 5.2: y' = (2x^2 + 1)sqrt(y), y(0)=4": {"eq": "(2*x**2 + 1)*sqrt(y)", "x0": "0", "y0": "4"},
    "Zad 5.4: y' + 2y = exp(-x), y(0)=2": {"eq": "-2*y + exp(-x)", "x0": "0", "y0": "2"},
    "Zad 6.2: y' = y / cos^2(x), y(0)=2": {"eq": "y / cos(x)**2", "x0": "0", "y0": "2"},
    "Zad 6.4: y' + 3y = 27x - 9, y(0)=-8": {"eq": "-3*y + 27*x - 9", "x0": "0", "y0": "-8"},
    "Zad 7.2: y' = y * ln(x), y(1)=exp(1)": {"eq": "y * ln(x)", "x0": "1", "y0": "exp(1)"},
    "Zad 7.4: y' + y*tg(x) = cos(x), y(0)=9": {"eq": "-y*tan(x) + cos(x)", "x0": "0", "y0": "9"},
    "Zad 8.2: y' = 2x + 1, y(1)=4": {"eq": "2*x + 1", "x0": "1", "y0": "4"},
    "Zad 8.4: y' - 4y = 8x + 16, y(0)=2": {"eq": "4*y + 8*x + 16", "x0": "0", "y0": "2"},
    "Własny przykład": {"eq": "", "x0": "0", "y0": "0"}
}

col_input, col_output = st.columns([1, 2], gap="large")

with col_input:
    st.subheader("Wybór zadania Cauchy'ego")
    wybor = st.selectbox("Wybierz przykład:", list(zadania_csr.keys()))
    
    data = zadania_csr[wybor]
    eq_in = st.text_input("y' =", data["eq"])
    x0_in = st.text_input("x0 =", data["x0"])
    y0_in = st.text_input("y0 =", data["y0"])

    generuj = st.button("📝 Rozpisz na piechotę", type="primary", use_container_width=True)

with col_output:
    if generuj:
        try:
            transformations = standard_transformations + (implicit_multiplication_application,)
            x = sp.Symbol('x')
            y_sym = sp.Symbol('y')
            y_fun = sp.Function('y')(x)
            
            f_x_y = parse_expr(eq_in.replace('^', '**'), local_dict={'y': y_sym}, transformations=transformations)
            x0 = parse_expr(x0_in.replace('^', '**'), transformations=transformations)
            y0 = parse_expr(y0_in.replace('^', '**'), transformations=transformations)
            
            eq_diff = sp.Eq(y_fun.diff(x), f_x_y.subs(y_sym, y_fun))
            
            st.subheader("📝 Karta Rozwiązania (CSR)")
            st.latex(rf"y^{{\prime}} = {sp.latex(f_x_y)} \quad ; \quad y({sp.latex(x0)}) = {sp.latex(y0)}")
            
            # KROK 1: COR
            cor = sp.dsolve(eq_diff, y_fun)
            st.markdown("**Krok 1: Wyznaczenie Całki Ogólnej (COR)**")
            st.latex(rf"COR: \ {sp.latex(cor)}")
            
            # KROK 2: Stała C
            st.markdown("**Krok 2: Wyznaczenie stałej C**")
            constants = [s for s in cor.free_symbols if str(s).startswith('C')]
            if constants:
                C_sym = constants[0]
                rhs_subs = cor.rhs.subs(x, x0)
                st.latex(rf"{sp.latex(y0)} = {sp.latex(rhs_subs)}")
                C_val = sp.solve(sp.Eq(y0, rhs_subs), C_sym)[0]
                st.latex(rf"{sp.latex(C_sym)} = {sp.latex(C_val)}")
                
                # KROK 3: CSR
                st.markdown("**Krok 3: Całka Szczególna (CSR)**")
                csr = cor.rhs.subs(C_sym, C_val)
                st.latex(rf"y(x) = {sp.latex(csr)}")
            
        except Exception as e:
            st.error(f"Błąd: {e}")