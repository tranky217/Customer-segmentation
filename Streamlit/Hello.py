import streamlit as st
import datetime
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from sqlalchemy.sql import text
import draw as draw
import query as query
import uuid
import time
# test pydeck
# import pandas as pd
# import numpy as np
# import pydeck as pdk

st.set_page_config(
    page_title="Customer Segmentation for Kuzma Clothing shop",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.title("Customer segmentation for Kuzma web clothing")

with open('./configs/credentials.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
    # print(config['cookie']['name'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)
print(authenticator.login())

if st.session_state["authentication_status"]:
    authenticator.logout()
    st.write(f'Welcome *{st.session_state["name"]}*')
    # st.title('Log in successfully')
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

# sidebar 
# segment customer by
# brand name
# category
# gender
# price range 
# interaction date

def segment_init():
    conn = st.connection("segment", type="sql")
    df = conn.query("select * from segment;", ttl="10m")
    n_segment = len(df)

    if n_segment > 0:    
        st.session_state["current_segment_id"] = int(df["segment_id"].max())
    else:
        st.session_state["current_segment_id"] = 0
        
def click_create(segment_name, brand_box, category_box, gender_box, price_slide, interaction_date):
    conn = st.connection("segment", type="sql")
    df = conn.query("select * from segment;")

    sql_name = 'select segment_name from segment;'
    name_df = conn.query(sql_name)
    name_list = list(name_df.iloc[:, 0])

    not_existed = (segment_name not in name_list)
    # st.write(not_existed)
    if not_existed:
        brand_df = conn.query("select * from brand")
        id = uuid.uuid1()
        current_id = id
        # for the next segment id
        with conn.session as s:
            s.execute(text('INSERT INTO public.segment (segment_id, segment_name, gender, min_price, max_price, min_date) VALUES (:id, :n, :g, :min_p, :max_p, :min_date);'), 
                    params=dict(id=current_id, n=segment_name, g=gender_box, min_p=price_slide[0],\
                                max_p=price_slide[1], min_date=interaction_date))
            if len(brand_box) > 0:
                for b in brand_box:
                    brand_id = conn.query("select brand_id from brand where brand_name = :b_n;", params=dict(b_n=b))
                    s.execute(text('INSERT INTO public.segment_brand (segment_id, brand_id) VALUES (:s_id, :b_id);'), params=dict(s_id=current_id, b_id=int(brand_id.iloc[0, 0])))
            if len(category_box) > 0: 
                for c in category_box:
                    cate_id = conn.query("select category_id from category where name = :cate_name;", params=dict(cate_name=c))
                    s.execute(text('INSERT INTO public.segment_category (segment_id, category_id) VALUES (:s_id, :c_id);'), params=dict(s_id=current_id, c_id=int(cate_id.iloc[0, 0])))
            s.commit()
            st.toast('Create completed', icon='🎉')
    else:
        st.toast('Segment name already existed', icon='⚠️')
        time.sleep(1)
        
def create_side_bar(): 
    with st.sidebar:    
        new_segment_expander = st.expander("Create new segment")
        segment_name = new_segment_expander.text_input("Name your segment")
        brand_box = new_segment_expander.multiselect("Brand Name", ("WALK LONDON",
                                                                    "Reebok", \
                                                                    "Nike", \
                                                                    "Jack & Jones",\
                                                                    "Crocs",\
                                                                    "Vans",\
                                                                    "Puma",\
                                                                    "New Balance",\
                                                                    "Tommy Jeans",\
                                                                    "Tommy Hilfiger",\
                                                                    "Bershka",\
                                                                    "New Look",\
                                                                    "AllSaints",\
                                                                    "Columbia",\
                                                                    "The North Face",\
                                                                    "Collusion",\
                                                                    "ASOS DESIGN",\
                                                                    "Topman",\
                                                                    "Dr Denim",\
                                                                    "Polo Ralph Lauren",\
                                                                    "ASOS Dark Future",\
                                                                    "Levi's",\
                                                                    "Threadbare",\
                                                                    "Calvin Klein",\
                                                                    "AAPE BY A BATHING APE®",\
                                                                    "Good For Nothing",\
                                                                    "Timberland",\
                                                                    "Pull and Bear",\
                                                                    "Koi Footwear",\
                                                                    "adidas performance",\
                                                                    "Nike Running",\
                                                                    "Dr Martens",\
                                                                    "River Island"))
        category_box = new_segment_expander.multiselect("Category", ("shoes",
                                                                    "slippers", \
                                                                    "heels", \
                                                                    "t-shirts", \
                                                                    "jackets", \
                                                                    "caps",\
                                                                    "shorts",\
                                                                    "sweaters",\
                                                                    "sneakers",\
                                                                    "shirts",\
                                                                    "boots",\
                                                                    "overshirts",\
                                                                    "pants",\
                                                                    "jeans",\
                                                                    "socks",\
                                                                    "belts",\
                                                                    "trainers"))
        gender_box = new_segment_expander.selectbox("Gender", ("Female", "Male"))

        price_slide = new_segment_expander.slider("Product price range", 0, 2000, (0, 1000))

        today = datetime.datetime.now()
        last_year = today.year - 2
        jan_1 = datetime.date(last_year, 1, 1)  
        dec_31 = datetime.date(today.year, 12, 31)

        interaction_date = new_segment_expander.date_input("Interaction Since", datetime.date(2022, 1, 1))
        
        # if "current_segment_id" in st.session_state:
        #     current_id = st.session_state["current_segment_id"]
        # else:
        #     current_id = 0
        if len(segment_name) == 0:
            st.toast("Segment name must not be empty", icon="⚠️")
        else:
            create_segment = new_segment_expander.button(label="Create Segment", on_click=click_create, args=(segment_name, brand_box, category_box, gender_box, price_slide, interaction_date))

if st.session_state["authentication_status"]:
    # segment_init()s
    # list_side_bar()
    create_side_bar()
    # draw.draw_map()