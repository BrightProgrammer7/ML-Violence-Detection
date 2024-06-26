import { useState } from "react";
import "./index.css";

function App() {
  const [file, setFile] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!file) {
      console.error("No file selected.");
      return;
    }

    const formData = new FormData();
    formData.append("video", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/detect_violence", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to process the video.");
      }

      const blob = await response.blob();
      setProcessedImage(URL.createObjectURL(blob));
    } catch (error) {
      console.error("Error processing the video:", error);
    }
  };

  return (
    <div className="container">
      <div className="sideBar">
        <form onSubmit={handleSubmit} id="upload-form">
          <div className="label">
            <label for="without_post_proccessing">
              Segmentation without Post-Processing:{" "}
            </label>
          </div>
          <input type="file" onChange={handleFileChange} />
          <button type="submit">Detect</button>
        </form>
      </div>
      {processedImage && (
        <img width={100} src={processedImage} alt="Processed" />
      )}
    </div>
  );
}

export default App;
