import {
  useEffect,
  useState
} from "react"

import axios from "axios"


export default function SmartAssignmentPanel({
  user
}) {

  const [assignment,
    setAssignment] =
    useState(null)

  const [loading,
    setLoading] =
    useState(true)

  const token =
    localStorage.getItem("token")


  const fetchAssignment =
    async () => {

      if (
        user?.role !== "admin" &&
        user?.role !== "manager"
      ) {

        setLoading(false)

        return
      }

      try {

        const response =
          await axios.get(

            "http://127.0.0.1:8000/dashboard/smart-assignment",

            {
              headers: {
                Authorization:
                  `Bearer ${token}`
              }
            }
          )

        setAssignment(response.data)

      } catch (error) {

        console.error(error)

      } finally {

        setLoading(false)
      }
    }


  useEffect(() => {

    fetchAssignment()

  }, [user?.role])


  if (
    user?.role !== "admin" &&
    user?.role !== "manager"
  ) {

    return null
  }


  if (loading) {

    return (

      <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-6 mt-8 text-slate-500">

        Loading smart assignment...

      </div>
    )
  }


  if (!assignment?.recommendation) {

    return (

      <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-6 mt-8 text-slate-500">

        Smart assignment is currently unavailable.

      </div>
    )
  }


  return (

    <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-6 mt-8">

      <div className="mb-5">

        <h2 className="text-2xl font-bold text-slate-900">

          Smart Assignment

        </h2>

        <p className="text-slate-500 mt-1">

          Recommended assignee based on current workload and completion history

        </p>

      </div>

      <div className="bg-emerald-50 border border-emerald-100 rounded-xl p-4 mb-5">

        <p className="text-sm font-semibold text-emerald-700">

          Recommended Employee

        </p>

        <p className="text-2xl font-bold text-emerald-950 mt-1">

          {assignment.recommendation.name}

        </p>

        <p className="text-sm text-emerald-800 mt-2">

          {assignment.recommendation.reason}

        </p>

      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-3">

        {assignment.candidates?.map(
          (candidate) => (

            <div
              key={candidate.user_id}
              className="border border-slate-200 rounded-xl p-4"
            >

              <div className="flex items-start justify-between gap-2">

                <div>

                  <p className="font-semibold text-slate-900">

                    {candidate.name}

                  </p>

                  <p className="text-xs text-slate-500 mt-1">

                    {candidate.email}

                  </p>

                </div>

                <span className="text-xs font-bold text-slate-700 bg-slate-100 rounded-lg px-2 py-1">

                  {candidate.score}

                </span>

              </div>

              <div className="grid grid-cols-3 gap-2 mt-4 text-center">

                <div>

                  <p className="text-lg font-bold text-slate-900">

                    {candidate.active_tasks}

                  </p>

                  <p className="text-xs text-slate-500">

                    Active

                  </p>

                </div>

                <div>

                  <p className="text-lg font-bold text-rose-700">

                    {candidate.high_priority_tasks}

                  </p>

                  <p className="text-xs text-slate-500">

                    High

                  </p>

                </div>

                <div>

                  <p className="text-lg font-bold text-amber-700">

                    {candidate.overdue_tasks}

                  </p>

                  <p className="text-xs text-slate-500">

                    Overdue

                  </p>

                </div>

              </div>

            </div>
          )
        )}

      </div>

    </div>
  )
}
