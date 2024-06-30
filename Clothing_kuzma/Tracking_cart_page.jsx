import React from 'react'
import { CartItemsList, CartTotals, SectionTitle } from '../components'
import { Link, useNavigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { toast } from 'react-toastify';
import { useState } from "react";
import { useEffect } from "react";
import axios from "axios";
import { trackSelfDescribingEvent } from '@snowplow/browser-tracker';
import { newTracker } from "@snowplow/browser-tracker";
import { GeolocationPlugin, enableGeolocationContext } from '@snowplow/browser-plugin-geolocation';

let tracker = newTracker('sp4', 'http://34.128.150.152', {
  appId: 'webId',
  platform: 'web',
  cookieSameSite: 'Lax',
  contexts: {
    webPage: true
},
plugins: [ GeolocationPlugin() ]
});
enableGeolocationContext();

const Cart = () => {

  const navigate = useNavigate();
  const loginState = useSelector((state) => state.auth.isLoggedIn);
  const { cartItems } = useSelector((state) => state.cart);
  const [id_user] = useState(localStorage.getItem("id"));
  const [userData, setUserData] = useState();
  // console.log(id_user);
  const getUserData = async () => {
    try {
      // console.log("get user data");
      const response = await axios(`http://localhost:8080/user/${id_user}`);
      setUserData(response.data);
    } catch (error) {
      toast.error("Error: ", error.response);
    }
  };
  useEffect(() => { getUserData() }, []);
  
  const isCartEmpty = () => {
    if (cartItems.length === 0) {
      toast.error("Your cart is empty");
    } else {
      for (let i = 0; i < cartItems.length; i++) {
        trackSelfDescribingEvent({
          event: {
            schema: 'iglu:kuzma/product_event/jsonschema/1-0-0',
            data: {
              action: "checkout",
              target: "cart"
            }
          },
          context: [{
            schema: 'iglu:kuzma/product_entity/jsonschema/1-0-0',
            data: {
              product_id: cartItems[i].id,
              product_name: cartItems[i]?.title,
              isInStock: cartItems[i]?.isInStock,
              gender: cartItems[i]?.gender,
              category: cartItems[i]?.category,
              quantity: cartItems[i]?.amount,
              price: cartItems[i]?.price,
              size: cartItems[i]?.selectedSize,
              rating: cartItems[i]?.rating,
              totalReviews: cartItems[i]?.totalReviews,
              productionDate: cartItems[i]?.productionDate,
              brandName: cartItems[i]?.brandName
            }
          },
          {
            schema: 'iglu:kuzma/user_entity/jsonschema/1-0-0',
            data: {
              user_id: userData?.id,
              user_name: userData?.name,
              user_lastName: userData?.lastname,
              email: userData?.email,
              address: userData?.adress,
              phone: userData?.phone
            }
          }
          ]
        });
        console.log("here is checkout from cart")
      }
      navigate("/thank-you");
    }
  }

  return (
    <>
      <SectionTitle title="Cart" path="Home | Cart" />
      <div className='mt-8 grid gap-8 lg:grid-cols-12 max-w-7xl mx-auto px-10'>
        <div className='lg:col-span-8'>
          <CartItemsList />
        </div>
        <div className='lg:col-span-4 lg:pl-4'>
          <CartTotals />
          {loginState ? (
            <button onClick={isCartEmpty} className='btn bg-blue-600 hover:bg-blue-500 text-white btn-block mt-8'>
              order now
            </button>
          ) : (
            <Link to='/login' className='btn bg-blue-600 hover:bg-blue-500 btn-block text-white mt-8'>
              please login
            </Link>
          )}
        </div>
      </div>
    </>
  )
}

export default Cart