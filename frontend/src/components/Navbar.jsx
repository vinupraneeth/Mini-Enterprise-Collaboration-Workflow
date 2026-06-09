import { Link } from "react-router-dom"


function Navbar({

  user,

  handleLogout
}) {

  return (

    <div className="bg-white shadow-sm border-b border-slate-200 sticky top-0 z-40">

      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4 flex flex-col lg:flex-row lg:justify-between lg:items-center gap-4">

        <div>

          <h1 className="text-2xl font-extrabold text-slate-900">

            Enterprise Workflow

          </h1>

          {
            user && (

              <div className="mt-2 flex items-center gap-3">

                <div className="w-9 h-9 rounded-full bg-slate-900 text-white flex items-center justify-center font-bold">

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

        <div className="flex items-center gap-3 flex-wrap">

          <Link
            to="/dashboard"
            className="bg-white hover:bg-slate-50 text-slate-800 border border-slate-300 px-4 py-2 rounded-xl font-semibold transition"
          >

            Dashboard

          </Link>

          {user && (

            <Link
              to="/approvals"
              className="bg-white hover:bg-slate-50 text-slate-800 border border-slate-300 px-4 py-2 rounded-xl font-semibold transition"
            >

              Approvals

            </Link>
          )}

          {user?.role === "admin" && (

            <Link
              to="/subscription-plans"
              className="bg-white hover:bg-slate-50 text-slate-800 border border-slate-300 px-4 py-2 rounded-xl font-semibold transition"
            >

              Subscription

            </Link>
          )}

          {user?.role === "admin" && (

            <Link
              to="/audit-logs"
              className="bg-white hover:bg-slate-50 text-slate-800 border border-slate-300 px-4 py-2 rounded-xl font-semibold transition"
            >

              Audit Logs

            </Link>
          )}

          <button
            onClick={handleLogout}
            className="bg-slate-900 hover:bg-slate-800 text-white px-4 py-2 rounded-xl font-semibold transition"
          >

            Logout

          </button>

        </div>

      </div>

    </div>
  );
}

export default Navbar;
