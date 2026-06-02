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

  const [users,
    setUsers] =
    useState([])

  const token =
    localStorage.getItem("token")

  const user =
    JSON.parse(
      localStorage.getItem("user")
    )


  const fetchAuditLogs =
    async () => {

      try {

        const [logsResponse,
          usersResponse] =
          await Promise.all([

            axios.get(

              "http://127.0.0.1:8000/audit-logs/?page=1&size=50",

              {
                headers: {
                  Authorization:
                    `Bearer ${token}`
                }
              }
            ),

            axios.get(

              "http://127.0.0.1:8000/users/?page=1&size=100",

              {
                headers: {
                  Authorization:
                    `Bearer ${token}`
                }
              }
            )
          ])

        setLogs(
          logsResponse.data.items ||
          logsResponse.data
        )

        setUsers(
          usersResponse.data.items ||
          usersResponse.data
        )

      } catch (error) {

        console.error(error)

      } finally {

        setLoading(false)
      }
    }


  useEffect(() => {

    if (
      user?.role !== "admin"
    ) {

      setLoading(false)

      return
    }

    fetchAuditLogs()

  }, [])


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


  const getUserLabel =
    (userId) => {

      const matchedUser =
        users.find(
          (userItem) =>
            userItem.id === userId
        )

      if (matchedUser) {

        return `${matchedUser.name} (#${userId})`
      }

      return userId
        ? `User #${userId}`
        : "-"
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

      <div className="max-w-6xl mx-auto px-6 py-10">

        {user?.role !== "admin" ? (

          <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-10 text-center">

            <h1 className="text-2xl font-bold text-slate-900">

              Audit logs are available only for admins

            </h1>

            <p className="text-slate-500 mt-2">

              System activity tracking is restricted for security.

            </p>

          </div>

        ) : (

          <>

            <div className="bg-white border border-slate-200 rounded-2xl shadow-sm px-6 py-5 mb-8">

              <h1 className="text-3xl font-bold text-slate-900">

                Audit Logs

              </h1>

              <p className="text-slate-500 mt-1">

                Track system actions with user, entity and timestamp details

              </p>

            </div>

            <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">

              {loading ? (

                <div className="p-8 text-slate-500">

                  Loading audit logs...

                </div>

              ) : logs.length > 0 ? (

                <div className="overflow-x-auto">

                  <table className="w-full text-sm">

                    <thead className="bg-slate-50 border-b border-slate-200 text-slate-600">

                      <tr>

                        <th className="text-left px-5 py-4 font-semibold">
                          User
                        </th>

                        <th className="text-left px-5 py-4 font-semibold">
                          Action
                        </th>

                        <th className="text-left px-5 py-4 font-semibold">
                          Entity
                        </th>

                        <th className="text-left px-5 py-4 font-semibold">
                          Entity ID
                        </th>

                        <th className="text-left px-5 py-4 font-semibold">
                          Time
                        </th>

                      </tr>

                    </thead>

                    <tbody>

                      {logs.map(
                        (log) => (

                          <tr
                            key={log.id}
                            className="border-b border-slate-100 last:border-b-0"
                          >

                            <td className="px-5 py-4 text-slate-700">

                              {getUserLabel(
                                log.user_id
                              )}

                            </td>

                            <td className="px-5 py-4 text-slate-900 font-medium">

                              {log.action}

                            </td>

                            <td className="px-5 py-4 text-slate-700 capitalize">

                              {log.entity}

                            </td>

                            <td className="px-5 py-4 text-slate-700">

                              {log.entity_id || "-"}

                            </td>

                            <td className="px-5 py-4 text-slate-500">

                              {formatDateTime(
                                log.timestamp
                              )}

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

    </div>
  )
}
