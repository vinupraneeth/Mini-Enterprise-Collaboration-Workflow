import { Link } from "react-router-dom"


function Navbar({

  user,

  handleLogout
}) {

  return (

    <div className="bg-white shadow-md border-b sticky top-0 z-40">

      <div className="max-w-7xl mx-auto px-8 py-5 flex justify-between items-center">

        <div>

          <h1 className="text-3xl font-extrabold bg-gradient-to-r from-teal-500 to-emerald-700 bg-clip-text text-transparent">

            Enterprise Workflow

          </h1>

          {
            user && (

              <div className="mt-2 flex items-center gap-3">

                <div className="w-10 h-10 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold">

                  {
                    user.name
                    ?.charAt(0)
                    ?.toUpperCase()
                  }

                </div>

                <div>

                  <p className="font-semibold text-gray-800">

                    {user.name}

                  </p>

                  <p className="text-sm text-gray-500 capitalize">

                    {user.role}

                  </p>

                </div>

              </div>
            )
          }

        </div>

        <div className="flex items-center gap-4">

          <Link
            to="/dashboard"
            className="bg-cyan-600 hover:bg-cyan-700 text-white px-5 py-3 rounded-2xl font-semibold shadow-lg transition"
          >

            Dashboard

          </Link>

          {user && (

            <Link
              to="/approvals"
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-3 rounded-2xl font-semibold shadow-lg transition"
            >

              Approvals

            </Link>
          )}

          {user?.role === "admin" && (

            <Link
              to="/audit-logs"
              className="bg-slate-800 hover:bg-slate-900 text-white px-5 py-3 rounded-2xl font-semibold shadow-lg transition"
            >

              Audit Logs

            </Link>
          )}

          <button
            onClick={handleLogout}
            className="bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-2xl font-semibold shadow-lg transition"
          >

            Logout

          </button>

        </div>

      </div>

    </div>
  );
}

export default Navbar;
