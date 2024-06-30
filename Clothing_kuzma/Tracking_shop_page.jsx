/* eslint-disable no-unused-vars */
import React, { useEffect, useState } from "react";
import {
  Filters,
  Pagination,
  ProductElement,
  SectionTitle,
} from "../components";
import "../styles/Shop.css";
import axios from "axios";
import { useLoaderData, useNavigate, useSearchParams } from "react-router-dom";
import { nanoid } from "nanoid";
import { trackSelfDescribingEvent } from '@snowplow/browser-tracker';
import { toast } from "react-toastify";
import { newTracker } from "@snowplow/browser-tracker";

let tracker = newTracker('sp3', 'http://34.128.150.152', {
  appId: 'webId',
  platform: 'web',
  cookieSameSite: 'Lax',
  contexts: {
    webPage: true
}
});

export const shopLoader = async ({ request }) => {
  const params = Object.fromEntries([
    ...new URL(request.url).searchParams.entries(),
  ]);
  // /posts?title=json-server&author=typicode
  // GET /posts?_sort=views&_order=asc
  // GET /posts/1/comments?_sort=votes&_order=asc

  let mydate = Date.parse(params.date);

  if (mydate && !isNaN(mydate)) {
    // The date is valid
    mydate = new Date(mydate).toISOString();
  } else {
    mydate = "";
  }

  const filterObj = {
    brand: params.brand ?? "all",
    category: params.category ?? "all",
    date: mydate ?? "",
    gender: params.gender ?? "all",
    order: params.order ?? "",
    price: params.price ?? "all",
    search: params.search ?? "",
    in_stock: params.stock === undefined ? false : true,
    current_page: Number(params.page) || 1
  };

  // set params in get apis
  let parameter = (`?_start=${(filterObj.current_page - 1) * 10}&_limit=10`) + // pre defined that limit of response is 10 & page number count 1
    (filterObj.brand !== 'all' ? `&brandName=${filterObj.brand}` : "") +
    (filterObj.category !== 'all' ? `&category=${filterObj.category}` : "") +
    (filterObj.gender !== 'all' ? `&gender=${filterObj.gender}` : ``) +
    ((filterObj.search != '') ? `&q=${encodeURIComponent(filterObj.search)}` : ``) +
    (filterObj.order ? `&_sort=price.current.value` : "") + // Check if the order exists, then sort it in ascending order. After that, the API response will be modified if descending order or any other filter is selected.
    (filterObj.in_stock ? (`&isInStock`) : '') +
    (filterObj.price !== 'all' ? `&price.current.value_lte=${filterObj.price}` : ``) +
    (filterObj.date ? `&productionDate=${filterObj.date}` : ``) // It only matched exact for the date and time. 

  try {
    const response = await axios(
      `http://localhost:8080/products${parameter}`

    );
    let data = response.data;

    // sorting in descending order
    if (filterObj.order && !(filterObj.order === "asc" || filterObj.order === "price low")) data.sort((a, b) => b.price.current.value - a.price.current.value)
    return { productsData: data, productsLength: data.length, page: filterObj.current_page, searchData: filterObj };
  } catch (error) {
    console.log(error.response);
  }
  // /posts?views_gte=10

  return null;
};




const Shop = () => {

  const productLoaderData = useLoaderData();
  const [id] = useState(localStorage.getItem("id"));
  const searchData = productLoaderData.searchData;
  // console.log("==================here is shop")
  // console.log(id)
  // console.log(productLoaderData)
  // console.log(searchData)
  // console.log(productLoaderData.productsLength)
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
  
  trackSelfDescribingEvent({
    event: {
      schema: 'iglu:kuzma/search_new_context/jsonschema/1-0-0',
      data: {
        brand: searchData.brand,
        category: searchData.category,
        gender: searchData.gender,
        max_price: parseInt(searchData.price),
        min_production_date: searchData.date,
        search_text: searchData.search,
        match_product: productLoaderData.productsLength
      }
    },
    context: [
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
  console.log("track search event ended")
  return (
    <>
      <SectionTitle title="Shop" path="Home | Shop" />
      <div className="max-w-7xl mx-auto mt-5">
        <Filters />
        {productLoaderData.productsData.length === 0 && <h2 className="text-accent-content text-center text-4xl my-10">No products found for this filter</h2>}
        <div className="grid grid-cols-4 px-2 gap-y-4 max-lg:grid-cols-3 max-md:grid-cols-2 max-sm:grid-cols-1 shop-products-grid">
          {productLoaderData.productsData.length !== 0 &&
            productLoaderData.productsData.map((product) => (
              <ProductElement
                key={nanoid()}
                id={product.id}
                title={product.name}
                image={product.imageUrl}
                rating={product.rating}
                price={product.price.current.value}
                brandName={product.brandName}
              />
            ))}
        </div>
      </div>

      <Pagination />
    </>
  );
};

export default Shop;
