import {
  useEffect,
  useState
} from "react"

import axios from "axios"


export default function RoleDashboardPanel({

  user

}) {

  const [roleView,
    setRoleView] =
    useState(null)

  const [loading,
    setLoading] =
    useState(true)

  const token =
    localStorage.getItem("token")

  const fetchRoleView =
    async () => {

      try {

        const response =
          await axios.get(

            "http://127.0.0.1:8000/dashboard/role-view",

            {
              headers: {
                Authorization:
                  `Bearer ${token}`
              }
            }
          )

        setRoleView(response.data)

      } catch (error) {

        console.error(error)

      } finally {

        setLoading(false)
      }
    }


  useEffect(() => {

    fetchRoleView()

  }, [user?.id])


  if (loading) {

    return (

      <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6 text-slate-500">

        Loading role dashboard...

      </div>
    )
  }


  if (!roleView) {

    return null
  }


  return (

    <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6">

      <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4 mb-6">

        <div>

          <h2 className="text-2xl font-bold text-slate-900">

            {roleView.title}

          </h2>

          <p className="text-sm text-slate-500 mt-1 capitalize">

            {roleView.role}
            {" "}
            dashboard overview

          </p>

        </div>

      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">

        {roleView.summary?.map(
          (item) => (

            <div
              key={item.label}
              className="bg-slate-50 border border-slate-200 rounded-xl p-4"
            >

              <p className="text-sm text-slate-600 font-semibold">

                {item.label}

              </p>

              <p className="text-3xl font-bold text-slate-900 mt-2">

                {item.value}

              </p>

            </div>
          )
        )}

      </div>

    </div>
  )
}
