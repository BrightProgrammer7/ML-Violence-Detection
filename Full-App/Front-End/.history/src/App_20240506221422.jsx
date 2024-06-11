import { useState } from "react";
import "./index.css";

function App() {
  const [file, setFile] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const resetPage 

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
            <label htmlFor="without_post_proccessing">
              {" "}
              Detecte Violence:{" "}
            </label>
          </div>
          <input
            type="file"
            onChange={handleFileChange}
            // accept=".mp3"
            accept="video/*"
            name="file"
            required
          />
          <button type="submit">Detect</button>
        </form>
      </div>
      {!processedImage ? (
        <div className="empty_container">Nothing to see at the moment</div>
      ) : (
        <div>
          <label htmlFor="without_post_proccessing">Scene Detected: </label>
          <img width={100} src={processedImage} alt="Processed" />
        </div>
      )}
      <button id="resetBtn" onClick={resetPage} type="button">Reset</button>
    </div>
    
  );
}

export default App;

<script>
        let resetBtn = document.querySelector("#resetBtn");
        resetBtn.addEventListener("click", () => {
            location.reload()
            // let empty_container = document.createElement("div");
            // empty_container.textContent = "Nothing to see at the moment";
            // empty_container.classList.add("empty_container");
            // document.querySelector("#vtk-container").replaceWith(empty_container)
        })
    </script>