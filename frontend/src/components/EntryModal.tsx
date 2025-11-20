import { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from './ui/dialog';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Label } from './ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import type { Entry, Severity, Status } from '../App';

interface EntryModalProps {
  isOpen: boolean;
  entry: Entry | null;
  onSave: (entry: Entry) => void;
  onClose: () => void;
}

export function EntryModal({ isOpen, entry, onSave, onClose }: EntryModalProps) {
  const [formData, setFormData] = useState<Omit<Entry, 'id'>>({
    errorCode: '',
    name: '',
    symptoms: '',
    rootCause: '',
    workarounds: '',
    resolution: '',
    severity: 'Medium',
    status: 'Draft'
  });

  // Reset form when modal opens with entry data
  useEffect(() => {
    if (isOpen) {
      if (entry) {
        setFormData({
          errorCode: entry.errorCode,
          name: entry.name,
          symptoms: entry.symptoms,
          rootCause: entry.rootCause,
          workarounds: entry.workarounds,
          resolution: entry.resolution,
          severity: entry.severity,
          status: entry.status
        });
      } else {
        setFormData({
          errorCode: '',
          name: '',
          symptoms: '',
          rootCause: '',
          workarounds: '',
          resolution: '',
          severity: 'Medium',
          status: 'Draft'
        });
      }
    }
  }, [isOpen, entry]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const entryData: Entry = {
      id: entry?.id || '',
      ...formData
    };
    
    onSave(entryData);
  };

  const handleChange = (field: keyof typeof formData, value: string) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto bg-white dark:bg-neutral-950 border-neutral-200 dark:border-neutral-800">
        <DialogHeader>
          <DialogTitle className="text-neutral-900 dark:text-neutral-50">
            {entry ? 'Edit Entry' : 'Create New Entry'}
          </DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="errorCode" className="text-neutral-700 dark:text-neutral-300">
                Error Code
              </Label>
              <Input
                id="errorCode"
                value={formData.errorCode}
                onChange={(e) => handleChange('errorCode', e.target.value)}
                placeholder="e.g., APP-502"
                required
                className="bg-white dark:bg-neutral-900 border-neutral-200 dark:border-neutral-800"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="name" className="text-neutral-700 dark:text-neutral-300">
                Name / Title
              </Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => handleChange('name', e.target.value)}
                placeholder="Brief description"
                required
                className="bg-white dark:bg-neutral-900 border-neutral-200 dark:border-neutral-800"
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="symptoms" className="text-neutral-700 dark:text-neutral-300">
              Symptoms
            </Label>
            <Textarea
              id="symptoms"
              value={formData.symptoms}
              onChange={(e) => handleChange('symptoms', e.target.value)}
              placeholder="Describe the observable symptoms of this error..."
              rows={3}
              className="bg-white dark:bg-neutral-900 border-neutral-200 dark:border-neutral-800"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="rootCause" className="text-neutral-700 dark:text-neutral-300">
              Root Cause
            </Label>
            <Textarea
              id="rootCause"
              value={formData.rootCause}
              onChange={(e) => handleChange('rootCause', e.target.value)}
              placeholder="Explain the underlying cause of this error..."
              rows={3}
              className="bg-white dark:bg-neutral-900 border-neutral-200 dark:border-neutral-800"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="workarounds" className="text-neutral-700 dark:text-neutral-300">
              Workarounds
            </Label>
            <Textarea
              id="workarounds"
              value={formData.workarounds}
              onChange={(e) => handleChange('workarounds', e.target.value)}
              placeholder="Temporary solutions to mitigate the issue..."
              rows={3}
              className="bg-white dark:bg-neutral-900 border-neutral-200 dark:border-neutral-800"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="resolution" className="text-neutral-700 dark:text-neutral-300">
              Resolution
            </Label>
            <Textarea
              id="resolution"
              value={formData.resolution}
              onChange={(e) => handleChange('resolution', e.target.value)}
              placeholder="Permanent fix or solution..."
              rows={3}
              className="bg-white dark:bg-neutral-900 border-neutral-200 dark:border-neutral-800"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="severity" className="text-neutral-700 dark:text-neutral-300">
                Severity
              </Label>
              <Select
                value={formData.severity}
                onValueChange={(value) => handleChange('severity', value as Severity)}
              >
                <SelectTrigger className="bg-white dark:bg-neutral-900 border-neutral-200 dark:border-neutral-800">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-white dark:bg-neutral-900 border-neutral-200 dark:border-neutral-800">
                  <SelectItem value="High">High</SelectItem>
                  <SelectItem value="Medium">Medium</SelectItem>
                  <SelectItem value="Low">Low</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="status" className="text-neutral-700 dark:text-neutral-300">
                Status
              </Label>
              <Select
                value={formData.status}
                onValueChange={(value) => handleChange('status', value as Status)}
              >
                <SelectTrigger className="bg-white dark:bg-neutral-900 border-neutral-200 dark:border-neutral-800">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-white dark:bg-neutral-900 border-neutral-200 dark:border-neutral-800">
                  <SelectItem value="Draft">Draft</SelectItem>
                  <SelectItem value="Pending Review">Pending Review</SelectItem>
                  <SelectItem value="Published">Published</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="flex justify-end gap-3 pt-4">
            <Button
              type="button"
              variant="outline"
              onClick={onClose}
              className="border-neutral-200 dark:border-neutral-800 text-neutral-700 dark:text-neutral-300"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              className="bg-blue-600 hover:bg-blue-700 dark:bg-blue-600 dark:hover:bg-blue-700 text-white"
            >
              Save Entry
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
