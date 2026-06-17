import {
  useEffect,
  useState
} from "react"

import axios from "axios"

import Navbar from "../components/Navbar"


export default function AuditLogsPage() {

  const [logs,
    setLogs] =
    useState([])

  const [loading,
    setLoading] =
    useState(true)

  const [selectedLog,
    setSelectedLog] =
    useState(null)

  const [filters,
    setFilters] =
    useState({
      module_name: "",
      user_id: "",
      start_date: "",
      end_date: ""
    })

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
      "auditor"
    ].includes(user?.role)

  const headers = {
    Authorization:
      `Bearer ${token}`
  }


  const fetchAuditLogs =
    async (url = "http://127.0.0.1:8000/audit-logs/?page=1&size=100") => {

      try {

        setLoading(true)

        const response =
          await axios.get(
            url,
            { headers }
          )

        setLogs(
          response.data.items ||
          response.data
        )

      } catch (error) {

        console.error(error)

        setMessage(
          error.response?.data?.detail ||
          "Unable to load audit logs"
        )

      } finally {

        setLoading(false)
      }
    }


  useEffect(() => {

    if (canView) {

      fetchAuditLogs()

    } else {

      setLoading(false)
    }

  }, [canView])


  const applyFilters =
    () => {

      if (filters.module_name) {

        fetchAuditLogs(
          `http://127.0.0.1:8000/audit-logs/module/${filters.module_name}?page=1&size=100`
        )

        return
      }

      if (filters.user_id) {

        fetchAuditLogs(
          `http://127.0.0.1:8000/audit-logs/user/${filters.user_id}?page=1&size=100`
        )

        return
      }

      if (
        filters.start_date &&
        filters.end_date
      ) {

        const startDate =
          new Date(filters.start_date).toISOString()

        const endDate =
          new Date(filters.end_date).toISOString()

        fetchAuditLogs(
          `http://127.0.0.1:8000/audit-logs/date-range?start_date=${encodeURIComponent(startDate)}&end_date=${encodeURIComponent(endDate)}&page=1&size=100`
        )

        return
      }

      fetchAuditLogs()
    }


  const clearFilters =
    () => {

      setFilters({
        module_name: "",
        user_id: "",
        start_date: "",
        end_date: ""
      })

      fetchAuditLogs()
    }


  const formatDateTime =
    (value) => {

      if (!value) {

        return "Not available"
      }

      return new Date(value).toLocaleString(
        "en-IN",
        {
          dateStyle: "medium",
          timeStyle: "short"
        }
      )
    }


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

              Audit logs are available only for admins and auditors

            </h1>

          </div>

        ) : (

          <>

            <div className="bg-white border border-slate-200 rounded-xl shadow-sm px-6 py-5 mb-6">
              <h1 className="text-3xl font-bold text-slate-900">
                Audit Logs
              </h1>
              <p className="text-slate-500 mt-1">
                Track system actions with module, user, and change details
              </p>
            </div>

            {message && (
              <div className="bg-white border border-slate-200 rounded-xl shadow-sm px-5 py-4 mb-6 text-sm text-slate-700">
                {message}
              </div>
            )}

            <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-5 mb-6 grid grid-cols-1 md:grid-cols-2 xl:grid-cols-[1fr_1fr_1fr_1fr_auto_auto] gap-4 items-end">

              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">
                  Module
                </label>
                <input
                  value={filters.module_name}
                  onChange={(event) =>
                    setFilters({
                      ...filters,
                      module_name:
                        event.target.value
                    })
                  }
                  placeholder="task, approval, sla"
                  className="w-full border border-slate-300 rounded-xl px-4 py-3"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">
                  User ID
                </label>
                <input
                  type="number"
                  value={filters.user_id}
                  onChange={(event) =>
                    setFilters({
                      ...filters,
                      user_id:
                        event.target.value
                    })
                  }
                  className="w-full border border-slate-300 rounded-xl px-4 py-3"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">
                  Start
                </label>
                <input
                  type="datetime-local"
                  value={filters.start_date}
                  onChange={(event) =>
                    setFilters({
                      ...filters,
                      start_date:
                        event.target.value
                    })
                  }
                  className="w-full border border-slate-300 rounded-xl px-4 py-3"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">
                  End
                </label>
                <input
                  type="datetime-local"
                  value={filters.end_date}
                  onChange={(event) =>
                    setFilters({
                      ...filters,
                      end_date:
                        event.target.value
                    })
                  }
                  className="w-full border border-slate-300 rounded-xl px-4 py-3"
                />
              </div>

              <button
                onClick={applyFilters}
                className="bg-slate-900 hover:bg-slate-800 text-white px-5 py-3 rounded-xl font-semibold"
              >
                Filter
              </button>

              <button
                onClick={clearFilters}
                className="border border-slate-300 text-slate-700 px-5 py-3 rounded-xl font-semibold"
              >
                Clear
              </button>

            </div>

            <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">

              {loading ? (

                <div className="p-8 text-slate-500">
                  Loading audit logs...
                </div>

              ) : logs.length > 0 ? (

                <div className="overflow-x-auto">

                  <table className="w-full text-sm">

                    <thead className="bg-slate-50 border-b border-slate-200 text-slate-600">
                      <tr>
                        <th className="text-left px-5 py-4">Log ID</th>
                        <th className="text-left px-5 py-4">User</th>
                        <th className="text-left px-5 py-4">Module</th>
                        <th className="text-left px-5 py-4">Action</th>
                        <th className="text-left px-5 py-4">Record</th>
                        <th className="text-left px-5 py-4">IP</th>
                        <th className="text-left px-5 py-4">Created</th>
                        <th className="text-left px-5 py-4">Actions</th>
                      </tr>
                    </thead>

                    <tbody>
                      {logs.map(
                        (log) => (
                          <tr
                            key={log.id}
                            className="border-b border-slate-100 last:border-b-0"
                          >
                            <td className="px-5 py-4">#{log.id}</td>
                            <td className="px-5 py-4">{log.user_id ? `#${log.user_id}` : "-"}</td>
                            <td className="px-5 py-4 capitalize">{log.module_name || log.entity}</td>
                            <td className="px-5 py-4 text-slate-900 font-medium">{log.action_type || log.action}</td>
                            <td className="px-5 py-4">{log.record_id || log.entity_id || "-"}</td>
                            <td className="px-5 py-4">{log.ip_address || "-"}</td>
                            <td className="px-5 py-4 text-slate-500">{formatDateTime(log.timestamp)}</td>
                            <td className="px-5 py-4">
                              <button
                                onClick={() =>
                                  setSelectedLog(log)
                                }
                                className="bg-slate-800 text-white px-3 py-2 rounded-lg text-xs font-semibold"
                              >
                                Details
                              </button>
                            </td>
                          </tr>
                        )
                      )}
                    </tbody>

                  </table>

                </div>

              ) : (

                <div className="p-8 text-slate-500">
                  No audit logs found.
                </div>
              )}

            </div>

          </>
        )}

      </div>

      {selectedLog && (

        <div className="fixed inset-0 bg-slate-950/50 flex justify-center items-center z-50 px-4">

          <div className="bg-white w-full max-w-2xl rounded-xl shadow-2xl p-6 max-h-[90vh] overflow-y-auto">

            <div className="flex items-start justify-between gap-4 mb-5">
              <div>
                <h2 className="text-2xl font-bold text-slate-900">
                  Audit Log #{selectedLog.id}
                </h2>
                <p className="text-sm text-slate-500 mt-1">
                  {formatDateTime(selectedLog.timestamp)}
                </p>
              </div>
              <button
                onClick={() =>
                  setSelectedLog(null)
                }
                className="text-slate-500 hover:text-red-600 text-xl"
              >
                x
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-4">
                <p className="text-slate-500 font-semibold mb-1">User</p>
                <p>#{selectedLog.user_id || "-"}</p>
              </div>
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-4">
                <p className="text-slate-500 font-semibold mb-1">Module</p>
                <p>{selectedLog.module_name || selectedLog.entity}</p>
              </div>
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-4">
                <p className="text-slate-500 font-semibold mb-1">Action</p>
                <p>{selectedLog.action_type || selectedLog.action}</p>
              </div>
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-4">
                <p className="text-slate-500 font-semibold mb-1">Record</p>
                <p>{selectedLog.record_id || selectedLog.entity_id || "-"}</p>
              </div>
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-4">
                <p className="text-slate-500 font-semibold mb-1">IP Address</p>
                <p>{selectedLog.ip_address || "-"}</p>
              </div>
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-4">
                <p className="text-slate-500 font-semibold mb-1">User Agent</p>
                <p className="break-words">{selectedLog.user_agent || "-"}</p>
              </div>
            </div>

            <div className="mt-4 space-y-4">
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-4">
                <p className="text-slate-500 font-semibold mb-2">Old Data</p>
                <pre className="text-xs whitespace-pre-wrap text-slate-700">
                  {selectedLog.old_data || "-"}
                </pre>
              </div>
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-4">
                <p className="text-slate-500 font-semibold mb-2">New Data</p>
                <pre className="text-xs whitespace-pre-wrap text-slate-700">
                  {selectedLog.new_data || "-"}
                </pre>
              </div>
            </div>

          </div>

        </div>
      )}

    </div>
  )
}
