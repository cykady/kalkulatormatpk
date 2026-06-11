import streamlit as st
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

st.set_page_config(page_title="Całki Nieoznaczone", layout="wide")

st.title("🧮 Zadanie 3: Całki Nieoznaczone")
st.markdown("Automatyczny kalkulator całek nieoznaczonych krok po kroku. Wykorzystuje **twierdzenie 1** (całka sumy) i **twierdzenie 2** (wyłączanie stałej).")
st.markdown("---")
st.caption("💡 Ściąga: ułamek -> (a)/(b) | pierwiastek -> sqrt(x) | pierwiastek 3-go stopnia -> x^(1/3) | e^x -> exp(x) | mnożenie zawsze z gwiazdką (*)")

x = sp.Symbol('x')
transformations = standard_transformations + (implicit_multiplication_application,)

# Słownik z gotowymi zadaniami ze zdjęć
baza_zadan = {
    "Zestaw 1 (Lewa kolumna)": {
        "a) ∫(4x + 2) dx": 4*x + 2,
        "b) ∫(3x^{-4} + x^{1/2}) dx": 3*x**-4 + x**sp.Rational(1, 2),
        "c) ∫(6x - x^4)/x^3 dx": (6*x - x**4)/x**3,
        "d) ∫ x^{7/5} dx": x**sp.Rational(7, 5),
        "e) ∫(2sin(x) + 3e^x + 6) dx": 2*sp.sin(x) + 3*sp.exp(x) + 6,
        "f) ∫(3x^2 + 1)^2 dx": (3*x**2 + 1)**2
    },
    "Zestaw 2 (Środkowa kolumna)": {
        "a) ∫(6x^2 + 4) dx": 6*x**2 + 4,
        "b) ∫(3x^{-7} + x^{2/3}) dx": 3*x**-7 + x**sp.Rational(2, 3),
        "c) ∫(2x^5 - 4x)/x^3 dx": (2*x**5 - 4*x)/x**3,
        "d) ∫ x^{3/4} dx": x**sp.Rational(3, 4),
        "e) ∫(5e^x - 2cos(x) + 1/x) dx": 5*sp.exp(x) - 2*sp.cos(x) + 1/x,
        "f) ∫(2 + x^3)^2 dx": (2 + x**3)**2
    },
    "Zestaw 3 (Prawa kolumna)": {
        "a) ∫(12x^3 + 5) dx": 12*x**3 + 5,
        "b) ∫(12x^{-3} + x^{1/3}) dx": 12*x**-3 + x**sp.Rational(1, 3),
        "c) ∫(7x^8 + 2x)/x^2 dx": (7*x**8 + 2*x)/x**2,
        "d) ∫ x^{5/7} dx": x**sp.Rational(5, 7),
        "e) ∫(9/x + 5cos(x) - 11e^x + 2) dx": 9/x + 5*sp.cos(x) - 11*sp.exp(x) + 2,
        "f) ∫(2√x + 1)^2 dx": (2*sp.sqrt(x) + 1)**2
    }
}

col1, col2 = st.columns(2)
with col1:
    wybrany_zestaw = st.selectbox("Wybierz zestaw (kolumnę ze zdjęcia):", list(baza_zadan.keys()) + ["✨ Własny przykład..."])

if wybrany_zestaw == "✨ Własny przykład...":
    f_str = st.text_input("Wpisz funkcję podcałkową f(x) (np. 4*x^2 + sin(x)): ", "4*x**2 + 3")
    f_expr = None
else:
    with col2:
        wybrane_zadanie = st.selectbox("Wybierz podpunkt:", list(baza_zadan[wybrany_zestaw].keys()))
    f_expr = baza_zadan[wybrany_zestaw][wybrane_zadanie]

if st.button("📝 Generuj rozwiązanie krok po kroku", type="primary"):
    try:
        if wybrany_zestaw == "✨ Własny przykład...":
            f_expr = parse_expr(f_str.replace('^', '**'), transformations=transformations)
            
        st.markdown("---")
        st.markdown("### 📝 Protokół Rozwiązania:")
        
        # 1. Zapis wyjściowy
        st.markdown("**Krok 1: Zapisujemy całkę wyjściową**")
        st.latex(rf"\int \left( {sp.latex(f_expr)} \right) dx")
        
        # 2. Uproszczenie (rozwinięcie wzorów skróconego mnożenia, podział ułamków)
        f_exp = sp.expand(f_expr)
        if f_exp != f_expr:
            st.markdown("**Krok 2: Przekształcamy wyrażenie (wymnażamy nawiasy lub rozbijamy ułamki)**")
            st.latex(rf"= \int \left( {sp.latex(f_exp)} \right) dx")
        else:
            st.markdown("**Krok 2: Funkcja jest w najprostszej postaci (brak nawiasów do wymnożenia)**")
            
        # 3. Zastosowanie tw. 1 i tw. 2 (Rozbicie na sumę całek)
        st.markdown("**Krok 3: Zastosowanie tw. 1 i tw. 2 (Rozbijamy na sumę całek i wyłączamy stałe przed znak)**")
        
        terms = f_exp.args if isinstance(f_exp, sp.Add) else [f_exp]
        parts_latex = []
        
        for term in terms:
            coeff, rest = term.as_coeff_Mul()
            if rest == 1:
                parts_latex.append(rf"{sp.latex(coeff)} \int 1 \, dx")
            else:
                if coeff == 1:
                    parts_latex.append(rf"\int {sp.latex(rest)} \, dx")
                elif coeff == -1:
                    parts_latex.append(rf"- \int {sp.latex(rest)} \, dx")
                else:
                    parts_latex.append(rf"{sp.latex(coeff)} \int {sp.latex(rest)} \, dx")
                    
        # Łączenie w jeden string i poprawa wyświetlania minusów
        sum_latex = " + ".join(parts_latex).replace("+ -", "- ")
        st.latex(rf"= {sum_latex}")
        
        # 4. Obliczenie całki
        st.markdown("**Krok 4: Czyste całkowanie i dodanie stałej C**")
        result = sp.integrate(f_exp, x)
        
        # Poprawa logarytmów do standardowego formatu z ln|x|
        result_latex = sp.latex(result)
        if "log" in str(result):
            result_latex = result_latex.replace(r"\log{\left(x \right)}", r"\ln|x|").replace(r"\log", r"\ln")
            
        st.latex(rf"= {result_latex} + C")
        
        st.success("✔ Całka obliczona poprawnie!")
        
    except Exception as e:
        st.error(f"Sprawdź zapis matematyczny własnej całki. Błąd: {e}")