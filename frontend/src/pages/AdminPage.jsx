import { useState, useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { adminApi, contributionsApi } from '../services/api';
import { CheckCircle, XCircle, BarChart2, FileText, Package } from 'lucide-react';

function StatCard({ icon: Icon, label, value, color }) {
  return (
    <div className="bg-card border border-border p-6 flex items-center gap-4">
      <div className={`p-3 rounded-full ${color}`}>
        <Icon size={20} className="text-white" />
      </div>
      <div>
        <div className="font-serif text-2xl text-ink">{value ?? '—'}</div>
        <div className="text-xs uppercase tracking-widest text-muted">{label}</div>
      </div>
    </div>
  );
}

export default function AdminPage() {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [contributions, setContributions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState('overview');

  if (!user) return <Navigate to="/login" replace />;
  if (user.role !== 'admin') {
    return (
      <div className="max-w-xl mx-auto px-6 py-24 text-center">
        <p className="font-serif text-2xl text-ink mb-2">Access Denied</p>
        <p className="text-sm text-muted">You need admin privileges to view this page.</p>
      </div>
    );
  }

  useEffect(() => {
    Promise.all([adminApi.getStats(), contributionsApi.getAll()])
      .then(([statsRes, contribRes]) => {
        setStats(statsRes.data);
        setContributions(contribRes.data || []);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const handleApprove = async (id) => {
    await contributionsApi.approve(id);
    setContributions(c => c.filter(x => x.id !== id));
  };

  const handleReject = async (id) => {
    await contributionsApi.reject(id, 'Rejected by admin');
    setContributions(c => c.filter(x => x.id !== id));
  };

  const pending = contributions.filter(c => c.status === 'pending');

  return (
    <div className="max-w-6xl mx-auto px-6 py-12">
      <div className="mb-8">
        <p className="section-label mb-1">Admin Panel</p>
        <h1 className="font-serif text-4xl text-ink">Dashboard</h1>
      </div>

      {/* Tabs */}
      <div className="flex gap-0 border border-border w-fit mb-8">
        {['overview', 'contributions'].map(t => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-6 py-2.5 text-sm capitalize transition-colors ${tab === t ? 'bg-primary text-white' : 'text-muted hover:text-ink'}`}
          >
            {t}
            {t === 'contributions' && pending.length > 0 && (
              <span className="ml-2 bg-accent text-white text-xs px-1.5 py-0.5 rounded-full">{pending.length}</span>
            )}
          </button>
        ))}
      </div>

      {/* Overview */}
      {tab === 'overview' && (
        <div>
          {loading ? (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {[...Array(4)].map((_, i) => <div key={i} className="h-24 bg-cream border border-border animate-pulse" />)}
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <StatCard icon={Package} label="Total Items" value={stats?.total_items} color="bg-primary" />
              <StatCard icon={FileText} label="Pending Review" value={stats?.pending_contributions} color="bg-accent" />
              <StatCard icon={CheckCircle} label="Published" value={stats?.published_items} color="bg-sage" />
              <StatCard icon={BarChart2} label="Total Views" value={stats?.total_views} color="bg-secondary" />
            </div>
          )}

          {stats?.items_by_type && (
            <div className="mt-10">
              <h2 className="font-serif text-xl text-ink mb-4">Items by Category</h2>
              <div className="bg-card border border-border">
                {Object.entries(stats.items_by_type).map(([type, count]) => (
                  <div key={type} className="flex items-center justify-between px-6 py-3 border-b border-border last:border-0">
                    <span className="text-sm text-ink capitalize">{type.replace('_', ' ')}</span>
                    <div className="flex items-center gap-4">
                      <div className="w-32 bg-cream h-2 rounded-full overflow-hidden">
                        <div
                          className="bg-primary h-2 rounded-full"
                          style={{ width: `${Math.min(100, (count / (stats.total_items || 1)) * 100)}%` }}
                        />
                      </div>
                      <span className="text-sm text-muted w-6 text-right">{count}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Contributions */}
      {tab === 'contributions' && (
        <div>
          <h2 className="font-serif text-xl text-ink mb-4">
            Pending Contributions
            {pending.length > 0 && <span className="ml-2 text-sm text-muted font-sans">({pending.length})</span>}
          </h2>
          {pending.length === 0 ? (
            <div className="text-center py-16 text-muted border border-border">
              <CheckCircle size={28} className="mx-auto mb-2 text-sage" />
              <p className="text-sm">No pending contributions</p>
            </div>
          ) : (
            <div className="space-y-4">
              {pending.map(c => (
                <div key={c.id} className="bg-card border border-border p-6">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-1">
                        <h3 className="font-serif text-lg text-ink">{c.title}</h3>
                        <span className="section-label">{c.type?.replace('_', ' ')}</span>
                      </div>
                      <p className="text-xs text-muted mb-2">{c.state} · {c.region}</p>
                      <p className="text-sm text-muted line-clamp-2">{c.description}</p>
                    </div>
                    <div className="flex gap-2 shrink-0">
                      <button
                        onClick={() => handleApprove(c.id)}
                        className="flex items-center gap-1 text-xs px-4 py-2 bg-sage/10 text-sage border border-sage/30 hover:bg-sage hover:text-white transition-colors"
                      >
                        <CheckCircle size={12} /> Approve
                      </button>
                      <button
                        onClick={() => handleReject(c.id)}
                        className="flex items-center gap-1 text-xs px-4 py-2 bg-red-50 text-red-600 border border-red-200 hover:bg-red-600 hover:text-white transition-colors"
                      >
                        <XCircle size={12} /> Reject
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

