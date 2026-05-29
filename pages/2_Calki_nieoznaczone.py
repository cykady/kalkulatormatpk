import streamlit as st
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

st.set_page_config(page_title="Całki nieoznaczone", layout="wide")
st.title("🧮 Całkowanie (Podstawienie i Częściowanie)")
st.markdown("---")

transformations = standard_transformations + (implicit_multiplication_application,)
x = sp.Symbol('x')

col1, col2 = st.columns(2)
with col1:
    str_func = st.text_input("Wpisz funkcję podcałkową:", "x * exp(x^2)")
    licz_calke = st.button("Oblicz całkę", type="primary")
    
with col2:
    if licz_calke:
        try:
            func = parse_expr(str_func.replace('^', '**'), transformations=transformations)
            st.markdown("**Całka:**")
            st.latex(rf"\int \left( {sp.latex(func)} \right) dx")
            
            wynik = sp.integrate(func, x)
            st.markdown("**Wynik:**")
            st.latex(rf"= {sp.latex(wynik)} + C")
        except:
            st.error("Błąd parsowania funkcji.")