import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Login, NewPassword, Reset, Signup, VerifyEmail } from "./components/auth";
import Home from "./components/Home";

function App() {
  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route
            path="/register"
            element={<Signup pageTitle="Create an account" />}
          />
          <Route
            path="/verify-email"
            element={<VerifyEmail pageTitle="Verify your account" />}
          />
          <Route
            path="/login"
            element={<Login pageTitle="Log in to your account." />}
          />
          
          <Route path="/reset" element={<Reset pageTitle="Reset password"/>}/>
          <Route path="/auth/:uidb64/:token" element={<NewPassword pageTitle="Set New Password"/>}/>
        </Routes>
      </Router>
    </>
  );
}

export default App;
