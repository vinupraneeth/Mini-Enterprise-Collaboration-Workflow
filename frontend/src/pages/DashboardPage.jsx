import {
  useEffect,
  useState
} from "react";

import {
  useNavigate
} from "react-router-dom";

import api from "../api/axios";

import Navbar from "../components/Navbar";

import CreateTaskForm from "../components/CreateTaskForm";

import EditTaskModal from "../components/EditTaskModal";

import TaskStatsCards from "../components/TaskStatsCards";

import EmptyState from "../components/EmptyState";


function DashboardPage() {

  const [user, setUser] =
    useState(null);

  const [tasks, setTasks] =
    useState([]);

  const [statusMap, setStatusMap] =
    useState({});

  const [editingTask, setEditingTask] =
    useState(null);

  const [stats, setStats] =
    useState({

      total: 0,

      todo: 0,

      inProgress: 0,

      done: 0
    });

  const navigate = useNavigate();


  useEffect(() => {

    fetchCurrentUser();

    fetchTasks();

  }, []);


  const fetchCurrentUser = async () => {

    try {

      const token = localStorage.getItem(
        "token"
      );

      const response = await api.get(

        "/auth/me",

        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }
      );

      setUser(response.data);

    } catch (error) {

      console.log(error);
    }
  };


  const fetchTasks = async () => {

    try {

      const token = localStorage.getItem(
        "token"
      );

      const response = await api.get(

        "/tasks",

        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }
      );

      setTasks(response.data);

      calculateStats(
        response.data
      );

    } catch (error) {

      console.log(error);
    }
  };


  const calculateStats = (
    taskData
  ) => {

    const total =
      taskData.length;

    const todo =
      taskData.filter(
        (task) =>
          task.status === "todo"
      ).length;

    const inProgress =
      taskData.filter(
        (task) =>
          task.status ===
          "in_progress"
      ).length;

    const done =
      taskData.filter(
        (task) =>
          task.status === "done"
      ).length;

    setStats({

      total,

      todo,

      inProgress,

      done
    });
  };


  const handleStatusChange = (
    taskId,
    value
  ) => {

    setStatusMap({

      ...statusMap,

      [taskId]: value
    });
  };


  const updateTaskStatus = async (
    taskId
  ) => {

    try {

      const token = localStorage.getItem(
        "token"
      );

      await api.patch(

        `/tasks/${taskId}/status`,

        {
          status:
            statusMap[taskId]
        },

        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }
      );

      fetchTasks();

    } catch (error) {

      console.log(error);
    }
  };


  const deleteTask = async (
    taskId
  ) => {

    const confirmDelete =
      window.confirm(
        "Delete this task?"
      );

    if (!confirmDelete) {

      return;
    }

    try {

      const token = localStorage.getItem(
        "token"
      );

      await api.delete(

        `/tasks/${taskId}`,

        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }
      );

      fetchTasks();

    } catch (error) {

      console.log(error);
    }
  };


  const handleLogout = () => {

    localStorage.removeItem(
      "token"
    );

    navigate("/");
  };


  const getStatusColor = (
    status
  ) => {

    if (status === "done") {

      return "bg-green-100 text-green-700";
    }

    if (
      status === "in_progress"
    ) {

      return "bg-yellow-100 text-yellow-700";
    }

    return "bg-gray-200 text-gray-700";
  };


  const getPriorityColor = (
    priority
  ) => {

    if (priority === "high") {

      return "bg-red-100 text-red-700";
    }

    if (priority === "medium") {

      return "bg-blue-100 text-blue-700";
    }

    return "bg-green-100 text-green-700";
  };


  return (

    <div className="min-h-screen bg-gradient-to-br from-slate-100 via-cyan-50 to-teal-100">

      <Navbar
        user={user}
        handleLogout={handleLogout}
      />

      <div className="max-w-7xl mx-auto px-8 py-8">

        <TaskStatsCards
          stats={stats}
        />

        {
          user &&
          (
            user.role === "admin"
            ||
            user.role === "manager"
          )
          &&
          (
            <CreateTaskForm
              fetchTasks={fetchTasks}
              currentUser={user}
            />
          )
        }

        {
          tasks.length === 0

          ?

          (

            <EmptyState />

          )

          :

          (

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-7">

              {
                tasks.map((task) => (

                  <div
                    key={task.id}
                    className="bg-white rounded-3xl shadow-lg p-7 hover:shadow-2xl hover:-translate-y-1 transition duration-300 border border-gray-100"
                  >

                    <div className="flex justify-between items-start gap-4">

                      <div>

                        <h2 className="text-2xl font-bold text-gray-800">
                          {task.title}
                        </h2>

                        <p className="text-gray-500 mt-3 leading-7">
                          {
                            task.description
                            ||
                            "No description provided"
                          }
                        </p>

                      </div>

                      <div className="flex flex-col gap-2">

                        <span
                          className={`px-4 py-1 rounded-full text-sm font-semibold text-center ${getStatusColor(task.status)}`}
                        >
                          {task.status}
                        </span>

                        <span
                          className={`px-4 py-1 rounded-full text-sm font-semibold text-center capitalize ${getPriorityColor(task.priority)}`}
                        >
                          {task.priority}
                        </span>

                      </div>

                    </div>

                    <div className="mt-7 grid grid-cols-2 gap-6">

                      <div className="bg-gray-50 rounded-2xl p-4">

                        <p className="text-gray-400 text-sm">
                          Due Date
                        </p>

                        <p className="font-semibold text-gray-800 mt-2">

                          {
                            task.due_date
                            ?
                            new Date(
                              task.due_date
                            ).toLocaleDateString()
                            :
                            "N/A"
                          }

                        </p>

                      </div>

                      <div className="bg-gray-50 rounded-2xl p-4">

                        <p className="text-gray-400 text-sm">
                          Task ID
                        </p>

                        <p className="font-semibold text-gray-800 mt-2">
                          #{task.id}
                        </p>

                      </div>

                    </div>

                    <div className="mt-7 flex flex-wrap gap-3">

                      <select

                        value={
                          statusMap[task.id]
                          || task.status
                        }

                        onChange={(e) =>
                          handleStatusChange(
                            task.id,
                            e.target.value
                          )
                        }

                        className="border border-gray-300 rounded-xl px-4 py-3 bg-white"
                      >

                        <option value="todo">
                          Todo
                        </option>

                        <option value="in_progress">
                          In Progress
                        </option>

                        <option value="done">
                          Done
                        </option>

                      </select>

                      <button

                        onClick={() =>
                          updateTaskStatus(
                            task.id
                          )
                        }

                        className="bg-teal-600 hover:bg-teal-700 text-white px-5 py-3 rounded-xl transition shadow-md"
                      >
                        Update
                      </button>

                      {
                        (
                          user.role === "admin"
                          ||
                          user.role ===
                          "manager"
                        )
                        &&
                        (
                          <>

                            <button

                              onClick={() =>
                                setEditingTask(task)
                              }

                              className="bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-3 rounded-xl transition shadow-md"
                            >
                              Edit
                            </button>

                            <button

                              onClick={() =>
                                deleteTask(
                                  task.id
                                )
                              }

                              className="bg-red-500 hover:bg-red-600 text-white px-5 py-3 rounded-xl transition shadow-md"
                            >
                              Delete
                            </button>

                          </>
                        )
                      }

                    </div>

                  </div>
                ))
              }

            </div>
          )
        }

      </div>

      {
        editingTask && (

          <EditTaskModal

            task={editingTask}

            closeModal={() =>
              setEditingTask(null)
            }

            fetchTasks={fetchTasks}

          />
        )
      }

    </div>
  );
}

export default DashboardPage;