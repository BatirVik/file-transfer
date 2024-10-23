import Link from "next/link";

export default function Loading() {
  return (
    <div className="w-screen h-screen flex-col flex items-center justify-center">
      <h1 className="text-center text-2xl mb-2 font-bold">Folder not found!</h1>
      <Link
        href="/"
        className="bg-slate-700 hover:bg-slate-500 transition-colors p-1 rounded-md text-white"
      >
        Go to upload page
      </Link>
    </div>
  );
}
