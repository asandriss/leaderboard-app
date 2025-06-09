import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Table, Spinner, Alert, Button } from "react-bootstrap";
import Layout from "../components/Layout";

interface Submission {
  title: string;
  score: number;
  date: string;
}

const UserPage = () => {
  const { username } = useParams();
  const navigate = useNavigate();
  const [submissions, setSubmissions] = useState<Submission[]>([]);
  const [topScores, setTopScores] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!username) return;
    fetch(`http://localhost:5000/submissions/${username}`)
      .then((res) => res.json())
      .then((data: Submission[]) => {
        setSubmissions(data);

        // Compute top 24 scores
        const scores = [...data.map((s) => s.score)]
          .sort((a, b) => b - a)
          .slice(0, 24);
        setTopScores(scores);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load submissions");
        setLoading(false);
      });
  }, [username]);

  const isTopScore = (score: number, used: Set<number>) => {
    const index = topScores.findIndex(
      (s, i) => s === score && !used.has(i)
    );
    if (index === -1) return false;
    used.add(index);
    return true;
  };

  return (
    <Layout>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2>Submissions for {username}</h2>
        <Button variant="secondary" onClick={() => navigate("/")}>
          ← Back
        </Button>
      </div>

      {loading && <Spinner animation="border" />}
      {error && <Alert variant="danger">{error}</Alert>}
      {!loading && !error && (
        <>
          <p className="mt-3">
            <strong>Top 24 total score:</strong>{" "}
            {topScores.reduce((a, b) => a + b, 0)}
          </p>
          <p>
            ✅ indicates submissions that contributed to the leaderboard score.
          </p>
          <Table striped bordered hover variant="dark">
            <thead>
              <tr>
                <th>Title</th>
                <th>Score</th>
                <th>Date</th>
                <th>Top Score?</th>
              </tr>
            </thead>
            <tbody>
              {(() => {
                const usedIndexes = new Set<number>();
                return submissions.map((sub, index) => {
                  const counted = isTopScore(sub.score, usedIndexes);
                  return (
                    <tr key={index}>
                      <td>{sub.title}</td>
                      <td>{sub.score}</td>
                      <td>{sub.date}</td>
                      <td className="text-center">{counted ? "✅" : ""}</td>
                    </tr>
                  );
                });
              })()}
            </tbody>
          </Table>
        </>
      )}
    </Layout>
  );
};

export default UserPage;
