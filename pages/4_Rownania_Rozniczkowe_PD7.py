import streamlit as st
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

st.set_page_config(page_title="Zadanie 4 - Równania Różniczkowe", layout="wide")

st.title("🧮 Zadanie 4: Równania Różniczkowe (Arkusz PD-7)")
st.markdown("Automatyczny gotowiec podzielony na podpunkty (1, 2, 3, 4) dla wszystkich zestawów od 1 do 8.")
st.markdown("---")

# Definicje symboli globalnych
x = sp.Symbol('x')
y_sym = sp.Symbol('y')
y_fun = sp.Function('y')(x)
transformations = standard_transformations + (implicit_multiplication_application,)

# Tworzenie systemu 4 podrozdziałów (tabs)
tab1, tab2, tab3, tab4 = st.tabs([
    "📌 Podrozdziały nr 1 (COR)", 
    "📌 Podrozdziały nr 2 (CSR)", 
    "📌 Podrozdziały nr 3 (COR)", 
    "📌 Podrozdziały nr 4 (CSR)"
])

# ==========================================
# TAB 1: PODPUNKTY NUMER 1 (Wyznaczanie COR na piechotę + Własny przykład)
# ==========================================
with tab1:
    st.subheader("Automatyczne rozdzielanie zmiennych krok po kroku (Podpunkty nr 1):")
    
    # Rozszerzona lista zadań o opcję niestandardową
    lista_1 = {
        "Zestaw 1.1: y' = 4x^3y": "4 * x^3 * y",
        "Zestaw 2.1: y' = y * sin(x)": "y * sin(x)",
        "Zestaw 3.1: y' = y * cos(x)": "y * cos(x)",
        "Zestaw 4.1: y' = y^2 * cos(x)": "y**2 * cos(x)",
        "Zestaw 5.1: y' = y^2 * e^x": "y**2 * exp(x)",
        "Zestaw 6.1: y' = 3y^2 / x^3": "(3 * y**2) / x**3",
        "Zestaw 7.1: y' = 4y^2 / x^5": "(4 * y**2) / x**5",
        "Zestaw 8.1: (x^2 - 4)y' = 2xy^2": "(2 * x * y**2) / (x**2 - 4)",
        "✨ Własny przykład... (wpisz poniżej)": "WLASNY"
    }
    
    wybor_1 = st.selectbox("Wybierz zadanie z listy lub opcję własną:", list(lista_1.keys()), key="sel_tab1")
    
    # Jeśli użytkownik wybierze własny przykład, aktywujemy pole tekstowe
    if lista_1[wybor_1] == "WLASNY":
        wzor_1 = st.text_input("Wpisz prawą stronę równania y' = (np. 5*x^2*y):", "5 * x^2 * y", key="custom_in_tab1")
    else:
        wzor_1 = lista_1[wybor_1]
        st.code(f"Wybrany wzór: y' = {wzor_1}")
    
    if st.button("📝 Generuj pełny protokół kolokwialny (Tab 1)", type="primary", key="btn_tab1"):
        try:
            expr_clean = wzor_1.replace('^', '**')
            f_x_y = parse_expr(expr_clean, local_dict={'y': y_sym}, transformations=transformations)
            
            st.markdown("---")
            st.markdown("### 📝 Rozwiązanie zadania do przepisania:")
            st.markdown("**Równanie wyjściowe:**")
            st.latex(rf"y^{{\prime}} = {sp.latex(f_x_y)}")
            st.markdown("---")
            
            # KROK 1: Zapis różniczkowy
            st.markdown("**Krok 1: Zastąpienie pochodnej stosunkiem różniczek**")
            st.markdown("Pochodną $y'$ zapisujemy jako $\\frac{dy}{dx}$:")
            st.latex(rf"\frac{{dy}}{{dx}} = {sp.latex(f_x_y)}")
            
            # KROK 2: Rozdzielenie
            st.markdown("**Krok 2: Mnożenie obustronne przez $dx$ i rozdzielenie zmiennych**")
            st.latex(rf"dy = {sp.latex(f_x_y)} \, dx")
            
            # Automatyczne wydzielenie g(y) oraz f(x)
            g_y = sp.simplify(f_x_y / f_x_y.subs(y_sym, 1)) if f_x_y.subs(y_sym, 1) != 0 else y_sym
            f_x = sp.simplify(f_x_y / g_y)
            left_side = 1 / g_y
            
            st.markdown(f"Dzielimy obustronnie przez składnik z $y$, czyli przez: ${sp.latex(g_y)}$ (zakładamy, że ${sp.latex(g_y)} \neq 0$):")
            st.latex(rf"{sp.latex(left_side)} \, dy = {sp.latex(f_x)} \, dx")
            
            # KROK 3: Nakładanie całek
            st.markdown("**Krok 3: Obustronne nałożenie całek nieoznaczonych**")
            st.latex(rf"\int {sp.latex(left_side)} \, dy = \int {sp.latex(f_x)} \, dx")
            
            # KROK 4: Obliczanie całek
            st.markdown("**Krok 4: Wyznaczenie całek składowych i dopisanie stałej C**")
            int_l = sp.integrate(left_side, y_sym)
            int_r = sp.integrate(f_x, x)
            
            # Korekta zapisu logarytmicznego dla oka
            int_l_latex = sp.latex(int_l)
            if "log" in str(int_l):
                int_l_latex = int_l_latex.replace(r"\log{\left(y \right)}", r"\ln|y|").replace(r"\log", r"\ln")
                
            st.markdown("Po obliczeniu całki z lewej strony oraz całki z prawej strony otrzymujemy postać uwikłaną:")
            st.latex(rf"{int_l_latex} = {sp.latex(int_r)} + C")
            
            # KROK 5: Przekształcenie do COR
            st.markdown("**Krok 5: Przekształcenie równania do postaci jawnej (COR)**")
            st.markdown("Uwalniamy zmienną $y$ (w przypadku logarytmów nakładamy obustronnie funkcję wykładniczą $e$, a stałą $e^C$ zastępujemy nową stałą $C_1$):")
            
            eq_diff = sp.Eq(y_fun.diff(x), f_x_y.subs(y_sym, y_fun))
            cor = sp.dsolve(eq_diff, y_fun)
            if isinstance(cor, list):
                cor = cor[0]
                
            st.latex(rf"\text{{COR:}} \quad {sp.latex(cor)}")
            st.success("✔ Całka Ogólna Równania (COR) została wyznaczona poprawnie!")
            
        except Exception as e:
            st.error(f"Wystąpił problem przy generowaniu kroków. Upewnij się, że wpisałeś mnożenie jako '*' (np. 5*x^2*y). Szczegóły: {e}")

