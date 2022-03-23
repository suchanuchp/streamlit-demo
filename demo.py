import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter


@st.cache(allow_output_mutation=True)
def get_dataframe():
    df = pd.read_pickle('df.pkl')
    df = df.rename(columns={'score': 'tscore', 'path': 'filename'})
    return df


def main():
    df = get_dataframe()
    df.filename = df.filename.apply(lambda p: p.split('/')[-1][:20])
    col1, col2 = st.columns([3, 1])
    group = col1.selectbox('Select group:', options=df.group.unique())
    max_score = col2.number_input('Max Score:', value=1.)
    df['score'] = df.tscore.apply(lambda s: min(s/max_score, 1))
    poi = df[(df.group == group) & (~df.filename.str.lower().str.contains('bible'))]
    fig = px.bar(poi, x="filename", y="score", orientation='v')
    st.plotly_chart(fig)

    col1, col2 = st.columns([3, 1])
    filename = col1.selectbox('Select filename:', options=poi.filename)
    n = col2.number_input('First N Words:', value=20)
    poi = df[df.filename == filename].iloc[0]
    label_row = df[(df.group == group) & (df.filename.str.lower().str.contains('bible'))].iloc[0]
    diff = set(label_row.texts).difference(poi.texts)
    diff_lst = [t for t in label_row.texts if t in diff]
    counts = Counter(diff_lst)
    counts = {k: v for k, v in sorted(counts.items(), key=lambda item: -item[1])[:n]}
    counts = {k: v for k, v in sorted(counts.items(), key=lambda item: item[1])}
    fig = go.Figure(go.Bar(
        x=list(counts.values()),
        y=list(counts.keys()),
        orientation='h'))
    fig.update_layout(barmode='stack', xaxis={
        'categoryorder': 'total descending'}, yaxis={'dtick': 1},
    )
    st.plotly_chart(fig)







if __name__ == "__main__":
    main()
