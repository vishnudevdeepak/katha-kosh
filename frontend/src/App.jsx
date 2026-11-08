import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import ArchivePage from './pages/ArchivePage';
import ItemDetailPage from './pages/ItemDetailPage';
import SearchPage from './pages/SearchPage';
import ContributePage from './pages/ContributePage';
import AdminPage from './pages/AdminPage';
import LoginPage from './pages/LoginPage';

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen flex flex-col bg-paper">
          <Navbar />
          <main className="flex-1">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/archive" element={<ArchivePage />} />
              <Route path="/archive/:id" element={<ItemDetailPage />} />
              <Route path="/search" element={<SearchPage />} />
              <Route path="/contribute" element={<ContributePage />} />
              <Route path="/admin" element={<AdminPage />} />
              <Route path="/login" element={<LoginPage />} />
            </Routes>
          </main>
        </div>
      </Router>
    </AuthProvider>
  );
}
