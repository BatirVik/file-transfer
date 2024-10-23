import { MouseEventHandler } from "react";
import Link from "next/link";

interface Props {
  onDownloadClick: MouseEventHandler;
  hideDownload: boolean;
}

export default function PanelDownload({
  onDownloadClick,
  hideDownload,
}: Props) {
  async function copyLinkToClipboard() {
    await navigator.clipboard.writeText(location.href);
  }
  return (
    <div className="flex text-white rounded-xl m-4 overflow-hidden h-12 bg-slate-500">
      <div className="flex flex-1 bg-slate-700 p-2 rounded-r-xl">
        <Link
          href="/"
          className="text-xl mr-auto flex items-center justify-center font-bold"
        >
          FileTransfer
        </Link>
        <button onClick={copyLinkToClipboard}>Copy Link</button>
      </div>
      <button
        type="submit"
        className="ml-auto flex items-center justify-center p-2 transition-all"
        onClick={onDownloadClick}
        style={hideDownload ? { width: 0, padding: 0 } : {}}
        disabled={hideDownload}
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
            d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8m15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8.5 4.5a.5.5 0 0 0-1 0v5.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293z"
          />
        </svg>
      </button>
    </div>
  );
}
