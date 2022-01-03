import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objs as go
import colorlover as cl
colors = cl.to_rgb(cl.scales['7']['qual']['Set2'])
from scripts import saproc
from hydralit import HydraHeadApp

class sentiment(HydraHeadApp):
#def app():

    def run(self):

        @st.cache
        def get_sa_markdown(sa_btn):

            sa_df = df_filtered.sort_values('compound', ascending=sa_btn).head(10)
            sa_df = sa_df[['source','url','title','date','compound']]

            return sa_df

        df_filtered = st.session_state.df_filtered

        # placeholder for status updates
        placeholder = st.empty()

        # header
        st.subheader('Sentiment analysis')

        # box plots
        placeholder.markdown('*. . . Visualizing data . . .*\n\n')

        # sect 1
        sent_btn = st.radio('', ['Article Text','Headline'])
        if sent_btn == 'Article Text':
            sent_query = 'compound'
        else:
            sent_query = 'title_compound'

        st.markdown("### Sentiment over time")
        st.caption("Distribution of mean sentiment by month. Scale: 1.0 is most positive, -1.0 is most negative.")

        sent_topic_plot = saproc.get_topic_plot(df_filtered, sent_query)
        st.plotly_chart(sent_topic_plot, use_container_width=True)

        # sect 2
        st.markdown("### Sentiment distribution by source")

        st.caption("Distribution of sentiment within publication sources. Scale: 1.0 is most positive, -1.0 is most negative.")

        sent_boxplot = saproc.get_sent_boxplot(df_filtered, sent_query)
        st.plotly_chart(sent_boxplot, use_container_width=True)

        # sect 3
        placeholder.markdown('*. . . Evaluating article sentiment . . .*\n\n')
        with st.expander("Top articles by sentiment"):

            st.caption("View articles by VADER sentiment analysis score. Scale: 1.0 is most positive, -1.0 is most negative.")
            sa_btn = st.radio('', ['Positive','Negative'])

            if sa_btn == 'Positive':
                st.markdown(f'10 articles with most positive sentiment analysis scores')
                sa_df = get_sa_markdown(False)
            else:
                st.markdown(f'10 articles with most negative sentiment analysis scores')
                sa_df = get_sa_markdown(True)

            sa_head = st.columns([1,3,1,1])
            sa_head[0].markdown('**Source**')
            sa_head[1].markdown('**Article**')
            sa_head[2].markdown('**Published date**')
            sa_head[3].markdown('**VADER score**')

            for i,r in sa_df.iterrows():
                sa_cols = st.columns([1,3,1,1])
                sa_cols[0].markdown(f'{r.source}')
                sa_cols[1].markdown(f'[{r.title}]({r.url})')
                sa_cols[2].markdown(f'{r.date}')
                sa_cols[3].markdown(f'{r.compound}')

            #for i,r in sa_df.iterrows():
                #st.markdown(f'{r.source} - [{r.title}]({r.url}) ({r.date})')

        placeholder.empty()
