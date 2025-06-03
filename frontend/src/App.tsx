import React, { useState } from 'react';
import { Form, Button, Alert } from 'react-bootstrap';
import axios from 'axios';
import Layout from './components/Layout';
import Leaderboard from './Leaderboard';

const App = () => {
  const [jsonResult, setJsonResult] = useState(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    const fileInput = form.elements.namedItem('file') as HTMLInputElement;
    if (!fileInput?.files?.[0]) return;

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
      const response = await axios.post('http://localhost:5000/upload', formData);
      setJsonResult(response.data);
      setError(null);
    } catch (err: unknown) {
      if (err instanceof Error) setError(err.message);
      else setError('Upload failed');
    }
  };

  return (
    <Layout>
      <h2>Upload JSON</h2>
      <Form onSubmit={handleFileUpload}>
        <Form.Group controlId="formFile" className="mb-3">
          <Form.Control type="file" name="file" accept=".json" required />
        </Form.Group>
        <Button variant="primary" type="submit">Upload</Button>
      </Form>
      {error && <Alert variant="danger" className="mt-3">{error}</Alert>}

      {jsonResult && (
        <div className="mt-4">
          <h4>Response</h4>
          <pre>{JSON.stringify(jsonResult, null, 2)}</pre>
        </div>
      )}

      <div className="mt-5">
        <Leaderboard />
      </div>
    </Layout>
  );
};

export default App;
