import { Link } from 'react-router-dom';

interface LeaderboardEntry {
  user: string;
  total_score: number;
}

const Leaderboard = ({ entries }: { entries: LeaderboardEntry[] }) => {
  if (!entries || entries.length === 0) {
    return <p>No data yet. Please upload a JSON file.</p>;
  }

  return (
    <div className="mt-4">
      <h1 className="mb-4">🏆 Leaderboard</h1>
      <table className="table table-dark table-striped table-bordered">
        <thead>
          <tr>
            <th>Rank</th>
            <th>User</th>
            <th>Total Score</th>
          </tr>
        </thead>
        <tbody>
          {entries.map((entry, index) => (
            <tr key={entry.user}>
              <td>{index + 1}</td>
              <td>
                <Link to={`/user/${entry.user}`}>{entry.user}</Link>
                </td>
              <td>{entry.total_score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Leaderboard;
