import { useState } from "react";

export default function AdoItems({ data }) {
  if (!data) return null;

  const [showModal, setShowModal] = useState(false);
  const metrics = data.metricsInfo || {};
  const items = data.adoItems || [];

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm flex flex-col min-h-[300px]">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold">ADO Items</h2>
        {items.length > 0 && (
          <button
            onClick={() => setShowModal(true)}
            className="text-sm bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded"
          >
            View Details
          </button>
        )}
      </div>

      {/* Summary Section */}
      <div className="flex-1">
        <h3 className="text-lg font-medium mb-2">Created by Type</h3>
        {Object.keys(metrics).length === 0 ? (
          <p className="text-slate-500 text-sm">No metrics found.</p>
        ) : (
          <ul className="list-disc pl-5 space-y-1 text-sm text-slate-700">
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

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-lg w-11/12 max-w-5xl max-h-[85vh] flex flex-col">
            {/* Modal Header */}
            <div className="flex justify-between items-center border-b p-4">
              <h3 className="text-lg font-semibold">ADO Item Details</h3>
              <button
                onClick={() => setShowModal(false)}
                className="text-slate-500 hover:text-slate-700"
              >
                ✕
              </button>
            </div>

            {/* Scroll inside table */}
            <div className="p-4 flex-1">
              <div className="overflow-y-auto max-h-[65vh] border border-slate-200 rounded-md">
                <table className="w-full text-sm border-collapse">
                  <thead className="bg-slate-100 sticky top-0 z-10">
                    <tr>
                      <th className="border-b p-2 text-left">ID</th>
                      <th className="border-b p-2 text-left">Title</th>
                      <th className="border-b p-2 text-left">Type</th>
                      <th className="border-b p-2 text-left">Created By</th>
                      <th className="border-b p-2 text-left">Created Date</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {items.map((item, idx) => (
                      <tr key={idx} className="hover:bg-slate-50">
                        <td className="p-2">{item.id}</td>
                        <td className="p-2">{item.fields["System.Title"]}</td>
                        <td className="p-2">{item.fields["System.WorkItemType"]}</td>
                        <td className="p-2">{item.fields["System.CreatedBy"]?.displayName}</td>
                        <td className="p-2 text-slate-500 text-xs">
                          {new Date(item.fields["System.CreatedDate"]).toLocaleString()}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Modal Footer */}
            <div className="border-t p-3 text-right">
              <button
                onClick={() => setShowModal(false)}
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
