export default function PriorityBadge({

  priority

}) {

  const styles = {

    low:
      "bg-green-100 text-green-700",

    medium:
      "bg-yellow-100 text-yellow-700",

    high:
      "bg-red-100 text-red-700"
  }


  return (

    <span
      className={`px-3 py-1 rounded-full text-xs font-semibold ${styles[priority]}`}
    >

      {priority}

    </span>
  )
}