import { Form, Button, Alert } from 'react-bootstrap';
import axios from 'axios';
import { useState, useEffect } from 'react';

const Uploader = ({ onUploadSuccess }: { onUploadSuccess: () => void }) => {
  const [status, setStatus] = useState<string | null>(null);

  const handleFileUpload = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const fileInput = (e.currentTarget.elements.namedItem('file') as HTMLInputElement);
    if (!fileInput?.files?.[0]) return;

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
      const response = await axios.post('http://localhost:5000/upload', formData);
      setStatus(`Stored ${response.data.stored} entries`);
      onUploadSuccess();
    } catch {
      setStatus("Upload failed");
    }
  };

  useEffect(() => {
  if (status) {
    const timer = setTimeout(() => setStatus(null), 3000);
    return () => clearTimeout(timer);
  }
}, [status]);

  return (
    <Form onSubmit={handleFileUpload}>
      <Form.Group controlId="formFile" className="mb-3">
        <Form.Control type="file" name="file" accept=".json" required />
      </Form.Group>
      <Button variant="primary" type="submit">Upload</Button>
      {status && <Alert variant="info" className="mt-3">{status}</Alert>}
    </Form>
  );
};

export default Uploader;
