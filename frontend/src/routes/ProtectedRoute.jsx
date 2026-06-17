import { Navigate } from "react-router-dom";


function ProtectedRoute({ children }) {

  const token = localStorage.getItem(
    "token"
  );

  const isTokenExpired =
    (tokenValue) => {

      try {

        const base64 =
          tokenValue.split(".")[1]
            .replace(/-/g, "+")
            .replace(/_/g, "/")

        const paddedBase64 =
          base64.padEnd(
            base64.length + (
              4 - base64.length % 4
            ) % 4,
            "="
          )

        const payload =
          JSON.parse(
            atob(paddedBase64)
          )

        return (
          payload.exp &&
          payload.exp * 1000 < Date.now()
        )

      } catch (error) {

        return true
      }
    }

  if (!token) {

    return <Navigate to="/" />;
  }

  if (isTokenExpired(token)) {

    localStorage.removeItem("token")

    localStorage.removeItem("refresh_token")

    localStorage.removeItem("user")

    return <Navigate to="/" />;
  }

  return children;
}

export default ProtectedRoute;
