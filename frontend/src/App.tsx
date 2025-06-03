import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Alert, Button } from 'react-bootstrap';
import axios from 'axios';
import Uploader from './Uploader';
import Leaderboard from './Leaderboard';
import './App.css';

const App = () => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [error, setError] = useState<string | null>(null);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  const fetchLeaderboard = async () => {
    try {
      const response = await axios.get('http://localhost:5000/leaderboard');
      setLeaderboard(response.data);
    } catch (err) {
      setError("Failed to load leaderboard");
    }
  };

  const clearData = async () => {
    try {
      await axios.delete('http://localhost:5000/submissions');
      setStatusMessage("All data cleared.");
      fetchLeaderboard();
    } catch {
      setStatusMessage("Failed to clear data.");
    }
  };

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  return (
    <div className="bg-dark text-light min-vh-100">
      <Container className="py-4">
        <Row>
          <Col><h2>Upload JSON</h2></Col>
          <Col className="text-end">
            <Button variant="danger" onClick={clearData}>Clear All Data</Button>
          </Col>
        </Row>
        {error && <Alert variant="danger">{error}</Alert>}
        {statusMessage && <Alert variant="info" className="mt-3">{statusMessage}</Alert>}
        <Uploader onUploadSuccess={fetchLeaderboard} />
        <hr className="border-light" />
        <Leaderboard entries={leaderboard} />
      </Container>
    </div>
  );
};

export default App;
