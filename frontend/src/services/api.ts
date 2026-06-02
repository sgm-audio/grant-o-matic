import axios from 'axios';

// Create an axios instance with base URL
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Grant matching interface
export interface GrantMatchRequest {
  project_description: string;
  artist_type?: string;
  residency?: string;
  genre?: string;
  project_type?: string;
  budget_amount?: number;
  limit?: number;
}

export interface GrantMatchResponse {
  id: string;
  program_name: string;
  administering_agency: string;
  match_score: number;
  match_grade: string;
  eligibility_score: number;
  project_type_score: number;
  keyword_score: number;
  complexity_score: number;
  matched_criteria: string[];
  missing_criteria: string[];
  description: string;
  deadline_info: {
    frequency: string;
    next_deadline: string | null;
    application_window: string | null;
  };
  funding_details: {
    min_amount: number;
    max_amount: number;
    average_award: number;
    funding_type: string;
    requires_matching_funds: boolean;
    matching_requirements: string | null;
  };
  application_requirements: string[];
  assessment_criteria: string[];
  url: string;
  budget_suggestion?: {
    project_type: string;
    total_budget: number;
    budget_breakdown: Record<string, number>;
    justification_text: string;
    notes: string[];
  };
}

export interface GrantListResponse {
  grants: GrantMatchResponse[];
  total_count: number;
  timestamp: string;
}

// API service functions
export const grantApi = {
  // Match a project to grants
  matchGrants: async (request: GrantMatchRequest): Promise<GrantListResponse> => {
    const response = await api.post('/match', request);
    return response.data;
  },

  // Get health status
  healthCheck: async (): Promise<{ status: string; timestamp: string }> => {
    const response = await api.get('/health');
    return response.data;
  },

  // Get all grants (for admin/testing)
  getAllGrants: async (skip: number = 0, limit: number = 100): Promise<{ grants: any[]; total_count: number }> => {
    const response = await api.get(`/grants?skip=${skip}&limit=${limit}`);
    return response.data;
  }
};

export default api;