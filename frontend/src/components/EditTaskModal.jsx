import {
  useEffect,
  useState
} from "react";

import api from "../api/axios";


function EditTaskModal({
  task,
  closeModal,
  fetchTasks
}) {

  const [title, setTitle] =
    useState("");

  const [description, setDescription] =
    useState("");

  const [priority, setPriority] =
    useState("medium");

  const [status, setStatus] =
    useState("todo");

  const [dueDate, setDueDate] =
    useState("");

  const [loading, setLoading] =
    useState(false);


  useEffect(() => {

    if (task) {

      setTitle(task.title);

      setDescription(
        task.description || ""
      );

      setPriority(task.priority);

      setStatus(task.status);

      setDueDate(

        task.due_date
        ?
        task.due_date.slice(0, 16)
        :
        ""
      );
    }

  }, [task]);


  const handleUpdate = async () => {

    setLoading(true);

    try {

      const token = localStorage.getItem(
        "token"
      );

      await api.put(

        `/tasks/${task.id}`,

        {
          title,
          description,
          priority,
          status,
          assigned_to:
            task.assigned_to,
          due_date:
            dueDate || null
        },

        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }
      );

      alert(
        "Task updated successfully"
      );

      closeModal();

      fetchTasks();

    } catch (error) {

      console.log(error);

      alert(
        error?.response?.data?.detail
        ||
        "Update failed"
      );

    } finally {

      setLoading(false);
    }
  };


  return (

    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex justify-center items-center z-50 p-4">

      <div className="bg-white w-full max-w-2xl rounded-3xl shadow-2xl overflow-hidden animate-in fade-in zoom-in duration-200">

        <div className="bg-gradient-to-r from-indigo-600 to-blue-700 px-8 py-6 flex justify-between items-center">

          <div>

            <h2 className="text-3xl font-bold text-white">
              Edit Task
            </h2>

            <p className="text-indigo-100 mt-1">
              Update workflow task details
            </p>

          </div>

          <button
            onClick={closeModal}
            className="text-white text-3xl hover:opacity-70 transition"
          >
            ×
          </button>

        </div>

        <div className="p-8 space-y-6">

          <div>

            <label className="block mb-2 font-semibold text-gray-700">
              Task Title
            </label>

            <input
              type="text"
              value={title}
              onChange={(e) =>
                setTitle(
                  e.target.value
                )
              }
              className="w-full border border-gray-300 rounded-2xl px-5 py-4 outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 transition"
            />

          </div>

          <div>

            <label className="block mb-2 font-semibold text-gray-700">
              Description
            </label>

            <textarea
              rows="5"
              value={description}
              onChange={(e) =>
                setDescription(
                  e.target.value
                )
              }
              className="w-full border border-gray-300 rounded-2xl px-5 py-4 outline-none resize-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 transition"
            />

          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">

            <div>

              <label className="block mb-2 font-semibold text-gray-700">
                Priority
              </label>

              <select
                value={priority}
                onChange={(e) =>
                  setPriority(
                    e.target.value
                  )
                }
                className="w-full border border-gray-300 rounded-2xl px-5 py-4 outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 transition"
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

              <label className="block mb-2 font-semibold text-gray-700">
                Status
              </label>

              <select
                value={status}
                onChange={(e) =>
                  setStatus(
                    e.target.value
                  )
                }
                className="w-full border border-gray-300 rounded-2xl px-5 py-4 outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 transition"
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

            </div>

            <div>

              <label className="block mb-2 font-semibold text-gray-700">
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
                className="w-full border border-gray-300 rounded-2xl px-5 py-4 outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 transition"
              />

            </div>

          </div>

          <div className="flex justify-end gap-4 pt-4">

            <button
              onClick={closeModal}
              className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-6 py-3 rounded-2xl font-semibold transition"
            >
              Cancel
            </button>

            <button
              onClick={handleUpdate}
              disabled={loading}
              className="bg-gradient-to-r from-indigo-600 to-blue-700 hover:opacity-90 text-white px-8 py-3 rounded-2xl font-semibold shadow-lg transition"
            >

              {
                loading
                ?
                "Saving..."
                :
                "Save Changes"
              }

            </button>

          </div>

        </div>

      </div>

    </div>
  );
}

export default EditTaskModal;