import Panel from "./components/Panel";
import Files from "./components/Files";
import { useImmer } from "use-immer";
import { v4 as uuidv4 } from "uuid";

export default function App() {
  const [selectedFiles, setSelectedFiles] = useImmer({});

  function onFilesChoose(event) {
    setSelectedFiles((draft) => {
      for (const file of event.target.files) {
        draft[uuidv4()] = file;
      }
    });
  }

  function onCopyClick(event) {
    alert(JSON.stringify(selectedFiles));
  }

  return (
    <div style={{ maxWidth: "750px" }} className="flex-1">
      <Panel onFilesChoose={onFilesChoose} onCopyClick={onCopyClick} />
      <Files files={selectedFiles} setFiles={setSelectedFiles} />
    </div>
  );
}
