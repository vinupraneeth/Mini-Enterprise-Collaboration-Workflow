export default function DashboardAnalytics({

  stats,

  analytics

}) {

  const pendingTasks =

    stats.todo +

    stats.inProgress +

    stats.review


  const completionRate =

    stats.total > 0

      ? Math.round(
          (stats.done / stats.total) * 100
        )

      : 0

  const pendingApprovals =
    analytics?.approvals?.pending ?? 0


  return (

    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">

      <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-6">

        <h3 className="text-sm font-semibold text-gray-500 mb-3">

          Completion Rate

        </h3>

        <p className="text-4xl font-bold text-emerald-700">

          {completionRate}%

        </p>

      </div>

      <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-6">

        <h3 className="text-sm font-semibold text-gray-500 mb-3">

          Pending Tasks

        </h3>

        <p className="text-4xl font-bold text-amber-700">

          {pendingTasks}

        </p>

      </div>

      <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-6">

        <h3 className="text-sm font-semibold text-gray-500 mb-3">

          Pending Approvals

        </h3>

        <p className="text-4xl font-bold text-indigo-600">

          {pendingApprovals}

        </p>

      </div>

    </div>
  )
}
