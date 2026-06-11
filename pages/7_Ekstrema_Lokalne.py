import streamlit as st
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

st.set_page_config(page_title="Ekstrema Lokalne", layout="wide")

st.title("🏔️ Zadanie 2: Ekstrema Lokalne")
st.markdown("Kalkulator wyznaczający ekstrema funkcji dwóch zmiennych zgodnie z metodą wyznacznika (macierzy Hessego).")
st.markdown("---")

x, y = sp.symbols('x y', real=True)
transformations = standard_transformations + (implicit_multiplication_application,)
st.caption("💡 Ściąga: ułamek -> (a)/(b) | pierwiastek -> sqrt(x) | pierwiastek 3-go stopnia -> x^(1/3) | e^x -> exp(x) | mnożenie zawsze z gwiazdką (*)")
st.subheader("Wybierz zadanie z listy lub wprowadź własne:")

zadania = {
    "Zadanie 2a (Zestaw 1): z = 8y - 2x^2*y": "8*y - 2*x**2*y",
    "Zadanie 2b (Zestaw 1): z = x^3 - 3x + y^2 - 4y + 4": "x**3 - 3*x + y**2 - 4*y + 4",
    "Zadanie 2a (Zestaw 2): z = x^2 - 2xy + y^2 + 20": "x**2 - 2*x*y + y**2 + 20",
    "Zadanie 2b (Zestaw 2): z = y^3 - x^2 - 6y": "y**3 - x**2 - 6*y",
    "Zadanie 2a (Zestaw 3): z = x^2*y - 4xy + 5": "x**2*y - 4*x*y + 5",
    "Zadanie 2b (Zestaw 3): z = 2x^3 + y^2 - 12x + 2y": "2*x**3 + y**2 - 12*x + 2*y",
    "Zadanie 2a (Zestaw 4): z = x^2 - xy + y^2 + 9x - 6y + 20": "x**2 - x*y + y**2 + 9*x - 6*y + 20",
    "Zadanie 2b (Zestaw 4): z = 1/3*x^3 + 1/2*y^2 - 2xy + 3": "1/3*x**3 + 1/2*y**2 - 2*x*y + 3",
    "✨ Własny przykład...": "WLASNY"
}

wybor = st.selectbox("Wybierz funkcję:", list(zadania.keys()))

if zadania[wybor] == "WLASNY":
    f_str = st.text_input("Wpisz funkcję z(x,y) (np. x^2 + y^2): ", "x**2 + y**2")
    st.caption("💡 Ściąga: ułamek -> (a)/(b) | potęga -> ^ lub ** | mnożenie zawsze z gwiazdką (*)")
else:
    f_str = zadania[wybor]
    st.code(f"Wybrana funkcja: z = {f_str.replace('**', '^')}")

