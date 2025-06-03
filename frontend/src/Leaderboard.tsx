import { useState, useEffect } from 'react';

interface LeaderboardEntry {
  user: string;
  total_score: number;
}

const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:5000/leaderboard")
      .then((res) => res.json())
      .then((data) => {
        setLeaderboard(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch leaderboard", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="mt-4">
      <h1 className="mb-4">🏆 Leaderboard</h1>
      {loading ? (
        <p>Loading...</p>
      ) : leaderboard.length === 0 ? (
        <p>No data yet. Please upload a JSON file.</p>
      ) : (
        <table className="table table-dark table-striped table-bordered">
          <thead>
            <tr>
              <th>Rank</th>
              <th>User</th>
              <th>Total Score</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.map((entry, index) => (
              <tr key={entry.user}>
                <td>{index + 1}</td>
                <td>{entry.user}</td>
                <td>{entry.total_score}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default Leaderboard;
