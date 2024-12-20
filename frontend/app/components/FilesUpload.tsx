"use client";

import {Dispatch, SetStateAction} from "react";
import {formatSize} from "@/app/utils/format";

type FilesData = { [key: string]: File };

interface Props {
  files: FilesData;
  setFiles: Dispatch<SetStateAction<FilesData>>;
}

export default function Files({files, setFiles}: Props) {
  function removeFile(id: string): void {
    const newFiles: FilesData = {}
    Object.assign(newFiles, files)
    delete newFiles[id]
    setFiles(newFiles);
  }

  const filesItems = Object.entries(files).map(([id, file]) => (
    <li key={id} className="gap-4 flex items-center m-6">
      <div>{file.name}</div>
      <div className="ml-auto text-nowrap">{formatSize(file.size)}</div>
      <button onClick={() => removeFile(id)}>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          fill="currentColor"
          viewBox="0 0 16 16"
        >
          <path
            d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
        </svg>
      </button>
    </li>
  ));
  return <ul>{filesItems}</ul>;
}
