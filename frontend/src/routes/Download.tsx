import PanelDownload from "@/components/PanelDownload";
import FilesDownload from "@/components/FilesDonwload";
import Loading from "@/components/Loading";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

const apiUrl: string = import.meta.env.VITE_API_URL;

interface FileInfo {
  id: string;
  filename?: string;
  size: number;
}

export default function Download() {
  const { folderId } = useParams();
  const [filesInfo, setFilesInfo] = useState([] as FileInfo[]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetch(apiUrl + "/v1/folders/" + folderId)
      .then(async (response) => {
        if (!response.ok) {
          throw new Error(
            `Failed: ${response.status} - ${await response.text()}`,
          );
        }
        const data = await response.json();
        setFilesInfo(data.files);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [folderId]);

  function OnDownloadClickHandler(event) {
    alert("Download all files");
  }

  const hideDownload = filesInfo.length === 0;
  return (
    <>
      {isLoading && <Loading />}
      <PanelDownload
        hideDownload={hideDownload}
        onDownloadClick={OnDownloadClickHandler}
      />
      <FilesDownload files={filesInfo} />
    </>
  );
}
