import {
  useEffect,
  useState
} from "react"

import axios from "axios"

import Navbar from "../components/Navbar"


export default function SubscriptionPlansPage() {

  const [plans,
    setPlans] =
    useState([])

  const [subscription,
    setSubscription] =
    useState(null)

  const [credits,
    setCredits] =
    useState([])

  const [loading,
    setLoading] =
    useState(true)

  const [paymentLoading,
    setPaymentLoading] =
    useState("")

  const [message,
    setMessage] =
    useState("")

  const token =
    localStorage.getItem("token")

  const [user,
    setUser] =
    useState(
      JSON.parse(
        localStorage.getItem("user")
      )
    )

  const headers = {
    Authorization:
      `Bearer ${token}`
  }


  const fetchDetails =
    async () => {

      try {

        const [
          meResponse,
          plansResponse,
          subscriptionResponse,
          creditsResponse
        ] = await Promise.all([

          axios.get(
            "http://127.0.0.1:8000/auth/me",
            { headers }
          ),

          axios.get(
            "http://127.0.0.1:8000/saas/plans",
            { headers }
          ),

          axios.get(
            "http://127.0.0.1:8000/saas/subscription",
            { headers }
          ),

          axios.get(
            "http://127.0.0.1:8000/saas/credits",
            { headers }
          )
        ])

        localStorage.setItem(
          "user",
          JSON.stringify(meResponse.data)
        )

        setUser(meResponse.data)

        setPlans(plansResponse.data)

        setSubscription(subscriptionResponse.data)

        setCredits(creditsResponse.data)

      } catch (error) {

        console.error(error)

        setMessage(
          error.response?.data?.detail ||
          "Subscription details could not be loaded"
        )

      } finally {

        setLoading(false)
      }
    }


  useEffect(() => {

    fetchDetails()

  }, [])


  const handleLogout = () => {

    localStorage.clear()

    window.location.href = "/"
  }


  const openRazorpayCheckout =
    (order) => {

      if (!window.Razorpay) {

        setMessage(
          "Razorpay checkout script is not loaded"
        )

        return
      }

      const razorpay =
        new window.Razorpay({

          key: order.key,

          amount: order.amount,

          currency: order.currency,

          name: "Enterprise Workflow",

          description:
            `${order.plan_name} Subscription`,

          order_id: order.order_id,

          handler: async (response) => {

            try {

              const verifyResponse =
                await axios.post(
                  "http://127.0.0.1:8000/payments/verify-razorpay",
                  {
                    razorpay_order_id:
                      response.razorpay_order_id,
                    razorpay_payment_id:
                      response.razorpay_payment_id,
                    razorpay_signature:
                      response.razorpay_signature,
                    plan_name:
                      order.plan_name
                  },
                  {
                    headers
                  }
                )

              setSubscription(
                verifyResponse.data.subscription
              )

              setMessage(
                verifyResponse.data.message
              )

              fetchDetails()

            } catch (error) {

              console.error(error)

              setMessage(
                error.response?.data?.detail ||
                "Payment verification failed"
              )
            }
          }
        })

      razorpay.on(
        "payment.failed",
        () => {

          setMessage(
            "Razorpay payment was not completed"
          )
        }
      )

      razorpay.open()
    }


  const handleRazorpayPayment =
    async (planName) => {

      try {

        setPaymentLoading(planName)

        const response =
          await axios.post(
            "http://127.0.0.1:8000/payments/create-payment",
            {
              provider: "razorpay",
              plan_name: planName
            },
            {
              headers
            }
          )

        openRazorpayCheckout(
          response.data
        )

      } catch (error) {

        console.error(error)

        setMessage(
          error.response?.data?.detail ||
          "Razorpay order could not be created"
        )

      } finally {

        setPaymentLoading("")
      }
    }


  const currentPlanName =
    subscription?.plan?.name


  const getPlanFeatures =
    (features) => (

      features
        ? features.split(";").map(
            (feature) => feature.trim()
          ).filter(Boolean)
        : []
    )


  return (

    <div className="min-h-screen bg-slate-100">

      <Navbar
        user={user}
        handleLogout={handleLogout}
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">

        <div className="bg-white border border-slate-200 rounded-xl shadow-sm px-6 py-5 mb-6 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">

          <div>

            <h1 className="text-3xl font-bold text-slate-900">

              Subscription

            </h1>

            <p className="text-slate-500 mt-1">

              Manage organization billing, plans, and usage credits

            </p>

          </div>

          {subscription && (

            <div className="grid grid-cols-2 gap-3 min-w-[280px]">

              <div className="bg-slate-50 border border-slate-200 rounded-xl px-4 py-3">

                <p className="text-sm text-slate-500">

                  Active Plan

                </p>

                <p className="text-xl font-bold text-slate-900">

                  {currentPlanName || "Not Set"}

                </p>

              </div>

              <div className="bg-slate-50 border border-slate-200 rounded-xl px-4 py-3">

                <p className="text-sm text-slate-500">

                  Credits

                </p>

                <p className="text-xl font-bold text-slate-900">

                  {subscription.credits_remaining}

                </p>

              </div>

            </div>
          )}

        </div>

        {message && (

          <div className="bg-white border border-slate-200 rounded-xl px-4 py-3 mb-6 text-slate-700">

            {message}

          </div>
        )}

        {loading ? (

          <div className="bg-white border border-slate-200 rounded-xl p-8 text-center text-slate-500">

            Loading subscription plans...

          </div>

        ) : user?.role !== "admin" ? (

          <div className="bg-white border border-slate-200 rounded-xl p-8 text-center text-slate-500">

            Subscription management is available only for admins.

          </div>

        ) : (

          <>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-5">

              {plans.map(
                (plan) => {

                  const isCurrent =
                    currentPlanName === plan.name

                  return (

                    <div
                      key={plan.id}
                      className={`bg-white border rounded-xl shadow-sm overflow-hidden ${
                        isCurrent
                          ? "border-emerald-300"
                          : "border-slate-200"
                      }`}
                    >

                      <div className="p-5 border-b border-slate-100">

                        <div className="flex items-start justify-between gap-3">

                          <div>

                            <h2 className="text-2xl font-bold text-slate-900">

                              {plan.name}

                            </h2>

                            <p className="text-slate-500 mt-1">

                              Rs {plan.monthly_price} / month

                            </p>

                          </div>

                          {isCurrent && (

                            <span className="bg-emerald-50 text-emerald-700 border border-emerald-100 rounded-lg px-3 py-1 text-sm font-bold">

                              Active

                            </span>
                          )}

                        </div>

                      </div>

                      <div className="p-5">

                        <div className="grid grid-cols-2 gap-3 mb-4">

                          <div className="bg-slate-50 border border-slate-200 rounded-xl px-4 py-3">

                            <p className="text-2xl font-bold text-slate-900">

                              {plan.monthly_credits}

                            </p>

                            <p className="text-sm text-slate-500">

                              Credits

                            </p>

                          </div>

                          <div className="bg-slate-50 border border-slate-200 rounded-xl px-4 py-3">

                            <p className="text-2xl font-bold text-slate-900">

                              {plan.max_users}

                            </p>

                            <p className="text-sm text-slate-500">

                              Users

                            </p>

                          </div>

                        </div>

                        <ul className="space-y-2 min-h-[168px]">

                          {getPlanFeatures(
                            plan.features
                          ).map(
                            (feature) => (

                              <li
                                key={feature}
                                className="flex gap-2 text-sm text-slate-700"
                              >

                                <span className="mt-1 h-2 w-2 rounded-full bg-emerald-600 shrink-0" />

                                <span>

                                  {feature}

                                </span>

                              </li>
                            )
                          )}

                        </ul>

                        <button
                          type="button"
                          disabled={paymentLoading === plan.name}
                          onClick={() =>
                            handleRazorpayPayment(plan.name)
                          }
                          className="w-full mt-5 py-3 rounded-xl font-semibold bg-emerald-700 hover:bg-emerald-800 text-white disabled:bg-slate-400"
                        >

                          {paymentLoading === plan.name
                            ? "Opening Razorpay..."
                            : isCurrent
                              ? "Renew Plan"
                              : `Choose ${plan.name}`}

                        </button>

                      </div>

                    </div>
                  )
                }
              )}

            </div>

            <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6 mt-8">

              <h2 className="text-xl font-bold text-slate-900 mb-4">

                Credit History

              </h2>

              <div className="space-y-3">

                {credits.length > 0 ? (

                  credits.slice(0, 8).map(
                    (entry) => (

                      <div
                        key={entry.id}
                        className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 border border-slate-200 rounded-xl px-4 py-3"
                      >

                        <p className="text-slate-700">

                          {entry.reason}

                        </p>

                        <span className="font-bold text-emerald-700">

                          +{entry.change_amount}

                        </span>

                      </div>
                    )
                  )

                ) : (

                  <div className="text-slate-500">

                    No credit history available.

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
