import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import UserPage from './pages/UserPage';

const App = () => (
  <Layout>
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/user/:username" element={<UserPage />} />
    </Routes>
  </Layout>
);

export default App;
