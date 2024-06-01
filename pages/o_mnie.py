import streamlit as st

def app():
    st.title('O mnie 🧑‍💼')

    st.markdown("""
    <style>
        .content {
            font-size: 20px;
        }
        .content h3 {
            font-size: 24px;
        }
        .content p {
            font-size: 20px;
            margin-left: 20px;
        }
    </style>
    <div class="content">
    Witaj na w mojej pierwszej aplikacji zbudowanej w Streamlit! 
    Mam na imię Grzegorz i na co dzień pracuję w jednej z wrocławskich firm w dziale finansowym. 
    Po pracy oddaję się swojej drugiej pasji, jaką są data science oraz programowanie w Pythonie! 📊💻

    ### 🧑‍💼 O mnie:
    <p>📆 ponad 14 lat doświadczenia w różnych branżach (doradztwo, audyt, bankowość, consumer finance, produkcja)</p>
    <p>👨‍🏫 Polski Biegły Rewident (CPA)</p>
    <p>🌟 Fellow ACCA Member</p>
    <p>🌍 pasjonat języków obcych: angielski, niemiecki, francuski, hiszpański, niderlandzki</p>

    ### 🎓 Edukacja:
    <p>📚 absolwent kierunku "Finanse i Rachunkowość" – Uniwersytet Ekonomiczny we Wrocławiu</p>
    <p>📘 6 studiów podyplomowych (MSSF, podatki, metody wyceny, Excel, analiza danych, VBA, Python) - 🌱 ciągły rozwój zawodowy i osobisty, który pozwala mi być na bieżąco z najnowszymi trendami i technikami w świecie finansów i technologii</p>
    <p>🎓 Executive MBA - opcja międzynarodowa – Uniwersytet Ekonomiczny we Wrocławiu</p>

    ### 🛠️ Moje kompetencje:
    <p>💼 finanse korporacyjne, metody wyceny spółek</p>
    <p>🧮 analiza danych i modelowanie finansowe</p>
    <p>📈 controlling i rachunek kosztów</p>
    <p>🕵️‍♂️ audyt finansowy i due diligence</p>
    <p>📊 BI - Business Intelligence</p>           
    <p>🐍 programowanie (Python, R, SQL, VBA)</p>
    <p>🌐 tworzenie aplikacji webowych (HTML, CSS, JavaScript)</p>

    ### 📜 Doświadczenie zawodowe:
    <p>🏢 obecnie pracuję jako Group CFO w Grupie Kapitałowej Saule Technologies, gdzie odpowiadam za zarządzanie finansami i strategiczne decyzje biznesowe</p>

    ### 🚀 Co mnie wyróżnia:
    <p>🔍 integracja wiedzy finansowej z data science – fascynuje mnie stosowanie nowoczesnych metod naukowych i algorytmów do przekształcania danych w cenne informacje biznesowe</p>
    <p>👨‍💻 pasja do programowania – znajomość Python'a, R, SQL, VBA pozwala mi na zaawansowane analizy i automatyzację procesów</p>

    <p>Zapraszam do kontaktu! 📧</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    app()
