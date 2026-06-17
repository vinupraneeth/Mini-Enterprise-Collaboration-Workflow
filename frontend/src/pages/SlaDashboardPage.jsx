import {
  useEffect,
  useMemo,
  useState
} from "react"

import axios from "axios"

import Navbar from "../components/Navbar"

import SLABadge from "../components/SLABadge"


export default function SlaDashboardPage() {

  const [activeRecords,
    setActiveRecords] =
    useState([])

  const [breachedRecords,
    setBreachedRecords] =
    useState([])

  const [completedRecords,
    setCompletedRecords] =
    useState([])

  const [moduleFilter,
    setModuleFilter] =
    useState("")

  const [statusFilter,
    setStatusFilter] =
    useState("")

  const [loading,
    setLoading] =
    useState(true)

  const [message,
    setMessage] =
    useState("")

  const token =
    localStorage.getItem("token")

  const user =
    JSON.parse(
      localStorage.getItem("user")
    )

  const canView =
    [
      "admin",
      "manager",
      "auditor"
    ].includes(user?.role)


  const fetchSlaRecords =
    async () => {

      try {

        setLoading(true)

        const headers = {
          Authorization:
            `Bearer ${token}`
        }

        const [
          activeResponse,
          breachedResponse,
          completedResponse
        ] =
          await Promise.all([
            axios.get(
              "http://127.0.0.1:8000/sla-tracking/active",
              { headers }
            ),
            axios.get(
              "http://127.0.0.1:8000/sla-tracking/breached",
              { headers }
            ),
            axios.get(
              "http://127.0.0.1:8000/sla-tracking/completed",
              { headers }
            )
          ])

        setActiveRecords(activeResponse.data)
        setBreachedRecords(breachedResponse.data)
        setCompletedRecords(completedResponse.data)

      } catch (error) {

        console.error(error)

        setMessage(
          error.response?.data?.detail ||
          "Unable to load SLA dashboard"
        )

      } finally {

        setLoading(false)
      }
    }


  useEffect(() => {

    if (canView) {

      fetchSlaRecords()
    }

  }, [canView])


  const allRecords =
    useMemo(
      () => [
        ...activeRecords,
        ...breachedRecords,
        ...completedRecords
      ],
      [
        activeRecords,
        breachedRecords,
        completedRecords
      ]
    )

  const filteredRecords =
    allRecords.filter(
      (record) =>
        (!moduleFilter ||
          record.module_name === moduleFilter) &&
        (!statusFilter ||
          record.status === statusFilter)
    )

  const escalatedCount =
    allRecords.filter(
      (record) =>
        record.status === "escalated"
    ).length


  const formatDateTime =
    (value) => {

      if (!value) {

        return "-"
      }

      return new Date(value).toLocaleString(
        "en-IN",
        {
          dateStyle: "medium",
          timeStyle: "short"
        }
      )
    }


  const cards = [
    {
      title: "Active SLA",
      value: activeRecords.length,
      color: "bg-blue-600"
    },
    {
      title: "Breached SLA",
      value: breachedRecords.length,
      color: "bg-red-600"
    },
    {
      title: "Completed Within SLA",
      value: completedRecords.length,
      color: "bg-emerald-600"
    },
    {
      title: "Escalated SLA",
      value: escalatedCount,
      color: "bg-orange-500"
    }
  ]


  return (

    <div className="min-h-screen bg-slate-100">

      <Navbar
        user={user}
        handleLogout={() => {
          localStorage.clear()
          window.location.href = "/"
        }}
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">

        {!canView ? (

          <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-10 text-center">

            <h1 className="text-2xl font-bold text-slate-900">

              SLA dashboard is not available for your role

            </h1>

          </div>

        ) : (

          <>

            <div className="bg-white border border-slate-200 rounded-xl shadow-sm px-6 py-5 mb-6">

              <h1 className="text-3xl font-bold text-slate-900">

                SLA Dashboard

              </h1>

              <p className="text-slate-500 mt-1">

                Monitor active, breached, and completed workflow SLA records

              </p>

            </div>

            {message && (

              <div className="bg-white border border-slate-200 rounded-xl shadow-sm px-5 py-4 mb-6 text-sm text-slate-700">
                {message}
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 mb-6">

              {cards.map(
                (card) => (
                  <div
                    key={card.title}
                    className={`${card.color} rounded-xl p-5 text-white shadow-sm`}
                  >
                    <p className="text-sm opacity-90">{card.title}</p>
                    <h2 className="text-4xl font-bold mt-3">{card.value}</h2>
                  </div>
                )
              )}

            </div>

            <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">

              <div className="px-5 py-4 border-b border-slate-200 flex flex-col md:flex-row gap-3 md:items-center md:justify-between">

                <h2 className="text-xl font-bold text-slate-900">

                  SLA Records

                </h2>

                <div className="flex gap-3">

                  <select
                    value={moduleFilter}
                    onChange={(event) =>
                      setModuleFilter(
                        event.target.value
                      )
                    }
                    className="border border-slate-300 rounded-xl px-3 py-2 text-sm"
                  >
                    <option value="">All modules</option>
                    <option value="task">Task</option>
                    <option value="approval">Approval</option>
                  </select>

                  <select
                    value={statusFilter}
                    onChange={(event) =>
                      setStatusFilter(
                        event.target.value
                      )
                    }
                    className="border border-slate-300 rounded-xl px-3 py-2 text-sm"
                  >
                    <option value="">All statuses</option>
                    <option value="active">Active</option>
                    <option value="breached">Breached</option>
                    <option value="completed_within_sla">Completed</option>
                  </select>

                </div>

              </div>

              {loading ? (

                <div className="p-8 text-slate-500">
                  Loading SLA records...
                </div>

              ) : filteredRecords.length > 0 ? (

                <div className="overflow-x-auto">

                  <table className="w-full text-sm">

                    <thead className="bg-slate-50 border-b border-slate-200 text-slate-600">
                      <tr>
                        <th className="text-left px-5 py-4">Module</th>
                        <th className="text-left px-5 py-4">Record ID</th>
                        <th className="text-left px-5 py-4">Status</th>
                        <th className="text-left px-5 py-4">Start</th>
                        <th className="text-left px-5 py-4">Due</th>
                        <th className="text-left px-5 py-4">Completed</th>
                        <th className="text-left px-5 py-4">Breach Reason</th>
                      </tr>
                    </thead>

                    <tbody>
                      {filteredRecords.map(
                        (record) => (
                          <tr
                            key={`${record.module_name}-${record.id}`}
                            className="border-b border-slate-100 last:border-b-0"
                          >
                            <td className="px-5 py-4 capitalize">{record.module_name}</td>
                            <td className="px-5 py-4">#{record.record_id}</td>
                            <td className="px-5 py-4">
                              <SLABadge status={record.status} />
                            </td>
                            <td className="px-5 py-4 text-slate-600">{formatDateTime(record.start_time)}</td>
                            <td className="px-5 py-4 text-slate-600">{formatDateTime(record.due_time)}</td>
                            <td className="px-5 py-4 text-slate-600">{formatDateTime(record.completed_time)}</td>
                            <td className="px-5 py-4 text-slate-600">{record.breach_reason || "-"}</td>
                          </tr>
                        )
                      )}
                    </tbody>

                  </table>

                </div>

              ) : (

                <div className="p-8 text-slate-500">
                  No SLA records found.
                </div>
              )}

            </div>

          </>
        )}

      </div>

    </div>
  )
}
