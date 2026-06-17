import {
  useEffect,
  useState
} from "react"

import axios from "axios"

import Navbar from "../components/Navbar"

import ToggleSwitch from "../components/ToggleSwitch"


export default function NotificationPreferencesPage() {

  const [preferences,
    setPreferences] =
    useState(null)

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

  const headers = {
    Authorization:
      `Bearer ${token}`
  }


  const fetchPreferences =
    async () => {

      try {

        setLoading(true)

        const response =
          await axios.get(
            "http://127.0.0.1:8000/notification-preferences/me",
            { headers }
          )

        setPreferences(response.data)

      } catch (error) {

        console.error(error)

        setMessage(
          error.response?.data?.detail ||
          "Unable to load notification preferences"
        )

      } finally {

        setLoading(false)
      }
    }


  useEffect(() => {

    fetchPreferences()

  }, [])


  const updatePreference =
    (
      key,
      value
    ) => {

      setPreferences({
        ...preferences,
        [key]: value
      })
    }


  const savePreferences =
    async () => {

      try {

        await axios.put(
          "http://127.0.0.1:8000/notification-preferences/me",
          {
            in_app_enabled:
              preferences.in_app_enabled,
            email_enabled:
              preferences.email_enabled,
            task_notifications:
              preferences.task_notifications,
            approval_notifications:
              preferences.approval_notifications,
            escalation_notifications:
              preferences.escalation_notifications,
            document_notifications:
              preferences.document_notifications
          },
          { headers }
        )

        setMessage("Notification preferences saved")

        fetchPreferences()

      } catch (error) {

        console.error(error)

        setMessage(
          error.response?.data?.detail ||
          "Unable to save notification preferences"
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

      <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8">

        <div className="bg-white border border-slate-200 rounded-xl shadow-sm px-6 py-5 mb-6">
          <h1 className="text-3xl font-bold text-slate-900">
            Notification Preferences
          </h1>
          <p className="text-slate-500 mt-1">
            Choose which workflow notifications you want to receive
          </p>
        </div>

        {message && (
          <div className="bg-white border border-slate-200 rounded-xl shadow-sm px-5 py-4 mb-6 text-sm text-slate-700">
            {message}
          </div>
        )}

        <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6">

          {loading || !preferences ? (

            <div className="text-slate-500">
              Loading preferences...
            </div>

          ) : (

            <div className="space-y-4">

              <ToggleSwitch
                label="In-app Notifications"
                checked={preferences.in_app_enabled}
                onChange={(value) =>
                  updatePreference(
                    "in_app_enabled",
                    value
                  )
                }
              />

              <ToggleSwitch
                label="Email Notifications"
                checked={preferences.email_enabled}
                onChange={(value) =>
                  updatePreference(
                    "email_enabled",
                    value
                  )
                }
              />

              <ToggleSwitch
                label="Task Notifications"
                checked={preferences.task_notifications}
                onChange={(value) =>
                  updatePreference(
                    "task_notifications",
                    value
                  )
                }
              />

              <ToggleSwitch
                label="Approval Notifications"
                checked={preferences.approval_notifications}
                onChange={(value) =>
                  updatePreference(
                    "approval_notifications",
                    value
                  )
                }
              />

              <ToggleSwitch
                label="Escalation Notifications"
                checked={preferences.escalation_notifications}
                onChange={(value) =>
                  updatePreference(
                    "escalation_notifications",
                    value
                  )
                }
              />

              <ToggleSwitch
                label="Document Notifications"
                checked={preferences.document_notifications}
                onChange={(value) =>
                  updatePreference(
                    "document_notifications",
                    value
                  )
                }
              />

              <div className="pt-2">
                <button
                  onClick={savePreferences}
                  className="bg-slate-900 hover:bg-slate-800 text-white px-6 py-3 rounded-xl font-semibold"
                >
                  Save Preferences
                </button>
              </div>

            </div>
          )}

        </div>

      </div>

    </div>
  )
}
