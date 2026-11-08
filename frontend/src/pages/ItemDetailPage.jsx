import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, MapPin, Users, Clock, Tag, ExternalLink } from 'lucide-react';
import { itemsApi } from '../services/api';
import HeritageCard from '../components/HeritageCard';
import { sampleItems } from '../data/sampleData';
import { resolveHeritageImage, TYPE_IMAGES } from '../data/heritageImages';

const statusColors = {
  Stable: 'bg-sage/10 text-sage border-sage/30',
  Vulnerable: 'bg-accent/10 text-accent border-accent/30',
  Endangered: 'bg-red-100 text-red-700 border-red-200',
  Critical: 'bg-red-200 text-red-800 border-red-300',
};

function Section({ title, children }) {
  return (
    <div className="mb-8">
      <h3 className="font-serif text-xl text-ink mb-3">{title}</h3>
      <p className="text-muted leading-relaxed text-sm">{children}</p>
    </div>
  );
}

export default function ItemDetailPage() {
  const { id } = useParams();
  const [item, setItem] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    itemsApi.getById(id)
      .then(res => {
        setItem(res.data);
        return itemsApi.getRecommendations(id);
      })
      .then(res => setRecommendations(res.data || []))
      .catch(() => {
        const found = sampleItems.find(i => i.id === parseInt(id));
        setItem(found || null);
        setRecommendations(sampleItems.filter(i => i.id !== parseInt(id)).slice(0, 3));
      })
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-6 py-16">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-cream w-48" />
          <div className="h-64 bg-cream w-full" />
          <div className="h-4 bg-cream w-full" />
          <div className="h-4 bg-cream w-3/4" />
        </div>
      </div>
    );
  }

  if (!item) {
    return (
      <div className="max-w-4xl mx-auto px-6 py-24 text-center">
        <p className="font-serif text-2xl text-ink mb-4">Item not found</p>
        <Link to="/archive" className="btn-outline">Back to Archive</Link>
      </div>
    );
  }

  const tags = Array.isArray(item.tags) ? item.tags : (typeof item.tags === 'string' ? item.tags.split(',') : []);

  return (
    <div className="max-w-6xl mx-auto px-6 py-12">
      {/* Back */}
      <Link to="/archive" className="inline-flex items-center gap-2 text-sm text-muted hover:text-ink transition-colors mb-8">
        <ArrowLeft size={14} /> Back to Archive
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-12">
        {/* Main content */}
        <div className="lg:col-span-3">
          <div className="mb-6">
            <div className="flex items-center gap-3 mb-3">
              <span className="section-label">{item.type?.replace('_', ' ')}</span>
              {item.preservation_status && (
                <span className={`text-xs px-2 py-0.5 border rounded-full ${statusColors[item.preservation_status] || 'bg-cream text-muted'}`}>
                  {item.preservation_status}
                </span>
              )}
            </div>
            <h1 className="font-serif text-4xl text-ink mb-2">{item.title}</h1>
            <div className="flex items-center gap-4 text-xs text-muted">
              {item.state && <span className="flex items-center gap-1"><MapPin size={11} />{item.state}{item.district ? `, ${item.district}` : ''}</span>}
              {item.historical_period && <span className="flex items-center gap-1"><Clock size={11} />{item.historical_period}</span>}
              {item.community && <span className="flex items-center gap-1"><Users size={11} />{item.community}</span>}
            </div>
          </div>

          <div className="aspect-video overflow-hidden mb-8 bg-cream">
            <img
              src={resolveHeritageImage(item)}
              alt={item.title}
              className="w-full h-full object-cover"
              onError={e => { e.target.src = TYPE_IMAGES[item.type] || TYPE_IMAGES.default; }}
            />
          </div>

          <Section title="About">{item.description}</Section>
          {item.cultural_significance && <Section title="Cultural Significance">{item.cultural_significance}</Section>}
          {item.traditional_technique && <Section title="Traditional Technique">{item.traditional_technique}</Section>}
          {item.why_it_matters && <Section title="Why It Matters">{item.why_it_matters}</Section>}

          {item.sources && (
            <div className="border-t border-border pt-6">
              <p className="text-xs uppercase tracking-widest text-muted mb-2">Sources</p>
              <p className="text-xs text-muted leading-relaxed">{item.sources}</p>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="lg:col-span-2">
          <div className="bg-card border border-border p-6 sticky top-24 space-y-6">
            <div>
              <p className="label-text">Region</p>
              <p className="text-sm text-ink">{item.region || '—'}</p>
            </div>
            <div>
              <p className="label-text">State</p>
              <p className="text-sm text-ink">{item.state || '—'}</p>
            </div>
            {item.language && (
              <div>
                <p className="label-text">Language</p>
                <p className="text-sm text-ink">{item.language}</p>
              </div>
            )}
            {item.artisan && (
              <div>
                <p className="label-text">Featured Artisan</p>
                <p className="text-sm text-ink">{item.artisan}</p>
              </div>
            )}
            {tags.length > 0 && (
              <div>
                <p className="label-text">Tags</p>
                <div className="flex flex-wrap gap-1.5">
                  {tags.map(t => (
                    <span key={t} className="text-xs bg-cream border border-border px-2 py-0.5 text-muted">
                      {typeof t === 'string' ? t.trim() : t}
                    </span>
                  ))}
                </div>
              </div>
            )}
            <Link to="/contribute" className="btn-primary w-full text-center text-xs tracking-widest uppercase block">
              Contribute Similar
            </Link>
          </div>
        </div>
      </div>

      {/* Recommendations */}
      {recommendations.length > 0 && (
        <div className="mt-16 pt-12 border-t border-border">
          <p className="section-label mb-2">You may also explore</p>
          <h2 className="font-serif text-2xl text-ink mb-6">Related Heritage</h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
            {recommendations.map(rec => <HeritageCard key={rec.id} item={rec} />)}
          </div>
        </div>
      )}
    </div>
  );
}

