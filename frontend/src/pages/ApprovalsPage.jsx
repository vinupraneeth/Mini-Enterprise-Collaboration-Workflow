import {
  useEffect,
  useState
} from "react"

import axios from "axios"

import Navbar from "../components/Navbar"


export default function ApprovalsPage() {

  const [approvals,
    setApprovals] =
    useState([])

  const [title,
    setTitle] =
    useState("")

  const [description,
    setDescription] =
    useState("")

  const [loading,
    setLoading] =
    useState(false)

  const token =
    localStorage.getItem("token")

  const [user,
    setUser] =
    useState(
      JSON.parse(
        localStorage.getItem("user")
      )
    )


  const fetchApprovals =
    async () => {

      try {

        const response =
          await axios.get(
            "http://127.0.0.1:8000/approvals/",
            {
              headers: {
                Authorization:
                  `Bearer ${token}`
              }
            }
          )

        setApprovals(
          response.data.items ||
          response.data
        )

      } catch (error) {

        console.error(error)
      }
    }


  useEffect(() => {

    fetchCurrentUser()

    fetchApprovals()

  }, [])


  const fetchCurrentUser =
    async () => {

      try {

        const response =
          await axios.get(
            "http://127.0.0.1:8000/auth/me",
            {
              headers: {
                Authorization:
                  `Bearer ${token}`
              }
            }
          )

        localStorage.setItem(
          "user",
          JSON.stringify(response.data)
        )

        setUser(response.data)

      } catch (error) {

        console.error(error)
      }
    }


  const handleCreateApproval =
    async (e) => {

      e.preventDefault()

      if (!title.trim()) {

        alert("Approval title is required")

        return
      }

      try {

        setLoading(true)

        await axios.post(
          "http://127.0.0.1:8000/approvals/",
          {
            title,
            description,
            task_id: null
          },
          {
            headers: {
              Authorization:
                `Bearer ${token}`
            }
          }
        )

        setTitle("")

        setDescription("")

        fetchApprovals()

      } catch (error) {

        console.error(error)

        alert(
          error.response?.data?.detail ||
          "Approval request failed"
        )

      } finally {

        setLoading(false)
      }
    }


  const canReviewApproval =
    (approval) => {

      if (approval.requested_by === user?.id) {

        return false
      }

      if (
        user?.role === "manager" &&
        approval.current_level === "manager"
      ) {

        return true
      }

      if (
        user?.role === "admin" &&
        approval.current_level === "admin"
      ) {

        return true
      }

      return false
    }


  const handleAction =
    async (
      approvalId,
      status
    ) => {

      try {

        let remarks =
          user?.role === "admin"
            ? "Approved by admin"
            : "Approved by manager"

        if (status === "rejected") {

          remarks =
            prompt(
              "Enter rejection remarks"
            )

          if (
            !remarks ||
            !remarks.trim()
          ) {

            alert(
              "Remarks are mandatory for rejection"
            )

            return
          }
        }

        if (status === "hold") {

          remarks =
            prompt(
              "Enter hold remarks"
            ) || "Approval placed on hold"
        }

        await axios.patch(
          `http://127.0.0.1:8000/approvals/${approvalId}/action`,
          {
            action:
              status === "approved"
                ? "approve"
                : status === "rejected"
                  ? "reject"
                  : "hold",
            comment: remarks
          },
          {
            headers: {
              Authorization:
                `Bearer ${token}`
            }
          }
        )

        fetchApprovals()

      } catch (error) {

        console.error(error)

        alert(
          error.response?.data?.detail ||
          `${status} failed`
        )
      }
    }


  const myApprovals = approvals.filter(
    (approval) =>
      approval.requested_by === user?.id
  )

  const approvalRecords = approvals.filter(
    (approval) =>
      approval.requested_by !== user?.id
  )


  const renderApprovalCard =
    (approval) => (

      <div
        key={approval.id}
        className="bg-white border border-slate-200 rounded-2xl shadow-sm p-6"
      >

        <div className="flex flex-col lg:flex-row lg:justify-between lg:items-start gap-6">

          <div>

            <div className="flex flex-wrap items-center gap-3">

              <h3 className="text-xl font-bold text-slate-900">

                {approval.title}

              </h3>

              <span className="bg-slate-100 text-slate-700 px-3 py-1 rounded-full text-sm">

                #{approval.id}

              </span>

            </div>

            <p className="text-slate-600 mt-3">

              {approval.description ||
                "No description provided"}

            </p>

            <div className="mt-4 flex flex-wrap gap-3">

              <span className="bg-amber-100 text-amber-800 px-3 py-1 rounded-full text-sm">

                {approval.status}

              </span>

              <span className="bg-indigo-100 text-indigo-800 px-3 py-1 rounded-full text-sm">

                Level:
                {" "}
                {approval.current_level}

              </span>

              <span className="bg-slate-100 text-slate-700 px-3 py-1 rounded-full text-sm">

                {approval.task_id
                  ? `Task #${approval.task_id}`
                  : "General request"}

              </span>

              <span className="bg-slate-100 text-slate-700 px-3 py-1 rounded-full text-sm">

                Requested by:
                {" "}
                #{approval.requested_by}

              </span>

            </div>

            {approval.remarks && (

              <div className="bg-slate-100 border border-slate-200 rounded-xl p-3 mt-4">

                <p className="text-xs font-semibold text-slate-500 mb-1">

                  Remarks

                </p>

                <p className="text-sm text-slate-700">

                  {approval.remarks}

                </p>

              </div>
            )}

          </div>

          {canReviewApproval(approval) && (

            <div className="flex gap-3 flex-wrap">

              <button
                onClick={() =>
                  handleAction(
                    approval.id,
                    "approved"
                  )
                }
                className="bg-emerald-700 hover:bg-emerald-800 text-white px-5 py-2 rounded-xl font-semibold"
              >

                Approve

              </button>

              <button
                onClick={() =>
                  handleAction(
                    approval.id,
                    "hold"
                  )
                }
                className="bg-amber-500 hover:bg-amber-600 text-white px-5 py-2 rounded-xl font-semibold"
              >

                Hold

              </button>

              <button
                onClick={() =>
                  handleAction(
                    approval.id,
                    "rejected"
                  )
                }
                className="bg-red-600 hover:bg-red-700 text-white px-5 py-2 rounded-xl font-semibold"
              >

                Reject

              </button>

            </div>
          )}

        </div>

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

      <div className="max-w-6xl mx-auto px-6 py-10">

        <div className="bg-white border border-slate-200 rounded-2xl shadow-sm px-6 py-5 mb-8">

          <h1 className="text-3xl font-bold text-slate-900">

            Approvals

          </h1>

          <p className="text-slate-500 mt-1">

            Raise requests and track approval status

          </p>

        </div>

        {user?.role !== "admin" && (

          <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-6 mb-8">

            <h2 className="text-xl font-bold text-slate-900 mb-1">

              Create Approval Request

            </h2>

            <p className="text-sm text-slate-500 mb-5">

            Use this for requests like laptop access, leave approval, purchase approval, or other internal approvals. General requests are sent to Admin.

            </p>

            <form
              onSubmit={handleCreateApproval}
              className="grid grid-cols-1 md:grid-cols-[1fr_1fr_auto] gap-4 items-end"
            >

              <div>

                <label className="block text-sm font-semibold text-slate-700 mb-2">

                  Title

                </label>

                <input
                  type="text"
                  value={title}
                  onChange={(e) =>
                    setTitle(
                      e.target.value
                    )
                  }
                  placeholder="Laptop request"
                  className="w-full border border-slate-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-slate-300"
                />

              </div>

              <div>

                <label className="block text-sm font-semibold text-slate-700 mb-2">

                  Description

                </label>

                <input
                  type="text"
                  value={description}
                  onChange={(e) =>
                    setDescription(
                      e.target.value
                    )
                  }
                  placeholder="Reason for the request"
                  className="w-full border border-slate-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-slate-300"
                />

              </div>

              <button
                type="submit"
                disabled={loading}
                className="bg-slate-900 hover:bg-slate-800 disabled:bg-slate-400 text-white px-6 py-3 rounded-xl font-semibold shadow-sm"
              >

                {loading
                  ? "Submitting..."
                  : "Submit"}

              </button>

            </form>

          </div>
        )}

        {user?.role !== "admin" && (

          <div className="mb-10">

            <h2 className="text-xl font-bold text-slate-900 mb-4">

              My Requests

            </h2>

            <div className="space-y-6">

              {myApprovals.length > 0 ? (

                myApprovals.map(
                  renderApprovalCard
                )

              ) : (

                <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-8 text-center text-slate-500">

                  No requests raised by you

                </div>
              )}

            </div>

          </div>
        )}

        <div>

          <h2 className="text-xl font-bold text-slate-900 mb-4">

            Approval Records

          </h2>

          <div className="space-y-6">

            {approvalRecords.length > 0 ? (

              approvalRecords.map(
                renderApprovalCard
              )

            ) : (

              <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-8 text-center text-slate-500">

                No approval records available

              </div>
            )}

          </div>

        </div>

      </div>

    </div>
  )
}
