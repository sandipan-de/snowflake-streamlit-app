# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response)

# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custome Smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie: ')
st.write('The name on your Smoothie will be: ', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table('smoothies.public.fruit_options')\
        .select(col('FRUIT_NAME'))
ingradient_list = \
        st.multiselect(
            'Choose upto 5 ingradients'
            , my_dataframe
            , max_selections=5)

if ingradient_list:
    ingradient_string = ''
    for fruit_chosen in ingradient_list:
        ingradient_string += fruit_chosen + ' '

    my_insert_statement = \
    """insert into smoothies.public.orders (ingredients, name_on_order)
        values ('""" + ingradient_string + """','""" + name_on_order + """')"""

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_statement).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
