import config from "@/app/config";

interface FileInfo {
  id: string;
  filename?: string;
  size: number;
}

interface FolderInfo {
  files: FileInfo[];
}

interface Response {
  status: number;
  data: any;
}

interface UploadFilesResponse extends Response {
  data: FolderInfo;
}

interface FetchFolderResponse extends Response {
  data: FolderInfo;
}

export async function fetchFolderInfo(
  id: string,
): Promise<FetchFolderResponse> {
  const url = `${config.API_URL}/v1/folders/${id}`;
  const response = await fetch(url);
  return {
    status: response.status,
    data: await response.json(),
  };
}

export async function uploadFiles(
  body: FormData,
): Promise<UploadFilesResponse> {
  const url = `${config.API_URL}/v1/folders`;
  const response = await fetch(url, {
    method: "POST",
    body,
  });
  return {
    status: response.status,
    data: await response.json(),
  };
}
