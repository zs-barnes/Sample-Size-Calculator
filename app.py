import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
from statsmodels.stats.power import tt_ind_solve_power, zt_ind_solve_power

st.title("Sample Size calculator")
st.subheader("A python implementation of")
st.subheader("https://nathaniel-t-stevens.shinyapps.io/SampleSizeCalculator/")
st.title("")
test = st.sidebar.radio("Type of Test", ("T-test", "Z-test"))
alternative = st.sidebar.radio(
    "Is the test One- or Two-Sided?", ("one-sided", "two-sided")
)
if alternative == "one-sided":
    alternative = "larger"
x_axis = st.sidebar.radio(
    "What parameter would you like to vary on the x-axis?",
    ("Significance level", "Power", "Effect Size"),
)

if test == "T-test":
    solver = tt_ind_solve_power
else:
    solver = zt_ind_solve_power

if x_axis == "Significance level":
    values = st.sidebar.slider("Alpha", 0.0, 0.1, (0.01, 0.05))
    power = st.sidebar.slider("Power:", 0.75, 1.0, 0.8)
    effect_size = st.sidebar.slider("Effect Size:", 0.0, 3.0, 0.5)
    x_axis_values = np.linspace(values[0], values[1], num=20)
    sample_size = []

    for val in x_axis_values:
        sample_size.append(
            solver(
                effect_size=effect_size, alpha=val, power=power, alternative=alternative
            )
        )


if x_axis == "Power":
    alpha = st.sidebar.slider("Significance Level", 0.0, 0.1, 0.05)
    values = st.sidebar.slider("Power", 0.75, 1.0, (0.8, 0.9))
    effect_size = st.sidebar.slider("Effect Size:", 0.0, 3.0, 0.5)
    x_axis_values = np.linspace(values[0], values[1], num=20)
    sample_size = []

    for val in x_axis_values:
        sample_size.append(
            solver(
                effect_size=effect_size, alpha=alpha, power=val, alternative=alternative
            )
        )

if x_axis == "Effect Size":
    alpha = st.sidebar.slider("Significance Level", 0.0, 0.1, 0.05)
    power = st.sidebar.slider("Power:", 0.75, 1.0, 0.8)
    values = st.sidebar.slider("Effect Size:", 0.0, 3.0, (0.5, 1.0))
    x_axis_values = np.linspace(values[0], values[1], num=20)
    sample_size = []

    for val in x_axis_values:
        sample_size.append(
            solver(effect_size=val, alpha=alpha, power=power, alternative=alternative)
        )


source = pd.DataFrame({f"{x_axis}": x_axis_values, "Sample Size": sample_size})

c = (
    alt.Chart(source)
    .mark_line()
    .encode(alt.Y("Sample Size", scale=alt.Scale(zero=False)), x=f"{x_axis}")
    .properties(title=f"Sample size vs {x_axis}", width=600, height=600)
    .configure_axis(labelFontSize=15, titleFontSize=20)
    .configure_title(fontSize=20)
)
st.altair_chart(c)
