import React from "react";
import FileUpload from "./components/FileUpload";
import "./App.css";

function App() {
  return (
    <div className="container mt-4">
      <h4 className="text-center mb-4">
        <i className="fab fa-react"></i> Bangla OCR
      </h4>
      <FileUpload></FileUpload>
    </div>
  );
}

export default App;
