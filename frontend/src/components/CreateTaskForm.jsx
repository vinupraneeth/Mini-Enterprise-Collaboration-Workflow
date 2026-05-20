import {
  useEffect,
  useState
} from "react";

import api from "../api/axios";


function CreateTaskForm({
  fetchTasks,
  currentUser
}) {

  const [title, setTitle] =
    useState("");

  const [description, setDescription] =
    useState("");

  const [priority, setPriority] =
    useState("medium");

  const [dueDate, setDueDate] =
    useState("");

  const [assignedTo, setAssignedTo] =
    useState("");

  const [users, setUsers] =
    useState([]);

  const [loading, setLoading] =
    useState(false);


  useEffect(() => {

    fetchUsers();

  }, []);


  const fetchUsers = async () => {

    try {

      const token = localStorage.getItem(
        "token"
      );

      const response = await api.get(

        "/users",

        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }
      );

      let filteredUsers =
        response.data;

      if (
        currentUser?.role ===
        "manager"
      ) {

        filteredUsers =
          response.data.filter(
            (user) =>
              user.role ===
              "employee"
          );
      }

      setUsers(filteredUsers);

    } catch (error) {

      console.log(error);
    }
  };


  const handleCreateTask = async (
    event
  ) => {

    event.preventDefault();

    setLoading(true);

    try {

      const token = localStorage.getItem(
        "token"
      );

      await api.post(

        "/tasks",

        {
          title,
          description,
          priority,
          due_date:
            dueDate || null,
          assigned_to:
            Number(assignedTo)
        },

        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }
      );

      alert(
        "Task created successfully"
      );

      setTitle("");

      setDescription("");

      setPriority("medium");

      setDueDate("");

      setAssignedTo("");

      fetchTasks();

    } catch (error) {

      console.log(error);

      alert(
        error?.response?.data?.detail
        ||
        "Task creation failed"
      );

    } finally {

      setLoading(false);
    }
  };


  return (

    <div className="bg-white rounded-2xl shadow-lg p-8 mb-8 border border-gray-100">

      <div className="flex justify-between items-center mb-8">

        <div>

          <h2 className="text-3xl font-bold text-gray-800">
            Create Task
          </h2>

          <p className="text-gray-500 mt-2">
            Assign workflow tasks to team members
          </p>

        </div>

        <div className="hidden md:flex items-center gap-2 bg-blue-50 text-blue-700 px-4 py-2 rounded-xl text-sm font-semibold">

          Active Workflow

        </div>

      </div>

      <form
        onSubmit={handleCreateTask}
        className="grid grid-cols-1 md:grid-cols-2 gap-6"
      >

        <div className="md:col-span-2">

          <label className="block text-sm font-semibold text-gray-700 mb-2">

            Task Title

          </label>

          <input
            type="text"
            placeholder="Enter task title"
            value={title}
            onChange={(e) =>
              setTitle(
                e.target.value
              )
            }
            className="w-full border border-gray-300 rounded-2xl px-5 py-4 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 transition"
            required
          />

        </div>

        <div className="md:col-span-2">

          <label className="block text-sm font-semibold text-gray-700 mb-2">

            Description

          </label>

          <textarea
            placeholder="Describe the task requirements..."
            value={description}
            onChange={(e) =>
              setDescription(
                e.target.value
              )
            }
            rows="5"
            className="w-full border border-gray-300 rounded-2xl px-5 py-4 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 resize-none transition"
          />

        </div>

        <div>

          <label className="block text-sm font-semibold text-gray-700 mb-2">

            Priority

          </label>

          <select
            value={priority}
            onChange={(e) =>
              setPriority(
                e.target.value
              )
            }
            className="w-full border border-gray-300 rounded-2xl px-5 py-4 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 transition"
          >

            <option value="low">
              Low Priority
            </option>

            <option value="medium">
              Medium Priority
            </option>

            <option value="high">
              High Priority
            </option>

          </select>

        </div>

        <div>

          <label className="block text-sm font-semibold text-gray-700 mb-2">

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
            className="w-full border border-gray-300 rounded-2xl px-5 py-4 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 transition"
          />

        </div>

        <div className="md:col-span-2">

          <label className="block text-sm font-semibold text-gray-700 mb-2">

            Assign Team Member

          </label>

          <select
            value={assignedTo}
            onChange={(e) =>
              setAssignedTo(
                e.target.value
              )
            }
            className="w-full border border-gray-300 rounded-2xl px-5 py-4 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 transition"
            required
          >

            <option value="">
              Select User
            </option>

            {
              users.map((user) => (

                <option
                  key={user.id}
                  value={user.id}
                >
                  {user.name}

                  {" • "}

                  {user.role}

                </option>
              ))
            }

          </select>

        </div>

        <div className="md:col-span-2 flex justify-end pt-2">

          <button
            type="submit"
            disabled={loading}
            className="bg-gradient-to-r from-blue-600 to-indigo-700 hover:opacity-90 text-white px-10 py-4 rounded-2xl font-semibold shadow-lg transition"
          >

            {
              loading
              ?
              "Creating Task..."
              :
              "Create Task"
            }

          </button>

        </div>

      </form>

    </div>
  );
}

export default CreateTaskForm;