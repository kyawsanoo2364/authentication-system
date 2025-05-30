import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import axiosInstance from "../../utils/axiosInstance";
import { useNavigate } from "react-router-dom";

const VerifyEmail = ({ pageTitle }: { pageTitle?: string }) => {
  useEffect(() => {
    if (pageTitle) {
      document.title = pageTitle;
    }
  }, [pageTitle]);
  const [code, setCode] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleOnSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!code) {
      toast.error("Code is requierd!");
      return;
    }
    try {
      setIsLoading(true);
      const res = await axiosInstance.post("/auth/verify/", { code });

      if (res.status === 200) {
        toast.success("Verified your email.");
        navigate("/login");
      }
    } catch (error) {
      console.log(error);
      toast.error(error.response.data.non_field_errors[0] || error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen min-w-screen bg-slate-50">
      <div className="w-full h-full flex justify-center items-center">
        <div className="mt-10 max-w-lg w-full p-6 shadow-md bg-white rounded-md">
          <h1 className="text-center font-bold text-3xl">
            Verify your account
          </h1>
          <div className="py-4 px-2">
            <form className="space-y-4" onSubmit={handleOnSubmit}>
              <div className="flex flex-col gap-2">
                <label htmlFor="" className="text-lg font-semibold">
                  Code
                </label>
                <input
                  type="number"
                  name="code"
                  placeholder="Enter your otp code "
                  className="py-4 px-2 focus:outline-blue-200 border border-gray-400 focus:ring-2 ring-cyan-200 rounded-md w-full"
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                />
              </div>

              <button
                type="submit"
                className="px-6 py-2 rounded-lg text-white bg-blue-500 cursor-pointer hover:bg-blue-600 w-full disabled:cursor-not-allowed"
                disabled={isLoading}
              >
                Send
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VerifyEmail;
