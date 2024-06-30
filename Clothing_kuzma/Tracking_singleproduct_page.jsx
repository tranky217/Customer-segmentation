import axios from "axios";
import React, { useState } from "react";
import {
  QuantityInput,
  SectionTitle,
  SelectSize,
  SingleProductRating,
  SingleProductReviews,
} from "../components";
import { FaHeart } from "react-icons/fa6";
import { FaCartShopping } from "react-icons/fa6";

import { Link, useLoaderData } from "react-router-dom";
import parse from "html-react-parser";
import { nanoid } from "nanoid";
import { useDispatch, useSelector } from "react-redux";
import { addToCart } from "../features/cart/cartSlice";
import {
  updateWishlist,
  removeFromWishlist,
} from "../features/wishlist/wishlistSlice";
import { toast } from "react-toastify";
import { store } from "../store";
import { trackSelfDescribingEvent } from '@snowplow/browser-tracker';
import { useEffect } from "react";
import { newTracker } from "@snowplow/browser-tracker";
import { GeolocationPlugin, enableGeolocationContext } from '@snowplow/browser-plugin-geolocation';

let tracker = newTracker('sp2', 'http://34.128.150.152', {
  appId: 'webId',
  platform: 'web',
  cookieSameSite: 'Lax',
  contexts: {
    webPage: true
},
plugins: [ GeolocationPlugin() ]
});
enableGeolocationContext();

export const singleProductLoader = async ({ params }) => {
  const { id } = params;

  const response = await axios(`http://localhost:8080/products/${id}`);

  return { productData: response.data };
};

