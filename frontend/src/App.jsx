import { useState } from "react";
import WorkloadForm from "./components/WorkloadForm.jsx";
import LoadingScreen from "./components/LoadingScreen.jsx";
import TeamSummary from "./components/TeamSummary.jsx";
import TaskList from "./components/TaskList.jsx";
import PRData from "./components/PRData.jsx";
import AdoItems from "./components/ADOItems.jsx";

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // wrapper called by form
  const analyze = async ({ org, project, pat }) => {
    setError("");
    setLoading(true);
    setResult(null);

    try {
      // call backend; backend expects analyze=true to run Gemini
      const params = new URLSearchParams({ org, project, pat, analyze: "true" });
      const res = await fetch(`http://127.0.0.1:8000/workitems?${params.toString()}`, {
        method: "GET",
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || JSON.stringify(data));

      // console.log(data);

      setResult(data);
    } catch (e) {
      console.error(e);
      setError(String(e));
    } finally {
      setLoading(false);
    }
  };

  const fetchOnly = async ({ org, project, pat }) => {
  setError("");
  setLoading(true);
  setResult(null);

  try {
    const params = new URLSearchParams({ org, project, pat });
    const res = await fetch(`http://127.0.0.1:8000/workitems?${params.toString()}`);
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || JSON.stringify(data));
    setResult(data);
  } catch (e) {
    console.error(e);
    setError(String(e));
  } finally {
    setLoading(false);
  }
};


  return (
    <div className="max-w-6xl mx-auto p-6">
      <header className="mb-6">
        <h1 className="text-3xl font-semibold text-slate-800">Workload Balancing Agent</h1>
        <p className="text-sm text-slate-500 mt-1">Analyze Azure DevOps tasks and get workload insights.</p>
      </header>

      <main>
        <div className="mb-6">
          <WorkloadForm onAnalyze={analyze} onFetchOnly={fetchOnly} disabled={loading} />
        </div>

        {loading && <LoadingScreen />}

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded mb-6">
            <strong>Error:</strong> {error}
          </div>
        )}

      {result && (
        <section className="space-y-6">
          {(() => {
            /*
            Normalize workItems:
            - If workItems has analyzed_items -> use those + team summary
            - Else if workItems is an array -> use it directly
            */
            const w = result.workItems;
            const isAnalyzed = w && typeof w === "object" && Array.isArray(w.analyzed_items);
            const analyzedItems = isAnalyzed ? w.analyzed_items : w
              // : Array.isArray(w) ? w 
                // : Array.isArray(w?.workItems) ? w.workItems
                //   : [];

            const teamSummary = isAnalyzed ? w.team_summary : null;

            return (
              <>
                {/* PR Data & ADO Items (top-level keys) */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                  <div>{result["PR Data"] ? <PRData data={result["PR Data"]} /> : null}</div>
                  <div>{result["ADO Items"] ? <AdoItems data={result["ADO Items"]} /> : null}</div>
                </div>

                {teamSummary ? (
                  /* If we have a team summary (analyzed path) show summary + analyzed tasks */
                  <>
                    <TeamSummary summary={teamSummary} />
                    <TaskList items={analyzedItems} />
                  </>
                ) : (
                  /* Otherwise show simple fetched task list */
                  <>
                    <h2 className="text-xl font-semibold text-slate-700">Fetched Work Items</h2>
                    <TaskList items={analyzedItems} />
                  </>
                )}

              </>
            );
          })()}
        </section>
      )}


      </main>
    </div>
  );
}
