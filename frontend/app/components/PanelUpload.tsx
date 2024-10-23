import { ChangeEventHandler, MouseEventHandler } from "react";
import Link from "next/link";

interface Props {
  onUploadClick: MouseEventHandler;
  onFilesChoose: ChangeEventHandler;
  hideUpload: boolean;
}

export default function PanelUpload({
  onUploadClick,
  onFilesChoose,
  hideUpload,
}: Props) {
  return (
    <div className="flex text-white rounded-xl m-4 overflow-hidden h-12 bg-slate-500">
      <div className="flex flex-1 bg-slate-700 p-2 rounded-r-xl">
        <Link
          href="/"
          className="text-xl mr-auto flex items-center justify-center font-bold"
        >
          FileTransfer
        </Link>
        <label
          htmlFor="file-input"
          className="ml-auto flex items-center justify-center hover:cursor-pointer"
        >
          Add Files
        </label>
        <input
          id="file-input"
          type="file"
          multiple
          onChange={onFilesChoose}
          className="hidden"
        />
      </div>

      <button
        id="files-form-submit"
        type="submit"
        onClick={onUploadClick}
        className="ml-auto flex items-center justify-center p-2 transition-all"
        style={hideUpload ? { width: 0, padding: 0 } : {}}
        disabled={hideUpload}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          fill="currentColor"
          viewBox="0 0 16 16"
        >
          <path
            fillRule="evenodd"
            d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8m15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-7.5 3.5a.5.5 0 0 1-1 0V5.707L5.354 7.854a.5.5 0 1 1-.708-.708l3-3a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 5.707z"
          />
        </svg>
      </button>
    </div>
  );
}
