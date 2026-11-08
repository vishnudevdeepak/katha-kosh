import { Link } from 'react-router-dom';
import { BookOpen, Github } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="border-t border-border bg-card mt-16">
      <div className="max-w-7xl mx-auto px-6 py-10">
        <div className="flex flex-col md:flex-row justify-between items-start gap-8">
          <div>
            <div className="flex items-center gap-2 mb-3">
              <BookOpen className="text-primary w-4 h-4" />
              <span className="font-serif text-lg text-primary">Kathā-Kosh</span>
            </div>
            <p className="text-sm text-muted max-w-xs leading-relaxed">
              A digital archive for India's living cultural heritage — preserving the stories that should not disappear.
            </p>
          </div>
          <div className="flex gap-12 text-sm text-muted">
            <div className="flex flex-col gap-2">
              <span className="text-xs uppercase tracking-widest text-ink font-medium mb-1">Explore</span>
              <Link to="/archive" className="hover:text-primary transition-colors">Archive</Link>
              <Link to="/search" className="hover:text-primary transition-colors">Search</Link>
              <Link to="/contribute" className="hover:text-primary transition-colors">Contribute</Link>
            </div>
            <div className="flex flex-col gap-2">
              <span className="text-xs uppercase tracking-widest text-ink font-medium mb-1">Heritage</span>
              <span>25+ Documented Items</span>
              <span>15+ Indian States</span>
              <span>Open Archive</span>
            </div>
          </div>
        </div>
        <div className="border-t border-border mt-8 pt-6 flex justify-between items-center">
          <p className="text-xs text-muted">© 2024 Kathā-Kosh. MIT License.</p>
          <p className="text-xs text-muted italic">Preserving the stories that should not disappear.</p>
        </div>
      </div>
    </footer>
  );
}

