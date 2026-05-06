# Import python packages.
import streamlit as st
import requests  
from snowflake.snowpark.functions import col 

# Write directly to the app.
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """
  Choose the fruits you want in your custom Smoothie!
  """
)

#Add a Name Box for Smoothie Orders
name_on_order = st.text_input("Name on Smoothie Order:")
st.write("The name on order is", name_on_order)

#Add the name_on_order to Order table

#Build a New SiS App!#

#Mel has decided to make a second app that can be used by the kitchen staff to see open orders 
#and mark them complete once they’ve been filled and given to the customer.

#Single select box
#option = st.selectbox(
#    "What is your favourite fruit?",
#    ("Banana", "Strawberries", "Peaches"),
#)

#st.write("You selected:", option)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients?",
    my_dataframe,
    max_selections = 5
)

if ingredients_list:

    #Create the INGREDIENTS_STRING Variable
    ingredients_string = ''
    #Storing the Orders
    for fruits_chosen in ingredients_list:
        ingredients_string += fruits_chosen + ' '
        #Display smoothiefroot nutrition information
        st.subheader(fruits_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruits_chosen )  
        st_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width = True)

    st.write(ingredients_string)

    #Build a SQL Insert Statement & Test It
    insert_stmt = """ insert into SMOOTHIES.PUBLIC.ORDERS(ingredients,name_on_order)
                        values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    #st.write(insert_stmt)
    time_to_insert = st.button('Submit Order')

    #Insert the Order into Snowflake
    if time_to_insert:
        session.sql(insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon = "✅")





