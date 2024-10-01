import DownloadPage from "./components/DownloadPage";
import UploadPage from "./components/UploadPage";

export default function App() {
  const params = new URLSearchParams(window.location.search);
  const id = params.get("id");
  if (id == undefined) {
    return <UploadPage />;
  } else {
    return <DownloadPage folderId={id} />;
  }
}
