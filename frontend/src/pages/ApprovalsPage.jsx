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

  const token =
    localStorage.getItem("token")

  const user =
    JSON.parse(
      localStorage.getItem("user")
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
          response.data
        )

      } catch (error) {

        console.error(error)
      }
    }


  useEffect(() => {

    fetchApprovals()

  }, [])


  const handleAction =
    async (
      approvalId,
      status
    ) => {

      try {

        let remarks =
          "Approved by manager"

        if (
          status === "rejected"
        ) {

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

        if (
          status === "hold"
        ) {

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


  return (

    <div className="min-h-screen bg-gradient-to-br from-slate-100 via-cyan-50 to-teal-100">

      <Navbar
        user={user}
        handleLogout={() => {

          localStorage.clear()

          window.location.href = "/"
        }}
      />

      <div className="max-w-6xl mx-auto px-6 py-10">

        <div className="mb-8">

          <h1 className="text-3xl font-bold text-gray-800">

            Pending Approvals

          </h1>

        </div>

        <div className="space-y-6">

          {approvals.length > 0 ? (

            approvals.map(
              (approval) => (

                <div
                  key={approval.id}
                  className="bg-white rounded-2xl shadow-lg p-6"
                >

                  <div className="flex justify-between items-start gap-6">

                    <div>

                      <h2 className="text-xl font-bold text-gray-800">

                        Approval Request
                        {" "}
                        #{approval.id}

                      </h2>

                      <p className="text-gray-600 mt-2">

                        Task ID:
                        {" "}
                        {approval.task_id}

                      </p>

                      <div className="mt-4 flex flex-col gap-3">

                        <span className="bg-yellow-100 text-yellow-700 px-3 py-1 rounded-full text-sm w-fit">

                          {approval.status}

                        </span>

                        {approval.remarks && (

                          <div className="bg-slate-100 border border-slate-200 rounded-xl p-3">

                            <p className="text-xs font-semibold text-gray-500 mb-1">

                              Remarks

                            </p>

                            <p className="text-sm text-gray-700">

                              {approval.remarks}

                            </p>

                          </div>
                        )}

                      </div>

                    </div>

                    <div className="flex gap-3 flex-wrap">

                      <button
                        onClick={() =>
                          handleAction(
                            approval.id,
                            "approved"
                          )
                        }
                        className="bg-green-600 hover:bg-green-700 text-white px-5 py-2 rounded-xl font-semibold"
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
                        className="bg-yellow-500 hover:bg-yellow-600 text-white px-5 py-2 rounded-xl font-semibold"
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

                  </div>

                </div>
              )
            )

          ) : (

            <div className="bg-white rounded-2xl shadow-lg p-10 text-center text-gray-500">

              No pending approvals

            </div>
          )}

        </div>

      </div>

    </div>
  )
}
