import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Filter, X } from 'lucide-react';
import { itemsApi } from '../services/api';
import HeritageCard from '../components/HeritageCard';
import { sampleItems } from '../data/sampleData';

const TYPES = [
  { value: '', label: 'All Categories' },
  { value: 'folk_art', label: 'Folk Art' },
  { value: 'textile', label: 'Textile' },
  { value: 'metalwork', label: 'Metalwork' },
  { value: 'folk_story', label: 'Folk Story' },
  { value: 'dance', label: 'Dance' },
  { value: 'ritual', label: 'Ritual' },
  { value: 'woodwork', label: 'Woodwork' },
  { value: 'music', label: 'Music' },
  { value: 'pottery', label: 'Pottery' },
  { value: 'craft', label: 'Craft' },
];

const REGIONS = [
  { value: '', label: 'All Regions' },
  { value: 'South India', label: 'South India' },
  { value: 'North India', label: 'North India' },
  { value: 'East India', label: 'East India' },
  { value: 'West India', label: 'West India' },
  { value: 'Central India', label: 'Central India' },
  { value: 'Northeast India', label: 'Northeast India' },
];

export default function ArchivePage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [items, setItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [showFilters, setShowFilters] = useState(false);

  const type = searchParams.get('type') || '';
  const region = searchParams.get('region') || '';
  const search = searchParams.get('search') || '';

  const setFilter = (key, value) => {
    const p = new URLSearchParams(searchParams);
    if (value) p.set(key, value);
    else p.delete(key);
    setSearchParams(p);
  };

  const clearFilters = () => setSearchParams({});

  useEffect(() => {
    setLoading(true);
    const params = { limit: 24 };
    if (type) params.type = type;
    if (region) params.region = region;
    if (search) params.search = search;

    itemsApi.getAll(params)
      .then(res => {
        setItems(res.data.items || []);
        setTotal(res.data.total || 0);
      })
      .catch(() => {
        let filtered = sampleItems;
        if (type) filtered = filtered.filter(i => i.type === type);
        if (region) filtered = filtered.filter(i => i.region === region);
        setItems(filtered);
        setTotal(filtered.length);
      })
      .finally(() => setLoading(false));
  }, [type, region, search]);

  const hasFilters = type || region || search;

  return (
    <div className="max-w-7xl mx-auto px-6 py-12">
      {/* Header */}
      <div className="mb-8">
        <p className="section-label mb-1">Kathā-Kosh</p>
        <div className="flex items-end justify-between">
          <h1 className="font-serif text-4xl text-ink">Heritage Archive</h1>
          <span className="text-sm text-muted">{total} items</span>
        </div>
      </div>

      {/* Filters */}
      <div className="mb-8">
        <div className="flex items-center gap-3 flex-wrap">
          <select
            value={type}
            onChange={e => setFilter('type', e.target.value)}
            className="input-field w-auto pr-8 text-xs"
          >
            {TYPES.map(t => <option key={t.value} value={t.value}>{t.label}</option>)}
          </select>
          <select
            value={region}
            onChange={e => setFilter('region', e.target.value)}
            className="input-field w-auto pr-8 text-xs"
          >
            {REGIONS.map(r => <option key={r.value} value={r.value}>{r.label}</option>)}
          </select>
          <input
            type="text"
            placeholder="Search items..."
            value={search}
            onChange={e => setFilter('search', e.target.value)}
            className="input-field w-auto text-xs"
          />
          {hasFilters && (
            <button onClick={clearFilters} className="flex items-center gap-1 text-xs text-muted hover:text-ink transition-colors">
              <X size={12} /> Clear filters
            </button>
          )}
        </div>
      </div>

      {/* Grid */}
      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {[...Array(8)].map((_, i) => (
            <div key={i} className="bg-card border border-border h-72 animate-pulse" />
          ))}
        </div>
      ) : items.length === 0 ? (
        <div className="text-center py-24 text-muted">
          <p className="font-serif text-2xl mb-2">No items found</p>
          <p className="text-sm">Try adjusting your filters</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {items.map(item => <HeritageCard key={item.id} item={item} />)}
        </div>
      )}
    </div>
  );
}

