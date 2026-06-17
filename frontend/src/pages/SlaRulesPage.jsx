import {
  useEffect,
  useMemo,
  useState
} from "react"

import axios from "axios"

import Navbar from "../components/Navbar"


const emptyForm = {
  module_name: "task",
  priority: "medium",
  allowed_hours: 24,
  escalation_enabled: false,
  escalation_after_hours: 48,
  is_active: true
}


export default function SlaRulesPage() {

  const [rules,
    setRules] =
    useState([])

  const [form,
    setForm] =
    useState(emptyForm)

  const [editingRuleId,
    setEditingRuleId] =
    useState(null)

  const [moduleFilter,
    setModuleFilter] =
    useState("")

  const [priorityFilter,
    setPriorityFilter] =
    useState("")

  const [loading,
    setLoading] =
    useState(true)

  const [message,
    setMessage] =
    useState("")

  const token =
    localStorage.getItem("token")

  const user =
    JSON.parse(
      localStorage.getItem("user")
    )


  const fetchRules =
    async () => {

      try {

        setLoading(true)

        const response =
          await axios.get(
            "http://127.0.0.1:8000/sla-rules/?page=1&size=100",
            {
              headers: {
                Authorization:
                  `Bearer ${token}`
              }
            }
          )

        setRules(
          response.data.items ||
          response.data
        )

      } catch (error) {

        console.error(error)

        setMessage(
          error.response?.data?.detail ||
          "Unable to load SLA rules"
        )

      } finally {

        setLoading(false)
      }
    }


  useEffect(() => {

    fetchRules()

  }, [])


  const filteredRules =
    useMemo(
      () =>
        rules.filter(
          (rule) =>
            (!moduleFilter ||
              rule.module_name === moduleFilter) &&
            (!priorityFilter ||
              rule.priority === priorityFilter)
        ),
      [
        rules,
        moduleFilter,
        priorityFilter
      ]
    )


  const resetForm =
    () => {

      setForm(emptyForm)

      setEditingRuleId(null)
    }


  const validateForm =
    () => {

      if (!form.module_name || !form.priority) {

        return "Module and priority are required"
      }

      if (Number(form.allowed_hours) <= 0) {

        return "Allowed hours must be greater than 0"
      }

      if (
        form.escalation_enabled &&
        Number(form.escalation_after_hours) <= 0
      ) {

        return "Escalation hours must be greater than 0"
      }

      return ""
    }


  const handleSubmit =
    async (event) => {

      event.preventDefault()

      const validationError =
        validateForm()

      if (validationError) {

        setMessage(validationError)

        return
      }

      const payload = {
        ...form,
        allowed_hours:
          Number(form.allowed_hours),
        escalation_after_hours:
          form.escalation_enabled
            ? Number(form.escalation_after_hours)
            : null
      }

      try {

        if (editingRuleId) {

          await axios.put(
            `http://127.0.0.1:8000/sla-rules/${editingRuleId}`,
            payload,
            {
              headers: {
                Authorization:
                  `Bearer ${token}`
              }
            }
          )

          setMessage("SLA rule updated")

        } else {

          await axios.post(
            "http://127.0.0.1:8000/sla-rules/",
            payload,
            {
              headers: {
                Authorization:
                  `Bearer ${token}`
              }
            }
          )

          setMessage("SLA rule created")
        }

        resetForm()

        fetchRules()

      } catch (error) {

        console.error(error)

        setMessage(
          error.response?.data?.detail ||
          "SLA rule save failed"
        )
      }
    }


  const editRule =
    (rule) => {

      setEditingRuleId(rule.id)

      setForm({
        module_name: rule.module_name,
        priority: rule.priority,
        allowed_hours: rule.allowed_hours,
        escalation_enabled:
          rule.escalation_enabled,
        escalation_after_hours:
          rule.escalation_after_hours || 1,
        is_active: rule.is_active
      })
    }


  const disableRule =
    async (ruleId) => {

      if (!window.confirm("Disable this SLA rule?")) {

        return
      }

      try {

        await axios.delete(
          `http://127.0.0.1:8000/sla-rules/${ruleId}`,
          {
            headers: {
              Authorization:
                `Bearer ${token}`
            }
          }
        )

        setMessage("SLA rule disabled")

        fetchRules()

      } catch (error) {

        console.error(error)

        setMessage(
          error.response?.data?.detail ||
          "Unable to disable SLA rule"
        )
      }
    }


  return (

    <div className="min-h-screen bg-slate-100">

      <Navbar
        user={user}
        handleLogout={() => {
          localStorage.clear()
          window.location.href = "/"
        }}
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">

        {user?.role !== "admin" ? (

          <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-10 text-center">

            <h1 className="text-2xl font-bold text-slate-900">

              SLA rules are available only for admins

            </h1>

          </div>

        ) : (

          <>

            <div className="bg-white border border-slate-200 rounded-xl shadow-sm px-6 py-5 mb-6">

              <h1 className="text-3xl font-bold text-slate-900">

                SLA Rules

              </h1>

              <p className="text-slate-500 mt-1">

                Manage time limits for task and approval workflows

              </p>

            </div>

            {message && (

              <div className="bg-white border border-slate-200 rounded-xl shadow-sm px-5 py-4 mb-6 text-sm text-slate-700">

                {message}

              </div>
            )}

            <div className="grid grid-cols-1 xl:grid-cols-[420px_minmax(0,1fr)] gap-6 items-start">

              <form
                onSubmit={handleSubmit}
                className="bg-white border border-slate-200 rounded-xl shadow-sm p-6 space-y-4"
              >

                <h2 className="text-xl font-bold text-slate-900">

                  {editingRuleId
                    ? "Edit SLA Rule"
                    : "Create SLA Rule"}

                </h2>

                <div>

                  <label className="block text-sm font-semibold text-slate-700 mb-2">
                    Module
                  </label>

                  <select
                    value={form.module_name}
                    onChange={(event) =>
                      setForm({
                        ...form,
                        module_name:
                          event.target.value
                      })
                    }
                    className="w-full border border-slate-300 rounded-xl px-4 py-3"
                  >
                    <option value="task">Task</option>
                    <option value="approval">Approval</option>
                  </select>

                </div>

                <div>

                  <label className="block text-sm font-semibold text-slate-700 mb-2">
                    Priority
                  </label>

                  <select
                    value={form.priority}
                    onChange={(event) =>
                      setForm({
                        ...form,
                        priority:
                          event.target.value
                      })
                    }
                    className="w-full border border-slate-300 rounded-xl px-4 py-3"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>

                </div>

                <div>

                  <label className="block text-sm font-semibold text-slate-700 mb-2">
                    Allowed Hours
                  </label>

                  <input
                    type="number"
                    min="1"
                    value={form.allowed_hours}
                    onChange={(event) =>
                      setForm({
                        ...form,
                        allowed_hours:
                          event.target.value
                      })
                    }
                    className="w-full border border-slate-300 rounded-xl px-4 py-3"
                  />

                </div>

                <label className="flex items-center gap-3 text-sm font-semibold text-slate-700">

                  <input
                    type="checkbox"
                    checked={form.escalation_enabled}
                    onChange={(event) =>
                      setForm({
                        ...form,
                        escalation_enabled:
                          event.target.checked
                      })
                    }
                  />

                  Escalation Enabled

                </label>

                <div>

                  <label className="block text-sm font-semibold text-slate-700 mb-2">
                    Escalation After Hours
                  </label>

                  <input
                    type="number"
                    min="1"
                    value={form.escalation_after_hours}
                    onChange={(event) =>
                      setForm({
                        ...form,
                        escalation_after_hours:
                          event.target.value
                      })
                    }
                    disabled={!form.escalation_enabled}
                    className="w-full border border-slate-300 rounded-xl px-4 py-3 disabled:bg-slate-100"
                  />

                </div>

                <label className="flex items-center gap-3 text-sm font-semibold text-slate-700">

                  <input
                    type="checkbox"
                    checked={form.is_active}
                    onChange={(event) =>
                      setForm({
                        ...form,
                        is_active:
                          event.target.checked
                      })
                    }
                  />

                  Active

                </label>

                <div className="flex gap-3">

                  <button
                    type="submit"
                    className="bg-slate-900 hover:bg-slate-800 text-white px-5 py-3 rounded-xl font-semibold"
                  >

                    {editingRuleId
                      ? "Update"
                      : "Create"}

                  </button>

                  {editingRuleId && (

                    <button
                      type="button"
                      onClick={resetForm}
                      className="border border-slate-300 text-slate-700 px-5 py-3 rounded-xl font-semibold"
                    >

                      Cancel

                    </button>
                  )}

                </div>

              </form>

              <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">

                <div className="px-5 py-4 border-b border-slate-200 flex flex-col md:flex-row gap-3 md:items-center md:justify-between">

                  <h2 className="text-xl font-bold text-slate-900">

                    Rule List

                  </h2>

                  <div className="flex gap-3">

                    <select
                      value={moduleFilter}
                      onChange={(event) =>
                        setModuleFilter(
                          event.target.value
                        )
                      }
                      className="border border-slate-300 rounded-xl px-3 py-2 text-sm"
                    >
                      <option value="">All modules</option>
                      <option value="task">Task</option>
                      <option value="approval">Approval</option>
                    </select>

                    <select
                      value={priorityFilter}
                      onChange={(event) =>
                        setPriorityFilter(
                          event.target.value
                        )
                      }
                      className="border border-slate-300 rounded-xl px-3 py-2 text-sm"
                    >
                      <option value="">All priorities</option>
                      <option value="low">Low</option>
                      <option value="medium">Medium</option>
                      <option value="high">High</option>
                    </select>

                  </div>

                </div>

                {loading ? (

                  <div className="p-8 text-slate-500">
                    Loading SLA rules...
                  </div>

                ) : filteredRules.length > 0 ? (

                  <div className="overflow-x-auto">

                    <table className="w-full text-sm">

                      <thead className="bg-slate-50 border-b border-slate-200 text-slate-600">
                        <tr>
                          <th className="text-left px-5 py-4">ID</th>
                          <th className="text-left px-5 py-4">Module</th>
                          <th className="text-left px-5 py-4">Priority</th>
                          <th className="text-left px-5 py-4">Allowed</th>
                          <th className="text-left px-5 py-4">Escalation</th>
                          <th className="text-left px-5 py-4">Status</th>
                          <th className="text-left px-5 py-4">Actions</th>
                        </tr>
                      </thead>

                      <tbody>
                        {filteredRules.map(
                          (rule) => (
                            <tr
                              key={rule.id}
                              className="border-b border-slate-100 last:border-b-0"
                            >
                              <td className="px-5 py-4">#{rule.id}</td>
                              <td className="px-5 py-4 capitalize">{rule.module_name}</td>
                              <td className="px-5 py-4 capitalize">{rule.priority}</td>
                              <td className="px-5 py-4">{rule.allowed_hours} hrs</td>
                              <td className="px-5 py-4">
                                {rule.escalation_enabled
                                  ? `${rule.escalation_after_hours || "-"} hrs`
                                  : "No"}
                              </td>
                              <td className="px-5 py-4">
                                <span className={`px-3 py-1 rounded-full text-xs font-semibold ${rule.is_active ? "bg-emerald-100 text-emerald-700" : "bg-slate-100 text-slate-600"}`}>
                                  {rule.is_active
                                    ? "Active"
                                    : "Disabled"}
                                </span>
                              </td>
                              <td className="px-5 py-4">
                                <div className="flex gap-2">
                                  <button
                                    onClick={() =>
                                      editRule(rule)
                                    }
                                    className="bg-slate-800 text-white px-3 py-2 rounded-lg text-xs font-semibold"
                                  >
                                    Edit
                                  </button>
                                  {rule.is_active && (
                                    <button
                                      onClick={() =>
                                        disableRule(rule.id)
                                      }
                                      className="bg-red-600 text-white px-3 py-2 rounded-lg text-xs font-semibold"
                                    >
                                      Disable
                                    </button>
                                  )}
                                </div>
                              </td>
                            </tr>
                          )
                        )}
                      </tbody>

                    </table>

                  </div>

                ) : (

                  <div className="p-8 text-slate-500">
                    No SLA rules found.
                  </div>
                )}

              </div>

            </div>

          </>
        )}

      </div>

    </div>
  )
}
