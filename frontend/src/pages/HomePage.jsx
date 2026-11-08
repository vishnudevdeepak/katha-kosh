import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Search, BookOpen, Layers } from 'lucide-react';
import { motion } from 'framer-motion';
import { itemsApi } from '../services/api';
import HeritageCard from '../components/HeritageCard';
import { sampleItems } from '../data/sampleData';

const CATEGORIES = [
  { key: 'folk_art', label: 'Folk Art' },
  { key: 'textile', label: 'Textile' },
  { key: 'metalwork', label: 'Metalwork' },
  { key: 'folk_story', label: 'Folk Story' },
  { key: 'dance', label: 'Dance' },
  { key: 'ritual', label: 'Ritual' },
  { key: 'woodwork', label: 'Woodwork' },
  { key: 'music', label: 'Music' },
];

export default function HomePage() {
  const [featured, setFeatured] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    itemsApi.getAll({ limit: 6 })
      .then(res => setFeatured(res.data.items || []))
      .catch(() => setFeatured(sampleItems.slice(0, 6)))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      {/* Hero */}
      <section className="relative bg-gradient-to-br from-primary via-secondary to-accent text-white overflow-hidden">
        <div className="absolute inset-0 opacity-10"
          style={{ backgroundImage: 'url("https://images.unsplash.com/photo-1517457373958-b7bdd4587205?w=1600")', backgroundSize: 'cover', backgroundPosition: 'center' }}
        />
        <div className="relative max-w-5xl mx-auto px-6 py-24 md:py-36 text-center">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7 }}>
            <p className="text-xs uppercase tracking-widest text-white/60 mb-4">भारतीय सांस्कृतिक विरासत</p>
            <h1 className="font-serif text-5xl md:text-7xl font-bold mb-6 leading-tight">
              Kathā-Kosh
            </h1>
            <p className="text-lg md:text-xl text-white/80 mb-10 max-w-2xl mx-auto leading-relaxed">
              A digital archive for India's living cultural heritage — folk stories, traditional crafts, oral histories, and art forms from across the subcontinent.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/archive" className="bg-white text-primary px-8 py-3 font-medium text-sm tracking-wide hover:bg-cream transition-colors inline-flex items-center gap-2">
                Explore Archive <ArrowRight size={16} />
              </Link>
              <Link to="/search" className="border border-white/40 text-white px-8 py-3 font-medium text-sm tracking-wide hover:bg-white/10 transition-colors inline-flex items-center gap-2">
                <Search size={16} /> Search
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Categories */}
      <section className="max-w-7xl mx-auto px-6 py-16">
        <div className="flex items-center justify-between mb-8">
          <div>
            <p className="section-label mb-1">Browse by</p>
            <h2 className="font-serif text-3xl text-ink">Categories</h2>
          </div>
          <Link to="/archive" className="text-sm text-primary hover:underline flex items-center gap-1">
            All items <ArrowRight size={14} />
          </Link>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {CATEGORIES.map(({ key, label }) => (
            <Link
              key={key}
              to={`/archive?type=${key}`}
              className="archive-card p-5 flex flex-col items-center gap-2 text-center group hover:border-primary/40 transition-colors"
            >
              <span className="text-sm font-medium text-ink group-hover:text-primary transition-colors">{label}</span>
            </Link>
          ))}
        </div>
      </section>

      {/* Featured items */}
      <section className="bg-cream py-16">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex items-center justify-between mb-8">
            <div>
              <p className="section-label mb-1">From the archive</p>
              <h2 className="font-serif text-3xl text-ink">Featured Heritage</h2>
            </div>
            <Link to="/archive" className="text-sm text-primary hover:underline flex items-center gap-1">
              View all <ArrowRight size={14} />
            </Link>
          </div>
          {loading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="bg-card border border-border h-80 animate-pulse" />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {featured.map(item => <HeritageCard key={item.id} item={item} />)}
            </div>
          )}
        </div>
      </section>

      {/* CTA */}
      <section className="max-w-3xl mx-auto px-6 py-20 text-center">
        <BookOpen className="text-primary mx-auto mb-4" size={32} />
        <h2 className="font-serif text-3xl text-ink mb-4">Know a story that should be preserved?</h2>
        <p className="text-muted mb-8 leading-relaxed">
          Help us document India's living heritage. Submit folk stories, craft traditions, oral histories, and regional art forms through our contribution portal.
        </p>
        <Link to="/contribute" className="btn-primary">
          Contribute to the Archive
        </Link>
      </section>
    </div>
  );
}
