import {
  useEffect,
  useState
} from "react";

import {
  useNavigate
} from "react-router-dom";

import api from "../api/axios";


function LoginPage() {

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const navigate = useNavigate();


  useEffect(() => {

    const token = localStorage.getItem(
      "token"
    );

    if (token) {

      navigate("/dashboard");
    }

  }, []);


  const handleLogin = async (
    event
  ) => {

    event.preventDefault();

    setLoading(true);

    try {

      const formData =
        new URLSearchParams();

      formData.append(
        "username",
        email
      );

      formData.append(
        "password",
        password
      );

      const response = await api.post(

        "/auth/login",

        formData,

        {
          headers: {
            "Content-Type":
              "application/x-www-form-urlencoded"
          }
        }
      );

      localStorage.setItem(

        "token",

        response.data.access_token
      );
      
      localStorage.setItem(

        "user",

        JSON.stringify({

          name: response.data.name,

          email: email,

          role: response.data.role
        })
      )  

      navigate("/dashboard");

    } catch (error) {

      console.log(error);

      alert("Invalid credentials");

    } finally {

      setLoading(false);
    }
  };


  return (

    <div className="min-h-screen flex">

      <div className="hidden md:flex w-1/2 bg-gradient-to-br from-emerald-600 via-teal-700 to-cyan-900 text-white items-center justify-center p-10">

        <div>

          <h1 className="text-5xl font-bold mb-6">
            Enterprise Workflow
          </h1>

          <p className="text-lg text-gray-200 leading-8">

            Manage tasks,
            collaborate with teams,
            assign work efficiently
            and track workflow
            progress securely.

          </p>

        </div>

      </div>

      <div className="w-full md:w-1/2 flex justify-center items-center bg-gray-100">

        <div className="w-[420px] bg-white shadow-2xl rounded-2xl p-10">

          <div className="mb-8 text-center">

            <h2 className="text-3xl font-bold text-gray-800">
              Welcome Back
            </h2>

            <p className="text-gray-500 mt-2">
              Login to continue
            </p>

          </div>

          <form
            onSubmit={handleLogin}
            className="space-y-5"
          >

            <div>

              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email
              </label>

              <input
                type="email"
                placeholder="Enter email"
                value={email}
                onChange={(e) =>
                  setEmail(
                    e.target.value
                  )
                }
                className="w-full border border-gray-300 rounded-lg px-4 py-3 outline-none focus:border-blue-500"
                required
              />

            </div>

            <div>

              <label className="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>

              <input
                type="password"
                placeholder="Enter password"
                value={password}
                onChange={(e) =>
                  setPassword(
                    e.target.value
                  )
                }
                className="w-full border border-gray-300 rounded-lg px-4 py-3 outline-none focus:border-blue-500"
                required
              />

            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-semibold transition"
            >

              {
                loading
                ?
                "Logging in..."
                :
                "Login"
              }

            </button>

          </form>

          <div className="mt-6 text-center text-gray-600">

            Don't have an account?

            {" "}

            <span
              onClick={() =>
                navigate("/register")
              }
              className="text-blue-600 font-semibold cursor-pointer hover:underline"
            >
              Register
            </span>

          </div>

        </div>

      </div>

    </div>
  );
}

export default LoginPage;