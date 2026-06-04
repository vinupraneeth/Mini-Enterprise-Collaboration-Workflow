import { useEffect, useState } from "react"

import { useNavigate } from "react-router-dom"

import axios from "axios"

import Navbar from "../components/Navbar"

import TaskStatsCards from "../components/TaskStatsCards"

import CreateTaskForm from "../components/CreateTaskForm"

import EditTaskModal from "../components/EditTaskModal"

import KanbanBoard from "../components/KanbanBoard"

import DashboardAnalytics from "../components/DashboardAnalytics"

import AiSummaryPanel from "../components/AiSummaryPanel"

import NotificationsPanel from "../components/NotificationsPanel"

import ActivityFeedPanel from "../components/ActivityFeedPanel"


export default function DashboardPage() {

  const navigate = useNavigate()

  const [tasks, setTasks] = useState([])

  const [loading, setLoading] =
    useState(true)

  const [analytics, setAnalytics] =
    useState(null)

  const [isModalOpen, setIsModalOpen] =
    useState(false)

  const [editingTask, setEditingTask] =
    useState(null)

  const token =
    localStorage.getItem("token")

  const storedUser =
    localStorage.getItem("user")

  const user = storedUser
    ? JSON.parse(storedUser)
    : null


  const fetchDashboardAnalytics =
    async () => {

      try {

        const response =
          await axios.get(

            "http://127.0.0.1:8000/dashboard/analytics",

            {
              headers: {
                Authorization:
                  `Bearer ${token}`
              }
            }
          )

        setAnalytics(response.data)

      } catch (error) {

        console.error(error)
      }
    }


  const fetchTasks = async () => {

    try {

      const response =
        await axios.get(

          "http://127.0.0.1:8000/tasks/",

          {
            headers: {
              Authorization:
                `Bearer ${token}`
            }
          }
        )

      setTasks(
        response.data.items ||
        response.data
      )

      fetchDashboardAnalytics()

    } catch (error) {

      console.error(error)

    } finally {

      setLoading(false)
    }
  }


  useEffect(() => {

    if (!token) {

      navigate("/")

      return
    }

    fetchTasks()

  }, [])


  const handleLogout = () => {

    localStorage.removeItem("token")

    localStorage.removeItem("user")

    navigate("/")
  }


  const handleDelete =
    async (taskId) => {

      const confirmDelete =
        window.confirm(
          "Delete this task?"
        )

      if (!confirmDelete) return

      try {

        await axios.delete(

          `http://127.0.0.1:8000/tasks/${taskId}`,

          {
            headers: {
              Authorization:
                `Bearer ${token}`
            }
          }
        )

        setTasks((prevTasks) =>

          prevTasks.filter(
            (task) =>
              task.id !== taskId
          )
        )

        fetchDashboardAnalytics()

      } catch (error) {

        console.error(error)

        alert(
          error.response?.data?.detail ||
          "Delete failed"
        )
      }
    }


  const handleEdit = (task) => {

    setEditingTask(task)

    setIsModalOpen(true)
  }


  const handleCreate = () => {

    setEditingTask(null)

    setIsModalOpen(true)
  }


  const handleStatusChange =
    async (taskId, status) => {

      try {

        await axios.patch(

          `http://127.0.0.1:8000/tasks/${taskId}/status`,

          {
            status
          },

          {
            headers: {
              Authorization:
                `Bearer ${token}`
            }
          }
        )

        setTasks((prevTasks) =>

          prevTasks.map((task) =>

            task.id === taskId
              ? {
                  ...task,
                  status
                }
              : task
          )
        )

        fetchDashboardAnalytics()

      } catch (error) {

        console.error(error)

        alert(
          error.response?.data?.detail ||
          "Status update failed"
        )
      }
    }


  const stats = {

    total: tasks.length,

    todo: tasks.filter(
      (task) =>
        task.status === "todo"
    ).length,

    inProgress: tasks.filter(
      (task) =>
        task.status ===
        "in_progress"
    ).length,

    review: tasks.filter(
      (task) =>
        task.status === "review"
    ).length,

    done: tasks.filter(
      (task) =>
        task.status === "done"
    ).length
  }


  return (

    <div className="min-h-screen bg-slate-100">

      <Navbar
        user={user}
        handleLogout={handleLogout}
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">

        <div className="bg-white border border-slate-200 rounded-xl shadow-sm px-6 py-5 flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">

          <div>

            <h1 className="text-3xl font-bold text-slate-900">

              Workflow Dashboard

            </h1>

            <p className="text-slate-500 mt-1">

              Manage enterprise workflow tasks

            </p>

          </div>

          {(user?.role === "admin" ||
            user?.role === "manager") && (

            <button
              onClick={handleCreate}
              className="bg-slate-900 hover:bg-slate-800 text-white px-6 py-3 rounded-xl font-semibold shadow-sm transition"
            >

              Create Task

            </button>
          )}
        </div>

        <TaskStatsCards
          stats={stats}
        />

        <div className="grid grid-cols-1 xl:grid-cols-[minmax(0,1fr)_360px] gap-6 mt-6 items-start">

          <div className="space-y-6 min-w-0">

            <DashboardAnalytics
              stats={stats}
              analytics={analytics}
            />

            <AiSummaryPanel />

          </div>

          <NotificationsPanel
            user={user}
          />

        </div>

        <div className="mt-8">

          <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-3 mb-4">

            <div>

              <h2 className="text-2xl font-bold text-slate-900">

                Task Board

              </h2>

              <p className="text-sm text-slate-500 mt-1">

                Track assigned work from creation to completion

              </p>

            </div>

          </div>

          {loading ? (

            <div className="text-center py-20 text-gray-500">

              Loading tasks...

            </div>

          ) : (

            <KanbanBoard

              tasks={tasks}

              user={user}

              onEdit={handleEdit}

              onDelete={handleDelete}

              onStatusChange={
                handleStatusChange
              }
            />
          )}
        </div>

        <ActivityFeedPanel />
      </div>

      {isModalOpen && !editingTask && (

        <div className="fixed inset-0 bg-slate-950/50 flex justify-center items-center z-50 px-4">

          <div className="bg-white w-full max-w-2xl rounded-2xl shadow-2xl p-6 max-h-[90vh] overflow-y-auto">

            <div className="flex items-center justify-between mb-6">

              <div>

                <h2 className="text-2xl font-bold text-slate-900">

                  Create Task

                </h2>

                <p className="text-sm text-slate-500 mt-1">

                  Add a new workflow task and assign ownership

                </p>

              </div>

              <button
                onClick={() =>
                  setIsModalOpen(false)
                }
                className="text-slate-500 hover:text-red-600 text-xl"
              >

                x

              </button>

            </div>

            <CreateTaskForm

              closeModal={() =>
                setIsModalOpen(false)
              }

              fetchTasks={() => {

                fetchTasks()

                setIsModalOpen(false)
              }}
            />

          </div>

        </div>
      )}

      {isModalOpen && editingTask && (

        <EditTaskModal

          task={editingTask}

          closeModal={() => {

            setIsModalOpen(false)

            setEditingTask(null)
          }}

          fetchTasks={() => {

            fetchTasks()

            setIsModalOpen(false)

            setEditingTask(null)
          }}
        />
      )}
    </div>
  )
}
