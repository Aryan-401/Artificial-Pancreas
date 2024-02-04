from constants import Constants
from bergman_model import Body
import streamlit as st


def main():
    
    st.markdown("<style>h6{margin-bottom: 0;}</style>", unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center;'>Bergman Minimal Model</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<h2>MEALS</h2>", unsafe_allow_html=True)
    st.markdown("<h6>Meal time should be added in interval of seconds so as to specify after how many seconds a meal should be given after start of simulation. </h6>", unsafe_allow_html=True)
    st.markdown("<h6>Meal quantity should be added in grams corresponding to the amount of carbohydrates in meal </h6>", unsafe_allow_html=True)

    num_meals = st.number_input("Enter the number of meal inputs", min_value=1, value=1)

    col1, col2 = st.columns(2)

    meal_times = []
    Dg = []

    for i in range(num_meals):
        with col1:
            st.markdown(
            f"<h6 style='margin-bottom: 0;'>Meal {i + 1} Time</h6>",
            unsafe_allow_html=True
            )
            time = st.number_input(label="Seconds", key=f"meal_time_{i}",max_value = 1440, min_value=0)
            meal_times.append(time)
            st.markdown("<br>", unsafe_allow_html=True)

        with col2:
            st.markdown(
            f"<h6 style='margin-bottom: 0;'>Meal {i + 1} Quantity</h6>",
            unsafe_allow_html=True
            )
            meal_quantity = st.number_input(label="Grams", key=f"meal_quantity_{i}", min_value=0)
            Dg.append(meal_quantity)
            st.markdown("<br>", unsafe_allow_html=True)

    meal_times.append(1900)
    Dg.append(8552)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<h2>INSULIN</h2>", unsafe_allow_html=True)
    st.markdown("<h6>Insulin dose time should be added in interval of seconds so as to specify after how many seconds an insulin dosage is given after start of simulation. </h6>", unsafe_allow_html=True)
    st.markdown("<h6>Insulin dosage should be added in microlitres(μL). </h6>", unsafe_allow_html=True)

    num_insulin_dosage = st.number_input("Enter the number of insulin dosage", min_value=1, value=1)

    col3, col4 = st.columns(2)

    u_quantity=[]
    insulin_time = []

    for i in range(num_insulin_dosage):
        with col3:
            st.markdown(
            f"<h6 style='margin-bottom: 0;'>Insulin dosage {i + 1} Time</h6>",
            unsafe_allow_html=True
            )
            insulin_inject_time = st.number_input(label="Seconds", key=f"insulin_time_{i}",max_value = 1440, min_value=0)
            insulin_time.append(insulin_inject_time)
            st.markdown("<br>", unsafe_allow_html=True)

        with col4:
            st.markdown(
            f"<h6 style='margin-bottom: 0;'>Insulin Dosage {i + 1} Quantity</h6>",
            unsafe_allow_html=True
            )
            insulin_dose = st.number_input(label="μL", key=f"insulin_dosage_{i}", min_value=0.0, step=0.0001, format="%.4f")
            u_quantity.append(insulin_dose)
            st.markdown("<br>", unsafe_allow_html=True)

    u_quantity.append(8552)
    insulin_time.append(9999)


    c = Constants()
    b = Body()
    b.get_graph(meal_times, insulin_time, u_quantity, Dg)


if __name__ == '__main__':
    main()
