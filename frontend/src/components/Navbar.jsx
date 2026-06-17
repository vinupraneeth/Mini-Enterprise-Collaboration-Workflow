import {
  useEffect,
  useState
} from "react"

import { Link } from "react-router-dom"

import axios from "axios"


function Navbar({

  user,

  handleLogout
}) {

  const isAdmin =
    user?.role === "admin"

  const isManager =
    user?.role === "manager"

  const isAuditor =
    user?.role === "auditor"

  const canViewGovernance =
    isAdmin ||
    isManager ||
    isAuditor

  const [attention,
    setAttention] =
    useState({
      approvals: false,
      escalations: false,
      delegations: false
    })

  const token =
    localStorage.getItem("token")

  const hasApprovalAttention =
    (approval) => {

      if (isAdmin) {

        return (
          approval.current_level === "admin" &&
          [
            "pending",
            "hold",
            "manager_approved"
          ].includes(approval.status)
        )
      }

      if (isManager) {

        return (
          approval.current_level === "manager" &&
          approval.requested_by !== user?.id &&
          [
            "pending",
            "hold"
          ].includes(approval.status)
        )
      }

      return (
        approval.requested_by === user?.id &&
        approval.current_level !== "completed" &&
        [
          "pending",
          "hold",
          "manager_approved"
        ].includes(approval.status)
      )
    }

  const showDot =
    (enabled) => (

      enabled ? (

        <span className="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full bg-red-500 border border-white" />
      ) : null
    )

  useEffect(() => {

    if (!token || !user) {

      return
    }

    const headers = {
      Authorization:
        `Bearer ${token}`
    }

    const fetchAttention =
      async () => {

        try {

          const nextAttention = {
            approvals: false,
            escalations: false,
            delegations: false
          }

          if (!isAuditor) {

            const approvalsResponse =
              await axios.get(
                "http://127.0.0.1:8000/approvals/?page=1&size=100",
                { headers }
              )

            const approvalItems =
              approvalsResponse.data.items ||
              approvalsResponse.data

            nextAttention.approvals =
              approvalItems.some(
                hasApprovalAttention
              )
          }

          if (canViewGovernance) {

            const escalationResponse =
              await axios.get(
                "http://127.0.0.1:8000/approval-escalations/pending?page=1&size=100",
                { headers }
              )

            nextAttention.escalations =
              (
                escalationResponse.data.items ||
                escalationResponse.data
              ).length > 0
          }

          if (isAdmin || isManager) {

            const delegationResponse =
              await axios.get(
                "http://127.0.0.1:8000/approval-delegations/me?page=1&size=100",
                { headers }
              )

            nextAttention.delegations =
              (
                delegationResponse.data.items ||
                delegationResponse.data
              ).some(
                (delegation) =>
                  delegation.is_active
              )
          }

          setAttention(nextAttention)

        } catch (error) {

          console.error(error)
        }
      }

    fetchAttention()

  }, [user?.id, user?.role])

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

          {user && user.role !== "auditor" && (

            <Link
              to="/approvals"
              className="relative bg-white hover:bg-slate-50 text-slate-800 border border-slate-300 px-4 py-2 rounded-xl font-semibold transition"
            >

              Approvals

              {showDot(attention.approvals)}

            </Link>
          )}

          {canViewGovernance && (

            <Link
              to="/dashboard/sla"
              className="bg-white hover:bg-slate-50 text-slate-800 border border-slate-300 px-4 py-2 rounded-xl font-semibold transition"
            >

              SLA Dashboard

            </Link>
          )}

          {isAdmin && (

            <Link
              to="/sla-rules"
              className="bg-white hover:bg-slate-50 text-slate-800 border border-slate-300 px-4 py-2 rounded-xl font-semibold transition"
            >

              SLA Rules

            </Link>
          )}

          {canViewGovernance && (

            <Link
              to="/approval-escalations"
              className="relative bg-white hover:bg-slate-50 text-slate-800 border border-slate-300 px-4 py-2 rounded-xl font-semibold transition"
            >

              Escalations

              {showDot(attention.escalations)}

            </Link>
          )}

          {(isAdmin || isManager) && (

            <Link
              to="/approval-delegations"
              className="relative bg-white hover:bg-slate-50 text-slate-800 border border-slate-300 px-4 py-2 rounded-xl font-semibold transition"
            >

              Delegations

              {showDot(attention.delegations)}

            </Link>
          )}

          {user && (

            <Link
              to="/settings/notification-preferences"
              className="bg-white hover:bg-slate-50 text-slate-800 border border-slate-300 px-4 py-2 rounded-xl font-semibold transition"
            >

              Preferences

            </Link>
          )}

          {isAdmin && (

            <Link
              to="/subscription-plans"
              className="bg-white hover:bg-slate-50 text-slate-800 border border-slate-300 px-4 py-2 rounded-xl font-semibold transition"
            >

              Subscription

            </Link>
          )}

          {(isAdmin || isAuditor) && (

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
