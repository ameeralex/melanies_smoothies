import requests
import pandas as pd

if ingredients_list:

    ingredients_string = " ".join(ingredients_list)

    for fruit_chosen in ingredients_list:

        # ✅ Get SEARCH_ON value from dataframe
        search_on = pd_df.loc[
            pd_df['FRUIT_NAME'] == fruit_chosen,
            'SEARCH_ON'
        ].iloc[0]

        # ✅ Show message (like screenshot)
        st.write('The search value for', fruit_chosen, 'is', search_on, '.')

        # ✅ Section header
        st.subheader(f"{fruit_chosen} Nutrition Information")

        try:
            # ✅ Use SEARCH_ON in API (IMPORTANT)
            url = f"https://my.smoothiefroot.com/api/fruit/{search_on}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                df_api = pd.json_normalize(data)
                st.dataframe(df_api, use_container_width=True)
            else:
                st.warning(f"{fruit_chosen} not found in Smoothiefroot database")

        except:
            st.error(f"Error fetching data for {fruit_chosen}")

    # ✅ Insert into Snowflake
    my_insert_stmt = f"""
    INSERT INTO SMOOTHIES.PUBLIC.ORDERS(ingredients, name_on_order)
    VALUES('{ingredients_string}', '{name_on_order}')
    """

    if st.button('Submit Order'):
        session.sql(my_insert_stmt).collect()
        st.success('Your smoothie is ordered', icon="✅")
