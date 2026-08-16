export interface Student {
  id: string;
  display_name: string;
  current_engagement: number;
  status: 'HIGH' | 'MODERATE' | 'LOW';
  trend: 'UP' | 'DOWN' | 'STABLE';
  confidence: number;
  state_version: number;
  total_states: number;
  conflicts_count: number;
  last_updated: string;
}

export interface StudentProfile {
  id: string;
  display_name: string;
  current_engagement: number;
  average_engagement: number;
  highest_engagement: number;
  lowest_engagement: number;
  status: 'HIGH' | 'MODERATE' | 'LOW';
  observations_count: number;
  state_versions_count: number;
  conflicts_count: number;
  out_of_order_count: number;
  latest_state: StudentState | null;
  created_at: string;
  updated_at: string;
}

export interface EngagementEvent {
  id: string;
  event_fingerprint: string;
  camera_id: string;
  timestamp: string;
  received_at: string;
  student_id_raw: string;
  resolved_student_id: string;
  engagement_score: number;
  confidence: number;
  source: string;
  spatial_x?: number;
  spatial_y?: number;
  is_replay: number;
  created_at: string;
}

export interface StudentState {
  id: string;
  student_id: string;
  version: number;
  event_id: string;
  effective_timestamp: string;
  engagement_score: number;
  confidence: number;
  state_status: string;
  created_at: string;
}

export interface TimelineItem {
  version: number;
  effective_timestamp: string;
  engagement_score: number;
  confidence: number;
  state_status: string;
  event_id: string;
  camera_id: string;
  source: string;
  spatial_x?: number;
  spatial_y?: number;
}

export interface CandidateEvent {
  event_id: string;
  camera_id?: string;
  score: number;
  confidence: number;
  timestamp: string;
  reliability?: number;
  fingerprint?: string;
}

export interface DecisionLogic {
  decision_type: string;
  student_id?: string;
  candidate_events?: CandidateEvent[];
  rules_evaluated?: string[];
  winning_event_id?: string;
  final_score?: number;
  reason?: string;
  tiebreaker_used?: string;
  raw_student_id?: string;
  resolved_student_id?: string;
  combined_score?: number;
}

export interface AuditLog {
  id: string;
  student_id: string;
  event_id?: string;
  decision_type: 'CONFLICT_RESOLUTION' | 'OUT_OF_ORDER_EVENT' | 'IDENTITY_RESOLUTION' | 'DUPLICATE_EVENT' | string;
  input_events?: any[];
  resolution_logic?: DecisionLogic;
  selected_event_id?: string;
  final_score: number;
  previous_score?: number;
  timestamp: string;
  created_at: string;
  human_readable_explanation?: string;
}

export interface CameraStatus {
  camera_id: string;
  total_events: number;
  last_event_at: string;
  avg_engagement: number;
  avg_confidence: number;
  reliability: number;
  status: 'ONLINE' | 'DEGRADED' | 'OFFLINE';
}

export interface DashboardSummary {
  total_students: number;
  active_cameras: number;
  total_events: number;
  conflicts_detected: number;
  duplicates_detected: number;
  out_of_order_events: number;
  average_engagement: number;
  high_engagement_students: number;
  moderate_engagement_students: number;
  low_engagement_students: number;
}

export interface ReplayResult {
  replay_id: string;
  event_count: number;
  result_hash: string;
  deterministic: boolean;
  status: string;
  started_at: string;
  completed_at: string;
  student_id?: string;
  reconstructed_state_count?: number;
  reconstructed_audit_count?: number;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
  };
  status?: string;
  message?: string;
  event_id?: string;
}
