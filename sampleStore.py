# Import libraries
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

# Page title
st.set_page_config(page_title='Sample Store Data Explorer', page_icon='📊')
st.title('📊 Sample Store Data Explorer')

# App description - Explain functionalities in an expander box
with st.expander('About this app'):
  st.markdown('**What can this app do?**')
  st.info('This app shows the use of Pandas for data wrangling, Altair for chart creation and editable dataframe for data interaction.')
  st.markdown('**How to use the app?**')
  st.warning('To engage with the app, 1. Select Category of your interest in the drop-down selection box and then 2. Select the year duration from the slider widget. As a result, this should generate an updated editable DataFrame and line plot.')

# Question header
st.subheader('Which Category performs ($) best at the Sample Store?')

# Load data - Read CSV into a Pandas DataFrame
df = pd.read_csv('data/Superstore_Orders.csv')
df.year = pd.DatetimeIndex(df['Order Date']).year

with st.sidebar:
    st.title('Filter Selection')
    # Category selection - Create dropdown menu for genre selection
    category_list = df.Category.unique()
    category_selection = st.multiselect('Select Category', category_list,['Technology'])

    # City selection - Create dropdown menu for genre selection
    city_list = df.City.unique()
    city_selection = st.selectbox('Select City', sorted(city_list))

    # Year selection - Create slider for year range selection
    year_list = df.year.unique()
    year_selection = st.slider('Select Year', 2020, 2023, (2020, 2023))
    year_selection_list = list(np.arange(year_selection[0], year_selection[1]+1))

# # Subset data - Filter DataFrame based on selections
# df_selection = df[df.Category.isin(category_selection) & df.City.isin(city_selection) & df.year.isin(year_selection_list)]
df_selection = df[df.Category.isin(category_selection) & df.City.str.contains(city_selection) & df.year.isin(year_selection_list)]

reshaped_df = df_selection.pivot_table(index='Order Date', columns='Category', values='Sales', aggfunc='sum', fill_value=0)
reshaped_df = reshaped_df.sort_values(by='Order Date', ascending=True)
print(reshaped_df)
# # Editable DataFrame - Allow users to made live edits to the DataFrame
df_editor = st.data_editor(reshaped_df, height=212, use_container_width=True,
                            column_config={"Order Date": st.column_config.DatetimeColumn("Order Date", format="D MMM YYYY"),
                                            "City":st.column_config.TextColumn("City")},
                            num_rows="dynamic")



# # Data preparation - Prepare data for charting
df_chart = pd.melt(df_editor.reset_index(), id_vars='Order Date', var_name='Category', value_name='Sales')
# # Display line chart
chart = alt.Chart(df_chart).mark_line().encode(
            x=alt.X('Order Date:N', title='Order Date'),
            y=alt.Y('Sales:Q', title='Gross earnings ($)'),
            color='Category:N'
            ).properties(height=320)
st.altair_chart(chart, use_container_width=True)