# ==========================================
# TAB 2: PODPUNKTY NUMER 2
# ==========================================
with tab2:
    st.subheader("Zagadnienie Cauchy'ego krok po kroku z rozpisaniem całek (Podpunkty nr 2):")
    
    lista_2 = {
        "Zestaw 1.2: y' = 2xy^2 ; y(0)=2": {"eq": "2*x*y**2", "x0": "0", "y0": "2"},
        "Zestaw 2.2: y' = y^2 / (2*sqrt(x)) ; y(1)=3": {"eq": "y**2 / (2*sqrt(x))", "x0": "1", "y0": "3"},
        "Zestaw 3.2: y' = y^2 / x ; y(e)=2": {"eq": "y**2 / x", "x0": "exp(1)", "y0": "2"},
        "Zestaw 4.2: y' = 2x(y-1) ; y(0)=4": {"eq": "2*x*(y-1)", "x0": "0", "y0": "4"},
        "Zestaw 5.2: y' = (2x^2 + 1)*sqrt(y) ; y(0)=4": {"eq": "(2*x**2 + 1)*sqrt(y)", "x0": "0", "y0": "4"},
        "Zestaw 6.2: y' = y / cos^2(x) ; y(0)=2": {"eq": "y / cos(x)**2", "x0": "0", "y0": "2"},
        "Zestaw 7.2: y' = sqrt(y)*e^x ; y(0)=9": {"eq": "sqrt(y)*exp(x)", "x0": "0", "y0": "9"},
        "Zestaw 8.2: y' = 2x+1 ; y(1)=4": {"eq": "2*x + 1", "x0": "1", "y0": "4"},
        "✨ Własny przykład... (wpisz poniżej)": {"eq": "WLASNY", "x0": "0", "y0": "1"}
    }
    
    wybor_2 = st.selectbox("Wybierz zadanie z listy lub opcję własną:", list(lista_2.keys()), key="sel_tab2")
    data_2 = lista_2[wybor_2]
    
    if data_2["eq"] == "WLASNY":
        col_custom_eq = st.text_input("Wpisz prawą stronę równania y' =:", "2 * x * y**2", key="custom_eq_tab2")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            col_custom_x0 = st.text_input("Punkt x0 =", "0", key="custom_x0_tab2")
        with col_c2:
            col_custom_y0 = st.text_input("Wartość y(x0) =", "2", key="custom_y0_tab2")
            
        wzor_2 = col_custom_eq
        x0_str = col_custom_x0
        y0_str = col_custom_y0
    else:
        wzor_2 = data_2["eq"]
        x0_str = data_2["x0"]
        y0_str = data_2["y0"]
        st.code(f"Wybrane zadanie: y' = {wzor_2}  |  y({x0_str}) = {y0_str}")
        
    if st.button("📝 Generuj pełny protokół kolokwialny (Tab 2)", type="primary", key="btn_tab2"):
        try:
            f_x_y = parse_expr(wzor_2.replace('^', '**'), local_dict={'y': y_sym}, transformations=transformations)
            x0 = parse_expr(x0_str.replace('^', '**'), transformations=transformations)
            y0 = parse_expr(y0_str.replace('^', '**'), transformations=transformations)
            
            st.markdown("---")
            st.markdown("### 📝 Protokół Rozwiązania Krok po Kroku:")
            st.latex(rf"y^{{\prime}} = {sp.latex(f_x_y)} \quad ; \quad y({sp.latex(x0)}) = {sp.latex(y0)}")
            st.markdown("---")
            
            st.markdown("**Krok 1: Rozdzielenie zmiennych**")
            st.latex(rf"\frac{{dy}}{{dx}} = {sp.latex(f_x_y)} \implies dy = {sp.latex(f_x_y)} \, dx")
            
            g_y = sp.simplify(f_x_y / f_x_y.subs(y_sym, 1)) if f_x_y.subs(y_sym, 1) != 0 else y_sym
            f_x = sp.simplify(f_x_y / g_y)
            left_side = 1 / g_y
            
            st.markdown("Przerzucamy wszystkie składniki z $y$ na lewą stronę:")
            st.latex(rf"{sp.latex(left_side)} \, dy = {sp.latex(f_x)} \, dx")
            
            st.markdown("**Krok 2: Obustronne nałożenie całek i obliczenia składowe**")
            st.latex(rf"\int {sp.latex(left_side)} \, dy = \int {sp.latex(f_x)} \, dx")
            
            int_l = sp.integrate(left_side, y_sym)
            int_r = sp.integrate(f_x, x)
            
            st.markdown("*Obliczamy całkę lewej strony względem zmiennej $y$:*")
            st.latex(rf"\int {sp.latex(left_side)} \, dy = {sp.latex(int_l)}")
            
            st.markdown("*Obliczamy całkę prawej strony względem zmiennej $x$:*")
            st.latex(rf"\int {sp.latex(f_x)} \, dx = {sp.latex(int_r)}")
            
            st.markdown("Zestawiamy wyniki całek nieoznaczonych i dopisujemy stałą $C$ po prawej stronie:")
            int_l_latex = sp.latex(int_l)
            if "log" in str(int_l):
                int_l_latex = int_l_latex.replace(r"\log{\left(y \right)}", r"\ln|y|").replace(r"\log", r"\ln")
                
            st.latex(rf"{int_l_latex} = {sp.latex(int_r)} + C")
            
            eq_diff = sp.Eq(y_fun.diff(x), f_x_y.subs(y_sym, y_fun))
            cor = sp.dsolve(eq_diff, y_fun)
            if isinstance(cor, list):
                cor = cor[0]
                
            st.markdown("Przekształcamy powyższą postać uwikłaną do jawnego wzoru funkcji ogólnej (COR):")
            st.latex(rf"\text{{COR:}} \quad {sp.latex(cor)}")
            st.markdown("---")
            
            st.markdown("**Krok 3: Wyznaczenie wartości stałej $C$ (Warunek początkowy)**")
            st.markdown(f"Podstawiamy wartości graniczne $x = {sp.latex(x0)}$ oraz $y = {sp.latex(y0)}$:")
            
            constants = [s for s in cor.free_symbols if str(s).startswith('C')]
            if constants:
                C_sym = constants[0]
                rhs_with_x0 = cor.rhs.subs(x, sp.Symbol(f'({sp.latex(x0)})'))
                st.latex(rf"{sp.latex(y0)} = {sp.latex(rhs_with_x0)}")
                
                rhs_evaluated = cor.rhs.subs(x, x0)
                st.markdown("Po wykonaniu działań arytmetycznych w miejscu zmiennej $x$ otrzymujemy proste równanie:")
                st.latex(rf"{sp.latex(y0)} = {sp.latex(rhs_evaluated)}")
                
                C_val = sp.solve(sp.Eq(y0, rhs_evaluated), C_sym)[0]
                st.markdown("Rozwiązujemy powstałe równanie, aby wyznaczyć dokładną wartość stałej:")
                st.latex(rf"{sp.latex(C_sym)} = {sp.latex(C_val)}")
                st.markdown("---")
                
                st.markdown("**Krok 4: Zapisanie finalnego rozwiązania (Całka Szczególna - CSR)**")
                csr_result = cor.rhs.subs(C_sym, C_val)
                st.latex(rf"\text{{CSR:}} \quad y(x) = {sp.latex(csr_result)}")
                st.success("✔ Cały proces wyznaczenia całki szczególnej gotowy do przepisania!")
            else:
                st.warning("To równanie nie posiada standardowej stałej całkowania.")
        except Exception as e:
            st.error(f"Błąd składniowy: {e}")
