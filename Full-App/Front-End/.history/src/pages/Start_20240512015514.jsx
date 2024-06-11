import { useState } from "react";

export const Start = () => {
  const [file, setFile] = useState(null);
  const [processedVideo, setProcessedVideo] = useState(null);
  const [uploadedVideo, setUploadedVideo] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setUploadedVideo(URL.createObjectURL(event.target.files[0]));
  };

  const resetPage = () => {
    setFile(null);
    setProcessedVideo(null);
    setUploadedVideo(null);
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
      setProcessedVideo(URL.createObjectURL(blob));
    } catch (error) {
      console.error("Error processing the video:", error);
    }
  };

  return (
    <div className="container mx-auto max-w-lg">
      <div className="p-4">
        <form onSubmit={handleSubmit} id="upload-form">
          <div className="mb-4">
            <label htmlFor="video" className="block text-gray-700 font-bold">
              Upload Video:
            </label>
            <input
              type="file"
              onChange={handleFileChange}
              accept="video/*"
              name="video"
              required
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            />
          </div>
          <div className="mb-4">
            <button
              type="submit"
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >
              Detect
            </button>
            <button
              type="button"
              onClick={resetPage}
              className="ml-2 bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded"
            >
              Reset
            </button>
          </div>
        </form>
      </div>
      {uploadedVideo && (
        <div className="p-4 border border-gray-300">
          <label className="block text-gray-700 font-bold mb-2">
            Uploaded Video:
          </label>
          <div className="aspect-w-16 aspect-h-9 mb-2">
            <video
              src={uploadedVideo}
              className="object-cover w-full h-full"
              controls
            ></video>
          </div>
        </div>
      )}
      {processedVideo && (
        <div className="p-4 border border-gray-300">
          <label className="block text-gray-700 font-bold mb-2">
            Detected Violence:
          </label>
          <div className="aspect-w-16 aspect-h-9">
            <video
              src={processedVideo}
              className="object-cover w-full h-full"
              controls
            ></video>
          </div>
        </div>
      )}
    </div>
  );
};
