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

  const [googleConfigured, setGoogleConfigured] =
    useState(false);

  const navigate = useNavigate();


  useEffect(() => {

    const token = localStorage.getItem(
      "token"
    );

    if (token) {

      navigate("/dashboard");
    }

    fetchGoogleStatus();

  }, []);


  const fetchGoogleStatus = async () => {

    try {

      const response = await api.get(
        "/auth/google/status"
      );

      setGoogleConfigured(
        response.data.configured
      );

    } catch (error) {

      console.error(error);
    }
  };


  const handleGoogleLogin = () => {

    window.location.href =
      `${api.defaults.baseURL}/auth/google`;
  };


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

        "refresh_token",

        response.data.refresh_token
      );
      
      localStorage.setItem(

        "user",

        JSON.stringify({

          id: response.data.id,

          name: response.data.name,

          email: email,

          role: response.data.role
        })
      )  

      navigate("/dashboard");

    } catch (error) {

      console.error(error);

      alert("Invalid credentials");

    } finally {

      setLoading(false);
    }
  };


  return (

    <div className="min-h-screen flex bg-slate-100">

      <div className="hidden md:flex w-1/2 bg-slate-900 text-white items-center justify-center p-10">

        <div className="max-w-md">

          <h1 className="text-5xl font-bold mb-6">
            Enterprise Workflow
          </h1>

          <p className="text-lg text-slate-300 leading-8">

            Manage tasks,
            collaborate with teams,
            assign work efficiently
            and track workflow
            progress securely.

          </p>

        </div>

      </div>

      <div className="w-full md:w-1/2 flex justify-center items-center bg-slate-100 px-6">

        <div className="w-full max-w-[420px] bg-white border border-slate-200 shadow-sm rounded-2xl p-10">

          <div className="mb-8 text-center">

            <h2 className="text-3xl font-bold text-slate-900">
              Welcome Back
            </h2>

            <p className="text-slate-500 mt-2">
              Login to continue
            </p>

          </div>

          <form
            onSubmit={handleLogin}
            className="space-y-5"
          >

            <div>

              <label className="block text-sm font-medium text-slate-700 mb-2">
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
                className="w-full border border-slate-300 rounded-lg px-4 py-3 outline-none focus:border-slate-500 focus:ring-2 focus:ring-slate-200"
                required
              />

            </div>

            <div>

              <label className="block text-sm font-medium text-slate-700 mb-2">
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
                className="w-full border border-slate-300 rounded-lg px-4 py-3 outline-none focus:border-slate-500 focus:ring-2 focus:ring-slate-200"
                required
              />

            </div>

            <div className="text-right">

              <button
                type="button"
                onClick={() =>
                  navigate("/forgot-password")
                }
                className="text-sm text-slate-900 font-semibold hover:underline"
              >
                Forgot password?
              </button>

            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-slate-900 hover:bg-slate-800 text-white py-3 rounded-lg font-semibold transition"
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

          <div className="mt-5">

            <div className="flex items-center gap-3 mb-5">

              <div className="h-px bg-slate-200 flex-1" />

              <span className="text-xs uppercase text-slate-400 font-semibold">
                or
              </span>

              <div className="h-px bg-slate-200 flex-1" />

            </div>

            <button
              type="button"
              onClick={handleGoogleLogin}
              disabled={!googleConfigured}
              className={`w-full border py-3 rounded-lg font-semibold transition ${
                googleConfigured
                  ? "border-slate-300 text-slate-800 hover:bg-slate-50"
                  : "border-slate-200 text-slate-400 bg-slate-50 cursor-not-allowed"
              }`}
            >
              Continue with Google
            </button>

            {!googleConfigured && (

              <p className="text-xs text-slate-500 text-center mt-3 leading-5">
                Google OAuth requires credentials in backend environment settings.
              </p>
            )}

          </div>

          <div className="mt-6 text-center text-slate-600">

            Don't have an account?

            {" "}

            <span
              onClick={() =>
                navigate("/register")
              }
              className="text-slate-900 font-semibold cursor-pointer hover:underline"
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
