import axios from "axios";
import { jwtDecode } from "jwt-decode";
import dayjs from "dayjs";

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

axiosInstance.interceptors.request.use(async(req) => {
  const token = localStorage.getItem("access");
  const refresh = localStorage.getItem("refresh") 
  if (token) {
    const decoded = jwtDecode(JSON.parse(token))
    const isExpired = dayjs.unix(decoded.exp as number).diff(dayjs()) < 1
    if(isExpired){
      //@ts-ignore
      const res = await axios.post(`${import.meta.env.VITE_BACKEND_API_URL}/auth/token/refresh/`,{refresh:JSON.parse(refresh)})
      if(res.status === 200){
        const data = res.data
        req.headers["Authorization"] = `Bearer ${data.access}`
        
        localStorage.setItem("access",JSON.stringify(data.access))
        return req
      } else {
        //@ts-ignore
        const res = await axios.post(`${import.meta.env.VITE_BACKEND_API_URL}/auth/logout/`,{refresh:JSON.parse(refresh)})
        if(res.status == 200){

          localStorage.clear()
          window.location.href = '/login'
        } 
      }
    } else{

      req.headers["Authorization"] = `Bearer ${JSON.parse(token)}`;
    }
  }
  return req;
});



export default axiosInstance;
