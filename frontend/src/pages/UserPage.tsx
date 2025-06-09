import { useParams, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { Button } from 'react-bootstrap';
import Layout from '../components/Layout';

interface Submission {
  title: string;
  score: number;
  date: string;
}

const UserPage = () => {
  const { username } = useParams();
  const [submissions, setSubmissions] = useState<Submission[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!username) return;

    fetch(`http://localhost:5000/submissions/${encodeURIComponent(username)}`)
      .then((res) => res.json())
      .then((data) => {
        setSubmissions(data);
        setLoading(false);
      });
  }, [username]);
  const navigate = useNavigate();
  return (
    <Layout>
      <h2>📄 Submissions for <strong>{username}</strong></h2>
      <Button variant="secondary" onClick={() => navigate(-1)}>
        ← Back
      </Button>
      <hr/>
      {loading ? (
        <p>Loading...</p>
      ) : submissions.length === 0 ? (
        <p>No submissions found.</p>
      ) : (
        <table className="table table-dark table-bordered table-striped">
          <thead>
            <tr>
              <th>Title</th>
              <th>Score</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {submissions.map((s, i) => (
              <tr key={i}>
                <td>{s.title}</td>
                <td>{s.score}</td>
                <td>{s.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </Layout>
  );
};

export default UserPage;
