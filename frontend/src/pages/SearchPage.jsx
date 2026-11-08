import { useState } from 'react';
import { Search, Upload, X } from 'lucide-react';
import { searchApi } from '../services/api';
import HeritageCard from '../components/HeritageCard';
import { sampleItems } from '../data/sampleData';

export default function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [searched, setSearched] = useState(false);
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState('text'); // 'text' | 'image'
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);

  const handleTextSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    setSearched(true);
    try {
      const res = await searchApi.textSearch(query);
      setResults(res.data.results || res.data || []);
    } catch {
      // fallback: simple keyword match on sample data
      const q = query.toLowerCase();
      setResults(sampleItems.filter(i =>
        i.title.toLowerCase().includes(q) ||
        i.description.toLowerCase().includes(q) ||
        i.state?.toLowerCase().includes(q) ||
        i.type?.toLowerCase().includes(q) ||
        (i.tags || []).some(t => t.toLowerCase().includes(q))
      ));
    } finally {
      setLoading(false);
    }
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setImageFile(file);
    setImagePreview(URL.createObjectURL(file));
  };

  const handleImageSearch = async () => {
    if (!imageFile) return;
    setLoading(true);
    setSearched(true);
    try {
      const form = new FormData();
      form.append('file', imageFile);
      const res = await searchApi.imageSearch(form);
      setResults(res.data.results || res.data || []);
    } catch {
      setResults(sampleItems.slice(0, 4));
    } finally {
      setLoading(false);
    }
  };

  const clearImage = () => {
    setImageFile(null);
    setImagePreview(null);
    setResults([]);
    setSearched(false);
  };

  return (
    <div className="max-w-5xl mx-auto px-6 py-12">
      <p className="section-label mb-1">Semantic & Visual</p>
      <h1 className="font-serif text-4xl text-ink mb-2">Search the Archive</h1>
      <p className="text-muted text-sm mb-10">
        Search with natural language or upload an image to find similar heritage artifacts.
      </p>

      {/* Mode tabs */}
      <div className="flex gap-0 mb-8 border border-border w-fit">
        <button
          onClick={() => setMode('text')}
          className={`px-6 py-2.5 text-sm flex items-center gap-2 transition-colors ${mode === 'text' ? 'bg-primary text-white' : 'text-muted hover:text-ink'}`}
        >
          <Search size={14} /> Text Search
        </button>
        <button
          onClick={() => setMode('image')}
          className={`px-6 py-2.5 text-sm flex items-center gap-2 transition-colors ${mode === 'image' ? 'bg-primary text-white' : 'text-muted hover:text-ink'}`}
        >
          <Upload size={14} /> Image Search
        </button>
      </div>

      {/* Text search */}
      {mode === 'text' && (
        <form onSubmit={handleTextSearch} className="flex gap-3 mb-10">
          <input
            type="text"
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="e.g. lost-wax metal casting Kerala, or silk weaving tradition..."
            className="input-field flex-1"
          />
          <button type="submit" className="btn-primary flex items-center gap-2 whitespace-nowrap">
            <Search size={15} /> Search
          </button>
        </form>
      )}

      {/* Image search */}
      {mode === 'image' && (
        <div className="mb-10">
          {!imagePreview ? (
            <label className="border-2 border-dashed border-border hover:border-primary/40 cursor-pointer p-12 flex flex-col items-center gap-3 text-muted transition-colors block">
              <Upload size={28} className="text-muted/50" />
              <span className="text-sm">Click to upload an image</span>
              <span className="text-xs">JPG, PNG up to 10MB</span>
              <input type="file" accept="image/*" className="hidden" onChange={handleImageUpload} />
            </label>
          ) : (
            <div className="relative w-64">
              <img src={imagePreview} alt="Upload preview" className="w-64 h-48 object-cover border border-border" />
              <button onClick={clearImage} className="absolute top-2 right-2 bg-white border border-border p-1 rounded-full text-muted hover:text-ink">
                <X size={14} />
              </button>
              <button onClick={handleImageSearch} className="btn-primary w-full mt-3 text-center block text-xs tracking-widest uppercase">
                Find Similar Artifacts
              </button>
            </div>
          )}
        </div>
      )}

      {/* Results */}
      {loading && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(6)].map((_, i) => <div key={i} className="bg-card border border-border h-72 animate-pulse" />)}
        </div>
      )}

      {!loading && searched && (
        <>
          <p className="text-sm text-muted mb-6">
            {results.length} result{results.length !== 1 ? 's' : ''} found
            {query ? ` for "${query}"` : ''}
          </p>
          {results.length === 0 ? (
            <div className="text-center py-16 text-muted">
              <p className="font-serif text-2xl mb-2">No results found</p>
              <p className="text-sm">Try different keywords or browse the archive</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {results.map(item => <HeritageCard key={item.id} item={item} />)}
            </div>
          )}
        </>
      )}
    </div>
  );
}

