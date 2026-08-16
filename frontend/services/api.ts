import { 
  DashboardSummary, CameraStatus, Student, StudentProfile, 
  TimelineItem, AuditLog, ReplayResult, ApiResponse, EngagementEvent 
} from './types';

const API_BASE_URL = process.env.EXPO_PUBLIC_API_BASE_URL || 'http://localhost:5000';

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const defaultHeaders = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };

  const response = await fetch(url, {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  });

  const json = await response.json();

  if (!response.ok || json.success === false) {
    const errorMsg = json.error?.message || `API Error: ${response.status}`;
    throw new Error(errorMsg);
  }

  return json.data !== undefined ? json.data : json;
}

export const ApiService = {
  // Dashboard APIs
  getDashboardSummary: (): Promise<DashboardSummary> => {
    return request<DashboardSummary>('/dashboard/summary');
  },

  getCameraSummaries: (): Promise<CameraStatus[]> => {
    return request<CameraStatus[]>('/dashboard/cameras');
  },

  // Student APIs
  getStudents: (): Promise<Student[]> => {
    return request<Student[]>('/students');
  },

  getStudentProfile: (studentId: string): Promise<StudentProfile> => {
    return request<StudentProfile>(`/student/${studentId}`);
  },

  getStudentTimeline: (studentId: string): Promise<{ student_id: string; total_versions: number; timeline: TimelineItem[] }> => {
    return request<{ student_id: string; total_versions: number; timeline: TimelineItem[] }>(`/student/${studentId}/timeline`);
  },

  getStudentAudit: (studentId: string): Promise<{ student_id: string; total_records: number; audit_logs: AuditLog[] }> => {
    return request<{ student_id: string; total_records: number; audit_logs: AuditLog[] }>(`/student/${studentId}/audit`);
  },

  // Conflict & Audit APIs
  getConflicts: (limit: number = 100): Promise<{ total_conflicts: number; conflicts: AuditLog[] }> => {
    return request<{ total_conflicts: number; conflicts: AuditLog[] }>(`/audit/conflicts?limit=${limit}`);
  },

  getAllAudits: (limit: number = 200): Promise<{ total: number; audit_logs: AuditLog[] }> => {
    return request<{ total: number; audit_logs: AuditLog[] }>(`/audit/all?limit=${limit}`);
  },

  // Event Ingestion API
  ingestEvent: (eventPayload: Partial<EngagementEvent>): Promise<any> => {
    return request<any>('/events', {
      method: 'POST',
      body: JSON.stringify(eventPayload),
    });
  },

  // Replay API
  startReplay: (params: { student_id?: string; from?: string; to?: string }): Promise<ReplayResult> => {
    return request<ReplayResult>('/replay', {
      method: 'POST',
      body: JSON.stringify(params),
    });
  },

  getReplayDetails: (replayId: string): Promise<ReplayResult> => {
    return request<ReplayResult>(`/replay/${replayId}`);
  },

  // CSV Export URLs
  getEngagementCsvUrl: () => `${API_BASE_URL}/export/engagement.csv`,
  getAuditCsvUrl: () => `${API_BASE_URL}/export/audit.csv`,
};
