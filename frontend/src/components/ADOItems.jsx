export default function AdoItems({ data }) {
  if (!data) return null;

  const metrics = data.metricsInfo || {};
  const items = data.adoItems || [];

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm">
      <h2 className="text-xl font-semibold mb-4">ADO Items (Non-Task)</h2>

      {/* Metrics Summary */}
      <div className="mb-4">
        <h3 className="text-lg font-medium mb-2">Created by Type</h3>
        {Object.keys(metrics).length === 0 ? (
          <p className="text-slate-500 text-sm">No metrics found.</p>
        ) : (
          <ul className="list-disc pl-5 space-y-1">
            {Object.entries(metrics).map(([name, typeCounts], idx) => (
              <li key={idx}>
                <strong>{name}</strong>:
                {Object.entries(typeCounts).map(([type, count]) => (
                  <span key={type}> {type} ({count}) </span>
                ))}
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Item List */}
      <div>
        <h3 className="text-lg font-medium mb-2">Recent ADO Items</h3>
        {items.length === 0 ? (
          <p className="text-slate-500 text-sm">No ADO items found.</p>
        ) : (
          <div className="overflow-auto">
            <table className="w-full text-sm border border-slate-200">
              <thead className="bg-slate-100">
                <tr>
                  <th className="border p-2">ID</th>
                  <th className="border p-2">Title</th>
                  <th className="border p-2">Type</th>
                  <th className="border p-2">Created By</th>
                  <th className="border p-2">Created Date</th>
                </tr>
              </thead>
              <tbody>
                {items.map((item, idx) => (
                  <tr key={idx}>
                    <td className="border p-2">{item.id}</td>
                    <td className="border p-2">{item.fields["System.Title"]}</td>
                    <td className="border p-2">{item.fields["System.WorkItemType"]}</td>
                    <td className="border p-2">{item.fields["System.CreatedBy.displayName"]}</td>
                    <td className="border p-2">{item.fields["System.CreatedDate"]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}