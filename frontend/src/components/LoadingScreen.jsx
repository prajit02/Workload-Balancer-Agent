export default function LoadingScreen() {
  return (
    <div className="flex items-center justify-center p-10">
      <div className="text-center">
        <div className="mx-auto mb-4 w-16 h-16 border-4 border-t-transparent rounded-full animate-spin border-brand-500"></div>
        <div className="text-slate-700 font-medium">Fetching tasks & analyzing with AI…</div>
        <div className="text-sm text-slate-500 mt-2">This may take up to 2 minutes. Please wait.</div>
      </div>
    </div>
  );
}
