import { Link } from 'react-router-dom';
import { MapPin } from 'lucide-react';
import { resolveHeritageImage, TYPE_IMAGES } from '../data/heritageImages';

const statusColors = {
  Stable: 'bg-sage/10 text-sage border-sage/30',
  Vulnerable: 'bg-accent/10 text-accent border-accent/30',
  Endangered: 'bg-red-100 text-red-700 border-red-200',
  Critical: 'bg-red-200 text-red-800 border-red-300',
};

const typeLabels = {
  metalwork: 'Metalwork',
  folk_story: 'Folk Story',
  woodwork: 'Woodwork',
  folk_art: 'Folk Art',
  textile: 'Textile',
  pottery: 'Pottery',
  dance: 'Dance',
  music: 'Music',
  ritual: 'Ritual',
  craft: 'Craft',
};

export default function HeritageCard({ item }) {
  return (
    <Link
      to={`/archive/${item.id}`}
      className="archive-card group block overflow-hidden"
    >
      <div className="aspect-[4/3] overflow-hidden bg-cream">
        <img
          src={resolveHeritageImage(item)}
          alt={item.title}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
          onError={(e) => {
            const fallback = TYPE_IMAGES[item.type] || TYPE_IMAGES.default;
            if (e.target.src !== fallback) e.target.src = fallback;
          }}
        />
      </div>
      <div className="p-5">
        <div className="flex items-center justify-between mb-2">
          <span className="section-label">{typeLabels[item.type] || item.type}</span>
          {item.preservation_status && (
            <span className={`text-xs px-2 py-0.5 border rounded-full ${statusColors[item.preservation_status] || 'bg-cream text-muted'}`}>
              {item.preservation_status}
            </span>
          )}
        </div>
        <h3 className="font-serif text-lg text-ink mb-2 group-hover:text-primary transition-colors line-clamp-1">
          {item.title}
        </h3>
        <p className="text-sm text-muted line-clamp-2 leading-relaxed mb-3">
          {item.description}
        </p>
        <div className="flex items-center gap-1 text-xs text-muted">
          <MapPin size={12} />
          <span>{item.state}{item.district ? `, ${item.district}` : ''}</span>
        </div>
        {item.tags && item.tags.length > 0 && (
          <div className="flex flex-wrap gap-1 mt-3">
            {item.tags.slice(0, 3).map(tag => (
              <span key={tag} className="text-xs bg-cream text-muted px-2 py-0.5 border border-border">
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>
    </Link>
  );
}

