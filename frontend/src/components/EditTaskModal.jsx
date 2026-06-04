import { useEffect, useState } from "react"

import axios from "axios"


export default function EditTaskModal({

  task,

  closeModal,

  fetchTasks
}) {

  const [title, setTitle] =
    useState(task.title)

  const [description,
    setDescription] =
    useState(task.description)

  const [priority,
    setPriority] =
    useState(task.priority)

  const [dueDate,
  setDueDate] =
  useState(
    task.due_date
      ? task.due_date.slice(0, 16)
      : ""
  )

  const [assignedTo,
    setAssignedTo] =
    useState(

      task.assigned_to || ""
    )

  const [users, setUsers] =
    useState([])

  const token =
    localStorage.getItem("token")

  const currentUser =
    JSON.parse(
      localStorage.getItem("user")
    )


  useEffect(() => {

    fetchUsers()

  }, [])


  const fetchUsers = async () => {

    try {

      const response =
        await axios.get(

          "http://127.0.0.1:8000/users/employees",

          {
            headers: {
              Authorization:
                `Bearer ${token}`
            }
          }
        )

      setUsers(
        response.data.items ||
        response.data
      )

    } catch (error) {

      console.error(error)
    }
  }


  const filteredUsers = users.filter(
    (userItem) => {

      // ADMIN

      if (
        currentUser.role === "admin"
      ) {

        return (

          userItem.role !== "admin"

          &&

          userItem.email !==
          currentUser.email
        )
      }

      // MANAGER

      if (
        currentUser.role === "manager"
      ) {

        return (
          userItem.role ===
          "employee"
        )
      }

      return false
    }
  )


  const handleSubmit =
    async (e) => {

      e.preventDefault()

      try {

        await axios.put(

          `http://127.0.0.1:8000/tasks/${task.id}`,

          {
            title,

            description,

            priority,

            due_date: dueDate || null,

            status: task.status,

            assigned_to:
              Number(assignedTo)
          },

          {
            headers: {
              Authorization:
                `Bearer ${token}`
            }
          }
        )

        fetchTasks()

        closeModal()

      } catch (error) {

        console.error(error)

        alert(

          typeof error.response?.data?.detail
            === "string"

            ? error.response.data.detail

            : "Task update failed"
        )
      }
    }


  return (

    <div className="fixed inset-0 bg-black/50 flex justify-center items-center z-50">

      <div className="bg-white w-full max-w-lg rounded-2xl shadow-2xl p-8">

        <div className="flex justify-between items-center mb-6">

          <h2 className="text-2xl font-bold text-gray-800">

            Edit Task

          </h2>

          <button
            onClick={closeModal}
            className="text-gray-500 hover:text-red-500 text-xl"
          >

            ✕

          </button>
        </div>

        <form
          onSubmit={handleSubmit}
          className="space-y-5"
        >

          <div>

            <label className="block mb-2 font-medium text-gray-700">

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
              required
              className="w-full border rounded-xl px-4 py-3"
            />
          </div>

          <div>

            <label className="block mb-2 font-medium text-gray-700">

              Description

            </label>

            <textarea
              value={description}
              onChange={(e) =>
                setDescription(
                  e.target.value
                )
              }
              required
              rows={4}
              className="w-full border rounded-xl px-4 py-3"
            />
          </div>

          <div>

            <label className="block mb-2 font-medium text-gray-700">

              Priority

            </label>

            <select
              value={priority}
              onChange={(e) =>
                setPriority(
                  e.target.value
                )
              }
              className="w-full border rounded-xl px-4 py-3"
            >

              <option value="low">

                Low

              </option>

              <option value="medium">

                Medium

              </option>

              <option value="high">

                High

              </option>
            </select>
          </div>

          <div>

            <label className="block mb-2 font-medium text-gray-700">

              Due Date

            </label>

            <input
              type="datetime-local"
              value={dueDate}
              onChange={(e) =>
                setDueDate(
                  e.target.value
                )
              }
              className="w-full border rounded-xl px-4 py-3"
            />
          </div>

          <div>

            <label className="block mb-2 font-medium text-gray-700">

              Assign To

            </label>

            <select
              value={assignedTo}
              onChange={(e) =>
                setAssignedTo(
                  e.target.value
                )
              }
              required
              className="w-full border rounded-xl px-4 py-3"
            >

              <option value="">

                Select User

              </option>

              {filteredUsers.map(
                (userItem) => (

                  <option
                    key={userItem.id}
                    value={userItem.id}
                  >

                    {userItem.name}
                    {" "}
                    (
                    {userItem.role}
                    )

                  </option>
                )
              )}
            </select>
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-xl font-semibold shadow-lg transition"
          >

            Update Task

          </button>
        </form>
      </div>
    </div>
  )
}
