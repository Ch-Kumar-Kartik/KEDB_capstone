import { Dialog, DialogContent, DialogHeader, DialogTitle } from './ui/dialog';
import { Badge } from './ui/badge';
import { Separator } from './ui/separator';
import type { Entry } from '../App';

interface EntryDetailModalProps {
  isOpen: boolean;
  entry: Entry | null;
  onClose: () => void;
}

export function EntryDetailModal({ isOpen, entry, onClose }: EntryDetailModalProps) {
  if (!entry) return null;

  const getStatusColor = (status: Entry['status']) => {
    switch (status) {
      case 'Published':
        return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400';
      case 'Pending Review':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400';
      case 'Draft':
        return 'bg-neutral-100 text-neutral-800 dark:bg-neutral-800 dark:text-neutral-400';
      default:
        return 'bg-neutral-100 text-neutral-800 dark:bg-neutral-800 dark:text-neutral-400';
    }
  };

  const getSeverityColor = (severity: Entry['severity']) => {
    switch (severity) {
      case 'High':
        return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400';
      case 'Medium':
        return 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400';
      case 'Low':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400';
      default:
        return 'bg-neutral-100 text-neutral-800 dark:bg-neutral-800 dark:text-neutral-400';
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto bg-white dark:bg-neutral-950 border-neutral-200 dark:border-neutral-800">
        <DialogHeader>
          <div className="flex items-center gap-3">
            <code className="px-3 py-1.5 rounded bg-neutral-100 dark:bg-neutral-900 text-neutral-900 dark:text-neutral-100">
              {entry.errorCode}
            </code>
            <DialogTitle className="text-neutral-900 dark:text-neutral-50">
              {entry.name}
            </DialogTitle>
          </div>
          <div className="flex items-center gap-2 pt-2">
            <Badge className={getSeverityColor(entry.severity)}>
              {entry.severity} Severity
            </Badge>
            <Badge className={getStatusColor(entry.status)}>
              {entry.status}
            </Badge>
          </div>
        </DialogHeader>

        <div className="space-y-6 pt-4">
          {/* Issue Details */}
          <div>
            <h3 className="text-neutral-900 dark:text-neutral-100 mb-2">
              Symptoms
            </h3>
            <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed">
              {entry.symptoms || 'No symptoms documented.'}
            </p>
          </div>

          <Separator className="bg-neutral-200 dark:bg-neutral-800" />

          {/* Root Cause */}
          <div>
            <h3 className="text-neutral-900 dark:text-neutral-100 mb-2">
              Root Cause
            </h3>
            <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed">
              {entry.rootCause || 'Root cause not yet identified.'}
            </p>
          </div>

          <Separator className="bg-neutral-200 dark:bg-neutral-800" />

          {/* Workarounds */}
          <div>
            <h3 className="text-neutral-900 dark:text-neutral-100 mb-2">
              Workarounds
            </h3>
            <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed">
              {entry.workarounds || 'No workarounds available.'}
            </p>
          </div>

          <Separator className="bg-neutral-200 dark:bg-neutral-800" />

          {/* Resolution */}
          <div>
            <h3 className="text-neutral-900 dark:text-neutral-100 mb-2">
              Resolution
            </h3>
            <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed">
              {entry.resolution || 'No permanent resolution documented.'}
            </p>
          </div>

          <Separator className="bg-neutral-200 dark:bg-neutral-800" />

          {/* Metadata */}
          <div className="bg-neutral-50 dark:bg-neutral-900/50 rounded-lg p-4 space-y-2">
            <h3 className="text-neutral-900 dark:text-neutral-100 mb-3">
              Metadata
            </h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-neutral-500 dark:text-neutral-400">Created By:</span>
                <p className="text-neutral-900 dark:text-neutral-100 mt-1">
                  {entry.createdBy || 'Unknown'}
                </p>
              </div>
              <div>
                <span className="text-neutral-500 dark:text-neutral-400">Created Date:</span>
                <p className="text-neutral-900 dark:text-neutral-100 mt-1">
                  {entry.createdDate || 'Unknown'}
                </p>
              </div>
              <div>
                <span className="text-neutral-500 dark:text-neutral-400">Last Updated:</span>
                <p className="text-neutral-900 dark:text-neutral-100 mt-1">
                  {entry.lastUpdated || 'Unknown'}
                </p>
              </div>
              <div>
                <span className="text-neutral-500 dark:text-neutral-400">Updated By:</span>
                <p className="text-neutral-900 dark:text-neutral-100 mt-1">
                  {entry.updatedBy || 'Unknown'}
                </p>
              </div>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
