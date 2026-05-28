import { useEffect, useState } from "react"

import { useNavigate } from "react-router-dom"

import axios from "axios"

import Navbar from "../components/Navbar"

import TaskStatsCards from "../components/TaskStatsCards"

import CreateTaskForm from "../components/CreateTaskForm"

import EditTaskModal from "../components/EditTaskModal"

import KanbanBoard from "../components/KanbanBoard"

import DashboardAnalytics from "../components/DashboardAnalytics"


export default function DashboardPage() {

  const navigate = useNavigate()

  const [tasks, setTasks] = useState([])

  const [loading, setLoading] =
    useState(true)

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

      setTasks(response.data)

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

    <div className="min-h-screen bg-gradient-to-br from-slate-100 via-cyan-50 to-teal-100">

      <Navbar
        user={user}
        handleLogout={handleLogout}
      />

      <div className="max-w-7xl mx-auto px-6 py-8">

        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-8">

          <div>

            <h1 className="text-3xl font-bold text-gray-800">

              Workflow Dashboard

            </h1>

            <p className="text-gray-500 mt-1">

              Manage enterprise workflow tasks

            </p>

          </div>

          {(user?.role === "admin" ||
            user?.role === "manager") && (

            <button
              onClick={handleCreate}
              className="bg-teal-600 hover:bg-teal-700 text-white px-6 py-3 rounded-xl font-semibold shadow-lg transition"
            >

              + Create Task

            </button>
          )}
        </div>

        <TaskStatsCards
          stats={stats}
        />
        <DashboardAnalytics
          stats={stats}
        />

        <div className="mt-10">

          {loading ? (

            <div className="text-center py-20 text-gray-500">

              Loading tasks...

            </div>

          ) : (

            <KanbanBoard

              tasks={tasks}

              onEdit={handleEdit}

              onDelete={handleDelete}

              onStatusChange={
                handleStatusChange
              }
            />
          )}
        </div>
      </div>

      {isModalOpen && !editingTask && (

        <CreateTaskForm

          closeModal={() =>
            setIsModalOpen(false)
          }

          fetchTasks={() => {

            fetchTasks()

            setIsModalOpen(false)
          }}
        />
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