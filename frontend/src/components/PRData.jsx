export default function PRData({ data }) {
  if (!data) return null;

  const metrics = data.metricsInfo || {};
  const pullRequests = data.pullRequests?.requestsInfo || [];

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm">
      <h2 className="text-xl font-semibold mb-4">PR Insights</h2>

      {/* Metrics Summary */}
      <div className="mb-4">
        <h3 className="text-lg font-medium mb-2">Contribution Metrics</h3>
        {Object.keys(metrics).length === 0 ? (
          <p className="text-slate-500 text-sm">No PR metrics found.</p>
        ) : (
          <ul className="list-disc pl-5 space-y-1">
            {Object.entries(metrics).map(([name, counts], idx) => (
              <li key={idx}>
                <strong>{name}</strong>: {counts.created_count || 0} created, {counts.reviewed_count || 0} reviewed
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* PR List */}
      <div>
        <h3 className="text-lg font-medium mb-2">Recent Pull Requests</h3>
        {pullRequests.length === 0 ? (
          <p className="text-slate-500 text-sm">No pull requests found.</p>
        ) : (
          <div className="overflow-auto">
            <table className="w-full text-sm border border-slate-200">
              <thead className="bg-slate-100">
                <tr>
                  <th className="border p-2">ID</th>
                  <th className="border p-2">Title</th>
                  <th className="border p-2">Created By</th>
                  <th className="border p-2">Status</th>
                  {/* you can add more columns if needed */}
                </tr>
              </thead>
              <tbody>
                {pullRequests.map((pr, idx) => (
                  <tr key={idx}>
                    <td className="border p-2">{pr.pullRequestId}</td>
                    <td className="border p-2">{pr.title}</td>
                    <td className="border p-2">{pr.createdBy?.displayName}</td>
                    <td className="border p-2">{pr.status}</td>
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
