import { Link, useLocation } from 'react-router-dom';
import { useState } from 'react';
import { Menu, X, BookOpen } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const navLinks = [
  { to: '/', label: 'Home' },
  { to: '/archive', label: 'Archive' },
  { to: '/search', label: 'Search' },
  { to: '/contribute', label: 'Contribute' },
];

export default function Navbar() {
  const [open, setOpen] = useState(false);
  const { user, logout } = useAuth();
  const location = useLocation();

  const isActive = (path) =>
    path === '/' ? location.pathname === '/' : location.pathname.startsWith(path);

  return (
    <nav className="border-b border-border bg-card sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 group">
            <BookOpen className="text-primary w-5 h-5" />
            <span className="font-serif text-xl text-primary tracking-wide">Kathā-Kosh</span>
          </Link>

          {/* Desktop nav */}
          <div className="hidden md:flex items-center gap-6">
            {navLinks.map(({ to, label }) => (
              <Link
                key={to}
                to={to}
                className={`text-sm tracking-wide transition-colors ${
                  isActive(to)
                    ? 'text-primary font-medium border-b border-primary pb-0.5'
                    : 'text-muted hover:text-ink'
                }`}
              >
                {label}
              </Link>
            ))}
            {user ? (
              <div className="flex items-center gap-4">
                {user.role === 'admin' && (
                  <Link to="/admin" className="text-sm text-sage hover:text-primary transition-colors">
                    Admin
                  </Link>
                )}
                <button
                  onClick={logout}
                  className="text-sm text-muted hover:text-ink transition-colors"
                >
                  Sign out
                </button>
              </div>
            ) : (
              <Link to="/login" className="btn-primary text-xs tracking-widest uppercase">
                Sign In
              </Link>
            )}
          </div>

          {/* Mobile toggle */}
          <button className="md:hidden text-muted" onClick={() => setOpen(!open)}>
            {open ? <X size={22} /> : <Menu size={22} />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {open && (
        <div className="md:hidden border-t border-border bg-card">
          <div className="px-6 py-4 flex flex-col gap-4">
            {navLinks.map(({ to, label }) => (
              <Link
                key={to}
                to={to}
                onClick={() => setOpen(false)}
                className={`text-sm ${isActive(to) ? 'text-primary font-medium' : 'text-muted'}`}
              >
                {label}
              </Link>
            ))}
            {user ? (
              <button onClick={() => { logout(); setOpen(false); }} className="text-sm text-left text-muted">
                Sign out
              </button>
            ) : (
              <Link to="/login" onClick={() => setOpen(false)} className="text-sm text-primary">
                Sign In
              </Link>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}

