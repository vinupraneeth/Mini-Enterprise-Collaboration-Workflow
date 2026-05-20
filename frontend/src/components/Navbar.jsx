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

        <button
          onClick={handleLogout}
          className="bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-2xl font-semibold shadow-lg transition"
        >
          Logout
        </button>

      </div>

    </div>
  );
}

export default Navbar;