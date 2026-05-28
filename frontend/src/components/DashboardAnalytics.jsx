export default function DashboardAnalytics({

  stats

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


  return (

    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">

      <div className="bg-white rounded-2xl shadow-lg p-6">

        <h3 className="text-sm font-semibold text-gray-500 mb-3">

          Completion Rate

        </h3>

        <p className="text-4xl font-bold text-green-600">

          {completionRate}%

        </p>

      </div>

      <div className="bg-white rounded-2xl shadow-lg p-6">

        <h3 className="text-sm font-semibold text-gray-500 mb-3">

          Pending Tasks

        </h3>

        <p className="text-4xl font-bold text-yellow-600">

          {pendingTasks}

        </p>

      </div>

      <div className="bg-white rounded-2xl shadow-lg p-6">

        <h3 className="text-sm font-semibold text-gray-500 mb-3">

          Tasks Under Review

        </h3>

        <p className="text-4xl font-bold text-indigo-600">

          {stats.review}

        </p>

      </div>

    </div>
  )
}