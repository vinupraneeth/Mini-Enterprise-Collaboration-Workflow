import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import LoginPage from "./pages/LoginPage";

import RegisterPage from "./pages/RegisterPage";

import DashboardPage from "./pages/DashboardPage";

import ProtectedRoute from "./routes/ProtectedRoute";

import ApprovalsPage from "./pages/ApprovalsPage"

import AuditLogsPage from "./pages/AuditLogsPage"


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

      </Routes>

    </BrowserRouter>
  );
}

export default App;
