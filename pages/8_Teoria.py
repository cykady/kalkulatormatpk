import streamlit as st

st.set_page_config(page_title="Teoria - Równania Różniczkowe i Całki", layout="centered")

st.title("📚 Teoria: Zagadnienia na Kolokwium")
st.markdown("Poniżej znajdziesz opracowane odpowiedzi na pytania teoretyczne. Kliknij w pytanie, aby rozwinąć odpowiedź.")
st.markdown("---")

with st.expander("1. Zapisz symbolicznie całkę nieoznaczoną oraz oznaczoną."):
    st.markdown("**Całka nieoznaczona:**")
    st.latex(r"\int f(x)dx = F(x) + C")
    st.markdown("**Całka oznaczona (Wzór Newtona-Leibniza):**")
    st.latex(r"\int_a^b f(x)dx = F(x)\Big|_a^b = F(b) - F(a)")

with st.expander("2. Wyjaśnij skróty: COR, CSRLN, RLN, CSR, RR."):
    st.markdown("""
    * **COR** – Całka Ogólna Równania (rozwiązanie zawierające stałe, np. $C_1, C_2$)
    * **CSRLN** – Całka Szczególna Równania Liniowego Niejednorodnego (konkretne rozwiązanie po wyznaczeniu stałych lub rozwiązanie szczególne przewidziane dla prawej strony równania)
    * **RLN** – Równanie Liniowe Niejednorodne (równanie, w którym po prawej stronie znajduje się funkcja $f(x) \neq 0$)
    * **CSR** – Całka Szczególna Równania (rozwiązanie równania dla konkretnych warunków początkowych, bez stałych $C$)
    * **RR** – Równanie Różniczkowe
    """)

with st.expander("3. Podaj zastosowania całek oznaczonych w matematyce."):
    st.markdown("""
    Całka oznaczona jest podstawowym narzędziem geometrycznym. Służy m.in. do:
    * Obliczania **pól figur płaskich** (obszarów ograniczonych krzywymi).
    * Obliczania **długości łuku** krzywej.
    * Obliczania **objętości brył obrotowych** (powstałych przez obrót krzywej wokół osi układu współrzędnych).
    * Obliczania **pola powierzchni brył obrotowych**.
    """)

with st.expander("4. Podaj zastosowania całek oznaczonych w fizyce i mechanice."):
    st.markdown("""
    W mechanice i fizyce całka oznaczona pozwala na sumowanie nieskończenie małych wartości. Stosuje się ją do:
    * Obliczania **pracy siły zmiennej** na danym odcinku (np. praca sprężyny, rozciąganie pręta).
    * Wyznaczania położenia **środka ciężkości / środka masy** figur płaskich i brył.
    * Obliczania **momentów bezwładności** oraz **momentów statycznych** figur płaskich (kluczowe przy zginaniu belek).
    * Obliczania **drogi** w ruchu zmiennym, gdy znana jest funkcja prędkości od czasu ($s = \int_{t_1}^{t_2} v(t)dt$).
    * Obliczania **parcia cieczy** na płaską pionową ściankę zbiornika.
    """)

with st.expander("5. Podaj wzór ogólny równania różniczkowego liniowego I i II-go rzędu o stałych współczynnikach."):
    st.markdown("**Równanie liniowe I rzędu:**")
    st.latex(r"y' + p \cdot y = f(x) \quad \text{gdzie } p = \text{const}")
    st.markdown("**Równanie liniowe II rzędu:**")
    st.latex(r"y'' + py' + qy = f(x) \quad \text{gdzie } p, q = \text{const}")

with st.expander("6. Podaj rozkład na ułamki proste funkcji f(x):"):
    st.markdown("**a) Ułamki z pojedynczymi pierwiastkami w mianowniku:**")
    st.latex(r"f(x) = \frac{1}{(x-a)(x+b)} = \frac{A}{x-a} + \frac{B}{x+b}")
    
    st.markdown("**b) Ułamki z wyrażeniem kwadratowym (nierozkładalnym, $\Delta < 0$) w mianowniku:**")
    st.markdown("Zauważ, że w liczniku nad trójmianem kwadratowym musi pojawić się funkcja liniowa ($Ax+B$):")
    st.latex(r"f(x) = \frac{1}{(x^2+a^2)(x-b)} = \frac{Ax+B}{x^2+a^2} + \frac{C}{x-b}")