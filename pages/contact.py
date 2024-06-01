import streamlit as st

def app():
    st.title('Kontakt ✉️')
    
    st.header('Zapraszam do kontaktu w razie pytań!')

    st.markdown(
        """
        <style>
            .contact-info {
                font-size: 18px; /* Powiększenie czcionki */
                font-weight: bold; /* Pogrubienie tekstu */
                color: #262730; /* Ustawienie koloru tekstu */
                margin-bottom: 30px; /* Duży odstęp dolny */
            }
        </style>
        <div class='contact-info'>
            Możesz skontaktować się ze mną na dwa sposoby: przez LinkedIn lub odwiedzając moją stronę internetową.
        </div>
        """,
        unsafe_allow_html=True
    )

    
    col1, col2 = st.columns([1, 1], gap="medium")
    
    # LinkedIn
    with col1:
        st.markdown(
            f"""
            <div style="text-align: center;">
                <a href="https://www.linkedin.com/in/grzegorz-macowicz-b75962122/" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn"
                         style="width:100px;height:100px;">
                </a>
                <p>LinkedIn</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    # strona www prywatna
    with col2:
        st.markdown(
            f"""
            <div style="text-align: center;">
                <a href="https://grzegorzmacowicz.pl/" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/561/561127.png" alt="Website"
                         style="width:100px;height:100px;">
                </a>
                <p>Strona internetowa grzegorzmacowicz.pl</p>
            </div>
            """,
            unsafe_allow_html=True
        )

