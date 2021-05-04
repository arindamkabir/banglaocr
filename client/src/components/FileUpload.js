import React, { Fragment, useState } from "react";
import Message from "./Message";
import Progress from "./Progress";
import axios from "axios";
const FileUpload = () => {
  const [file, setFile] = useState("");
  const [filename, setFilename] = useState("Choose File");
  const [uploadedFile, setUploadedFile] = useState({});
  const [message, setMessage] = useState("");
  const [uploadPercentage, setUploadPercentage] = useState(0);
  const [words, setWords] = useState(0);
  const [letters, setLetters] = useState(0);
  const [predictions, setPredictions] = useState(0);

  const onChange = (e) => {
    setFile(e.target.files[0]);
    setFilename(e.target.files[0].name);
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://127.0.0.1:8000/upload/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress: (progressEvent) => {
          setUploadPercentage(
            parseInt(
              Math.round((progressEvent.loaded * 100) / progressEvent.total)
            )
          );

          // Clear percentage
          setTimeout(() => setUploadPercentage(0), 10000);
        },
      });
      console.log(res.data);
      setWords(res.data.wordCount);
      setLetters(res.data.letterCount);
      setPredictions(res.data.predictions);
      const filePath = "http://127.0.0.1:8000/media/" + filename;
      setUploadedFile({ filename, filePath });

      setMessage("File Uploaded");
    } catch (err) {
      if (err.response.status === 500) {
        setMessage("There was a problem with the server");
      } else {
        setMessage(err.response.data.msg);
      }
    }
  };

  function word_content() {
    let rowContents = [];
    rowContents.push();
    for (let index = 0; index < words; index++) {
      let word_file =
        "http://127.0.0.1:8000/media/cropped/words/" + index + ".jpg";

      rowContents.push(
        <div className="col-md-6 mt-4">
          <img src={word_file} alt="" width="100%" />
        </div>
      );
    }
    return (
      <div className="card mt-4">
        <div className="card-body">
          <h4 className="text-center text-info">Words</h4>
          <div className="row">{rowContents}</div>
        </div>
      </div>
    );
  }
  function letter_content() {
    let rowContents = [];
    rowContents.push();
    for (let index = 0; index < letters; index++) {
      let letter_file =
        "http://127.0.0.1:8000/media/cropped/letters/" + index + ".jpg";

      console.log(letter_file);
      rowContents.push(
        <div className="col-md-3 mt-4">
          <img src={letter_file} alt="" width="100%" />
          <h4 className="text-center text-info">{predictions[index]}</h4>
        </div>
      );
    }
    return (
      <div className="card mt-4">
        <div className="card-body">
          <h4 className="text-center text-info">Letters</h4>
          <div className="row">{rowContents}</div>
        </div>
      </div>
    );
  }

  return (
    <Fragment>
      {message ? <Message msg={message} /> : null}
      <form onSubmit={onSubmit}>
        <div className="custom-file mb-4">
          <input
            type="file"
            className="custom-file-input"
            id="customFile"
            onChange={onChange}
          />
          <label className="custom-file-label" htmlFor="customFile">
            {filename}
          </label>
        </div>

        <Progress percentage={uploadPercentage} />

        <input
          type="submit"
          value="Upload"
          className="btn btn-primary btn-block mt-4"
        />
      </form>
      {uploadedFile ? (
        <div className="row mt-5">
          <div className="col-md-6 m-auto">
            <h3 className="text-center">{uploadedFile.filename}</h3>
            <img style={{ width: "100%" }} src={uploadedFile.filePath} alt="" />
          </div>
        </div>
      ) : null}

      {words ? word_content() : null}
      {letters ? letter_content() : null}
    </Fragment>
  );
};

export default FileUpload;
