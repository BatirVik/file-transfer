import PropTypes from "prop-types";

export default function Panel({
  onFilesChoose,
  onCopyClick,
  isCopyBtnDisabled,
}) {
  return (
    <div className="flex text-white rounded-xl m-4 overflow-hidden h-12 bg-gray-700 ">
      <h1 className="text-xl mr-auto flex items-center justify-center p-2 font-bold">
        FileTransfer
      </h1>
      <div className="flex bg-gray-800">
        <label
          htmlFor="files-input"
          id="files-input-label"
          className="ml-auto bg-gray-700 rounded-r-xl flex items-center justify-center p-2  hover:cursor-pointer"
        >
          Add files
        </label>
        <input
          type="file"
          id="files-input"
          multiple
          className="hidden"
          onChange={onFilesChoose}
        />
        <button
          id="files-form-submit"
          type="submit"
          onClick={onCopyClick}
          className="ml-auto flex items-center justify-center p-2 transition-all"
          style={isCopyBtnDisabled ? { width: 0, padding: 0 } : {}}
          disabled={isCopyBtnDisabled}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            fill="currentColor"
            viewBox="0 0 16 16"
          >
            <path d="M4.715 6.542 3.343 7.914a3 3 0 1 0 4.243 4.243l1.828-1.829A3 3 0 0 0 8.586 5.5L8 6.086a1 1 0 0 0-.154.199 2 2 0 0 1 .861 3.337L6.88 11.45a2 2 0 1 1-2.83-2.83l.793-.792a4 4 0 0 1-.128-1.287z" />
            <path d="M6.586 4.672A3 3 0 0 0 7.414 9.5l.775-.776a2 2 0 0 1-.896-3.346L9.12 3.55a2 2 0 1 1 2.83 2.83l-.793.792c.112.42.155.855.128 1.287l1.372-1.372a3 3 0 1 0-4.243-4.243z" />
          </svg>
        </button>
      </div>
    </div>
  );
}

Panel.propTypes = {
  onFilesChoose: PropTypes.func.isRequired,
  onCopyClick: PropTypes.func.isRequired,
  isCopyBtnDisabled: PropTypes.bool.isRequired,
};
