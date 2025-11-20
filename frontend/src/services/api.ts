// API Service for KEDB Backend Integration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080/api/v1';

// Backend Entry Interface
export interface BackendEntry {
  id: string;
  title: string;
  description: string;
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info';
  workflow_state: 'draft' | 'in_review' | 'published' | 'retired' | 'merged';
  status: 'active' | 'archived';
  created_by: string;
  updated_by?: string;
  created_at: string;
  updated_at: string;
  published_at?: string;
  root_cause?: string;
  impact_summary?: string;
  detection_method?: string;
  symptoms: any[];
  incidents: any[];
  tags: any[];
  solutions?: any[];
  reviews?: any[];
}

// Frontend Entry Interface  
export interface FrontendEntry {
  id: string;
  errorCode: string;
  name: string;
  symptoms: string;
  rootCause: string;
  workarounds: string;
  resolution: string;
  severity: 'High' | 'Medium' | 'Low';
  status: 'Draft' | 'Pending Review' | 'Published';
  createdBy?: string;
  createdDate?: string;
  lastUpdated?: string;
  updatedBy?: string;
}

// Map backend to frontend
export function mapBackendToFrontend(backendEntry: BackendEntry): FrontendEntry {
  const severityMap: Record<string, 'High' | 'Medium' | 'Low'> = {
    critical: 'High',
    high: 'High',
    medium: 'Medium',
    low: 'Low',
    info: 'Low'
  };

  const statusMap: Record<string, 'Draft' | 'Pending Review' | 'Published'> = {
    draft: 'Draft',
    in_review: 'Pending Review',
    published: 'Published',
    retired: 'Published',
    merged: 'Published'
  };

  return {
    id: backendEntry.id,
    errorCode: backendEntry.id.substring(0, 8).toUpperCase(),
    name: backendEntry.title,
    symptoms: backendEntry.symptoms?.map((s: any) => s.description).join('; ') || backendEntry.description,
    rootCause: backendEntry.root_cause || 'Not specified',
    workarounds: backendEntry.solutions?.filter((s: any) => s.type === 'workaround').map((s: any) => s.description).join('; ') || 'No workaround available',
    resolution: backendEntry.solutions?.filter((s: any) => s.type === 'resolution').map((s: any) => s.description).join('; ') || 'Resolution pending',
    severity: severityMap[backendEntry.severity] || 'Medium',
    status: statusMap[backendEntry.workflow_state] || 'Draft',
    createdBy: backendEntry.created_by,
    createdDate: new Date(backendEntry.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
    lastUpdated: new Date(backendEntry.updated_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
    updatedBy: backendEntry.updated_by || backendEntry.created_by
  };
}

// Map frontend to backend
export function mapFrontendToBackend(frontendEntry: Partial<FrontendEntry>): Partial<BackendEntry> {
  const severityMap: Record<string, 'critical' | 'high' | 'medium' | 'low'> = {
    'High': 'high',
    'Medium': 'medium',
    'Low': 'low'
  };

  const statusMap: Record<string, 'draft' | 'in_review' | 'published'> = {
    'Draft': 'draft',
    'Pending Review': 'in_review',
    'Published': 'published'
  };

  return {
    title: frontendEntry.name,
    description: frontendEntry.symptoms || '',
    severity: frontendEntry.severity ? severityMap[frontendEntry.severity] : 'medium',
    workflow_state: frontendEntry.status ? statusMap[frontendEntry.status] : 'draft',
    status: 'active',
    created_by: 'user@example.com', // TODO: Get from auth context
    root_cause: frontendEntry.rootCause,
  };
}

// API Functions
export async function fetchEntries(): Promise<FrontendEntry[]> {
  const response = await fetch(`${API_BASE_URL}/entries/`);
  if (!response.ok) {
    throw new Error('Failed to fetch entries');
  }
  const backendEntries: BackendEntry[] = await response.json();
  return backendEntries.map(mapBackendToFrontend);
}

export async function fetchEntryById(id: string): Promise<FrontendEntry> {
  const response = await fetch(`${API_BASE_URL}/entries/${id}`);
  if (!response.ok) {
    throw new Error('Failed to fetch entry');
  }
  const backendEntry: BackendEntry = await response.json();
  return mapBackendToFrontend(backendEntry);
}

export async function createEntry(entry: Partial<FrontendEntry>): Promise<FrontendEntry> {
  const backendData = mapFrontendToBackend(entry);
  
  const response = await fetch(`${API_BASE_URL}/entries/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(backendData),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to create entry');
  }
  
  const backendEntry: BackendEntry = await response.json();
  return mapBackendToFrontend(backendEntry);
}

export async function updateEntry(id: string, entry: Partial<FrontendEntry>): Promise<FrontendEntry> {
  const backendData = mapFrontendToBackend(entry);
  
  const response = await fetch(`${API_BASE_URL}/entries/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(backendData),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to update entry');
  }
  
  const backendEntry: BackendEntry = await response.json();
  return mapBackendToFrontend(backendEntry);
}

export async function deleteEntry(id: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/entries/${id}`, {
    method: 'DELETE',
  });
  
  if (!response.ok) {
    throw new Error('Failed to delete entry');
  }
}

