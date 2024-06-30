import streamlit as st
import draw as draw
from sqlalchemy.sql import text
import time
import pandas as pd
import numpy as np
import datetime

st.set_page_config(
    page_title="View segment detail",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

def view_segment_detail():
    start_time = datetime.datetime.now()
    seg_id = st.session_state["current_segment"]["segment_id"]
    seg_name = st.session_state["current_segment"]["segment_name"]
    seg_gender = st.session_state["current_segment"]["gender"]
    seg_min_price = st.session_state["current_segment"]["min_price"]
    seg_max_price = st.session_state["current_segment"]["max_price"]
    seg_min_date = st.session_state["current_segment"]["min_date"]
    brand_list = st.session_state["current_brand_list"]
    cate_list = st.session_state["current_cate_list"]

    conn = st.connection("warehouse", type="sql")
    # customer list
    sql_customer = '''
                    select distinct user_full_name, email, phone, address
                    from purchase_history pe 
                    where gender = :g and
                    brand_name in :b_l and
                    category in :c_l and
                    price >= :min_p and price <= :max_p and
                    interaction_date > :min_d;
                    '''
    # total revenue, total number of orders(purchase) => avg purchase value
    sql_revenue = '''select sum(price) as revenue, count(root_id_event) as orders
                    from purchase_history pe
                    where action = 'checkout' and 
                        gender = :g and
                        brand_name in :b_l and
                        category in :c_l and
                        price >= :min_p and price <= :max_p and
                        interaction_date > :min_d
                    group by action;'''
    
    # total purchases, total number of customer => avg purchase frequency rate
    sql_fre= '''
                select count(distinct user_id) as customers
                from purchase_history pe
                where action = 'checkout' and 
                    gender = :g and
                    brand_name in :b_l and
                    category in :c_l and
                    price >= :min_p and price <= :max_p and
                    interaction_date > :min_d
                group by user_id; 
            '''

    sql_lifespan = '''select count(root_id_event) as lifespan 
                    from purchase_history pe
                    where "action" = 'checkout' and 
                        gender = :g and
                        brand_name in :b_l and
                        category in :c_l and
                        price >= :min_p and price <= :max_p and
                        interaction_date > :min_d
                    group by year;'''
    sql_conversion = '''select count(root_id_event) as total_count, action 
                        from purchase_history pe 
                        where gender = :g and
                            brand_name in :b_l and
                            category in :c_l and
                            price >= :min_p and price <= :max_p and
                            interaction_date > :min_d
                        group by "action";'''
    # with conn.session as s:
    customer_params = dict(g=seg_gender.lower(), b_l=tuple(brand_list), c_l=tuple(cate_list), min_p=seg_min_price, max_p=seg_max_price, min_d=str(seg_min_date))
    customer_df = conn.query(sql_customer, params=customer_params)
    
    avg_purchase_value = 0
    avg_purchase_fre_rate = 0
    avg_customer_lifespan= 0
    clv = 0
    sale_conversion_rate = 0
    total_revenue = 0
    total_customer = 0

    if len(customer_df) > 0:
        value_params = dict(g=seg_gender.lower(), b_l=tuple(brand_list), c_l=tuple(cate_list), min_p=seg_min_price, max_p=seg_max_price, min_d=str(seg_min_date))
        customer_value = conn.query(sql_revenue, params=value_params)
        total_customer = len(customer_df)
        
        if len(customer_value) > 0:
            avg_purchase_value = customer_value.iloc[0, 0]/customer_value.iloc[0, 1]
            avg_purchase_fre_rate = customer_value.iloc[0, 1]/len(customer_df)
            total_revenue = customer_value.iloc[0, 0]

        fre_rate = conn.query(sql_fre, params=value_params)

        lifespan = conn.query(sql_lifespan, params=value_params)
        sale_conversion = conn.query(sql_conversion, params=value_params)
        
        if len(lifespan) > 0:
            avg_customer_lifespan =  lifespan.iloc[0, 0] * 20/(len(customer_df))
            clv = avg_purchase_value * avg_purchase_fre_rate * avg_customer_lifespan
        if len(sale_conversion) > 0:
            sale_conversion_rate = int(sale_conversion.loc[sale_conversion["action"] == "checkout", "total_count"].sum())/int(sale_conversion["total_count"].sum())
    
    m1, m2, m3, m4, m5 = st.columns((1,1,1,1,1))

    m1.metric("Total Number Of Customer", f"{total_customer}")
    m2.metric("Total Revenue", f"{total_revenue}$")
    m3.metric("Customer Life Time Value", f"{round(clv, 2)}$")
    m4.metric("Average Order Value", f"{round(avg_purchase_value, 2)}$")
    m5.metric("Sale Conversion Rate", f"{round(sale_conversion_rate, 2) * 100}%")

    if len(customer_df) > 0:
        full_size = st.container()
        with full_size:
            st.table(customer_df)
    
    end_time = datetime.datetime.now()
    execution_time = (end_time - start_time).total_seconds()
    print(f"execution time of view segment detail metrics: {execution_time} s")

def visulization_tab():
    start_time = datetime.datetime.now()
    seg_id = st.session_state["current_segment"]["segment_id"]
    seg_name = st.session_state["current_segment"]["segment_name"]
    seg_gender = st.session_state["current_segment"]["gender"]
    seg_min_price = st.session_state["current_segment"]["min_price"]
    seg_max_price = st.session_state["current_segment"]["max_price"]
    seg_min_date = st.session_state["current_segment"]["min_date"]

    # col1, col2 = st.columns([7, 3])
    con1 = st.container()
    con2 = st.container()
    # col1 = st.container()
    with con1:
        # map_options = st.multiselect("Action on map", ["view", "add", "remove", "checkout"], default=["view", "add", "remove", "checkout"])
        map_options = ["view", "add", "remove", "checkout"]
        map_sql = '''select latitude, longitude
                    from purchase_history pe 
                    where action in :map_opts;'''
        conn = st.connection("warehouse", type="sql")
        # if len(map_options) > 0:
        map_df = conn.query(map_sql, params=dict(map_opts=tuple(map_options)))
        draw.draw_map(map_df)
    # with con2:
        # word cloud

    c1, c2 = st.columns([6, 4])
    #  = st.container()
    with c1:
        action_sql = '''select action, count(*) as action_count
                        from purchase_history pe
                        group by action;'''
        action_df = conn.query(action_sql)
        total = int(action_df['action_count'].sum())
        views = int(action_df.loc[action_df['action'] == 'view', 'action_count'].sum())
        adds = int(action_df.loc[action_df['action'] == 'add', 'action_count'].sum())
        checkouts = int(action_df.loc[action_df['action'] == 'checkout', 'action_count'].sum())
        st.plotly_chart(draw.draw_funnel([total, views, adds, checkouts]))
    # c2 = st.container()
    with c2:
        pie_sql = '''select gender, count(*) as count_gender
                        from purchase_history pe
                        group by gender;'''

        gender_df = conn.query(pie_sql)
        st.pyplot(draw.draw_pie([int(gender_df.loc[gender_df['gender'] == 'male', 'count_gender']), int(gender_df.loc[gender_df['gender'] == 'female', 'count_gender'])]))

    # word cloud for select box, brand, cate, text
    # radar chart for ?

    c1, c2, c3, c4 = st.columns([2.5, 2.5, 2.5, 2.5])
    with c1:
        rating_sql = '''select rating, count(rating) as count_rating
                        from purchase_history pe 
                        where "action" = 'checkout'
                        group by rating;'''
        rating_df = conn.query(rating_sql)
        # st.write(brand_df)
        st.write("Bar chart of product rating")
        draw.draw_bar(rating_df)
    with c2:
        device_sql = '''select device_name, count(device_name) as count_device_name
                        from purchase_history pe 
                        where "action" = 'checkout'
                        group by device_name;'''
        
        device_df = conn.query(device_sql)
        st.write("Bar chart of customer device")
        draw.draw_bar(device_df)
    with c3:
        agent_sql = '''select agent_name, count(agent_name) as count_agent_name
                        from purchase_history pe 
                        where "action" = 'checkout'
                        group by agent_name;'''
        
        agent_df = conn.query(agent_sql)
        st.write("Bar chart of customer agent")
        draw.draw_bar(agent_df)
    with c4:
        os_sql = '''select operating_system_name, count(operating_system_name) as count_os
                        from purchase_history pe 
                        where "action" = 'checkout'
                        group by operating_system_name;'''
        
        os_df = conn.query(os_sql)
        st.write("Bar chart of customer os")
        draw.draw_bar(os_df)

    hour_sql = '''select hour_of_day, "action", count(hour_of_day) as hour_count 
                    from purchase_history ph
                    group by hour_of_day, "action";'''
    
    hour_df = conn.query(hour_sql)
    # st.write(hour_df)
    # draw.draw_bar(hour_df, '#ffaa00')
    draw.draw_line(hour_df)
    # draw word cloud``
    # wordcloud_sql = '''select string_agg(search_text, ', ') as search_string 
                        # from search_event se ;'''
    # chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["col1", "col2", "col3"])
    # st.write(chart_data)    
    # word_df = conn.query(wordcloud_sql)

    # st.dataframe(word_df)
    # draw.draw_wordcloud(word_df)

    # hour_sql = '''select action, hour_of_day from product_event pe;'''
    # hour_df = conn.query(hour_sql)
    # draw.draw_hist(hour_df, "checkout")
    end_time = datetime.datetime.now()
    execution_time = (end_time - start_time).total_seconds()
    print(f"execution time of view segment detail visualization: {execution_time} s")

def delete_segment():
    seg_id = st.session_state["current_segment"]["segment_id"]
    conn = st.connection("segment", type="sql")

    with conn.session as s:
        s.execute(text("delete from segment_brand where segment_id = :seg_id;"), params=dict(seg_id=seg_id))
        s.execute(text("delete from segment_category where segment_id = :seg_id;"), params=dict(seg_id=seg_id))
        s.execute(text("delete from segment where segment_id = :seg_id;"), params=dict(seg_id=seg_id))

        s.commit()
        st.toast('Delete completed', icon="🚨")

def main_canva(segment_df):
    seg_id = st.session_state["current_segment"]["segment_id"]
    seg_name = st.session_state["current_segment"]["segment_name"]
    seg_gender = st.session_state["current_segment"]["gender"]
    seg_min_price = st.session_state["current_segment"]["min_price"]
    seg_max_price = st.session_state["current_segment"]["max_price"]
    seg_min_date = st.session_state["current_segment"]["min_date"]

    conn = st.connection("segment", type="sql")

    sql_brand = '''select brand_name from brand b
                    inner join segment_brand s on s.brand_id = b.brand_id
                    where s.segment_id = :s_id
                    '''
    sql_cate = '''select name from category c
                  inner join segment_category s on s.category_id = c.category_id
                  where s.segment_id = :s_id
                '''

    brand = conn.query(sql_brand, params=dict(s_id=seg_id))
    if len(brand) > 0:
        brand_list = list(brand.iloc[:, 0])
        st.session_state["current_brand_list"] = brand_list

    cate = conn.query(sql_cate, params=dict(s_id=seg_id))
    if len(cate) > 0:
        cate_list = list(cate.iloc[:, 0])
        st.session_state["current_cate_list"] = cate_list

    if True:
        with st.sidebar:
            segment_detail_df = pd.DataFrame(
                {
                "Fields": ["Gender", "Brands", "Categories", "Min price", "Max price", "Interaction date since"],
                "Value": [seg_gender, ", ".join(brand_list), ", ".join(cate_list), seg_min_price, seg_max_price, seg_min_date]
                }
            )
            st.data_editor(
                segment_detail_df,
                column_config={
                    "widgets": st.column_config.Column(
                        "Streamlit Widgets",
                        help="Streamlit **widget** commands 🎈",
                        width="medium",
                        required=True,
                    )
                },
                hide_index=True,
                num_rows="dynamic",
            )
            # st.table(segment_detail_df)

            st.button("Delete", on_click=delete_segment)
    
    tab1, tab2 = st.tabs(["Metrics", "Visulization"])

    with tab1:
        st.header("General metrics on customer segementation")
        view_segment_detail()
    with tab2:
        st.header("Segment data visulization")
        visulization_tab()

def list_segment():
    st.cache_data.clear()

    conn = st.connection("segment", type="sql")
    segment_df = conn.query("select * from segment;")

    n_segment = len(segment_df)
    # st.write(f"number of segment {n_segment}")
    # st.write(st.session_state)
    c1, c2 = st.columns([9, 1])
    with c1:
        segment_list_expander = st.expander("Segmnent list")

        if int(n_segment) > 0:
            segment_names = list(segment_df["segment_name"])
            pressed = []
            for i in range(n_segment):
                temp = segment_df.iloc[i]
                seg_id = temp["segment_id"]
                seg_name = temp["segment_name"]
                pressed_i = segment_list_expander.button(label=f"{seg_name}")
                pressed.append(pressed_i)
            if True in pressed:
                st.session_state["current_segment"] = segment_df.iloc[pressed.index(True, 0, n_segment)]
                main_canva(segment_df)
        else:
            st.write("There is no segment")
    with c2:
        clicked = st.button("Refresh")
        st.session_state['refreshed'] = clicked

list_segment()

if "refreshed" in st.session_state:
    # st.write(f"refresh clicked {st.session_state['refreshed']}")
    st.session_state['refreshed'] = False
    # st.write(f"refresh clicked {st.session_state['refreshed']}")
    st.cache_data.clear()
    # st.write("cache cleared")
    # list_segment()