# ==========================================
# TAB 3: PODPUNKTY NUMER 3
# ==========================================
with tab3:
    st.subheader("Równania Liniowe Niejednorodne krok po kroku (Podpunkty nr 3):")
    
    lista_3 = {
        "Zestaw 1.3: y' - 5y = 10x^2": {"p": "-5", "f_x": "10*x**2"},
        "Zestaw 2.3: y' + 3y = 6x^2 - 9": {"p": "3", "f_x": "6*x**2 - 9"},
        "Zestaw 3.3: y' + 5y = 10x^2 - 20": {"p": "5", "f_x": "10*x**2 - 20"},
        "Zestaw 4.3: y' + 2y = 4x^2 - 16": {"p": "2", "f_x": "4*x**2 - 16"},
        "Zestaw 5.3: y' - 4y = 2x^2 + 8": {"p": "-4", "f_x": "2*x**2 + 8"},
        "Zestaw 6.3: y' - 12y = 12x^2 - 24": {"p": "-12", "f_x": "12*x**2 - 24"},
        "Zestaw 7.3: y' - 7y = 7x^2 - 7x": {"p": "-7", "f_x": "7*x**2 - 7*x"},
        "Zestaw 8.3: y' + 2y = 4x^2 + 6": {"p": "2", "f_x": "4*x**2 + 6"},
        "✨ Własny przykład... (wpisz poniżej)": {"p": "WLASNY", "f_x": "WLASNY"}
    }
    
    wybor_3 = st.selectbox("Wybierz zadanie z listy lub opcję własną:", list(lista_3.keys()), key="sel_tab3")
    data_3 = lista_3[wybor_3]
    
    if data_3["p"] == "WLASNY":
        col_p = st.text_input("Wpisz współczynnik p przy y (np. -2 dla y' - 2y):", "-2", key="custom_p_tab3")
        col_fx = st.text_input("Wpisz funkcję f(x) z prawej strony (np. 4*x^2):", "4 * x**2", key="custom_fx_tab3")
        p_str = col_p
        fx_str = col_fx
    else:
        p_str = data_3["p"]
        fx_str = data_3["f_x"]
        znak = "+" if float(parse_expr(p_str)) >= 0 else ""
        st.code(f"Wybrane zadanie: y' {znak}{p_str}y = {fx_str}")

    if st.button("📝 Generuj pełny protokół kolokwialny (Tab 3)", type="primary", key="btn_tab3"):
        try:
            p = parse_expr(p_str)
            f_x_expr = parse_expr(fx_str.replace('^', '**'), transformations=transformations)
            
            st.markdown("---")
            st.markdown("### 📝 Rozwiązanie zadania metodą przewidywań:")
            znak_latex = "+" if p >= 0 else ""
            st.latex(rf"y^{{\prime}} {znak_latex} {sp.latex(p)}y = {sp.latex(f_x_expr)}")
            st.markdown("---")
            
            st.markdown("**Etap 1: Rozwiązanie równania jednorodnego (CORLJ)**")
            st.latex(rf"y^{{\prime}} {znak_latex} {sp.latex(p)}y = 0 \implies \frac{{dy}}{{dx}} = {-p}y")
            st.latex(rf"\frac{{1}}{{y}} dy = {-p} \, dx \implies \int \frac{{1}}{{y}} dy = \int {-p} \, dx")
            
            y_0_r = sp.Symbol('C_1') * sp.exp(-p * x)
            st.latex(rf"\ln|y| = {-p}x + C \implies y_0(x) = C_1 e^{{{sp.latex(-p * x)}}}")
            st.markdown("---")
            
            st.markdown("**Etap 2: Wyznaczenie całki szczególnej równania niejednorodnego (CSRLN)**")
            st.markdown("Przewidujemy rozwiązanie ($y_s$) w postaci wielomianu kwadratowego:")
            st.latex(rf"y_s(x) = Ax^2 + Bx + C")
            st.latex(rf"y_s^{{\prime}}(x) = 2Ax + B")
            
            st.markdown("Podstawiamy $y_s$ oraz $y_s'$ do równania wyjściowego:")
            A_s, B_s, C_s = sp.Symbol('A'), sp.Symbol('B'), sp.Symbol('C')
            y_s = A_s*x**2 + B_s*x + C_s
            dy_s = 2*A_s*x + B_s
            lewa_strona_podst = sp.collect(dy_s + p*y_s, x)
            
            st.latex(rf"({sp.latex(dy_s)}) {znak_latex} {sp.latex(p)}({sp.latex(y_s)}) = {sp.latex(f_x_expr)}")
            st.latex(rf"{sp.latex(lewa_strona_podst)} = {sp.latex(f_x_expr)}")
            
            rownanie_uproszczone = dy_s + p*y_s - f_x_expr
            poly_uproszczone = sp.Poly(rownanie_uproszczone, x)
            uklad = sp.solve(poly_uproszczone.coeffs(), (A_s, B_s, C_s))
            
            st.markdown("Porównując współczynniki przy potęgach $x$, otrzymujemy układ równań i jego wyliczone wartości:")
            st.latex(rf"A = {sp.latex(uklad[A_s])}, \quad B = {sp.latex(uklad[B_s])}, \quad C = {sp.latex(uklad[C_s])}")
            
            y_s_wynik = uklad[A_s]*x**2 + uklad[B_s]*x + uklad[C_s]
            st.latex(rf"y_s(x) = {sp.latex(y_s_wynik)}")
            st.markdown("---")
            
            st.markdown("**Etap 3: Zapisanie ostatecznego rozwiązania (CORLN)**")
            eq_diff_full = sp.Eq(y_fun.diff(x) + p*y_fun, f_x_expr)
            cor_full = sp.dsolve(eq_diff_full, y_fun)
            
            st.latex(rf"\text{{CORLN:}} \quad {sp.latex(cor_full)}")
            st.success("✔ Pełne rozwiązanie równania liniowego wygenerowane do zeszytu!")
        except Exception as e:
            st.error(f"Błąd przetwarzania: {e}")

