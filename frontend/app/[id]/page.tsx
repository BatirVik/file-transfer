import PanelDownload from "@/app/components/PanelDownload";
import FilesDownload from "@/app/components/FilesDonwload";
import NotFound from "@/app/components/NotFound";
import Loading from "@/app/components/Loading";
import { Suspense, useEffect, useState } from "react";
import { useRouter } from "next/router";

const apiUrl: string = import.meta.env.VITE_API_URL;



interface Props {
  id: string;
}

export default async function Download({ id }: Props) {
  const [isLoading, setIsLoading] = useState(true);
  const [notFound, setNotFound] = useState(false);


    console.error(`Failed: ${response.status} - ${await response.text()}`);
  }
  const filesInfo = data.files;

  function onDownloadClickHandler() {
    const a = document.createElement("a");
    document.body.appendChild(a);
    a.href = `${apiUrl}/v1/folders/${id}/download`;
    a.click();
    a.remove();
  }

  if (notFound) {
    return <NotFound />;
  }

  const hideDownload = filesInfo.length === 0;
  return (
    <>
      <PanelDownload
        hideDownload={hideDownload}
        onDownloadClick={onDownloadClickHandler}
      />
      <Suspense>
        <FilesDownload files={filesInfo} />
      </Suspense>
    </>
  );
}
