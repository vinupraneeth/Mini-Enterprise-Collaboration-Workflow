import {
  useEffect,
  useState
} from "react"

import axios from "axios"

import Navbar from "../components/Navbar"


export default function ApprovalDelegationsPage() {

  const [myDelegations,
    setMyDelegations] =
    useState([])

  const [activeDelegations,
    setActiveDelegations] =
    useState([])

  const [approvers,
    setApprovers] =
    useState([])

  const [form,
    setForm] =
    useState({
      delegatee_id: "",
      start_date: "",
      end_date: "",
      reason: ""
    })

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

  const canManage =
    [
      "admin",
      "manager"
    ].includes(user?.role)

  const headers = {
    Authorization:
      `Bearer ${token}`
  }


  const fetchDelegations =
    async () => {

      try {

        setLoading(true)

        const [
          mineResponse,
          activeResponse,
          approversResponse
        ] =
          await Promise.all([
            axios.get(
              "http://127.0.0.1:8000/approval-delegations/me?page=1&size=100",
              { headers }
            ),
            axios.get(
              "http://127.0.0.1:8000/approval-delegations/active?page=1&size=100",
              { headers }
            ),
            axios.get(
              "http://127.0.0.1:8000/users/approvers?page=1&size=100",
              { headers }
            )
          ])

        setMyDelegations(
          mineResponse.data.items ||
          mineResponse.data
        )

        setActiveDelegations(
          activeResponse.data.items ||
          activeResponse.data
        )

        setApprovers(
          (
            approversResponse.data.items ||
            approversResponse.data
          ).filter(
            (approver) =>
              approver.role === user?.role &&
              approver.id !== user?.id
          )
        )

      } catch (error) {

        console.error(error)

        setMessage(
          error.response?.data?.detail ||
          "Unable to load delegations"
        )

      } finally {

        setLoading(false)
      }
    }


  useEffect(() => {

    if (canManage) {

      fetchDelegations()
    }

  }, [canManage])


  const createDelegation =
    async (event) => {

      event.preventDefault()

      if (
        !form.delegatee_id ||
        !form.start_date ||
        !form.end_date ||
        !form.reason.trim()
      ) {

        setMessage(
          "Delegatee, dates, and reason are required"
        )

        return
      }

      if (
        new Date(form.end_date) <=
        new Date(form.start_date)
      ) {

        setMessage(
          "End date must be after start date"
        )

        return
      }

      try {

        await axios.post(
          "http://127.0.0.1:8000/approval-delegations/",
          {
            delegatee_id:
              Number(form.delegatee_id),
            start_date:
              new Date(form.start_date).toISOString(),
            end_date:
              new Date(form.end_date).toISOString(),
            reason: form.reason
          },
          { headers }
        )

        setForm({
          delegatee_id: "",
          start_date: "",
          end_date: "",
          reason: ""
        })

        setMessage("Approval delegation created")

        fetchDelegations()

      } catch (error) {

        console.error(error)

        setMessage(
          error.response?.data?.detail ||
          "Delegation failed"
        )
      }
    }


  const cancelDelegation =
    async (delegationId) => {

      if (!window.confirm("Cancel this delegation?")) {

        return
      }

      try {

        await axios.put(
          `http://127.0.0.1:8000/approval-delegations/${delegationId}/cancel`,
          {},
          { headers }
        )

        setMessage("Delegation cancelled")

        fetchDelegations()

      } catch (error) {

        console.error(error)

        setMessage(
          error.response?.data?.detail ||
          "Unable to cancel delegation"
        )
      }
    }


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


  const renderTable =
    (
      rows,
      title,
      showActions
    ) => (

      <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">

        <div className="px-5 py-4 border-b border-slate-200">
          <h2 className="text-xl font-bold text-slate-900">{title}</h2>
        </div>

        {loading ? (

          <div className="p-8 text-slate-500">
            Loading delegations...
          </div>

        ) : rows.length > 0 ? (

          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-600">
                <tr>
                  <th className="text-left px-5 py-4">Delegator</th>
                  <th className="text-left px-5 py-4">Delegatee</th>
                  <th className="text-left px-5 py-4">Start</th>
                  <th className="text-left px-5 py-4">End</th>
                  <th className="text-left px-5 py-4">Reason</th>
                  <th className="text-left px-5 py-4">Status</th>
                  {showActions && (
                    <th className="text-left px-5 py-4">Actions</th>
                  )}
                </tr>
              </thead>
              <tbody>
                {rows.map(
                  (delegation) => (
                    <tr
                      key={delegation.id}
                      className="border-b border-slate-100 last:border-b-0"
                    >
                      <td className="px-5 py-4">#{delegation.delegator_id}</td>
                      <td className="px-5 py-4">#{delegation.delegatee_id}</td>
                      <td className="px-5 py-4 text-slate-600">{formatDateTime(delegation.start_date)}</td>
                      <td className="px-5 py-4 text-slate-600">{formatDateTime(delegation.end_date)}</td>
                      <td className="px-5 py-4 text-slate-600">{delegation.reason}</td>
                      <td className="px-5 py-4">
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${delegation.is_active ? "bg-emerald-100 text-emerald-700" : "bg-slate-100 text-slate-600"}`}>
                          {delegation.is_active
                            ? "Active"
                            : "Cancelled"}
                        </span>
                      </td>
                      {showActions && (
                        <td className="px-5 py-4">
                          {delegation.is_active ? (
                            <button
                              onClick={() =>
                                cancelDelegation(
                                  delegation.id
                                )
                              }
                              className="bg-red-600 text-white px-3 py-2 rounded-lg text-xs font-semibold"
                            >
                              Cancel
                            </button>
                          ) : "-"}
                        </td>
                      )}
                    </tr>
                  )
                )}
              </tbody>
            </table>
          </div>

        ) : (

          <div className="p-8 text-slate-500">
            No delegations found.
          </div>
        )}

      </div>
    )


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

        {!canManage ? (

          <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-10 text-center">
            <h1 className="text-2xl font-bold text-slate-900">
              Approval delegations are available only for admins and managers
            </h1>
          </div>

        ) : (

          <>

            <div className="bg-white border border-slate-200 rounded-xl shadow-sm px-6 py-5 mb-6">
              <h1 className="text-3xl font-bold text-slate-900">
                Approval Delegations
              </h1>
              <p className="text-slate-500 mt-1">
                Delegate approval responsibility for a selected date range
              </p>
            </div>

            {message && (
              <div className="bg-white border border-slate-200 rounded-xl shadow-sm px-5 py-4 mb-6 text-sm text-slate-700">
                {message}
              </div>
            )}

            <form
              onSubmit={createDelegation}
              className="bg-white border border-slate-200 rounded-xl shadow-sm p-6 mb-6 grid grid-cols-1 md:grid-cols-2 xl:grid-cols-[1fr_1fr_1fr_2fr_auto] gap-4 items-end"
            >
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">
                  Delegatee
                </label>
                <select
                  value={form.delegatee_id}
                  onChange={(event) =>
                    setForm({
                      ...form,
                      delegatee_id:
                        event.target.value
                    })
                  }
                  className="w-full border border-slate-300 rounded-xl px-4 py-3"
                >
                  <option value="">Select user</option>
                  {approvers.map(
                    (approver) => (
                      <option
                        key={approver.id}
                        value={approver.id}
                      >
                        {approver.name} ({approver.role})
                      </option>
                    )
                  )}
                </select>
              </div>

              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">
                  Start
                </label>
                <input
                  type="datetime-local"
                  value={form.start_date}
                  onChange={(event) =>
                    setForm({
                      ...form,
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
                  value={form.end_date}
                  onChange={(event) =>
                    setForm({
                      ...form,
                      end_date:
                        event.target.value
                    })
                  }
                  className="w-full border border-slate-300 rounded-xl px-4 py-3"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">
                  Reason
                </label>
                <input
                  value={form.reason}
                  onChange={(event) =>
                    setForm({
                      ...form,
                      reason:
                        event.target.value
                    })
                  }
                  className="w-full border border-slate-300 rounded-xl px-4 py-3"
                  placeholder="Unavailable for approval review"
                />
              </div>

              <button
                type="submit"
                className="bg-slate-900 hover:bg-slate-800 text-white px-5 py-3 rounded-xl font-semibold"
              >
                Delegate
              </button>
            </form>

            <div className="space-y-6">
              {renderTable(
                myDelegations,
                "My Delegations",
                true
              )}
              {renderTable(
                activeDelegations,
                "Active Delegations",
                false
              )}
            </div>

          </>
        )}

      </div>

    </div>
  )
}
