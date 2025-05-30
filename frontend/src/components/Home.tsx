
import { Link } from "react-router-dom"
import { getUser } from "../utils/user"
import { useEffect } from "react"
import axiosInstance from "../utils/axiosInstance"
import axios from "axios"
import toast from "react-hot-toast"


const Home = () => {
  const user = getUser()


  useEffect(()=>{
    document.title = "Home | My authentication"
    fetchData()
  },[])

  const fetchData = async()=>{
    try {
      const res = await axiosInstance.get("/auth/profile/")
      if(res.status === 200){
        console.log(res.data)
      }
    } catch (error) {
      console.log(error)
      console.log("Unauthenticated!")
    }
  }

  const handleLogout = async()=>{
    try {
        const refresh = localStorage.getItem("refresh")
        if(refresh){
          const res = await axiosInstance.post(`/auth/logout/`,{refresh:JSON.parse(refresh)})
          if(res.status == 200){
  
            localStorage.clear()
            window.location.href = '/login'
          } else{
            toast.error("Logout Failed")
          }
        }
    } catch (error) {
      console.log(error)
    }
  }

  return (
    <div className="min-h-screen min-w-screen bg-slate-100">
      <div className="w-full h-full flex items-center justify-center">
          <div className="my-32">
            <h1 className="text-3xl font-bold">{user? `Hello, ${user.name}` : "Welcome to my authentication."}</h1>
            <div className="mt-6 gap-6 flex items-center justify-center">
              {user? <button className="px-4 py-2 rounded-md text-white bg-red-500 cursor-pointer hover:bg-red-600" onClick={handleLogout}>Logout</button>:(<>
              <Link to={'/login'} className="px-4 py-2 rounded-md text-white bg-green-500 cursor-pointer hover:bg-green-600">Login</Link>
                <Link to={"/register"} className="px-4 py-2 rounded-md text-white bg-green-500 cursor-pointer hover:bg-green-600">Register</Link>
              </>)}
            </div>
          </div>
      </div>
    </div>
  )
}

export default Home