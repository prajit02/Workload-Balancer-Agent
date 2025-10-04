export default function TeamSummary({ summary }) {
  // defensive defaults
  const overloaded = (summary && summary.overloaded_members) || [];
  const under = (summary && summary.underutilized_members) || [];
  const efficient = (summary && summary.most_efficient_members) || [];

  const card = (title, list, emptyText, colorClass) => (
    <div className="bg-white rounded-lg shadow p-4 flex-1">
      <h3 className={`text-lg font-semibold ${colorClass}`}>{title}</h3>
      <div className="mt-3 space-y-2">
        {list.length === 0 ? (
          <div className="text-sm text-slate-500">{emptyText}</div>
        ) : (
          list.map((m, i) => (
            <div key={i} className="border border-slate-100 p-3 rounded">
              <div className="font-medium">{m.name}</div>
              <div className="text-sm text-slate-600 mt-1">{m.reason}</div>
            </div>
          ))
        )}
      </div>
    </div>
  );

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {card("Overloaded", overloaded, "No overloaded members detected.", "text-red-600")}
      {card("Can Take More", under, "No clear underutilized members.", "text-amber-600")}
      {card("Most Efficient", efficient, "No efficiency winners identified.", "text-green-600")}
    </div>
  );
}
