import {

  useEffect,

  useState

} from "react"

import axios from "axios"


export default function CreateTaskForm({

  fetchTasks

}) {

  const [title,
    setTitle] =
    useState("")

  const [description,
    setDescription] =
    useState("")

  const [priority,
    setPriority] =
    useState("medium")

  const [dueDate,
    setDueDate] =
    useState("")

  const [assignedTo,
    setAssignedTo] =
    useState("")

  const [employees,
    setEmployees] =
    useState([])

  const token =
    localStorage.getItem("token")


  const fetchEmployees =
    async () => {

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

        setEmployees(
          response.data.items ||
          response.data
        )

      } catch (error) {

        console.error(error)
      }
    }


  useEffect(() => {

    fetchEmployees()

  }, [])


  const handleSubmit =
    async (e) => {

      e.preventDefault()

      try {

        await axios.post(

          "http://127.0.0.1:8000/tasks/",

          {
            title,

            description,

            priority,

            due_date: dueDate,

            assigned_to:
              parseInt(assignedTo)
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

        setPriority("medium")

        setDueDate("")

        setAssignedTo("")

        fetchTasks()

      } catch (error) {

        console.error(error)

        alert(

          typeof error.response?.data?.detail
          === "string"

            ? error.response.data.detail

            : JSON.stringify(
                error.response?.data?.detail
              ) ||

              "Task creation failed"
        )
      }
    }


  return (

    <div>

      <form
        onSubmit={handleSubmit}
        className="grid grid-cols-1 md:grid-cols-2 gap-5"
      >

        <div className="md:col-span-2">

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
            className="w-full border border-slate-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-slate-300"
          />

        </div>

        <div className="md:col-span-2">

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
            className="w-full border border-slate-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-slate-300"
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
            className="w-full border border-slate-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-slate-300"
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
            required
            className="w-full border border-slate-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-slate-300"
          />

        </div>

        <div className="md:col-span-2">

          <label className="block mb-2 font-medium text-gray-700">

            Assign Employee

          </label>

          <select
            required
            value={assignedTo}
            onChange={(e) =>
              setAssignedTo(
                e.target.value
              )
            }
            className="w-full border border-slate-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-slate-300"
          >

            <option value="">

              Select Employee

            </option>

            {employees

              .filter(
                (employee) =>
                  employee.role === "employee"
              )

              .map(
                (employee) => (

                  <option
                    key={employee.id}
                    value={employee.id}
                  >

                    {employee.name || employee.username}

                  </option>
                )
              )}

          </select>

        </div>

        <button
          type="submit"
          className="md:col-span-2 w-full bg-slate-900 hover:bg-slate-800 text-white font-semibold py-3 rounded-xl"
        >

          Create Task

        </button>

      </form>

    </div>
  )
}
