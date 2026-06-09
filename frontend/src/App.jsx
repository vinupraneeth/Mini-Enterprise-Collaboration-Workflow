import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import LoginPage from "./pages/LoginPage";

import RegisterPage from "./pages/RegisterPage";

import ForgotPasswordPage from "./pages/ForgotPasswordPage";

import ResetPasswordPage from "./pages/ResetPasswordPage";

import OAuthCallbackPage from "./pages/OAuthCallbackPage";

import DashboardPage from "./pages/DashboardPage";

import ProtectedRoute from "./routes/ProtectedRoute";

import ApprovalsPage from "./pages/ApprovalsPage"

import AuditLogsPage from "./pages/AuditLogsPage"

import SubscriptionPlansPage from "./pages/SubscriptionPlansPage"


function App() {

  return (

    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={<LoginPage />}
        />

        <Route
          path="/register"
          element={<RegisterPage />}
        />

        <Route
          path="/forgot-password"
          element={<ForgotPasswordPage />}
        />

        <Route
          path="/reset-password"
          element={<ResetPasswordPage />}
        />

        <Route
          path="/oauth/callback"
          element={<OAuthCallbackPage />}
        />

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>

              <DashboardPage />

            </ProtectedRoute>
          }
          
        />
        <Route

          path="/approvals"

          element={
            <ProtectedRoute>

              <ApprovalsPage />

            </ProtectedRoute>
          }
        />

        <Route

          path="/audit-logs"

          element={
            <ProtectedRoute>

              <AuditLogsPage />

            </ProtectedRoute>
          }
        />

        <Route

          path="/subscription-plans"

          element={
            <ProtectedRoute>

              <SubscriptionPlansPage />

            </ProtectedRoute>
          }
        />

      </Routes>

    </BrowserRouter>
  );
}

export default App;
