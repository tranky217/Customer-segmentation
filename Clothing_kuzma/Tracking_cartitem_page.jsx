import { useDispatch } from "react-redux";
import { removeItem, updateCartAmount } from "../features/cart/cartSlice";
import { useState } from "react";
import { useEffect } from "react";
import { toast } from "react-toastify";
import axios from "axios";
import { trackSelfDescribingEvent } from '@snowplow/browser-tracker';
import { newTracker } from "@snowplow/browser-tracker";
import { GeolocationPlugin, enableGeolocationContext } from '@snowplow/browser-plugin-geolocation';

let tracker = newTracker('sp5', 'http://34.49.68.53', {
  appId: 'webId',
  platform: 'web',
  cookieSameSite: 'Lax',
  contexts: {
    webPage: true
},
plugins: [ GeolocationPlugin() ]
});
enableGeolocationContext();


const CartItem = ({ cartItem }) => {
  const { id, title, price, image, amount, brandName, selectedSize } = cartItem;
  const [id_user] = useState(localStorage.getItem("id"));
  const dispatch = useDispatch();
  const [userData, setUserData] = useState();
  const getUserData = async () => {
    try {
      console.log("get user data");
      const response = await axios(`http://localhost:8080/user/${id_user}`);
      setUserData(response.data);
    } catch (error) {
      toast.error("Error: ", error.response);
    }
  };
  useEffect(() => { getUserData() }, []);

  return (
    <article
      key={id}
      className="mb-12 flex flex-col gap-y-4 sm:flex-row flex-wrap border-b border-base-300 pb-6 last:border-b-0"
    >
      {/* IMAGE */}
      <img
        src={`https://${image}`}
        alt={title}
        className="h-24 w-24 rounded-lg sm:h-32 sm:w-32 object-cover"
      />
      {/* INFO */}
      <div className="sm:ml-16 sm:w-48">
        {/* TITLE */}
        <h3 className="capitalize font-medium text-accent-content">{title}</h3>
        {/* COMPANY */}
        <h4 className="mt-2 capitalize text-sm text-accent-content">
          Brand: {brandName}
        </h4>
        <h4 className="mt-2 capitalize text-sm text-accent-content">
          Size: {selectedSize}
        </h4>
      </div>
      <div className="sm:ml-12">
        {/* AMOUNT */}
        <div className="form-control max-w-xs">
          <label htmlFor="amount" className="label p-0">
            <span className="label-text text-accent-content">Amount</span>
          </label>
          <input
            name="number"
            id="amount"
            className="mt-2 input input-bordered input-sm w-full max-w-xs text-accent-content"
            value={amount}
            onChange={(event) => dispatch(updateCartAmount({ id: id, amount: event.target.value }))}
          />
        </div>
        {/* REMOVE */}
        <button
          className="mt-2 link link-warning link-hover text-sm text-accent-content"
          onClick={() => {
            dispatch(removeItem(id))
            console.log("remove from cart")
            trackSelfDescribingEvent({
              event: {
                schema: 'iglu:kuzma/product_event/jsonschema/1-0-0',
                data: {
                  action: "remove",
                  target: "cart"
                }
              },
              context: [{
                schema: 'iglu:kuzma/product_entity/jsonschema/1-0-0',
                data: {
                  product_id: cartItem.id,
                  product_name: cartItem?.title,
                  isInStock: cartItem?.isInStock,
                  gender: cartItem?.gender,
                  category: cartItem?.category,
                  quantity: cartItem?.amount,
                  price: cartItem?.price,
                  size: cartItem?.selectedSize,
                  rating: cartItem?.rating,
                  totalReviews: cartItem?.totalReviews,
                  productionDate: cartItem?.productionDate,
                  brandName: cartItem?.brandName
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
            console.log("here is remove from cart")


          }}
        >
          remove
        </button>
      </div>

      {/* PRICE */}
      <p className="font-medium sm:ml-auto text-accent-content">${(price * amount).toFixed(2)}</p>
    </article>
  );
};

export default CartItem;
