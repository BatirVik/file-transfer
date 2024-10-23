export default function Loading() {
  return (
    <div className="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-75">
      <span className="animate-ping absolute inline-flex h-32 w-32 rounded-full bg-sky-400 opacity-75"></span>
    </div>
  );
}
