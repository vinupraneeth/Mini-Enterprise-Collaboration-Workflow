import {
  useEffect,
  useState
} from "react"

import axios from "axios"


export default function AiSummaryPanel() {

  const [summary,
    setSummary] =
    useState(null)

  const [loading,
    setLoading] =
    useState(true)

  const token =
    localStorage.getItem("token")


  const fetchSummary =
    async () => {

      try {

        const response =
          await axios.get(

            "http://127.0.0.1:8000/dashboard/ai-summary",

            {
              headers: {
                Authorization:
                  `Bearer ${token}`
              }
            }
          )

        setSummary(response.data)

      } catch (error) {

        console.error(error)

      } finally {

        setLoading(false)
      }
    }


  useEffect(() => {

    fetchSummary()

  }, [])


  if (loading) {

    return (

      <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-6 mt-8 text-slate-500">

        Loading AI summary...

      </div>
    )
  }


  if (!summary) {

    return (

      <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-6 mt-8 text-slate-500">

        AI summary is currently unavailable.

      </div>
    )
  }


  return (

    <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-6 mt-8">

      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">

        <div>

          <h2 className="text-2xl font-bold text-slate-900">

            AI Workflow Summary

          </h2>

          <p className="text-slate-500 mt-1">

            Dynamic insights based on current workflow data

          </p>

        </div>

      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">

        <div className="bg-slate-50 border border-slate-200 rounded-xl p-4">

          <p className="text-sm text-slate-600 font-semibold">

            Pending Tasks

          </p>

          <p className="text-3xl font-bold text-slate-900 mt-2">

            {summary.pending_tasks}

          </p>

        </div>

        <div className="bg-red-50 border border-red-100 rounded-xl p-4">

          <p className="text-sm text-rose-700 font-semibold">

            High Priority

          </p>

          <p className="text-3xl font-bold text-rose-900 mt-2">

            {summary.high_priority_tasks}

          </p>

        </div>

        <div className="bg-amber-50 border border-amber-100 rounded-xl p-4">

          <p className="text-sm text-amber-700 font-semibold">

            Delayed Tasks

          </p>

          <p className="text-3xl font-bold text-amber-900 mt-2">

            {summary.delayed_tasks}

          </p>

        </div>

      </div>

      <div className="space-y-3">

        {summary.insights?.map(
          (insight, index) => (

            <div
              key={index}
              className="bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-gray-700"
            >

              {insight}

            </div>
          )
        )}

      </div>

    </div>
  )
}
