export default function TaskList({ items }) {
  if (!items || items.length === 0) {
    return <div className="mt-4 text-slate-500">No tasks analyzed yet.</div>;
  }

  return (
    <div className="mt-6">
      <h2 className="text-xl font-semibold mb-4">Task Breakdown</h2>
      <div className="space-y-3">
        {items.map((it) => (
          <div key={it.id} className="bg-white rounded p-4 shadow-sm">
            <div className="flex items-start justify-between">
              <div>
                <div className="text-lg font-medium">{it.fields?.["System.Title"] || "Untitled"}</div>
                <div className="text-sm text-slate-500 mt-1">
                  Assigned to: <span className="font-medium">{it.fields?.["System.AssignedTo"]?.displayName || "Unassigned"}</span>
                </div>
              </div>
              <div className="text-right">
                <div className="text-sm text-slate-500">Workload score</div>
                <div className="text-2xl font-semibold text-brand-700">{it.analysis?.score ?? "-"}</div>
              </div>
            </div>

            <div className="mt-3 text-slate-700">
              <div className="font-medium">AI Reason:</div>
              <div className="text-sm text-slate-600 mt-1">{it.analysis?.reason || "No reason provided."}</div>

              <details className="mt-3 text-sm">
                <summary className="cursor-pointer text-slate-500">View comments / raw AI output</summary>
                <pre className="bg-slate-50 p-3 rounded mt-2 text-xs overflow-auto">
{JSON.stringify({ comments: it.comments, raw: it.analysis?.raw }, null, 2)}
                </pre>
              </details>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
