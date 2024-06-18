import { useState } from 'react'
import axios from 'axios'

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      setError('Please upload a file first.');
      return;
    }

    setLoading(true);
    setError('');
    const formData = new FormData();
    formData.append('image', file);

    try {
      const response = await axios.post(`${import.meta.env.VITE_BACKEND_URL}/api/image_upload/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setResult(response.data);
    } catch (err) {
      console.error(err);
      setError('Error uploading file.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Urine Strip Analyzer</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="image/*" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {result && (
        <div>
          <h2>RGB Values</h2>
          <ul>
            {Object.keys(result).map((key) => (
              <li key={key}>
                {key}: {result[key].join(', ')}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App
