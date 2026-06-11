import streamlit as st
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

st.set_page_config(page_title="Pochodne Cząstkowe", layout="wide")

st.title("📐 Zadanie 1: Pochodne Cząstkowe")
st.markdown("Kalkulator pochodnych dostrojony do wymogów wykładowcy: wyciąganie stałych przed znak pochodnej, zapis $()'$ oraz jawne dodawanie zer.")
st.markdown("---")

x, y = sp.symbols('x y')
transformations = standard_transformations + (implicit_multiplication_application,)

# Nowa funkcja generująca kroki DOKŁADNIE jak na zdjęciu
def pokaz_kroki_wykladowca(expr_input, var, var_name, stala_name, pochodna_symbol):
    # Wymuszamy rozwinięcie funkcji (żeby rozbić nawiasy na proste składniki dodawania)
    expr = sp.expand(expr_input)
    terms = sp.Add.make_args(expr)
    
    parts_step1 = [] # Część ze stałymi na zewnątrz i primami np. 4y(x^3)' + 0
    parts_step2 = [] # Część z wyliczonymi pochodnymi np. 4y * 3x^2 + 0
    
    for t in terms:
        t_var = 1
        t_const = 1
        # Rozdzielamy każdy składnik na część zmienną i stałą
        for factor in sp.Mul.make_args(t):
            if factor.has(var):
                t_var *= factor
            else:
                t_const *= factor
                
        if t_var == 1:
            # Brak zmiennej - to czysta stała, więc pochodna to 0
            parts_step1.append("0")
            parts_step2.append("0")
        else:
            latex_var = sp.latex(t_var)
            latex_const = sp.latex(t_const)
            diff_var = sp.latex(sp.diff(t_var, var))
            
            if t_const == 1:
                parts_step1.append(rf"\left({latex_var}\right)'")
                parts_step2.append(rf"{diff_var}")
            elif t_const == -1:
                parts_step1.append(rf"- \left({latex_var}\right)'")
                parts_step2.append(rf"- \left({diff_var}\right)")
            else:
                parts_step1.append(rf"{latex_const} \left({latex_var}\right)'")
                # Jeśli wyliczona pochodna to np. 3x^2, dodajemy kropkę mnożenia dla czytelności
                parts_step2.append(rf"{latex_const} \cdot \left({diff_var}\right)")

    # Łączymy elementy w ładny string matematyczny
    step1_str = " + ".join(parts_step1).replace("+ -", "- ").replace("+ 0", "+ 0")
    step2_str = " + ".join(parts_step2).replace("+ -", "- ")
    
    wynik_koncowy = sp.simplify(sp.diff(expr_input, var))
    
    # Wyświetlanie w stylu wykładowcy
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown(f"<div style='text-align: right; font-weight: bold; font-size: 1.2em; color: gray;'>{stala_name} = stała</div>", unsafe_allow_html=True)
    with col2:
        st.latex(rf"{pochodna_symbol} = {step1_str}")
        # Pokazujemy krok z mnożeniem tylko jeśli coś realnie się zmieniło względem primów
        if step1_str != step2_str:
            st.latex(rf"= {step2_str}")
        st.latex(rf"= {sp.latex(wynik_koncowy)}")
        
    return wynik_koncowy

# --- Koniec funkcji pomocniczej ---
st.caption("💡 Ściąga: ułamek -> (a)/(b) | pierwiastek -> sqrt(x) | pierwiastek 3-go stopnia -> x^(1/3) | e^x -> exp(x) | mnożenie zawsze z gwiazdką (*)")
st.subheader("Wybierz zadanie z listy lub wprowadź własne:")

zadania = {
    "Zadanie 1a: z = 4x^3*y + y^7": "4*x**3*y + y**7",
    "Zadanie 1b: z = 4x^3*y^7": "4*x**3*y**7",
    "Zadanie 1c: z = (3x^2*y + 2y)*sin(x)": "(3*x**2*y + 2*y)*sin(x)",
    "Zadanie 1d: z = (2*sqrt(x) + 7y)*ln(y)": "(2*sp.sqrt(x) + 7*y)*sp.log(y)",
    "✨ Własny przykład...": "WLASNY"
}

wybor = st.selectbox("Wybierz funkcję:", list(zadania.keys()))

if zadania[wybor] == "WLASNY":
    f_str = st.text_input("Wpisz funkcję z(x,y) (np. x^2*y + y^3): ", "x**2 * y + y**3")
    st.caption("💡 Ściąga: logarytm naturalny to -> sp.log(y) | pierwiastek -> sp.sqrt(x) | mnożenie z (*)")
else:
    f_str = zadania[wybor]
    st.code(f"Wybrana funkcja: z = {f_str.replace('**', '^').replace('sp.', '')}")

if st.button("📝 Generuj procedurę dla wykładowcy", type="primary"):
    try:
        f_expr = parse_expr(f_str.replace('^', '**'), local_dict={'x': x, 'y': y, 'sp': sp}, transformations=transformations)
        
        st.markdown("---")
        st.markdown("### 📝 Protokół z zachowaniem notacji:")
        st.latex(rf"z = {sp.latex(f_expr)}")
        st.markdown("---")
        
        # 1. POCHODNE PIERWSZEGO RZĘDU
        st.markdown("#### 1. Pochodne cząstkowe pierwszego rzędu")
        dz_dx = pokaz_kroki_wykladowca(f_expr, x, "x", "y", r"\frac{\partial z}{\partial x}")
        st.markdown("---")
        dz_dy = pokaz_kroki_wykladowca(f_expr, y, "y", "x", r"\frac{\partial z}{\partial y}")
        st.markdown("---")
        
        # 2. POCHODNE DRUGIEGO RZĘDU (Czyste)
        st.markdown("#### 2. Pochodne cząstkowe drugiego rzędu (czyste)")
        d2z_dx2 = pokaz_kroki_wykladowca(dz_dx, x, "x", "y", r"\frac{\partial^2 z}{\partial x^2}")
        st.markdown("---")
        d2z_dy2 = pokaz_kroki_wykladowca(dz_dy, y, "y", "x", r"\frac{\partial^2 z}{\partial y^2}")
        st.markdown("---")
        
        # 3. POCHODNE MIESZANE
        st.markdown("#### 3. Pochodne cząstkowe mieszane")
        d2z_dxdy = pokaz_kroki_wykladowca(dz_dx, y, "y", "x", r"\frac{\partial^2 z}{\partial x \partial y}")
        st.markdown("---")
        d2z_dydx = pokaz_kroki_wykladowca(dz_dy, x, "x", "y", r"\frac{\partial^2 z}{\partial y \partial x}")
        
        # Weryfikacja Schwarza
        st.markdown("---")
        st.markdown("**Sprawdzenie warunku Schwarza:**")
        if sp.simplify(d2z_dxdy - d2z_dydx) == 0:
            st.success("✔ Twierdzenie Schwarza zachowane (pochodne mieszane są równe).")
        else:
            st.warning("Pochodne mieszane się różnią!")

    except Exception as e:
        st.error(f"Wystąpił błąd podczas analizy funkcji: {e}")