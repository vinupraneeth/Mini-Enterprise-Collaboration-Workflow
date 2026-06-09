import {
  useState
} from "react";

import {
  useLocation,
  useNavigate
} from "react-router-dom";

import api from "../api/axios";


function ResetPasswordPage() {

  const location = useLocation();

  const navigate = useNavigate();

  const [token, setToken] =
    useState(
      location.state?.resetToken || ""
    );

  const [newPassword, setNewPassword] =
    useState("");

  const [loading, setLoading] =
    useState(false);


  const handleResetPassword = async (
    event
  ) => {

    event.preventDefault();

    setLoading(true);

    try {

      const response = await api.post(

        "/auth/password-reset/confirm",

        {
          token,
          new_password: newPassword
        }
      );

      alert(
        response.data.message
      );

      navigate("/");

    } catch (error) {

      console.error(error);

      alert(
        error.response?.data?.detail ||
        "Password reset failed"
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
            Reset Password
          </h1>

          <p className="text-lg text-slate-300 leading-8">

            Use the generated
            reset token to set
            a new secure password
            for your account.

          </p>

        </div>

      </div>

      <div className="w-full md:w-1/2 flex justify-center items-center bg-slate-100 px-6 py-8">

        <div className="w-full max-w-[480px] bg-white border border-slate-200 shadow-sm rounded-2xl p-10">

          <div className="mb-8 text-center">

            <h2 className="text-3xl font-bold text-slate-900">
              Set New Password
            </h2>

            <p className="text-slate-500 mt-2">
              Confirm token and password
            </p>

          </div>

          <form
            onSubmit={handleResetPassword}
            className="space-y-5"
          >

            <div>

              <label className="block text-sm font-medium text-slate-700 mb-2">
                Reset Token
              </label>

              <textarea
                placeholder="Paste reset token"
                value={token}
                onChange={(e) =>
                  setToken(
                    e.target.value
                  )
                }
                className="w-full h-28 border border-slate-300 rounded-lg px-4 py-3 outline-none focus:border-slate-500 focus:ring-2 focus:ring-slate-200 resize-none"
                required
              />

            </div>

            <div>

              <label className="block text-sm font-medium text-slate-700 mb-2">
                New Password
              </label>

              <input
                type="password"
                placeholder="Enter new password"
                value={newPassword}
                onChange={(e) =>
                  setNewPassword(
                    e.target.value
                  )
                }
                className="w-full border border-slate-300 rounded-lg px-4 py-3 outline-none focus:border-slate-500 focus:ring-2 focus:ring-slate-200"
                required
              />

            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-slate-900 hover:bg-slate-800 text-white py-3 rounded-lg font-semibold transition"
            >

              {
                loading
                ?
                "Resetting password..."
                :
                "Reset Password"
              }

            </button>

          </form>

          <div className="mt-6 text-center text-slate-600">

            Back to

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

export default ResetPasswordPage;
