"use client";

import PanelDownload from "@/app/components/PanelDownload";
import FilesDownload from "@/app/components/FilesDonwload";
import NotFound from "@/app/components/NotFound";
import Loading from "@/app/components/Loading";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

interface FileInfo {
  id: string;
  filename?: string;
  size: number;
}

export default function Page() {
  const [filesInfo, setFilesInfo] = useState([] as FileInfo[]);
  const [isLoading, setIsLoading] = useState(true);
  const [notFound, setNotFound] = useState(false);

  const { id } = useParams<{ id: string }>();

  useEffect(() => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/v1/folders/${id}`;
    fetch(url)
      .then(async (response) => {
        if (response.ok) {
          const data = await response.json();
          setFilesInfo(data.files);
          setNotFound(false);
          return;
        }
        console.error(`Failed: ${response.status} - ${await response.json()}`);
        if ([404, 410, 422].includes(response.status)) {
          setNotFound(true);
        }
      })
      .finally(() => {
        setIsLoading(false);
      });
  });

  function downloadFolder() {
    const a = document.createElement("a");
    document.body.appendChild(a);
    a.href = `${process.env.NEXT_PUBLIC_API_URL}/v1/folders/${id}/download`;
    a.click();
    a.remove();
  }

  if (notFound) {
    return <NotFound />;
  }

  const hideDownload = filesInfo.length === 0;
  return (
    <>
      <div className="flex justify-center">
        {isLoading && <Loading />}
        <div style={{ width: 750 }}>
          <PanelDownload
            hideDownload={hideDownload}
            onDownloadClick={downloadFolder}
          />
          <FilesDownload files={filesInfo} />
        </div>
      </div>
    </>
  );
}
