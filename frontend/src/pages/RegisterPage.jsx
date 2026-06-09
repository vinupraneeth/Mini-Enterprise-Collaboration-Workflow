import {
  useEffect,
  useState
} from "react";

import {
  useNavigate
} from "react-router-dom";

import api from "../api/axios";


function RegisterPage() {

  const [name, setName] =
    useState("");

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [role, setRole] =
    useState("employee");

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


  const handleGoogleRegister = () => {

    window.location.href =
      `${api.defaults.baseURL}/auth/google`;
  };


  const handleRegister = async (
    event
  ) => {

    event.preventDefault();

    setLoading(true);

    try {

      await api.post(

        "/auth/register",

        {
          name,
          email,
          password,
          role
        }
      );

      alert(
        "Registration successful"
      );

      navigate("/");

    } catch (error) {

      console.error(error);

      alert(
        "Registration failed"
      );

    } finally {

      setLoading(false);
    }
  };


  return (

    <div className="min-h-screen flex bg-slate-100">

      <div className="hidden md:flex w-1/2 bg-slate-900 text-white items-center justify-center p-10">

        <div className="max-w-md">

          <h1 className="text-5xl font-bold mb-6">
            Team Collaboration
          </h1>

          <p className="text-lg text-slate-300 leading-8">

            Create users,
            manage enterprise workflows,
            collaborate with teams
            and streamline
            productivity securely.

          </p>

        </div>

      </div>

      <div className="w-full md:w-1/2 flex justify-center items-center bg-slate-100 px-6 py-8">

        <div className="w-full max-w-[420px] bg-white border border-slate-200 shadow-sm rounded-2xl p-10">

          <div className="mb-8 text-center">

            <h2 className="text-3xl font-bold text-slate-900">
              Create Account
            </h2>

            <p className="text-slate-500 mt-2">
              Register new user
            </p>

          </div>

          <form
            onSubmit={handleRegister}
            className="space-y-5"
          >

            <div>

              <label className="block text-sm font-medium text-slate-700 mb-2">
                Name
              </label>

              <input
                type="text"
                placeholder="Enter name"
                value={name}
                onChange={(e) =>
                  setName(
                    e.target.value
                  )
                }
                className="w-full border border-slate-300 rounded-lg px-4 py-3 outline-none focus:border-slate-500 focus:ring-2 focus:ring-slate-200"
                required
              />

            </div>

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

            <div>

              <label className="block text-sm font-medium text-slate-700 mb-2">
                Role
              </label>

              <select
                value={role}
                onChange={(e) =>
                  setRole(
                    e.target.value
                  )
                }
                className="w-full border border-slate-300 rounded-lg px-4 py-3 outline-none focus:border-slate-500 focus:ring-2 focus:ring-slate-200"
              >

                <option value="employee">
                  Employee
                </option>

                <option value="manager">
                  Manager
                </option>

                <option value="admin">
                  Admin
                </option>

              </select>

            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-slate-900 hover:bg-slate-800 text-white py-3 rounded-lg font-semibold transition"
            >

              {
                loading
                ?
                "Registering..."
                :
                "Register"
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
              onClick={handleGoogleRegister}
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

            Already have an account?

            {" "}

            <span
              onClick={() =>
                navigate("/")
              }
              className="text-slate-900 font-semibold cursor-pointer hover:underline"
            >
              Login
            </span>

          </div>

        </div>

      </div>

    </div>
  );
}

export default RegisterPage;
