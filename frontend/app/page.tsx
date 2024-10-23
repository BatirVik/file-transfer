"use client";

import FilesUpload from "@/app/components/FilesUpload";
import PanelUpload from "@/app/components/PanelUpload";

import { ChangeEvent, MouseEvent, useState } from "react";
import { redirect } from "next/navigation";
import { v4 as uuidv4 } from "uuid";
import Loading from "./components/Loading";

interface Files {
  [key: string]: File;
}

export default function Page() {
  const [selectedFiles, setSelectedFiles] = useState({} as Files);
  const [isLoading, setIsLoading] = useState(false);

  function onFilesChoose(event: ChangeEvent<HTMLInputElement>) {
    const files = event.target.files;
    if (!files || !files.length) {
      return;
    }
    const newSelectedFiles: Files = {};
    Object.assign(newSelectedFiles, selectedFiles);
    for (const file of files) {
      newSelectedFiles[uuidv4()] = file;
    }
    setSelectedFiles(newSelectedFiles);
  }

  async function uploadFiles(): Promise<string> {
    const formData = new FormData();
    for (const file of Object.values(selectedFiles)) {
      formData.append("files", file);
    }
    formData.append("lifetimeMinutes", "100");
    const url = `${process.env.NEXT_PUBLIC_API_URL}/v1/folders`;
    const response = await fetch(url, {
      method: "POST",
      body: formData,
    });
    if (!response.ok) {
      throw new Error(`Failed: ${response.status} - ${await response.text()}`);
    }
    const data = await response.json();
    return data.id;
  }

  async function onUploadClick(event: MouseEvent) {
    event.preventDefault();
    setIsLoading(true);
    try {
      const id = await uploadFiles();
      redirect(`/${id}`);
    } finally {
      setIsLoading(false);
    }
  }

  const hideUpload = Object.keys(selectedFiles).length === 0;
  return (
    <div className="flex justify-center">
      {isLoading && <Loading />}
      <div style={{ width: 750 }}>
        <PanelUpload
          onFilesChoose={onFilesChoose}
          onUploadClick={onUploadClick}
          hideUpload={hideUpload || isLoading}
        />
        <FilesUpload files={selectedFiles} setFiles={setSelectedFiles} />
      </div>
    </div>
  );
}
