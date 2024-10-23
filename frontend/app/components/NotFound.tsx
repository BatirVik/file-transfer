import { Link } from "react-router-dom";

export default function Loading() {
  return (
    <div className="fixed inset-0 w-screen h-screen flex justify-center items-center flex-col font-bold">
      <h1 className="text-4xl mb-4">Folder not found</h1>
      <p>
        {"Go to "}
        <Link to="/" className="text-blue-500 underline ">
          upload page
        </Link>
      </p>
    </div>
  );
}
