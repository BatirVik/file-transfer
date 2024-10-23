import PanelDownload from "@/components/PanelDownload";
import FilesDownload from "@/components/FilesDonwload";
import NotFound from "@/components/NotFound";
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
  const [notFound, setNotFound] = useState(false);

  useEffect(() => {
    fetch(apiUrl + "/v1/folders/" + folderId)
      .then(async (response) => {
        if (!response.ok) {
          if ([404, 410, 422].includes(response.status)) {
            setNotFound(true);
          }
          console.error(
            `Failed: ${response.status} - ${await response.text()}`,
          );
          return;
        }
        const data = await response.json();
        setFilesInfo(data.files);
        setNotFound(false);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [folderId]);

  function OnDownloadClickHandler() {
    const a = document.createElement("a");
    document.body.appendChild(a);
    a.href = `${apiUrl}/v1/folders/${folderId}/download`;
    a.click();
    a.remove();
  }

  if (notFound) {
    return <NotFound />;
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
