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

  const navigate = useNavigate();


  useEffect(() => {

    const token = localStorage.getItem(
      "token"
    );

    if (token) {

      navigate("/dashboard");
    }

  }, []);


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

      console.log(error);

      alert(
        "Registration failed"
      );

    } finally {

      setLoading(false);
    }
  };


  return (

    <div className="min-h-screen flex">

      <div className="hidden md:flex w-1/2 bg-gradient-to-br from-orange-500 via-rose-600 to-pink-800 text-white items-center justify-center p-10">

        <div>

          <h1 className="text-5xl font-bold mb-6">
            Team Collaboration
          </h1>

          <p className="text-lg text-gray-200 leading-8">

            Create users,
            manage enterprise workflows,
            collaborate with teams
            and streamline
            productivity securely.

          </p>

        </div>

      </div>

      <div className="w-full md:w-1/2 flex justify-center items-center bg-gray-100">

        <div className="w-[420px] bg-white shadow-2xl rounded-2xl p-10">

          <div className="mb-8 text-center">

            <h2 className="text-3xl font-bold text-gray-800">
              Create Account
            </h2>

            <p className="text-gray-500 mt-2">
              Register new user
            </p>

          </div>

          <form
            onSubmit={handleRegister}
            className="space-y-5"
          >

            <div>

              <label className="block text-sm font-medium text-gray-700 mb-2">
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
                className="w-full border border-gray-300 rounded-lg px-4 py-3 outline-none focus:border-purple-500"
                required
              />

            </div>

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
                className="w-full border border-gray-300 rounded-lg px-4 py-3 outline-none focus:border-purple-500"
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
                className="w-full border border-gray-300 rounded-lg px-4 py-3 outline-none focus:border-purple-500"
                required
              />

            </div>

            <div>

              <label className="block text-sm font-medium text-gray-700 mb-2">
                Role
              </label>

              <select
                value={role}
                onChange={(e) =>
                  setRole(
                    e.target.value
                  )
                }
                className="w-full border border-gray-300 rounded-lg px-4 py-3 outline-none focus:border-purple-500"
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
              className="w-full bg-purple-600 hover:bg-purple-700 text-white py-3 rounded-lg font-semibold transition"
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

          <div className="mt-6 text-center text-gray-600">

            Already have an account?

            {" "}

            <span
              onClick={() =>
                navigate("/")
              }
              className="text-purple-600 font-semibold cursor-pointer hover:underline"
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