export default function ToggleSwitch({
  checked,
  onChange,
  label
}) {

  return (

    <label className="flex items-center justify-between gap-4 bg-slate-50 border border-slate-200 rounded-xl px-4 py-3">

      <span className="font-semibold text-slate-700">

        {label}

      </span>

      <button
        type="button"
        onClick={() =>
          onChange(!checked)
        }
        className={`w-12 h-7 rounded-full transition flex items-center px-1 ${checked ? "bg-slate-900 justify-end" : "bg-slate-300 justify-start"}`}
      >

        <span className="w-5 h-5 bg-white rounded-full shadow-sm" />

      </button>

    </label>
  )
}