const SingleProduct = () => {
  const [id, setId] = useState(localStorage.getItem("id"));
  const [currentImage, setCurrentImage] = useState(0);
  const [quantity, setQuantity] = useState(1);
  const [size, setSize] = useState(0);
  const { wishItems } = useSelector((state) => state.wishlist);
  const { userId } = useSelector((state) => state.auth);
  const dispatch = useDispatch();
  const loginState = useSelector((state) => state.auth.isLoggedIn);
  const [rating, setRating] = useState([
    "empty star",
    "empty star",
    "empty star",
    "empty star",
    "empty star",
  ]);

  const { productData } = useLoaderData();

  const product = {
    id: productData?.id,
    title: productData?.name,
    image: productData?.imageUrl,
    rating: productData?.rating,
    price: productData?.price?.current?.value,
    brandName: productData?.brandName,
    amount: quantity,
    isInStock: productData?.isInStock,
    gender: productData?.gender,
    category: productData?.category,
    totalReviews: productData?.totalReviewCount,
    productionDate: productData?.productionDate?.substring(0, 10),
    selectedSize: size || productData?.availableSizes[0],
    isInWishList:
      wishItems.find((item) => item.id === productData?.id + size) !==
      undefined,
  };

  const [userData, setUserData] = useState()
  const getUserData = async () => {
    try {
      const response = await axios(`http://localhost:8080/user/${id}`);
      setUserData(response.data);
    } catch (error) {
      toast.error("Error: ", error.response);
    }
  };
  useEffect(() => { getUserData() }, []);
  // console.log("==============endd============")
  // console.log("is this missing?")
  // console.log(userData)
  // console.log(product)
  if (typeof userData !== 'undefined') {
    trackSelfDescribingEvent({
      event: {
        schema: 'iglu:kuzma/product_event/jsonschema/1-0-0',
        data: {
          action: "view",
          target: "none"
        }
      },
      context: [{
        schema: 'iglu:kuzma/product_entity/jsonschema/1-0-0',
        data: {
          product_id: product.id,
          product_name: product.title,
          isInStock: product.isInStock,
          gender: product.gender,
          category: product.category,
          quantity: product.amount,
          price: product.price,
          size: product.selectedSize,
          rating: product.rating,
          totalReviews: product.totalReviews,
          productionDate: product.productionDate,
          brandName: product.brandName
        }
      }
        ,
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
  }
  console.log("out of tracking view event")

  for (let i = 0; i < productData?.rating; i++) {
    rating[i] = "full star";
  }

  const addToWishlistHandler = async (product) => {
    try {
      const getResponse = await axios.get(
        `http://localhost:8080/user/${localStorage.getItem("id")}`
      );
      const userObj = getResponse.data;


      userObj.userWishlist = userObj.userWishlist || [];

      userObj.userWishlist.push(product);

      const postResponse = await axios.put(
        `http://localhost:8080/user/${localStorage.getItem("id")}`,
        userObj
      );


      store.dispatch(updateWishlist({ userObj }));
      toast.success("Product added to the wishlist!");

      trackSelfDescribingEvent({
        event: {
          schema: 'iglu:kuzma/product_event/jsonschema/1-0-0',
          data: {
            action: "add",
            target: "wishlist"
          }
        },
        context: [{
          schema: 'iglu:kuzma/product_entity/jsonschema/1-0-0',
          data: {
            product_id: productData.id,
            product_name: productData?.name,
            isInStock: productData?.isInStock,
            gender: productData?.gender,
            category: productData?.category,
            quantity: 0,
            price: productData?.price?.current?.value,
            size: product?.selectedSize,
            rating: productData?.rating,
            totalReviews: productData?.totalReviewCount,
            productionDate: productData?.productionDate?.substring(0, 10),
            brandName: productData?.brandName
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
      console.log("end of adding to wish list");

    } catch (error) {
      console.error(error);
    }
  };

  const removeFromWishlistHandler = async (product) => {
    const getResponse = await axios.get(
      `http://localhost:8080/user/${localStorage.getItem("id")}`
    );
    const userObj = getResponse.data;

    userObj.userWishlist = userObj.userWishlist || [];

    const newWishlist = userObj.userWishlist.filter(
      (item) => product.id !== item.id
    );

    userObj.userWishlist = newWishlist;

    const postResponse = await axios.put(
      `http://localhost:8080/user/${localStorage.getItem("id")}`,
      userObj
    );


    store.dispatch(removeFromWishlist({ userObj }));
    toast.success("Product removed from the wishlist!");

    trackSelfDescribingEvent({
      event: {
        schema: 'iglu:kuzma/product_event/jsonschema/1-0-0',
        data: {
          action: "remove",
          target: "wishlist"
        }
      },
      context: [{
        schema: 'iglu:kuzma/product_entity/jsonschema/1-0-0',
        data: {
          product_id: productData.id,
          product_name: productData?.name,
          isInStock: productData?.isInStock,
          gender: productData?.gender,
          category: productData?.category,
          quantity: 0,
          price: productData?.price?.current?.value,
          size: product?.selectedSize,
          rating: productData?.rating,
          totalReviews: productData?.totalReviewCount,
          productionDate: productData?.productionDate?.substring(0, 10),
          brandName: productData?.brandName
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
    console.log("here is remove from wish list")

  };

  return (
    <>
      <SectionTitle title="Product page" path="Home | Shop | Product page" />
      <div className="grid grid-cols-2 max-w-7xl mx-auto mt-5 max-lg:grid-cols-1 max-lg:mx-5">
        <div className="product-images flex flex-col justify-center max-lg:justify-start">
          <img
            src={`https://${productData?.additionalImageUrls[currentImage]}`}
            className="w-96 text-center border border-gray-600 cursor-pointer"
            alt={productData.name}
          />
          <div className="other-product-images mt-1 grid grid-cols-3 w-96 gap-y-1 gap-x-2 max-sm:grid-cols-2 max-sm:w-64">
            {productData?.additionalImageUrls.map((imageObj, index) => (
              <img
                src={`https://${imageObj}`}
                key={nanoid()}
                onClick={() => setCurrentImage(index)}
                alt={productData.name}
                className="w-32 border border-gray-600 cursor-pointer"
              />
            ))}
          </div>
        </div>
        <div className="single-product-content flex flex-col gap-y-5 max-lg:mt-2">
          <h2 className="text-5xl max-sm:text-3xl text-accent-content">
            {productData?.name}
          </h2>
          <SingleProductRating rating={rating} productData={productData} />
          <p className="text-3xl text-error">
            ${productData?.price?.current?.value}
          </p>
          <div className="text-xl max-sm:text-lg text-accent-content">
            {parse(productData?.description)}
          </div>
          <div className="text-2xl">
            <SelectSize
              sizeList={productData?.availableSizes}
              size={size}
              setSize={setSize}
            />
          </div>
          <div>
            <label htmlFor="Quantity" className="sr-only">
              {" "}
              Quantity{" "}
            </label>

            <div className="flex items-center gap-1">
              <QuantityInput quantity={quantity} setQuantity={setQuantity} />
            </div>
          </div>
          <div className="flex flex-row gap-x-2 max-sm:flex-col max-sm:gap-x">
            <button
              className="btn bg-blue-600 hover:bg-blue-500 text-white"
              onClick={() => {
                // console.log(product)
                if (loginState) {
                  dispatch(addToCart(product));
                  trackSelfDescribingEvent({
                    event: {
                      schema: 'iglu:kuzma/product_event/jsonschema/1-0-0',
                      data: {
                        action: "add",
                        target: "cart"
                      }
                    },
                    context: [{
                      schema: 'iglu:kuzma/product_entity/jsonschema/1-0-0',
                      data: {
                        product_id: product.id,
                        product_name: product?.title,
                        isInStock: product?.isInStock,
                        gender: product?.gender,
                        category: product?.category,
                        quantity: product?.amount,
                        price: product?.price,
                        size: product?.selectedSize,
                        rating: product?.rating,
                        totalReviews: product?.totalReviews,
                        productionDate: product?.productionDate,
                        brandName: product?.brandName
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
                  console.log("here is add to cart")

                } else {
                  toast.error(
                    "You must be logged in to add products to the cart"
                  );
                }
              }}
            >
              <FaCartShopping className="text-xl mr-1" />
              Add to cart
            </button>

            {product?.isInWishList ? (
              <button
                className="btn bg-blue-600 hover:bg-blue-500 text-white"
                onClick={() => {
                  if (loginState) {
                    removeFromWishlistHandler(product);
                  } else {
                    toast.error(
                      "You must be logged in to remove products from the wishlist"
                    );
                  }
                }}
              >
                <FaHeart className="text-xl mr-1" />
                Remove from wishlist
              </button>
            ) : (
              <button
                className="btn bg-blue-600 hover:bg-blue-500 text-white"
                onClick={() => {
                  if (loginState) {
                    addToWishlistHandler(product);
                  } else {
                    toast.error(
                      "You must be logged in to add products to the wishlist"
                    );
                  }
                }}
              >
                <FaHeart className="text-xl mr-1" />
                Add to wishlist
              </button>
            )}
          </div>
          <div className="other-product-info flex flex-col gap-x-2">
            <div className="badge bg-gray-700 badge-lg font-bold text-white p-5 mt-2">
              Brand: {productData?.brandName}
            </div>
            <div className="badge bg-gray-700 badge-lg font-bold text-white p-5 mt-2">
              Gender: {productData?.gender}
            </div>
            <div
              className={
                productData?.isInStock
                  ? "badge bg-gray-700 badge-lg font-bold text-white p-5 mt-2"
                  : "badge bg-gray-700 badge-lg font-bold text-white p-5 mt-2"
              }
            >
              In Stock: {productData?.isInStock ? "Yes" : "No"}
            </div>
            <div className="badge bg-gray-700 badge-lg font-bold text-white p-5 mt-2">
              SKU: {productData?.productCode}
            </div>
            <div className="badge bg-gray-700 badge-lg font-bold text-white p-5 mt-2">
              Category: {productData?.category}
            </div>
            <div className="badge bg-gray-700 badge-lg font-bold text-white p-5 mt-2">
              Production Date:{" "}
              {productData?.productionDate?.substring(0, 10)}
            </div>
          </div>
        </div>
      </div>

      <SingleProductReviews rating={rating} productData={productData} />
    </>
  );
};

export default SingleProduct;
