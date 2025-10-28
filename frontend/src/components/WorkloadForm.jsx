import { useState } from "react";

export default function WorkloadForm({ onAnalyze, onFetchOnly, disabled }) {
  const [org, setOrg] = useState("");
  const [project, setProject] = useState("");
  const [pat, setPat] = useState("");

  const handleSubmit = (e, analyze) => {
    e.preventDefault();
    if (!org || !project || !pat) {
      alert("Please fill Organization, Project and PAT.");
      return;
    }
    if (analyze) onAnalyze({ org, project, pat });
    else onFetchOnly({ org, project, pat });
  };

  return (
    <form className="bg-white p-6 rounded-lg shadow-sm grid gap-4 sm:grid-cols-3">
      <div className="sm:col-span-1">
        <label className="block text-sm text-slate-700 mb-1">Organization</label>
        <input
          value={org}
          onChange={(e) => setOrg(e.target.value)}
          className="w-full border border-slate-200 rounded p-2"
          placeholder="your-org"
          disabled={disabled}
        />
      </div>

      <div className="sm:col-span-1">
        <label className="block text-sm text-slate-700 mb-1">Project</label>
        <input
          value={project}
          onChange={(e) => setProject(e.target.value)}
          className="w-full border border-slate-200 rounded p-2"
          placeholder="your-project"
          disabled={disabled}
        />
      </div>

      <div className="sm:col-span-1">
        <label className="block text-sm text-slate-700 mb-1">Azure DevOps PAT</label>
        <input
          value={pat}
          onChange={(e) => setPat(e.target.value)}
          type="password"
          className="w-full border border-slate-200 rounded p-2"
          placeholder="Personal Access Token"
          disabled={disabled}
        />
      </div>

      <div className="sm:col-span-3 flex justify-end gap-3 mt-2">
        <button
          type="button"
          onClick={(e) => handleSubmit(e, false)}
          disabled={disabled}
          className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded shadow"
        >
          {disabled ? "Fetching..." : "Fetch Only"}
        </button>

        <button
          type="button"
          onClick={(e) => handleSubmit(e, true)}
          disabled={disabled}
          className="bg-brand-500 hover:bg-brand-600 text-white px-4 py-2 rounded shadow"
        >
          {disabled ? "Analyzing..." : "Analyze with AI"}
        </button>
      </div>
    </form>
  );
}
