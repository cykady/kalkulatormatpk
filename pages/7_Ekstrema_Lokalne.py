import streamlit as st
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

st.set_page_config(page_title="Ekstrema Lokalne", layout="wide")

st.title("🏔️ Zadanie 2: Ekstrema Lokalne")
st.markdown("Kalkulator wyznaczający ekstrema funkcji dwóch zmiennych zgodnie z metodą wyznacznika (macierzy Hessego).")
st.markdown("---")

x, y = sp.symbols('x y', real=True)
transformations = standard_transformations + (implicit_multiplication_application,)

st.subheader("Wprowadź funkcję do zbadania:")
f_str = st.text_input("Wpisz funkcję z(x,y):", "x^3 + 6*x*y - y^2 + 2")
st.caption("💡 Ściąga: ułamek -> a/b | potęga -> ^ lub ** | mnożenie zawsze z gwiazdką (*)")

if st.button("📝 Szukaj ekstremów", type="primary"):
    try:
        f_expr = parse_expr(f_str.replace('^', '**'), local_dict={'x': x, 'y': y}, transformations=transformations)
        
        st.markdown("---")
        st.markdown("### 📝 Protokół Rozwiązania:")
        st.latex(rf"z = f(x,y) = {sp.latex(f_expr)}")
        
        # ==========================================
        # ETAP I: PIERWSZE POCHODNE I UKŁAD
        # ==========================================
        st.markdown("#### I. Pierwsze pochodne i punkty stacjonarne (Warunek Konieczny)")
        
        fx = sp.diff(f_expr, x)
        fy = sp.diff(f_expr, y)
        
        col1, col2 = st.columns(2)
        with col1:
            st.latex(rf"f'_x = \frac{{\partial z}}{{\partial x}} = {sp.latex(fx)}")
        with col2:
            st.latex(rf"f'_y = \frac{{\partial z}}{{\partial y}} = {sp.latex(fy)}")
            
        st.markdown("Przyrównujemy pochodne cząstkowe do zera, tworząc układ równań:")
        st.latex(r"\begin{cases} " + sp.latex(fx) + r" = 0 \\ " + sp.latex(fy) + r" = 0 \end{cases}")
        
        # --- ANALITYCZNE ROZPISANIE ROZWIĄZANIA UKŁADU RÓWNAŃ ---
        st.markdown("##### 🔍 Algorytm wyznaczania punktów stacjonarnych:")
        
        if not fx.has(y) and not fy.has(x):
            st.markdown("Równania są odseparowane (niezależne). Rozwiązujemy każde z nich osobno:")
            sols_x = sp.solve(sp.Eq(fx, 0), x)
            sols_y = sp.solve(sp.Eq(fy, 0), y)
            st.latex(rf"{sp.latex(fx)} = 0 \implies x \in {sp.latex(sols_x)}")
            st.latex(rf"{sp.latex(fy)} = 0 \implies y \in {sp.latex(sols_y)}")
            
        else:
            sols_y_from_fy = sp.solve(sp.Eq(fy, 0), y)
            sols_x_from_fx = sp.solve(sp.Eq(fx, 0), x)
            
            if sols_y_from_fy and not any(sol.has(y) for sol in sols_y_from_fy) and len(sols_y_from_fy) == 1:
                y_iso = sols_y_from_fy[0]
                st.markdown("Z drugiego równania ($f'_y = 0$) wyznaczamy zmienną $y$:")
                st.latex(rf"{sp.latex(fy)} = 0 \implies y = {sp.latex(y_iso)}")
                
                fx_subbed = sp.simplify(fx.subs(y, y_iso))
                st.markdown("Podstawiamy wyznaczone wyrażenie do pierwszego równania ($f'_x = 0$):")
                st.latex(rf"{sp.latex(fx.subs(y, u_sub if 'u_sub' in locals() else y_iso))} = 0 \implies {sp.latex(fx_subbed)} = 0")
                
                sols_x = sp.solve(sp.Eq(fx_subbed, x), x) if fx_subbed.has(x) else sp.solve(sp.Eq(fx_subbed, 0), x)
                st.markdown("Rozwiązujemy powstałe równanie jednej zmiennej dla $x$:")
                st.latex(rf"x \in {sp.latex(sols_x)}")
                
            elif sols_x_from_fx and not any(sol.has(x) for sol in sols_x_from_fx) and len(sols_x_from_fx) == 1:
                x_iso = sols_x_from_fx[0]
                st.markdown("Z pierwszego równania ($f'_x = 0$) wyznaczamy zmienną $x$:")
                st.latex(rf"{sp.latex(fx)} = 0 \implies x = {sp.latex(x_iso)}")
                
                fy_subbed = sp.simplify(fy.subs(x, x_iso))
                st.markdown("Podstawiamy wyrażenie do drugiego równania ($f'_y = 0$):")
                st.latex(rf"{sp.latex(fy.subs(x, x_iso))} = 0 \implies {sp.latex(fy_subbed)} = 0")
                
                sols_y = sp.solve(sp.Eq(fy_subbed, y), y) if fy_subbed.has(y) else sp.solve(sp.Eq(fy_subbed, 0), y)
                st.markdown("Rozwiązujemy powstałe równanie dla zmiennej $y$:")
                st.latex(rf"y \in {sp.latex(sols_y)}")
            else:
                st.markdown("Układ jest silnie sprzężony lub nieliniowy. Silnik algebraiczny wyznacza punkty przecięcia krzywych metodą eliminacji wielomianowej.")

        rozwiazania = sp.solve((sp.Eq(fx, 0), sp.Eq(fy, 0)), (x, y), dict=True)
        punkty_stacjonarne = []
        for sol in rozwiazania:
            if sol[x].is_real and sol[y].is_real:
                punkty_stacjonarne.append((sol[x], sol[y]))
                
        if not punkty_stacjonarne:
            st.warning("Brak rzeczywistych punktów stacjonarnych. Funkcja nie posiada ekstremów lokalnych.")
            st.stop()
            
        st.markdown("**Wyznaczone punkty stacjonarne (współrzędne geometrii ekstremum):**")
        for idx, pt in enumerate(punkty_stacjonarne):
            st.latex(rf"P_{idx+1} = \left( {sp.latex(pt[0])}, \quad {sp.latex(pt[1])} \right)")
            
        st.markdown("---")
        
        # ==========================================
        # ETAP II: DRUGIE POCHODNE I HESJAN
        # ==========================================
        st.markdown("#### II. Drugie pochodne i Wyznacznik (Macierz Hessego)")
        
        fxx = sp.diff(fx, x)
        fyy = sp.diff(fy, y)
        fxy = sp.diff(fx, y)
        
        col3, col4, col5 = st.columns(3)
        with col3:
            st.latex(rf"A(x,y) = f''_{{xx}} = \frac{{\partial^2 z}}{{\partial x^2}} = {sp.latex(fxx)}")
        with col4:
            st.latex(rf"B(x,y) = f''_{{xy}} = \frac{{\partial^2 z}}{{\partial x \partial y}} = {sp.latex(fxy)}")
        with col5:
            st.latex(rf"C(x,y) = f''_{{yy}} = \frac{{\partial^2 z}}{{\partial y^2}} = {sp.latex(fyy)}")
            
        st.markdown("Konstruujemy ogólny wyznacznik macierzy Hessego ($W$):")
        # Poprawiony błąd w składni LaTeX!
        st.latex(rf"W(x,y) = \begin{{vmatrix}} f''_{{xx}} & f''_{{xy}} \\ f''_{{yx}} & f''_{{yy}} \end{{vmatrix}} = \begin{{vmatrix}} {sp.latex(fxx)} & {sp.latex(fxy)} \\ {sp.latex(fxy)} & {sp.latex(fyy)} \end{{vmatrix}}")
        
        W_expr = sp.simplify(fxx * fyy - fxy**2)
        st.latex(rf"W(x,y) = A \cdot C - B^2 = \left({sp.latex(fxx)}\right) \cdot \left({sp.latex(fyy)}\right) - \left({sp.latex(fxy)}\right)^2 = {sp.latex(W_expr)}")
        
        st.markdown("---")
        
        # ==========================================
        # ETAP III: BADANIE PUNKTÓW (WW)
        # ==========================================
        st.markdown("#### III. Badanie punktów i weryfikacja kryterium (Warunek Wystarczający)")
        
        for idx, pt in enumerate(punkty_stacjonarne):
            x_val, y_val = pt[0], pt[1]
            st.markdown(f"📦 **Analiza kryterium dla punktu $P_{idx+1} \\left( {sp.latex(x_val)}, {sp.latex(y_val)} \\right)$:**")
            
            A_val = fxx.subs({x: x_val, y: y_val})
            B_val = fxy.subs({x: x_val, y: y_val})
            C_val = fyy.subs({x: x_val, y: y_val})
            W_val = W_expr.subs({x: x_val, y: y_val})
            
            st.markdown("*Podstawienie współrzędnych do pochodnych drugiego rzędu:*")
            st.latex(rf"A = {sp.latex(A_val)}, \quad B = {sp.latex(B_val)}, \quad C = {sp.latex(C_val)}")
            st.markdown("*Obliczenie wartości Hesjanu:*")
            st.latex(rf"W = A \cdot C - B^2 = ({sp.latex(A_val)}) \cdot ({sp.latex(C_val)}) - ({sp.latex(B_val)})^2 = {sp.latex(W_val)}")
            
            if W_val > 0:
                if A_val > 0:
                    st.success(f"▲ **$W = {sp.latex(W_val)} > 0$ oraz $A = {sp.latex(A_val)} > 0 \implies$ Minimum lokalne**")
                    z_min = f_expr.subs({x: x_val, y: y_val})
                    st.latex(rf"z_{{min}} = f({sp.latex(x_val)}, {sp.latex(y_val)}) = {sp.latex(z_min)}")
                elif A_val < 0:
                    st.success(f"▼ **$W = {sp.latex(W_val)} > 0$ oraz $A = {sp.latex(A_val)} < 0 \implies$ Maksimum lokalne**")
                    z_max = f_expr.subs({x: x_val, y: y_val})
                    st.latex(rf"z_{{max}} = f({sp.latex(x_val)}, {sp.latex(y_val)}) = {sp.latex(z_max)}")
                else:
                    st.warning("Przypadek osobliwy ($W>0$, ale $A=0$).")
            elif W_val < 0:
                st.error(f"❌ **$W = {sp.latex(W_val)} < 0 \implies$ Brak ekstremum** (Punkt siodłowy - powierzchnia nieliniowa)")
            else:
                st.info(f"❓ **$W = 0 \implies$ Przypadek nie rozstrzyga o istnieniu ekstremum**. Należy badać otoczenie punktu wyższymi pochodnymi.")
            
            st.markdown("<br>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Wystąpił błąd obliczeniowy. Sprawdź poprawność zapisu równania. Szczegóły: {e}")