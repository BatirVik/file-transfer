import PropTypes from "prop-types";

export default function Files({ files, setFiles }) {
  function removeFile(id) {
    setFiles((draft) => {
      delete draft[id];
    });
  }

  function format_size(bytes_count) {
    if (bytes_count < 1000) {
      return `${bytes_count} bytes`;
    }
    if (bytes_count < 1_000_000) {
      return `${(bytes_count / 1000).toFixed(2)} KB`;
    }
    return `${(bytes_count / 1_000_000).toFixed(2)} MB`;
  }

  const filesItems = Object.entries(files).map(([id, file]) => (
    <li key={id} className="gap-4 flex items-center m-6">
      <div>{file.name}</div>
      <div className="ml-auto text-nowrap">{format_size(file.size)}</div>
      <button onClick={() => removeFile(id)}>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          fill="currentColor"
          viewBox="0 0 16 16"
        >
          <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708" />
        </svg>
      </button>
    </li>
  ));
  return <ul>{filesItems}</ul>;
}

Files.propTypes = {
  files: PropTypes.object.isRequired,
  setFiles: PropTypes.func.isRequired,
};
