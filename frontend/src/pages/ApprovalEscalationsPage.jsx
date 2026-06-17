import {
  useEffect,
  useState
} from "react"

import axios from "axios"

import Navbar from "../components/Navbar"


export default function ApprovalEscalationsPage() {

  const [escalations,
    setEscalations] =
    useState([])

  const [approvals,
    setApprovals] =
    useState([])

  const [approvers,
    setApprovers] =
    useState([])

  const [form,
    setForm] =
    useState({
      approval_id: "",
      escalated_to: "",
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

  const canView =
    [
      "admin",
      "manager",
      "auditor"
    ].includes(user?.role)

  const canManage =
    [
      "admin",
      "manager"
    ].includes(user?.role)

  const canCreateEscalation =
    user?.role === "manager"


  const headers = {
    Authorization:
      `Bearer ${token}`
  }


  const fetchEscalations =
    async () => {

      try {

        setLoading(true)

        const response =
          await axios.get(
            "http://127.0.0.1:8000/approval-escalations/?page=1&size=100",
            { headers }
          )

        setEscalations(
          response.data.items ||
          response.data
        )

      } catch (error) {

        console.error(error)

        setMessage(
          error.response?.data?.detail ||
          "Unable to load escalations"
        )

      } finally {

        setLoading(false)
      }
    }


  const fetchFormData =
    async () => {

      if (!canCreateEscalation) {

        return
      }

      try {

        const [
          approvalsResponse,
          approversResponse
        ] =
          await Promise.all([
            axios.get(
              "http://127.0.0.1:8000/approvals/?page=1&size=100",
              { headers }
            ),
            axios.get(
              "http://127.0.0.1:8000/users/approvers?page=1&size=100",
              { headers }
            )
          ])

        setApprovals(
          (
            approvalsResponse.data.items ||
            approvalsResponse.data
          ).filter(
            (approval) =>
              approval.current_level === "manager" &&
              [
                "pending",
                "hold"
              ].includes(approval.status) &&
              !approval.is_escalated &&
              approval.requested_by !== user?.id
          )
        )

        setApprovers(
          (
            approversResponse.data.items ||
            approversResponse.data
          ).filter(
            (approver) =>
              approver.role === "admin"
          )
        )

      } catch (error) {

        console.error(error)
      }
    }


  useEffect(() => {

    if (canView) {

      fetchEscalations()

      fetchFormData()
    }

  }, [canView])


  const createEscalation =
    async (event) => {

      event.preventDefault()

      if (
        !form.approval_id ||
        !form.escalated_to ||
        !form.reason.trim()
      ) {

        setMessage(
          "Approval, assignee, and reason are required"
        )

        return
      }

      try {

        await axios.post(
          "http://127.0.0.1:8000/approval-escalations/",
          {
            approval_id:
              Number(form.approval_id),
            escalated_to:
              Number(form.escalated_to),
            reason: form.reason
          },
          { headers }
        )

        setForm({
          approval_id: "",
          escalated_to: "",
          reason: ""
        })

        setMessage("Approval escalated")

        fetchEscalations()

      } catch (error) {

        console.error(error)

        setMessage(
          error.response?.data?.detail ||
          "Escalation failed"
        )
      }
    }


  const updateEscalation =
    async (
      escalationId,
      action
    ) => {

      try {

        await axios.put(
          `http://127.0.0.1:8000/approval-escalations/${escalationId}/${action}`,
          {},
          { headers }
        )

        setMessage(
          action === "resolve"
            ? "Escalation resolved"
            : "Escalation cancelled"
        )

        fetchEscalations()

      } catch (error) {

        console.error(error)

        setMessage(
          error.response?.data?.detail ||
          "Escalation update failed"
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
              Approval escalations are not available for your role
            </h1>
          </div>

        ) : (

          <>

            <div className="bg-white border border-slate-200 rounded-xl shadow-sm px-6 py-5 mb-6">
              <h1 className="text-3xl font-bold text-slate-900">
                Approval Escalations
              </h1>
              <p className="text-slate-500 mt-1">
                Track delayed approvals and escalation responsibility
              </p>
            </div>

            {message && (
              <div className="bg-white border border-slate-200 rounded-xl shadow-sm px-5 py-4 mb-6 text-sm text-slate-700">
                {message}
              </div>
            )}

            {canCreateEscalation && (

              <form
                onSubmit={createEscalation}
                className="bg-white border border-slate-200 rounded-xl shadow-sm p-6 mb-6 grid grid-cols-1 md:grid-cols-[1fr_1fr_2fr_auto] gap-4 items-end"
              >

                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">
                    Approval
                  </label>
                  <select
                    value={form.approval_id}
                    onChange={(event) =>
                      setForm({
                        ...form,
                        approval_id:
                          event.target.value
                      })
                    }
                    className="w-full border border-slate-300 rounded-xl px-4 py-3"
                  >
                    <option value="">Select approval</option>
                    {approvals.map(
                      (approval) => (
                        <option
                          key={approval.id}
                          value={approval.id}
                        >
                          #{approval.id} - {approval.title}
                        </option>
                      )
                    )}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">
                    Escalate To Admin
                  </label>
                  <select
                    value={form.escalated_to}
                    onChange={(event) =>
                      setForm({
                        ...form,
                        escalated_to:
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
                    placeholder="Delayed approval follow-up"
                  />
                </div>

                <button
                  type="submit"
                  className="bg-slate-900 hover:bg-slate-800 text-white px-5 py-3 rounded-xl font-semibold"
                >
                  Escalate
                </button>

              </form>
            )}

            <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">

              {loading ? (
                <div className="p-8 text-slate-500">
                  Loading escalations...
                </div>
              ) : escalations.length > 0 ? (

                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead className="bg-slate-50 border-b border-slate-200 text-slate-600">
                      <tr>
                        <th className="text-left px-5 py-4">ID</th>
                        <th className="text-left px-5 py-4">Approval</th>
                        <th className="text-left px-5 py-4">From</th>
                        <th className="text-left px-5 py-4">To</th>
                        <th className="text-left px-5 py-4">Level</th>
                        <th className="text-left px-5 py-4">Status</th>
                        <th className="text-left px-5 py-4">Escalated At</th>
                        <th className="text-left px-5 py-4">Reason</th>
            {canManage && (
                          <th className="text-left px-5 py-4">Actions</th>
                        )}
                      </tr>
                    </thead>
                    <tbody>
                      {escalations.map(
                        (escalation) => (
                          <tr
                            key={escalation.id}
                            className="border-b border-slate-100 last:border-b-0"
                          >
                            <td className="px-5 py-4">#{escalation.id}</td>
                            <td className="px-5 py-4">#{escalation.approval_id}</td>
                            <td className="px-5 py-4">#{escalation.escalated_from}</td>
                            <td className="px-5 py-4">#{escalation.escalated_to}</td>
                            <td className="px-5 py-4">{escalation.escalation_level}</td>
                            <td className="px-5 py-4">
                              <span className={`px-3 py-1 rounded-full text-xs font-semibold ${escalation.status === "pending" ? "bg-orange-100 text-orange-700" : escalation.status === "resolved" ? "bg-emerald-100 text-emerald-700" : "bg-slate-100 text-slate-600"}`}>
                                {escalation.status}
                              </span>
                            </td>
                            <td className="px-5 py-4 text-slate-600">{formatDateTime(escalation.escalated_at)}</td>
                            <td className="px-5 py-4 text-slate-600">{escalation.reason}</td>
                            {canManage && (
                              <td className="px-5 py-4">
                                {escalation.status === "pending" ? (
                                  <div className="flex gap-2">
                                    <button
                                      onClick={() =>
                                        updateEscalation(
                                          escalation.id,
                                          "resolve"
                                        )
                                      }
                                      className="bg-emerald-700 text-white px-3 py-2 rounded-lg text-xs font-semibold"
                                    >
                                      Resolve
                                    </button>
                                    <button
                                      onClick={() =>
                                        updateEscalation(
                                          escalation.id,
                                          "cancel"
                                        )
                                      }
                                      className="bg-red-600 text-white px-3 py-2 rounded-lg text-xs font-semibold"
                                    >
                                      Cancel
                                    </button>
                                  </div>
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
                  No approval escalations found.
                </div>
              )}

            </div>

          </>
        )}

      </div>

    </div>
  )
}
