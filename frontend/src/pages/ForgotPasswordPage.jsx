import {
  useState
} from "react";

import {
  useNavigate
} from "react-router-dom";

import api from "../api/axios";


function ForgotPasswordPage() {

  const [email, setEmail] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [resetToken, setResetToken] =
    useState("");

  const [message, setMessage] =
    useState("");

  const navigate = useNavigate();


  const handleRequestReset = async (
    event
  ) => {

    event.preventDefault();

    setLoading(true);

    setMessage("");

    setResetToken("");

    try {

      const response = await api.post(

        "/auth/password-reset/request",

        {
          email
        }
      );

      setMessage(
        response.data.message
      );

      setResetToken(
        response.data.reset_token || ""
      );

    } catch (error) {

      console.error(error);

      alert(
        "Password reset request failed"
      );

    } finally {

      setLoading(false);
    }
  };


  const goToReset = () => {

    navigate(
      "/reset-password",
      {
        state: {
          resetToken
        }
      }
    );
  };


  return (

    <div className="min-h-screen flex bg-slate-100">

      <div className="hidden md:flex w-1/2 bg-slate-900 text-white items-center justify-center p-10">

        <div className="max-w-md">

          <h1 className="text-5xl font-bold mb-6">
            Account Recovery
          </h1>

          <p className="text-lg text-slate-300 leading-8">

            Generate a secure
            password reset token
            and restore access
            to your workflow account.

          </p>

        </div>

      </div>

      <div className="w-full md:w-1/2 flex justify-center items-center bg-slate-100 px-6 py-8">

        <div className="w-full max-w-[480px] bg-white border border-slate-200 shadow-sm rounded-2xl p-10">

          <div className="mb-8 text-center">

            <h2 className="text-3xl font-bold text-slate-900">
              Forgot Password
            </h2>

            <p className="text-slate-500 mt-2">
              Request a reset token
            </p>

          </div>

          <form
            onSubmit={handleRequestReset}
            className="space-y-5"
          >

            <div>

              <label className="block text-sm font-medium text-slate-700 mb-2">
                Email
              </label>

              <input
                type="email"
                placeholder="Enter registered email"
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

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-slate-900 hover:bg-slate-800 text-white py-3 rounded-lg font-semibold transition"
            >

              {
                loading
                ?
                "Generating token..."
                :
                "Generate Reset Token"
              }

            </button>

          </form>

          {message && (

            <div className="mt-6 border border-slate-200 bg-slate-50 rounded-xl p-4">

              <p className="text-sm text-slate-700">
                {message}
              </p>

              {resetToken && (

                <div className="mt-4">

                  <label className="block text-xs font-semibold text-slate-500 mb-2">
                    Reset Token for Local Testing
                  </label>

                  <textarea
                    value={resetToken}
                    readOnly
                    className="w-full h-28 text-xs border border-slate-300 rounded-lg p-3 bg-white text-slate-700 resize-none"
                  />

                  <button
                    type="button"
                    onClick={goToReset}
                    className="mt-4 w-full bg-slate-900 hover:bg-slate-800 text-white py-3 rounded-lg font-semibold transition"
                  >
                    Continue to Reset Password
                  </button>

                </div>
              )}

            </div>
          )}

          <div className="mt-6 text-center text-slate-600">

            Remember your password?

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

export default ForgotPasswordPage;