# ==========================================
# TAB 4: PODPUNKTY NUMER 4 (CSR Liniowe na piechotę + Własny przykład)
# ==========================================
with tab4:
    st.subheader("Zagadnienia Cauchy'ego dla równań liniowych niejednorodnych (Podpunkty nr 4):")
    
    lista_4 = {
        "Zestaw 1.4: y' + 2y = 6x + 2 ; y(0)=-4": {"p": "2", "f_x": "6*x + 2", "x0": "0", "y0": "-4"},
        "Zestaw 2.4: y' - 2y = 2x + 4 ; y(0)=2": {"p": "-2", "f_x": "2*x + 4", "x0": "0", "y0": "2"},
        "Zestaw 3.4: y' + 3y = 6x + 12 ; y(0)=6": {"p": "3", "f_x": "6*x + 12", "x0": "0", "y0": "6"},
        "Zestaw 4.4: y' + 8y = 16x - 16 ; y(0)=-2": {"p": "8", "f_x": "16*x - 16", "x0": "0", "y0": "-2"},
        "Zestaw 5.4: y' + 2y = 6x - 2 ; y(0)=0": {"p": "2", "f_x": "6*x - 2", "x0": "0", "y0": "0"},
        "Zestaw 6.4: y' + 3y = 27x - 9 ; y(0)=-2": {"p": "3", "f_x": "27*x - 9", "x0": "0", "y0": "-2"},
        "Zestaw 7.4: y' + 2y = 10x - 2 ; y(0)=6": {"p": "2", "f_x": "10*x - 2", "x0": "0", "y0": "6"},
        "Zestaw 8.4: y' - 4y = 8x + 16 ; y(0)=2": {"p": "-4", "f_x": "8*x + 16", "x0": "0", "y0": "2"},
        "✨ Własny przykład... (wpisz poniżej)": {"p": "WLASNY", "f_x": "WLASNY", "x0": "0", "y0": "1"}
    }
    
    wybor_4 = st.selectbox("Wybierz zadanie z listy lub opcję własną:", list(lista_4.keys()), key="sel_tab4")
    data_4 = lista_4[wybor_4]
    
    if data_4["p"] == "WLASNY":
        col_p4 = st.text_input("Wpisz współczynnik p przy y (np. 2 dla y' + 2y):", "2", key="custom_p_tab4")
        col_fx4 = st.text_input("Wpisz funkcję f(x) (np. 6*x + 2):", "6*x + 2", key="custom_fx_tab4")
        col_c1_4, col_c2_4 = st.columns(2)
        with col_c1_4:
            col_custom_x0_4 = st.text_input("Punkt x0 =", "0", key="custom_x0_tab4")
        with col_c2_4:
            col_custom_y0_4 = st.text_input("Wartość y(x0) =", "-4", key="custom_y0_tab4")
            
        p_str4 = col_p4
        fx_str4 = col_fx4
        x0_str4 = col_custom_x0_4
        y0_str4 = col_custom_y0_4
    else:
        p_str4 = data_4["p"]
        fx_str4 = data_4["f_x"]
        x0_str4 = data_4["x0"]
        y0_str4 = data_4["y0"]
        znak4 = "+" if float(parse_expr(p_str4)) >= 0 else ""
        st.code(f"Wybrane zadanie: y' {znak4}{p_str4}y = {fx_str4}  |  y({x0_str4}) = {y0_str4}")

    if st.button("📝 Generuj pełny protokół kolokwialny (Tab 4)", type="primary", key="btn_tab4"):
        try:
            p4 = parse_expr(p_str4)
            f_x_expr4 = parse_expr(fx_str4.replace('^', '**'), transformations=transformations)
            x0_4 = parse_expr(x0_str4.replace('^', '**'), transformations=transformations)
            y0_4 = parse_expr(y0_str4.replace('^', '**'), transformations=transformations)
            
            st.markdown("---")
            st.markdown("### 📝 Pełne rozwiązanie zagadnienia Cauchy'ego:")
            znak_latex4 = "+" if p4 >= 0 else ""
            st.latex(rf"y^{{\prime}} {znak_latex4} {sp.latex(p4)}y = {sp.latex(f_x_expr4)} \quad ; \quad y({sp.latex(x0_4)}) = {sp.latex(y0_4)}")
            st.markdown("---")
            
            # KROK 1: CORLJ
            st.markdown("**Krok 1: Rozwiązanie równania jednorodnego (CORLJ)**")
            st.latex(rf"y^{{\prime}} {znak_latex4} {sp.latex(p4)}y = 0 \implies y_0(x) = C_1 e^{{{sp.latex(-p4 * x)}}}")
            st.markdown("---")
            
            # KROK 2: CSRLN (Przewidywanie)
            st.markdown("**Krok 2: Wyznaczenie całki szczególnej (CSRLN) metodą przewidywań**")
            # Ponieważ w zadaniach typu 4 stopień wielomianu po prawej stronie to 1 (postać Ax + B), przewidujemy wielomian liniowy
            A_s4, B_s4 = sp.Symbol('A'), sp.Symbol('B')
            y_s4 = A_s4*x + B_s4
            dy_s4 = A_s4
            
            st.markdown("Przewidujemy rozwiązanie i obliczamy pochodną:")
            st.latex(rf"y_s(x) = Ax + B \implies y_s^{{\prime}}(x) = A")
            
            st.markdown("Podstawiamy do równania wyjściowego i porządkujemy składniki:")
            lewa_strona_podst4 = sp.collect(dy_s4 + p4*y_s4, x)
            st.latex(rf"({sp.latex(dy_s4)}) {znak_latex4} {sp.latex(p4)}({sp.latex(y_s4)}) = {sp.latex(f_x_expr4)}")
            st.latex(rf"{sp.latex(lewa_strona_podst4)} = {sp.latex(f_x_expr4)}")
            
            rownanie_uproszczone4 = dy_s4 + p4*y_s4 - f_x_expr4
            poly_uproszczone4 = sp.Poly(rownanie_uproszczone4, x)
            uklad4 = sp.solve(poly_uproszczone4.coeffs(), (A_s4, B_s4))
            
            st.markdown("Z porównania współczynników przy odpowiednich potęgach $x$ otrzymujemy:")
            st.latex(rf"A = {sp.latex(uklad4[A_s4])}, \quad B = {sp.latex(uklad4[B_s4])}")
            
            y_s_wynik4 = uklad4[A_s4]*x + uklad4[B_s4]
            st.latex(rf"y_s(x) = {sp.latex(y_s_wynik4)}")
            st.markdown("---")
            
            # KROK 3: Złożenie CORLN
            st.markdown("**Krok 3: Złożenie rozwiązania ogólnego (CORLN)**")
            cor_combined = sp.Symbol('C_1') * sp.exp(-p4 * x) + y_s_wynik4
            st.latex(rf"y(x) = y_0(x) + y_s(x) \implies y(x) = C_1 e^{{{sp.latex(-p4 * x)}}} + {sp.latex(y_s_wynik4)}")
            st.markdown("---")
            
            # KROK 4: Warunek początkowy na piechotę
            st.markdown("**Krok 4: Wyznaczenie stałej $C_1$ z warunku początkowego**")
            st.markdown(f"Podstawiamy punkt $x = {sp.latex(x0_4)}$ oraz wartość $y = {sp.latex(y0_4)}$:")
            
            rhs_with_x0_4 = cor_combined.subs(x, sp.Symbol(f'({sp.latex(x0_4)})'))
            st.latex(rf"{sp.latex(y0_4)} = {sp.latex(rhs_with_x0_4)}")
            
            rhs_eval4 = cor_combined.subs(x, x0_4)
            st.latex(rf"{sp.latex(y0_4)} = {sp.latex(rhs_eval4)}")
            
            C1_sym = sp.Symbol('C_1')
            C1_val = sp.solve(sp.Eq(y0_4, rhs_eval4), C1_sym)[0]
            st.latex(rf"C_1 = {sp.latex(C1_val)}")
            st.markdown("---")
            
            # KROK 5: Ostateczny CSRLN
            st.markdown("**Krok 5: Całka Szczególna Równania Niejednorodnego (CSRLN)**")
            csr_final4 = cor_combined.subs(C1_sym, C1_val)
            st.latex(rf"\text{{Wynik końcowy (CSRLN):}} \quad y(x) = {sp.latex(csr_final4)}")
            st.success("✔ Pełne zagadnienie Cauchy'ego dla równania liniowego rozpisane poprawnie!")
            
        except Exception as e:
            st.error(f"Błąd podczas obliczeń symbolicznych: {e}")