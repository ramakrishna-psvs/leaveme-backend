import axios from "axios";

const API = axios.create({
  baseURL: "https://leaveme-backend-production.up.railway.app"
});

export default API;
