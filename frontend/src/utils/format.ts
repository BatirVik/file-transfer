export function formatSize(bytes: number | undefined): string {
  if (typeof bytes === "undefined") {
    return "unknown size";
  }
  if (bytes < 1000) {
    return `${bytes} B`;
  }
  if (bytes < 1_000_000) {
    return `${(bytes / 1000).toFixed(2)} KB`;
  }
  return `${(bytes / 1_000_000).toFixed(2)} MB`;
}
