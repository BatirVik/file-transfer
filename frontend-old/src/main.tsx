import * as React from "react";
import * as ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Download from "@/routes/Download";
import Upload from "@/routes/Upload";
import "./index.css";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Upload />,
  },
  {
    path: "/:folderId",
    element: <Download />,
  },
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <div style={{ maxWidth: "750px" }} className="flex-1">
      <RouterProvider router={router} />
    </div>
  </React.StrictMode>,
);
