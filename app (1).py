import streamlit as st
import pandas as pd
import pickle

model = pickle.load(open("car_price_model.pkl", "rb"))
df = pd.read_csv("cleaned_car_data.csv")

st.set_page_config(
    page_title="AutoValue AI",
    page_icon="sports_car_cropped.png",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0f172a,#1e293b);
}

.block-container {
    padding-top: 2rem;
}

label {
    font-size: 18px !important;
    font-weight: 600 !important;
    color: #f8fafc !important;
    font-style: italic !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    background: #ffffff;
    border-radius: 12px;
    border: 1px solid #38bdf8;
}

.stNumberInput input {
    background: #ffffff;
    border-radius: 12px;
    border: 1px solid #38bdf8;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(90deg,#0284c7,#38bdf8);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 14px;
    font-size: 18px;
    font-weight: 700;
    font-style: italic;
}

.stButton > button:hover {
    background: linear-gradient(90deg,#0369a1,#0ea5e9);
    color: white;
}

.result-card {
    background: linear-gradient(135deg,#0284c7,#0ea5e9);
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    margin-top: 25px;
    box-shadow: 0 10px 25px rgba(14,165,233,0.25);
}

.result-title {
    font-size: 18px;
    color: #e0f2fe;
    font-style: italic;
}

.result-price {
    font-size: 40px;
    font-weight: 800;
    color: white;
    margin-top: 6px;
}
</style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([1, 4])

with col1:
    st.image("sports_car_cropped.png", width=140)

with col2:
    st.markdown(
        """
        <h1 style="
        color:#f8fafc;
        font-size:58px;
        font-weight:800;
        margin-bottom:0px;">
        AutoValue AI
        </h1>

        <p style="
        color:#cbd5e1;
        font-size:20px;
        font-style:italic;
        margin-top:0px;">
        Smart Used Car Price Prediction System
        </p>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

left, center, right = st.columns([1, 2, 1])

with center:
    company = st.selectbox("Car Brand", sorted(df["company"].unique()))

    car_name = st.selectbox(
        "Car Model",
        sorted(df[df["company"] == company]["name"].unique())
    )

    year = st.number_input(
        "Manufacturing Year",
        min_value=1995,
        max_value=2026,
        value=2015
    )

    fuel_type = st.selectbox("Fuel Type", sorted(df["fuel_type"].unique()))

    kms_driven = st.number_input(
        "Kilometers Driven",
        min_value=0,
        max_value=300000,
        value=50000
    )

    predict = st.button("Predict Price")

    if predict:
        input_df = pd.DataFrame({
            "name": [car_name],
            "company": [company],
            "year": [year],
            "kms_driven": [kms_driven],
            "fuel_type": [fuel_type]
        })

        prediction = model.predict(input_df)[0]

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-title">Predicted Market Value</div>
                <div class="result-price">₹ {int(prediction):,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
