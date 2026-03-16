import { useState } from "react";
import axios from "axios";

function App() {

  // encode states
  const [image, setImage] = useState(null);
  const [message, setMessage] = useState("");
  const [password, setPassword] = useState("");
  const [encodedImage, setEncodedImage] = useState(null);

  // decode states
  const [decodeImage, setDecodeImage] = useState(null);
  const [decodePassword, setDecodePassword] = useState("");
  const [decodedMessage, setDecodedMessage] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // ======================
  // ENCODE FUNCTION
  // ======================
  const handleEncode = async (e) => {
    e.preventDefault();

    if (!image) {
      setError("Please upload an image.");
      return;
    }

    setError("");
    setLoading(true);

    const formData = new FormData();
    formData.append("image", image);
    formData.append("message", message);
    formData.append("password", password);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/encode/",
        formData
      );

      setEncodedImage(response.data.encoded_image);

    } catch (err) {
      console.error(err);
      setError("Encoding failed.");
    }

    setLoading(false);
  };

  // ======================
  // DECODE FUNCTION
  // ======================
  const handleDecode = async (e) => {
    e.preventDefault();

    if (!decodeImage) {
      setError("Please upload encoded image.");
      return;
    }

    setError("");
    setLoading(true);

    const formData = new FormData();
    formData.append("image", decodeImage);
    formData.append("password", decodePassword);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/decode/",
        formData
      );

      setDecodedMessage(response.data.decoded_message);

    } catch (err) {
      console.error(err);
      setError("Decoding failed.");
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>

      <h1>Steganography Tool</h1>

      {/* ================= ENCODE ================= */}

      <h2>Encode Message</h2>

      <form onSubmit={handleEncode}>

        <input
          type="file"
          accept="image/*"
          onChange={(e) => setImage(e.target.files[0])}
        />

        <br /><br />

        <input
          type="text"
          placeholder="Secret message"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />

        <br /><br />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <br /><br />

        <button type="submit">
          {loading ? "Encoding..." : "Encode"}
        </button>

      </form>

      {encodedImage && (
        <div style={{ marginTop: "20px" }}>
          <h3>Encoded Image</h3>

          <img
            src={`data:image/png;base64,${encodedImage}`}
            width="300"
            alt="encoded"
          />

          <br /><br />

          <a
            href={`data:image/png;base64,${encodedImage}`}
            download="encoded.png"
          >
            Download Image
          </a>
        </div>
      )}

      <hr style={{ margin: "40px 0" }} />

      {/* ================= DECODE ================= */}

      <h2>Decode Message</h2>

      <form onSubmit={handleDecode}>

        <input
          type="file"
          accept="image/*"
          onChange={(e) => setDecodeImage(e.target.files[0])}
        />

        <br /><br />

        <input
          type="password"
          placeholder="Password"
          value={decodePassword}
          onChange={(e) => setDecodePassword(e.target.value)}
        />

        <br /><br />

        <button type="submit">
          {loading ? "Decoding..." : "Decode"}
        </button>

      </form>

      {decodedMessage && (
        <div style={{ marginTop: "20px" }}>
          <h3>Decoded Message</h3>
          <p>{decodedMessage}</p>
        </div>
      )}

      {error && (
        <p style={{ color: "red" }}>{error}</p>
      )}

    </div>
  );
}

export default App;