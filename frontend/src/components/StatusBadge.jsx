export default function StatusBadge({

  status,

  label

}) {

  const styles = {

    todo:
      "bg-gray-100 text-gray-700",

    in_progress:
      "bg-blue-100 text-blue-700",

    review:
      "bg-yellow-100 text-yellow-700",

    done:
      "bg-green-100 text-green-700"
  }

  const displayValue =
    status?.replace(
      "_",
      " "
    )


  return (

    <span
      className={`px-3 py-1 rounded-full text-xs font-semibold capitalize ${styles[status] || "bg-slate-100 text-slate-600"}`}
    >

      {label
        ? `${label}: ${displayValue}`
        : displayValue}

    </span>
  )
}
