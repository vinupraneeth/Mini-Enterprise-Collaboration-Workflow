import {
  useEffect,
  useState
} from "react"

import axios from "axios"


export default function NotificationsPanel({

  id,

  user,

  refreshKey

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

  const unreadCount =
    notifications.filter(
      (notification) =>
        !notification.is_read
    ).length


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

  }, [refreshKey])


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

    <div
      id={id}
      className="bg-white border border-slate-200 rounded-xl shadow-sm p-5 xl:sticky xl:top-6 scroll-mt-6"
    >

      <div className="flex items-start justify-between gap-4 mb-5">

        <div>

          <h2 className="text-xl font-bold text-slate-900">

            Notifications

          </h2>

          <p className="text-sm text-slate-500 mt-1">

            {subtitle}

          </p>

        </div>

        <span className="bg-slate-100 text-slate-700 border border-slate-200 rounded-full px-3 py-1 text-xs font-semibold">

          {unreadCount} unread

        </span>

      </div>

      {loading ? (

        <div className="text-gray-500 py-6">

          Loading notifications...

        </div>

      ) : notifications.length > 0 ? (

        <div className="space-y-3 max-h-[420px] overflow-y-auto pr-1 nice-scrollbar">

          {notifications.slice(0, 6).map(
            (notification) => (

              <div
                key={notification.id}
                className={`border rounded-lg px-4 py-3 flex flex-col gap-3 ${
                  notification.is_read
                    ? "bg-slate-50 border-slate-200"
                    : "bg-blue-50 border-blue-100"
                }`}
              >

                <div>

                  <p className="text-sm text-gray-800 font-medium leading-5">

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
