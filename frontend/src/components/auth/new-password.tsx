import { useEffect, useState } from "react";
import toast from "react-hot-toast";

import axiosInstance from "../../utils/axiosInstance";
import { useNavigate, useParams } from "react-router-dom";


const NewPassword = ({ pageTitle }: { pageTitle?: string }) => {
  const navigate = useNavigate();
  const {uidb64,token} = useParams()
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState({
    password: "",

    password2: "",
  });

 


  useEffect(() => {
    if (pageTitle) {
      document.title = pageTitle;
    }
  }, [pageTitle]);

  const handleOnChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleOnSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const { password2, password } = formData;
    if (!password2 || !password) {
      toast.error("All fields are required!");
      return;
    }
    if(password !== password2){
      toast.error("Passwords do not match.")
      return;
    }

    try {
      setIsLoading(true);
      const res = await axiosInstance.patch("/auth/reset/set-new-password/", {...formData,uidb64,token});
    
      if (res.status === 200) {
       
        toast.success("Reset password successfully");
       
       
        navigate("/login");
      }
    } catch (error) {
      console.log(error);
      //@ts-ignore
      toast.error(error.response.data.detail ||  error?.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen min-w-screen bg-slate-50">
      <div className="w-full h-full flex justify-center items-center">
        <div className="mt-10 max-w-lg w-full p-6 shadow-md bg-white rounded-md">
          <h1 className="text-center font-bold text-3xl">Set New Password</h1>
          <div className="py-4 px-2">
            <form className="space-y-4" onSubmit={handleOnSubmit}>
              <div className="flex flex-col gap-2">
                <label htmlFor="" className="text-lg font-semibold">
                  Password
                </label>
                <input
                  type="text"
                  name="password"
                  placeholder="Enter your new password"
                  className="py-4 px-2 focus:outline-blue-200 border border-gray-400 focus:ring-2 ring-cyan-200 rounded-md w-full"
                  onChange={handleOnChange}
                  value={formData.password}
                />
              </div>

              <div className="flex flex-col gap-2">
                <label htmlFor="" className="text-lg font-semibold">
                 Confirm Password
                </label>
                <input
                  type="text"
                  name="password2"
                  placeholder="Confirm Password"
                  className="py-4 px-2 focus:outline-blue-200 border border-gray-400 focus:ring-2 ring-cyan-200 rounded-md w-full"
                  onChange={handleOnChange}
                  value={formData.password2}
                />
              </div>
             
              <div className="w-full flex flex-row items-center">
                <button
                  type="submit"
                  className="px-6 w-full py-2 rounded-lg text-white bg-blue-500 cursor-pointer hover:bg-blue-600 disabled:cursor-not-allowed"
                  disabled={isLoading}
                >
                  Set New Password
                </button>
               
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NewPassword;
