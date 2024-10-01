import Panel from "./Panel";
import Files from "./Files";
import { useImmer } from "use-immer";
import { v4 as uuidv4 } from "uuid";
import Loading from "./Loading";

const apiURL = import.meta.env.VITE_API_URL;

export default function UploadPage() {
  const [selectedFiles, setSelectedFiles] = useImmer({});
  const [isLoading, setIsLoading] = useImmer(false);

  function onFilesChoose(event) {
    setSelectedFiles((draft) => {
      for (const file of event.target.files) {
        draft[uuidv4()] = file;
      }
    });
  }

  async function uploadFiles() {
    const formData = new FormData();
    for (const file of Object.values(selectedFiles)) {
      formData.append("files", file);
    }
    formData.append("lifetime_minutes", 100);
    const response = await fetch(apiURL + "/v1/folders", {
      method: "POST",
      body: formData,
    });
    if (!response.ok) {
      throw new Error(`Failed: ${response.status} - ${await response.text()}`);
    }
    const data = await response.json();
    if (data.id === undefined) {
      throw new Error(`Response don't include folder id`);
    }
    return data.id;
  }

  async function onCopyClick(event) {
    event.preventDefault();
    setIsLoading(true);
    try {
      const id = await uploadFiles();
      const url = new URL(window.origin);
      url.searchParams.set("id", id);
      await navigator.clipboard.writeText(url);
    } finally {
      setIsLoading(false);
    }
  }

  const isCopyBtnDisabled = Object.keys(selectedFiles).length === 0;
  return (
    <div style={{ maxWidth: "750px" }} className="flex-1">
      {isLoading && <Loading />}
      <Panel
        onFilesChoose={onFilesChoose}
        onCopyClick={onCopyClick}
        isCopyBtnDisabled={isCopyBtnDisabled}
      />
      <Files files={selectedFiles} setFiles={setSelectedFiles} />
    </div>
  );
}
