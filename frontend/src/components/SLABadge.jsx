export default function SLABadge({
  status,
  breached,
  label
}) {

  const normalizedStatus =
    status || (
      breached
        ? "breached"
        : "not_started"
    )

  const styles = {

    active:
      "bg-blue-100 text-blue-700",

    completed_within_sla:
      "bg-emerald-100 text-emerald-700",

    breached:
      "bg-red-100 text-red-700",

    escalated:
      "bg-orange-100 text-orange-700",

    not_started:
      "bg-slate-100 text-slate-600"
  }

  const labels = {

    active: "Active",

    completed_within_sla:
      "Completed",

    breached: "Breached",

    escalated: "Escalated",

    not_started: "No SLA"
  }

  return (

    <span
      className={`px-3 py-1 rounded-full text-xs font-semibold ${styles[normalizedStatus] || styles.not_started}`}
    >

      {label
        ? `${label}: `
        : ""}

      {labels[normalizedStatus] ||
        normalizedStatus.replace(
          "_",
          " "
        )}

    </span>
  )
}
