import { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { EntryList } from './components/EntryList';
import { EntryModal } from './components/EntryModal';
import { EntryDetailModal } from './components/EntryDetailModal';
import { Button } from './components/ui/button';
import { Input } from './components/ui/input';
import { Plus, Search } from 'lucide-react';
import { 
  fetchEntries, 
  createEntry as apiCreateEntry, 
  updateEntry as apiUpdateEntry, 
  deleteEntry as apiDeleteEntry,
  type FrontendEntry
} from './services/api';

export type Severity = 'High' | 'Medium' | 'Low';
export type Status = 'Draft' | 'Pending Review' | 'Published';

export type Entry = FrontendEntry;

export default function App() {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [entries, setEntries] = useState<Entry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingEntry, setEditingEntry] = useState<Entry | null>(null);
  const [isDetailModalOpen, setIsDetailModalOpen] = useState(false);
  const [selectedEntry, setSelectedEntry] = useState<Entry | null>(null);

  // Fetch entries on mount
  useEffect(() => {
    loadEntries();
  }, []);

  // Apply dark mode class to document
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDarkMode]);

  const loadEntries = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchEntries();
      setEntries(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load entries');
      console.error('Error loading entries:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
  };

  const handleCreateEntry = () => {
    setEditingEntry(null);
    setIsModalOpen(true);
  };

  const handleEditEntry = (entry: Entry) => {
    setEditingEntry(entry);
    setIsModalOpen(true);
  };

  const handleDeleteEntry = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this entry?')) {
      try {
        await apiDeleteEntry(id);
        setEntries(entries.filter(entry => entry.id !== id));
      } catch (err) {
        alert('Failed to delete entry: ' + (err instanceof Error ? err.message : 'Unknown error'));
      }
    }
  };

  const handleSaveEntry = async (entry: Entry) => {
    try {
      if (editingEntry) {
        // Update existing entry
        const updated = await apiUpdateEntry(entry.id, entry);
        setEntries(entries.map(e => e.id === updated.id ? updated : e));
      } else {
        // Create new entry
        const created = await apiCreateEntry(entry);
        setEntries([...entries, created]);
      }
      setIsModalOpen(false);
      setEditingEntry(null);
    } catch (err) {
      alert('Failed to save entry: ' + (err instanceof Error ? err.message : 'Unknown error'));
    }
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setEditingEntry(null);
  };

  const handleViewEntry = (entry: Entry) => {
    setSelectedEntry(entry);
    setIsDetailModalOpen(true);
  };

  const handleCloseDetailModal = () => {
    setIsDetailModalOpen(false);
    setSelectedEntry(null);
  };

  // Filter entries based on search query
  const filteredEntries = entries.filter(entry => {
    const query = searchQuery.toLowerCase();
    return (
      entry.errorCode?.toLowerCase().includes(query) ||
      entry.name?.toLowerCase().includes(query) ||
      entry.symptoms?.toLowerCase().includes(query) ||
      entry.rootCause?.toLowerCase().includes(query)
    );
  });

  if (loading) {
    return (
      <div className="min-h-screen bg-white dark:bg-neutral-950 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-neutral-600 dark:text-neutral-400">Loading entries...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-white dark:bg-neutral-950 flex items-center justify-center">
        <div className="text-center max-w-md">
          <div className="text-red-600 dark:text-red-400 text-xl mb-4">⚠️ Error</div>
          <p className="text-neutral-600 dark:text-neutral-400 mb-4">{error}</p>
          <Button onClick={loadEntries} className="bg-blue-600 hover:bg-blue-700">
            Retry
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white dark:bg-neutral-950 transition-colors">
      <Header 
        isDarkMode={isDarkMode} 
        onToggleDarkMode={handleToggleDarkMode} 
      />
      
      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Action Bar */}
        <div className="flex items-center gap-4 mb-8">
          <Button 
            onClick={handleCreateEntry}
            className="bg-blue-600 hover:bg-blue-700 dark:bg-blue-600 dark:hover:bg-blue-700 text-white"
          >
            <Plus className="w-4 h-4 mr-2" />
            New Entry
          </Button>
          
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-neutral-400" />
            <Input
              type="text"
              placeholder="Search by error code, name, or symptom..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 bg-neutral-50 dark:bg-neutral-900 border-neutral-200 dark:border-neutral-800"
            />
          </div>
        </div>

        {/* Entry List */}
        <EntryList 
          entries={filteredEntries}
          onEdit={handleEditEntry}
          onDelete={handleDeleteEntry}
          onView={handleViewEntry}
        />
      </main>

      {/* Create/Edit Modal */}
      <EntryModal
        isOpen={isModalOpen}
        entry={editingEntry}
        onSave={handleSaveEntry}
        onClose={handleCloseModal}
      />

      {/* Detail Modal */}
      <EntryDetailModal
        isOpen={isDetailModalOpen}
        entry={selectedEntry}
        onClose={handleCloseDetailModal}
      />
    </div>
  );
}