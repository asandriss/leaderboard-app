import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Alert, Button } from 'react-bootstrap';
import axios from 'axios';
import Uploader from '../components/Uploader';
import Leaderboard from '../components/Leaderboard';

const HomePage = () => {
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
      setTimeout(() => setStatusMessage(null), 3000);
      fetchLeaderboard();
    } catch {
      setStatusMessage("Failed to clear data.");
    }
  };

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  return (
    <>
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
    </>
  );
};

export default HomePage;
