import FilesUpload from "@/components/FilesUpload";
import Loading from "@/components/Loading";
import PanelUpload from "@/components/PanelUpload";

import { ChangeEvent, MouseEvent } from "react";

import { v4 as uuidv4 } from "uuid";
import { useImmer } from "use-immer";
import { useNavigate } from "react-router-dom";

const apiURL: string = import.meta.env.VITE_API_URL;

export default function Upload() {
  const [selectedFiles, setSelectedFiles] = useImmer(
    {} as { [key: string]: File },
  );
  const [isLoading, setIsLoading] = useImmer(false);
  const navigate = useNavigate();

  function onFilesChoose(event: ChangeEvent<HTMLInputElement>) {
    setSelectedFiles((draft) => {
      const target = event.target;
      for (const file of target.files!) {
        draft[uuidv4()] = file;
      }
      return draft;
    });
  }

  async function uploadFiles(): Promise<string> {
    const formData = new FormData();
    for (const file of Object.values(selectedFiles)) {
      formData.append("files", file);
    }
    formData.append("lifetime_minutes", "100");
    const response = await fetch(apiURL + "/v1/folders", {
      method: "POST",
      body: formData,
    });
    if (!response.ok) {
      throw new Error(`Failed: ${response.status} - ${await response.text()}`);
    }
    const data = await response.json();
    if (typeof data.id !== "string") {
      throw new Error(
        `Response don't include valid folder id {..., "id": ${data.id}}`,
      );
    }
    return data.id;
  }

  async function onUploadClick(event: MouseEvent) {
    event.preventDefault();
    setIsLoading(true);
    try {
      const id = await uploadFiles();
      navigate(id);
    } catch (err) {
      alert("Failed");
      throw err;
    } finally {
      setIsLoading(false);
    }
  }

  const hideUpload = Object.keys(selectedFiles).length === 0;
  return (
    <>
      {isLoading && <Loading />}
      <PanelUpload
        onFilesChoose={onFilesChoose}
        onUploadClick={onUploadClick}
        hideUpload={hideUpload}
      />
      <FilesUpload files={selectedFiles} setFiles={setSelectedFiles} />
    </>
  );
}
