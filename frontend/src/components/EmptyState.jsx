function EmptyState() {

  return (

    <div className="bg-white rounded-3xl shadow-lg p-16 text-center border border-gray-100">

      <div className="w-24 h-24 bg-blue-100 rounded-full flex items-center justify-center mx-auto">

        <span className="text-5xl">
          📋
        </span>

      </div>

      <h2 className="text-3xl font-bold text-gray-800 mt-8">

        No Tasks Found

      </h2>

      <p className="text-gray-500 mt-4 max-w-md mx-auto leading-7">

        There are currently no workflow tasks available.
        Create and assign tasks to start managing your enterprise workflow efficiently.

      </p>

    </div>
  );
}

export default EmptyState;