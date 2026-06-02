import {
  useEffect,
  useState
} from "react"

import axios from "axios"


export default function ActivityFeedPanel() {

  const [activities,
    setActivities] =
    useState([])

  const [loading,
    setLoading] =
    useState(true)

  const token =
    localStorage.getItem("token")


  const fetchActivities =
    async () => {

      try {

        const response =
          await axios.get(

            "http://127.0.0.1:8000/activity/?page=1&size=8",

            {
              headers: {
                Authorization:
                  `Bearer ${token}`
              }
            }
          )

        setActivities(
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

    fetchActivities()

  }, [])


  const formatDateTime =
    (value) => {

      if (!value) {

        return "Not available"
      }

      return new Date(value).toLocaleString(
        "en-IN",
        {
          dateStyle: "medium",
          timeStyle: "short"
        }
      )
    }


  return (

    <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-6 mt-8">

      <div className="mb-6">

        <h2 className="text-2xl font-bold text-slate-900">

          Activity Feed

        </h2>

        <p className="text-slate-500 mt-1">

          Recent workflow activity visible to your role

        </p>

      </div>

      {loading ? (

        <div className="text-slate-500 py-6">

          Loading activity feed...

        </div>

      ) : activities.length > 0 ? (

        <div className="space-y-3">

          {activities.map(
            (activity, index) => (

              <div
                key={`${activity.type}-${activity.created_at}-${index}`}
                className="bg-slate-50 border border-slate-200 rounded-xl px-4 py-3"
              >

                <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-2">

                  <p className="font-medium text-slate-800">

                    {activity.message}

                  </p>

                  <span className="text-xs text-slate-500">

                    {formatDateTime(
                      activity.created_at
                    )}

                  </span>

                </div>

                <p className="text-xs text-slate-500 mt-1 capitalize">

                  {activity.type.replace(
                    "_",
                    " "
                  )}

                </p>

              </div>
            )
          )}

        </div>

      ) : (

        <div className="text-slate-500 py-6">

          No recent activity found.

        </div>
      )}

    </div>
  )
}
