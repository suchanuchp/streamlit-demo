import streamlit as st
import plotly.express as px


def main():
    st.title('Iris Demo')
    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")
    st.plotly_chart(fig)


if __name__ == "__main__":
    main()