if st.button("📝 Szukaj ekstremów", type="primary"):
    try:
        f_expr = parse_expr(f_str.replace('^', '**'), local_dict={'x': x, 'y': y}, transformations=transformations)
        
        st.markdown("---")
        st.markdown("### 📝 Protokół Rozwiązania:")
        st.latex(rf"z = f(x,y) = {sp.latex(f_expr)}")
        
        # ETAP I: Pierwsze pochodne i punkty stacjonarne
        st.markdown("#### I. Pierwsze pochodne i punkty stacjonarne (WK)")
        
        fx = sp.diff(f_expr, x)
        fy = sp.diff(f_expr, y)
        
        col1, col2 = st.columns(2)
        with col1:
            st.latex(rf"f'_x = {sp.latex(fx)}")
        with col2:
            st.latex(rf"f'_y = {sp.latex(fy)}")
            
        st.markdown("Przyrównujemy pochodne do zera, tworząc układ równań:")
        st.latex(r"\begin{cases} " + sp.latex(fx) + r" = 0 \\ " + sp.latex(fy) + r" = 0 \end{cases}")
        
        # Rozwiązywanie układu równań
        rozwiazania = sp.solve((sp.Eq(fx, 0), sp.Eq(fy, 0)), (x, y), dict=True)
        
        # Filtrujemy tylko rzeczywiste rozwiązania (odrzucamy urojone, które czasem wypluwa solver)
        punkty_stacjonarne = []
        for sol in rozwiazania:
            if sol[x].is_real and sol[y].is_real:
                punkty_stacjonarne.append((sol[x], sol[y]))
                
        if not punkty_stacjonarne:
            st.warning("Brak rzeczywistych punktów stacjonarnych. Funkcja nie posiada ekstremów.")
            st.stop()
            
        st.markdown("Punkty stacjonarne (podejrzane o ekstremum):")
        for idx, pt in enumerate(punkty_stacjonarne):
            st.latex(rf"P_{idx+1} \left( {sp.latex(pt[0])}, \quad {sp.latex(pt[1])} \right)")
            
        st.markdown("---")
        
        # ETAP II: Drugie pochodne i wyznacznik
        st.markdown("#### II. Drugie pochodne i Wyznacznik (Macierz Hessego)")
        
        fxx = sp.diff(fx, x)
        fyy = sp.diff(fy, y)
        fxy = sp.diff(fx, y) # to samo co fyx
        
        col3, col4, col5 = st.columns(3)
        with col3:
            st.latex(rf"A = f''_{{xx}} = {sp.latex(fxx)}")
        with col4:
            st.latex(rf"B = f''_{{xy}} = {sp.latex(fxy)}")
        with col5:
            st.latex(rf"C = f''_{{yy}} = {sp.latex(fyy)}")
            
        st.markdown("Konstruujemy wyznacznik $W$:")
        st.latex(rf"W(x,y) = \begin{{vmatrix}} f''_{{xx}} & f''_{{xy}} \\ f''_{{yx}} & f''_{{yy}} \end{{vmatrix}} = \begin{{vmatrix}} {sp.latex(fxx)} & {sp.latex(fxy)} \\ {sp.latex(fxy)} & {sp.latex(fyy)} \end{{vmatrix}}")
        
        # Ogólny wzór wyznacznika
        W_expr = sp.simplify(fxx * fyy - fxy**2)
        st.latex(rf"W(x,y) = A \cdot C - B^2 = ({sp.latex(fxx)}) \cdot ({sp.latex(fyy)}) - ({sp.latex(fxy)})^2 = {sp.latex(W_expr)}")
        
        st.markdown("---")
        
        # ETAP III: Badanie punktów stacjonarnych
        st.markdown("#### III. Badanie punktów (WW)")
        
        for idx, pt in enumerate(punkty_stacjonarne):
            x_val, y_val = pt[0], pt[1]
            st.markdown(f"**Dla punktu $P_{idx+1} \\left( {sp.latex(x_val)}, {sp.latex(y_val)} \\right)$:**")
            
            # Podstawianie do A, B, C
            A_val = fxx.subs({x: x_val, y: y_val})
            W_val = W_expr.subs({x: x_val, y: y_val})
            
            st.latex(rf"W = {sp.latex(W_val)}, \quad A = {sp.latex(A_val)}")
            
            # Logika decyzyjna wg notatek
            if W_val > 0:
                if A_val > 0:
                    st.success(f"✔ **$W > 0$ i $A > 0 \implies$ Minimum lokalne** w punkcie $P_{idx+1}$")
                    z_min = f_expr.subs({x: x_val, y: y_val})
                    st.latex(rf"z_{{min}} = {sp.latex(z_min)}")
                elif A_val < 0:
                    st.success(f"✔ **$W > 0$ i $A < 0 \implies$ Maksimum lokalne** w punkcie $P_{idx+1}$")
                    z_max = f_expr.subs({x: x_val, y: y_val})
                    st.latex(rf"z_{{max}} = {sp.latex(z_max)}")
                else:
                    st.warning("Przypadek patologiczny ($W>0$, ale $A=0$ - niemożliwe dla funkcji gładkich).")
            elif W_val < 0:
                st.error(f"❌ **$W < 0 \implies$ Brak ekstremum** (punkt siodłowy) w punkcie $P_{idx+1}$")
            else:
                st.info(f"❓ **$W = 0 \implies$ Przypadek wątpliwy** (może być). Metoda nie rozstrzyga o istnieniu ekstremum w punkcie $P_{idx+1}$.")
            
            st.markdown("<br>", unsafe_allow_html=True) # odstęp

    except Exception as e:
        st.error(f"Wystąpił błąd obliczeniowy. Sprawdź zapis funkcji. Szczegóły: {e}")