import {
  useEffect,
  useState
} from "react";

import {
  useNavigate,
  useSearchParams
} from "react-router-dom";

import api from "../api/axios";


function OAuthCallbackPage() {

  const [searchParams] =
    useSearchParams();

  const [message, setMessage] =
    useState("Completing Google login...");

  const navigate = useNavigate();


  useEffect(() => {

    const accessToken =
      searchParams.get("access_token");

    const refreshToken =
      searchParams.get("refresh_token");

    if (!accessToken) {

      setMessage(
        "Google login did not return an access token."
      );

      return;
    }

    localStorage.setItem(
      "token",
      accessToken
    );

    if (refreshToken) {

      localStorage.setItem(
        "refresh_token",
        refreshToken
      );
    }

    fetchCurrentUser(
      accessToken
    );

  }, []);


  const fetchCurrentUser = async (
    accessToken
  ) => {

    try {

      const response = await api.get(
        "/auth/me",
        {
          headers: {
            Authorization:
              `Bearer ${accessToken}`
          }
        }
      );

      localStorage.setItem(
        "user",
        JSON.stringify(
          response.data
        )
      );

      navigate(
        "/dashboard"
      );

    } catch (error) {

      console.error(error);

      setMessage(
        "Google login completed, but user details could not be loaded."
      );
    }
  };


  return (

    <div className="min-h-screen flex justify-center items-center bg-slate-100 px-6">

      <div className="w-full max-w-[420px] bg-white border border-slate-200 shadow-sm rounded-2xl p-10 text-center">

        <h1 className="text-2xl font-bold text-slate-900 mb-3">
          Google Login
        </h1>

        <p className="text-slate-500 leading-6">
          {message}
        </p>

        <button
          type="button"
          onClick={() =>
            navigate("/")
          }
          className="mt-6 text-slate-900 font-semibold hover:underline"
        >
          Back to Login
        </button>

      </div>

    </div>
  );
}

export default OAuthCallbackPage;
