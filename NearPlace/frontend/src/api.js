import axios from "axios";

const baseUrl = process.env.API_URL || "http://35.189.64.107/api/";
// const baseUrl = process.env.API_URL || "http://127.0.0.1:8000/api/";
axios.defaults.baseURL = baseUrl;

// get nearby bar
export const getNearbyPlaceApi = (category, lat, lng) =>
  axios.get(`places/?category=${category}&location=${lng},${lat}`);
