import streamlit as st
from kfre import kfre_person

# Add background image via CSS (using external link)
# Page setup
st.set_page_config(page_title="Odhad rizika selhání ledvin", layout="centered")
# Title
st.markdown("<h1 style='text-align: center;'>📊 Odhad rizika selhání ledvin (KFRE)</h1>", unsafe_allow_html=True)

st.markdown("""
<p style='text-align: center;'>Tento nástroj vypočítá riziko selhání ledvin během <strong>2 a 5 let</strong> pomocí modelu KFRE.</p>
<hr>
""", unsafe_allow_html=True)

# Input layout
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Věk", min_value=18, max_value=120, value=50, help="Pacientův aktuální věk")
    eGFR = st.number_input("eGFR (ml/min/1.73 m²)", min_value=1.0, max_value=100.0, value=20.0, help="Odhadovaná glomerulární filtrace")
    uACR = st.number_input("uACR (mg/g)", min_value=1.0, max_value=5000.0, value=100.0, help="Poměr albuminu a kreatininu v moči")
    is_male = st.radio("Pohlaví", ["Žena", "Muž"], help="Vyberte pohlaví pacienta") == "Muž"
    is_north_american = st.checkbox("Severoamerický pacient?", value=False)

with col2:
    dm = st.selectbox("Diabetes", ["Nezadáno", "Ano", "Ne"], help="Má pacient diabetes?")
    htn = st.selectbox("Hypertenze", ["Nezadáno", "Ano", "Ne"], help="Má pacient vysoký krevní tlak?")
    albumin = st.number_input("Albumin (g/L) – volitelné", value=0.0)
    phosphorous = st.number_input("Fosfor (mmol/L) – volitelné", value=0.0)
    bicarbonate = st.number_input("Bikarbonát (mmol/L) – volitelné", value=0.0)
    calcium = st.number_input("Vápník (mmol/L) – volitelné", value=0.0)

# Helper functions
def to_none(val):
    return None if val == 0.0 else val

def map_optional(val):
    return {"Ano": True, "Ne": False, "Nezadáno": None}[val]

# Calculate and display risk
if st.button("🔍 Vypočítat riziko"):
    common_args = {
        "age": age,
        "is_male": is_male,
        "eGFR": eGFR,
        "uACR": uACR,
        "is_north_american": is_north_american,
        "dm": map_optional(dm),
        "htn": map_optional(htn),
        "albumin": to_none(albumin),
        "phosphorous": to_none(phosphorous),
        "bicarbonate": to_none(bicarbonate),
        "calcium": to_none(calcium)
    }

    risk_2y = kfre_person(**common_args, years=2) * 100
    risk_5y = kfre_person(**common_args, years=5) * 100

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="
        background-color: #f2f2f2;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #ccc;
    ">
    <h5>Riziko progrese pacienta k selhání ledvin vyžadující dialýzu nebo transplantaci.

</h5>
    <ul>
        <li><strong>Do 2 let:</strong> {risk_2y:.2f}%</li>
        <li><strong>Do 5 let:</strong> {risk_5y:.2f}%</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
