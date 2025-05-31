import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { Link } from "react-router-dom";
import axiosInstance from "../../utils/axiosInstance";
import { useNavigate } from "react-router-dom";
import { getUser } from "../../utils/user";
import { GoogleLogin, GoogleOAuthProvider } from "@react-oauth/google";


const Login = ({ pageTitle }: { pageTitle?: string }) => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState({
    email: "",

    password: "",
  });

  useEffect(() => {
    const user = getUser();
    if (user) {
      navigate("/");
    }
  }, []);

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

    const { email, password } = formData;
    if (!email || !password) {
      toast.error("All fields are required!");
      return;
    }

    try {
      setIsLoading(true);
      const res = await axiosInstance.post("/auth/login/", formData);
      const data = res.data.data;
      if (res.status === 200) {
        toast.success("Login successfully.");
        const user = {
          email: data.email,
          name: data.full_name,
        };
        localStorage.setItem("user", JSON.stringify(user));
        localStorage.setItem("access", JSON.stringify(data.access));
        localStorage.setItem("refresh", JSON.stringify(data.refresh));
        navigate("/");
      }
    } catch (error) {
      console.log(error);
      //@ts-ignore
      toast.error(error.response.data.detail || error?.message);
    } finally {
      setIsLoading(false);
    }
  };

  const LoginWithGoogle = async (token: string | undefined) => {
    try {
      const res = await axiosInstance.post("/auth/google/", { token });
      const data = res.data.data;
      if (res.status === 200) {
        toast.success("Login successfully.");
        const user = {
          email: data.email,
          name: data.full_name,
        };
        localStorage.setItem("user", JSON.stringify(user));
        localStorage.setItem("access", JSON.stringify(data.access));
        localStorage.setItem("refresh", JSON.stringify(data.refresh));
        navigate("/");
      }
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <GoogleOAuthProvider clientId={import.meta.env.VITE_GOOGLE_CLIENT_ID}>
      <div className="min-h-screen min-w-screen bg-slate-50">
        <div className="w-full h-full flex justify-center items-center">
          <div className="mt-10 max-w-lg w-full p-6 shadow-md bg-white rounded-md">
            <h1 className="text-center font-bold text-3xl">Log In</h1>
            <div className="py-4 px-2">
              <form className="space-y-4" onSubmit={handleOnSubmit}>
                <div className=" flex flex-row justify-center items-center">
                  <GoogleLogin
                    size="large"
                    shape="circle"
                    onSuccess={(response) => {
                      const token = response.credential;
                      LoginWithGoogle(token);
                    }}
                    onError={() => {
                      console.log("Login failed");
                    }}
                  />
                </div>
                <div className="flex flex-col gap-2">
                  <label htmlFor="" className="text-lg font-semibold">
                    Email
                  </label>
                  <input
                    type="email"
                    name="email"
                    placeholder="Enter your email address"
                    className="py-4 px-2 focus:outline-blue-200 border border-gray-400 focus:ring-2 ring-cyan-200 rounded-md w-full"
                    onChange={handleOnChange}
                    value={formData.email}
                  />
                </div>

                <div className="flex flex-col gap-2">
                  <label htmlFor="" className="text-lg font-semibold">
                    Password
                  </label>
                  <input
                    type="password"
                    name="password"
                    placeholder="******"
                    className="py-4 px-2 focus:outline-blue-200 border border-gray-400 focus:ring-2 ring-cyan-200 rounded-md w-full"
                    onChange={handleOnChange}
                    value={formData.password}
                  />
                </div>
                <div className="my-4">
                  <Link to={"/reset"} className="text-blue-500 hover:underline">
                    Forgot Password?
                  </Link>
                </div>
                <div className="w-full flex flex-row justify-between items-center">
                  <button
                    type="submit"
                    className="px-6 py-2 rounded-lg text-white bg-blue-500 cursor-pointer hover:bg-blue-600 disabled:cursor-not-allowed"
                    disabled={isLoading}
                  >
                    Log In
                  </button>
                  <span className="text-gray-500">
                    Haven't an account yet?{" "}
                    <Link
                      to={"/register"}
                      className="text-blue-500 hover:underline"
                    >
                      Register
                    </Link>
                  </span>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </GoogleOAuthProvider>
  );
};

export default Login;
