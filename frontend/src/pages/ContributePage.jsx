import { useState } from 'react';
import { contributionsApi } from '../services/api';
import { CheckCircle } from 'lucide-react';

const TYPES = ['folk_art', 'textile', 'metalwork', 'folk_story', 'dance', 'ritual', 'woodwork', 'music', 'pottery', 'craft'];
const REGIONS = ['South India', 'North India', 'East India', 'West India', 'Central India', 'Northeast India'];
const STATUSES = ['Stable', 'Vulnerable', 'Endangered', 'Critical'];

export default function ContributePage() {
  const [form, setForm] = useState({
    title: '', type: '', region: '', state: '', language: '', community: '',
    description: '', cultural_significance: '', traditional_technique: '',
    why_it_matters: '', preservation_status: '', artisan: '', sources: '', tags: '',
  });
  const [image, setImage] = useState(null);
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = e => setForm(f => ({ ...f, [e.target.name]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const fd = new FormData();
      Object.entries(form).forEach(([k, v]) => fd.append(k, v));
      if (image) fd.append('image', image);
      await contributionsApi.submit(fd);
      setSubmitted(true);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Submission failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <div className="max-w-xl mx-auto px-6 py-24 text-center">
        <CheckCircle className="text-sage mx-auto mb-4" size={48} />
        <h2 className="font-serif text-3xl text-ink mb-3">Thank you!</h2>
        <p className="text-muted text-sm leading-relaxed">
          Your contribution has been submitted and will be reviewed by our team. Once approved, it will be published in the archive.
        </p>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto px-6 py-12">
      <p className="section-label mb-1">Help preserve heritage</p>
      <h1 className="font-serif text-4xl text-ink mb-2">Contribute</h1>
      <p className="text-muted text-sm mb-10 leading-relaxed">
        Submit a folk story, craft tradition, art form, dance, or any cultural heritage item for inclusion in the archive.
        All submissions are reviewed before publication.
      </p>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
          <div>
            <label className="label-text">Title *</label>
            <input name="title" required value={form.title} onChange={handleChange} className="input-field" placeholder="e.g. Aranmula Kannadi" />
          </div>
          <div>
            <label className="label-text">Category *</label>
            <select name="type" required value={form.type} onChange={handleChange} className="input-field">
              <option value="">Select category</option>
              {TYPES.map(t => <option key={t} value={t}>{t.replace('_', ' ')}</option>)}
            </select>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
          <div>
            <label className="label-text">Region *</label>
            <select name="region" required value={form.region} onChange={handleChange} className="input-field">
              <option value="">Select region</option>
              {REGIONS.map(r => <option key={r} value={r}>{r}</option>)}
            </select>
          </div>
          <div>
            <label className="label-text">State</label>
            <input name="state" value={form.state} onChange={handleChange} className="input-field" placeholder="e.g. Kerala" />
          </div>
          <div>
            <label className="label-text">Language</label>
            <input name="language" value={form.language} onChange={handleChange} className="input-field" placeholder="e.g. Malayalam" />
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
          <div>
            <label className="label-text">Community / Practitioners</label>
            <input name="community" value={form.community} onChange={handleChange} className="input-field" placeholder="e.g. Vishwakarma artisans" />
          </div>
          <div>
            <label className="label-text">Featured Artisan</label>
            <input name="artisan" value={form.artisan} onChange={handleChange} className="input-field" placeholder="e.g. Rajan Vishwakarma" />
          </div>
        </div>

        {/* Description fields */}
        {[
          { name: 'description', label: 'Description *', required: true, placeholder: 'What is this heritage item? Give an overview.' },
          { name: 'cultural_significance', label: 'Cultural Significance', required: false, placeholder: 'Why is it significant in its community?' },
          { name: 'traditional_technique', label: 'Traditional Technique', required: false, placeholder: 'How is it made or performed?' },
          { name: 'why_it_matters', label: 'Why It Matters', required: false, placeholder: 'Why should it be preserved?' },
        ].map(({ name, label, required, placeholder }) => (
          <div key={name}>
            <label className="label-text">{label}</label>
            <textarea
              name={name}
              required={required}
              value={form[name]}
              onChange={handleChange}
              rows={4}
              className="input-field resize-none"
              placeholder={placeholder}
            />
          </div>
        ))}

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
          <div>
            <label className="label-text">Preservation Status</label>
            <select name="preservation_status" value={form.preservation_status} onChange={handleChange} className="input-field">
              <option value="">Select status</option>
              {STATUSES.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
          <div>
            <label className="label-text">Tags (comma-separated)</label>
            <input name="tags" value={form.tags} onChange={handleChange} className="input-field" placeholder="e.g. mirror, metal, GI-tag" />
          </div>
        </div>

        <div>
          <label className="label-text">Sources / References</label>
          <input name="sources" value={form.sources} onChange={handleChange} className="input-field" placeholder="Books, institutions, websites..." />
        </div>

        <div>
          <label className="label-text">Image (optional)</label>
          <input
            type="file"
            accept="image/*"
            onChange={e => setImage(e.target.files[0])}
            className="block w-full text-sm text-muted file:mr-4 file:py-2 file:px-4 file:border file:border-border file:text-xs file:bg-cream file:text-ink hover:file:bg-primary hover:file:text-white file:transition-colors cursor-pointer"
          />
        </div>

        {error && <p className="text-sm text-red-600">{error}</p>}

        <button type="submit" disabled={loading} className="btn-primary w-full text-center">
          {loading ? 'Submitting...' : 'Submit Contribution'}
        </button>
      </form>
    </div>
  );
}

