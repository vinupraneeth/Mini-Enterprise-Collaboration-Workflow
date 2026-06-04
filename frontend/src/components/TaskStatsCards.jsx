function TaskStatsCards({
  stats
}) {

const cards = [

  {
    title: "Total Tasks",
    value: stats.total,
    color:
      "from-cyan-500 to-blue-700"
  },

  {
    title: "Todo",
    value: stats.todo,
    color:
      "from-slate-500 to-slate-700"
  },

  {
    title: "In Progress",
    value: stats.inProgress,
    color:
      "from-orange-400 to-amber-600"
  },

  {
    title: "Completed",
    value: stats.done,
    color:
      "from-emerald-500 to-green-700"
  }
]

  return (

    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 mb-6">

      {
        cards.map((card) => (

          <div
            key={card.title}
            className={`bg-gradient-to-r ${card.color} rounded-xl p-5 text-white shadow-sm`}
          >

            <p className="text-sm opacity-90">
              {card.title}
            </p>

            <h2 className="text-4xl font-bold mt-3">
              {card.value}
            </h2>

          </div>
        ))
      }

    </div>
  );
}

export default TaskStatsCards;
