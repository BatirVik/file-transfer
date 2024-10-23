import { formatSize } from "@/app/utils/format";
import config from "@/app/config";

interface FileInfo {
  id: string;
  filename?: string;
  size: number;
}

interface Props {
  files: FileInfo[];
}

const apiURL = config.API_URL;

export default function FilesDownload({ files }: Props) {
  const filesItems = files.map((file) => (
    <li key={file.id} className="gap-4 flex items-center m-6">
      <div>{file.filename}</div>
      <div className="ml-auto text-nowrap">{formatSize(file.size)}</div>
      <a href={`${apiURL}/v1/files/${file.id}/download`} download>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          fill="currentColor"
          viewBox="0 0 16 16"
        >
          <path
            fillRule="evenodd"
            d="M8 1a.5.5 0 0 1 .5.5v11.793l3.146-3.147a.5.5 0 0 1 .708.708l-4 4a.5.5 0 0 1-.708 0l-4-4a.5.5 0 0 1 .708-.708L7.5 13.293V1.5A.5.5 0 0 1 8 1"
          />
        </svg>
      </a>
    </li>
  ));
  return <ul>{filesItems}</ul>;
}
