import {
  useEffect,
  useState
} from "react"

import axios from "axios"


export default function NotificationsPanel({

  user

}) {

  const [notifications,
    setNotifications] =
    useState([])

  const [loading,
    setLoading] =
    useState(true)

  const token =
    localStorage.getItem("token")

  const subtitle =
    user?.role === "admin"
      ? "Recent system workflow updates"
      : user?.role === "manager"
        ? "Recent team workflow updates"
        : "Recent updates assigned to you"


  const fetchNotifications =
    async () => {

      try {

        const response =
          await axios.get(

            "http://127.0.0.1:8000/notifications/",

            {
              headers: {
                Authorization:
                  `Bearer ${token}`
              }
            }
          )

        setNotifications(
          response.data.items ||
          response.data
        )

      } catch (error) {

        console.error(error)

      } finally {

        setLoading(false)
      }
    }


  useEffect(() => {

    fetchNotifications()

  }, [])


  const markAsRead =
    async (notificationId) => {

      try {

        await axios.patch(

          `http://127.0.0.1:8000/notifications/${notificationId}/read`,

          {},

          {
            headers: {
              Authorization:
                `Bearer ${token}`
            }
          }
        )

        fetchNotifications()

      } catch (error) {

        console.error(error)
      }
    }


  return (

    <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-6 mt-8">

      <div className="flex items-center justify-between mb-6">

        <div>

          <h2 className="text-2xl font-bold text-slate-900">

            Notifications

          </h2>

          <p className="text-slate-500 mt-1">

            {subtitle}

          </p>

        </div>

      </div>

      {loading ? (

        <div className="text-gray-500 py-6">

          Loading notifications...

        </div>

      ) : notifications.length > 0 ? (

        <div className="space-y-3">

          {notifications.slice(0, 6).map(
            (notification) => (

              <div
                key={notification.id}
                className={`border rounded-xl px-4 py-3 flex flex-col md:flex-row md:items-center md:justify-between gap-3 ${
                  notification.is_read
                    ? "bg-slate-50 border-slate-200"
                    : "bg-blue-50 border-blue-100"
                }`}
              >

                <div>

                  <p className="text-gray-800 font-medium">

                    {notification.message}

                  </p>

                  <p className="text-xs text-gray-500 mt-1">

                    {notification.is_read
                      ? "Read"
                      : "Unread"}

                  </p>

                </div>

                {!notification.is_read && (

                  <button
                    onClick={() =>
                      markAsRead(notification.id)
                    }
                    className="bg-slate-900 hover:bg-slate-800 text-white px-4 py-2 rounded-xl text-sm font-semibold"
                  >

                    Mark Read

                  </button>
                )}

              </div>
            )
          )}

        </div>

      ) : (

        <div className="text-gray-500 py-6">

          No notifications yet.

        </div>
      )}

    </div>
  )
}
