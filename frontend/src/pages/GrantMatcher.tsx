import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { grantApi, type GrantMatchResponse } from '../services/api';

type GrantMatch = GrantMatchResponse

interface GrantMatcherFormValues {
  project_description: string;
  artist_type: string;
  residency: string;
  genre: string;
  project_type: string;
}

const fetchGrantMatches = async (formData: GrantMatcherFormValues): Promise<GrantMatch[]> => {
  try {
    const result = await grantApi.matchGrants({
      project_description: formData.project_description,
      artist_type: formData.artist_type,
      residency: formData.residency,
      genre: formData.genre,
      project_type: formData.project_type,
    });
    return result.grants;
  } catch {
    // Fall back to mock data if backend is unavailable
    await new Promise(resolve => setTimeout(resolve, 1500));
    const mockGrants = [
    {
      "id": "grant001",
      "program_name": "Juried Sound Recording",
      "administering_agency": "FACTOR",
      "description": "Support for the creation and production of sound recordings by Canadian artists.",
      "eligibility_criteria": {
        "artist_type": ["individual", "group"],
        "residency_requirements": ["Canadian citizen", "Permanent resident"],
        "genre_restrictions": ["All genres"],
        "career_stage": ["Emerging", "Established"],
        "project_type": ["Recording", "Production"]
      },
      "deadline_info": {
        "frequency": "Quarterly",
        "next_deadline": "2024-03-15",
        "application_window": "2024-01-01 to 2024-03-15"
      },
      "funding_details": {
        "min_amount": 5000,
        "max_amount": 50000,
        "average_award": 20000,
        "funding_type": "Grant",
        "requires_matching_funds": true,
        "matching_requirements": "1:1 matching funds required"
      },
      "application_requirements": [
        "Project description",
        "Budget",
        "Work samples (audio)",
        "Artist bio",
        "Marketing plan",
        "Letters of support"
      ],
      "assessment_criteria": [
        "Artistic merit",
        "Market potential",
        "Project feasibility"
      ],
      "url": "https://factor.ca/programs/juried-sound-recording/",
      "last_updated": "2024-01-15",
      "status": "Active"
    },
    {
      "id": "grant002",
      "program_name": "Artist Development",
      "administering_agency": "FACTOR",
      "description": "Emerging artist development funding for recording and market development.",
      "eligibility_criteria": {
        "artist_type": ["individual", "group"],
        "residency_requirements": ["Canadian citizen", "Permanent resident"],
        "genre_restrictions": ["All genres"],
        "career_stage": ["Emerging"],
        "project_type": ["Recording", "Marketing", "Touring"]
      },
      "deadline_info": {
        "frequency": "Rolling",
        "next_deadline": "2024-06-30",
        "application_window": "Ongoing"
      },
      "funding_details": {
        "min_amount": 2000,
        "max_amount": 5000,
        "average_award": 3500,
        "funding_type": "Grant",
        "requires_matching_funds": true,
        "matching_requirements": "25% artist contribution (can be sweat equity)"
      },
      "application_requirements": [
        "Project description",
        "Budget",
        "Work samples",
        "Artist bio",
        "Marketing plan"
      ],
      "assessment_criteria": [
        "Artistic merit",
        "Career development potential",
        "Project feasibility"
      ],
      "url": "https://factor.ca/programs/artist-development/",
      "last_updated": "2024-01-10",
      "status": "Active"
    },
    {
      "id": "grant003",
      "program_name": "Explore and Create: Research and Creation",
      "administering_agency": "Canada Council for the Arts",
      "description": "Grants for artists to research and create new work.",
      "eligibility_criteria": {
        "artist_type": ["individual", "group"],
        "residency_requirements": ["Canadian citizen", "Permanent resident"],
        "genre_restrictions": ["All genres"],
        "career_stage": ["Any"],
        "project_type": ["Creation", "Research"]
      },
      "deadline_info": {
        "frequency": "Rolling",
        "next_deadline": null,
        "application_window": "Ongoing"
      },
      "funding_details": {
        "min_amount": 1000,
        "max_amount": 25000,
        "average_award": 8000,
        "funding_type": "Grant",
        "requires_matching_funds": false,
        "matching_requirements": null
      },
      "application_requirements": [
        "Project description",
        "Budget",
        "Work samples",
        "Artist bio",
        "Supporting material"
      ],
      "assessment_criteria": [
        "Artistic merit",
        "Project feasibility",
        "Contribution to the arts"
      ],
      "url": "https://canadacouncil.ca/funding/grants/explore-and-create-research-and-creation",
      "last_updated": "2024-01-05",
      "status": "Active"
    }
  ];

  // Simple mock matching logic based on form data
  const matches = mockGrants.map(grant => {
    // Calculate a simple match score based on keyword matching
    const desc = grant.description.toLowerCase();
    const projDesc = formData.project_description.toLowerCase();
    const genre = formData.genre.toLowerCase();
    const projectType = formData.project_type.toLowerCase();
    
    let score = 50; // Base score
    
    // Boost if project type matches
    if (grant.eligibility_criteria.project_type.some(p => p.toLowerCase().includes(projectType))) {
      score += 20;
    }
    
    // Boost if genre matches (or if grant accepts all genres)
    if (grant.eligibility_criteria.genre_restrictions.includes("All genres") || 
        grant.eligibility_criteria.genre_restrictions.some(g => g.toLowerCase().includes(genre))) {
      score += 15;
    }
    
    // Boost if artist type matches
    if (grant.eligibility_criteria.artist_type.some(a => a.toLowerCase().includes(formData.artist_type.toLowerCase()))) {
      score += 10;
    }
    
    // Boost if residency matches
    if (grant.eligibility_criteria.residency_requirements.some(r => r.toLowerCase().includes(formData.residency.toLowerCase()))) {
      score += 5;
    }
    
    // Cap at 100
    score = Math.min(score, 100);
    
    // Determine matched and missing criteria (simplified)
    const matched = [];
    const missing = [];
    
    if (grant.eligibility_criteria.artist_type.some(a => a.toLowerCase().includes(formData.artist_type.toLowerCase()))) {
      matched.push(`Artist type: ${formData.artist_type}`);
    } else {
      missing.push(`Artist type: ${formData.artist_type} (allowed: ${grant.eligibility_criteria.artist_type.join(', ')})`);
    }
    
    if (grant.eligibility_criteria.residency_requirements.some(r => r.toLowerCase().includes(formData.residency.toLowerCase()))) {
      matched.push(`Residency: ${formData.residency}`);
    } else {
      missing.push(`Residency: ${formData.residency} (allowed: ${grant.eligibility_criteria.residency_requirements.join(', ')})`);
    }
    
    if (grant.eligibility_criteria.genre_restrictions.includes("All genres") || 
        grant.eligibility_criteria.genre_restrictions.some(g => g.toLowerCase().includes(genre))) {
      matched.push(`Genre: ${formData.genre}`);
    } else {
      missing.push(`Genre: ${formData.genre} (allowed: ${grant.eligibility_criteria.genre_restrictions.join(', ')})`);
    }
    
    if (grant.eligibility_criteria.project_type.some(p => p.toLowerCase().includes(projectType))) {
      matched.push(`Project type: ${formData.project_type}`);
    } else {
      missing.push(`Project type: ${formData.project_type} (allowed: ${grant.eligibility_criteria.project_type.join(', ')})`);
    }
    
    return {
      ...grant,
      match_score: score,
      match_grade: score >= 85 ? 'A' : score >= 70 ? 'B' : score >= 55 ? 'C' : score >= 40 ? 'D' : 'F',
      eligibility_score: Math.min(score + 10, 100),
      project_type_score: Math.min(score + 5, 100),
      keyword_score: Math.max(score - 10, 0),
      complexity_score: 70,
      matched_criteria: matched,
      missing_criteria: missing,
      description: grant.description,
      deadline_info: grant.deadline_info,
      funding_details: grant.funding_details,
      application_requirements: grant.application_requirements,
      url: grant.url
    };
  });
  
    return matches.sort((a, b) => b.match_score - a.match_score);
  }
};

export default function GrantMatcher() {
  const [formData, setFormData] = useState<GrantMatcherFormValues>({
    project_description: '',
    artist_type: '',
    residency: '',
    genre: '',
    project_type: ''
  });
  
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors, isSubmitting }
  } = useForm<GrantMatcherFormValues>();
  
  const { data: matches, isLoading, error } = useQuery<GrantMatch[], Error>({
    queryKey: ['grants', formData],
    queryFn: () => fetchGrantMatches(formData),
    enabled: !!formData.project_description && !!formData.artist_type && !!formData.residency && !!formData.genre && !!formData.project_type
  });
  
  const onSubmit = (data: GrantMatcherFormValues) => {
    setFormData(data);
  };
  
  const watchValues = watch();
  
  // Reset query when form changes
  // This is handled by the enabled flag in useQuery
  
  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Find Matching Grants</h2>
        <p className="text-gray-600 mb-4">
          Tell us about your project to get personalized grant recommendations
        </p>
        
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Project Description
              </label>
              <textarea
                {...register('project_description', {
                  required: 'Project description is required',
                  minLength: {
                    value: 20,
                    message: 'Please provide a detailed description (at least 20 characters)'
                  }
                })}
                className={`w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                  errors.project_description ? 'border-red-500' : ''
                }`}
                rows={4}
                placeholder="Describe your artistic project, goals, and what you need funding for..."
              >
              </textarea>
              {errors.project_description && (
                <p className="mt-1 text-sm text-red-600">{errors.project_description.message}</p>
              )}
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Artist Type
              </label>
              <select
                {...register('artist_type', {
                  required: 'Please select your artist type'
                })}
                className={`w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                  errors.artist_type ? 'border-red-500' : ''
                }`}
              >
                <option value="">Select artist type</option>
                <option value="individual">Individual Artist</option>
                <option value="group">Group/Band</option>
                <option value="organization">Organization/Company</option>
                <option value="producer">Producer</option>
                <option value="songwriter">Songwriter/Composer</option>
              </select>
              {errors.artist_type && (
                <p className="mt-1 text-sm text-red-600">{errors.artist_type.message}</p>
              )}
            </div>
          </div>
          
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Province/Territory
              </label>
              <select
                {...register('residency', {
                  required: 'Please select your province/territory'
                })}
                className={`w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                  errors.residency ? 'border-red-500' : ''
                }`}
              >
                <option value="">Select province/territory</option>
                <option value="Canadian citizen">Canadian Citizen</option>
                <option value="Permanent resident">Permanent Resident</option>
                <option value="Ontario">Ontario</option>
                <option value="Quebec">Quebec</option>
                <option value="British Columbia">British Columbia</option>
                <option value="Alberta">Alberta</option>
                <option value="Nova Scotia">Nova Scotia</option>
                <option value="Manitoba">Manitoba</option>
                <option value="Saskatchewan">Saskatchewan</option>
                <option value="New Brunswick">New Brunswick</option>
                <option value="Newfoundland and Labrador">Newfoundland and Labrador</option>
                <option value="Prince Edward Island">Prince Edward Island</option>
                <option value="Northwest Territories">Northwest Territories</option>
                <option value="Yukon">Yukon</option>
                <option value="Nunavut">Nunavut</option>
              </select>
              {errors.residency && (
                <p className="mt-1 text-sm text-red-600">{errors.residency.message}</p>
              )}
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Genre/Discipline
              </label>
              <input
                {...register('genre', {
                  required: 'Please specify your genre or discipline'
                })}
                className={`w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                  errors.genre ? 'border-red-500' : ''
                }`}
                placeholder="e.g., electronic music, hip hop, jazz, classical, film scoring, etc."
              />
              {errors.genre && (
                <p className="mt-1 text-sm text-red-600">{errors.genre.message}</p>
              )}
            </div>
          </div>
          
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Project Type
              </label>
              <select
                {...register('project_type', {
                  required: 'Please select your project type'
                })}
                className={`w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                  errors.project_type ? 'border-red-500' : ''
                }`}
              >
                <option value="">Select project type</option>
                <option value="recording">Recording/Production</option>
                <option value="touring">Touring/Performance</option>
                <option value="marketing">Marketing/Promotion</option>
                <option value="video">Music Video</option>
                <option value="creation">Creation/Composition</option>
                <option value="research">Research/Development</option>
                <option value="business">Business Development</option>
              </select>
              {errors.project_type && (
                <p className="mt-1 text-sm text-red-600">{errors.project_type.message}</p>
              )}
            </div>
          </div>
          
          <div className="flex justify-end">
            <button
              type="submit"
              disabled={isSubmitting}
              className={`px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${
                isSubmitting ? 'bg-blue-400' : ''
              }`}
            >
              {isSubmitting ? 'Finding Matches...' : 'Find Matching Grants'}
            </button>
          </div>
        </form>
      </div>
      
      {(isLoading || Object.keys(watchValues).length > 0) && !matches && (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Searching for grants...</p>
        </div>
      )}
      
      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-4">
          <p className="text-red-700">
            Error fetching grants: {error.message}
          </p>
        </div>
      )}
      
      {matches && matches.length > 0 && (
        <>
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Matching Grants ({matches.length} found)
            </h2>
            <p className="text-gray-600 mb-4">
              Here are grants that match your project profile. Click on each grant for more details.
            </p>
          </div>
          
          <div className="space-y-4">
            {matches.map((grant, index) => (
              <div key={grant.id} className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow cursor-pointer border-l-4"
                   style={{ borderLeftColor: `hsl(${(index * 40) % 360}, 70%, 50%)` }}>
                <div className="p-6">
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h3 className="text-xl font-semibold text-gray-900">{grant.program_name}</h3>
                      <p className="text-sm text-gray-600">{grant.administering_agency}</p>
                    </div>
                    <div className="text-right space-x-2">
                      <div className="flex items-center">
                        <span className="text-xs font-medium text-gray-600">Match:</span>
                        <span className="ml-1 text-lg font-bold text-green-600">{grant.match_score}%</span>
                      </div>
                    </div>
                  </div>
                  
                  <p className="text-gray-700 mb-3 line-clamp-3">{grant.description}</p>
                  
                  <div className="grid md:grid-cols-2 gap-4 mb-4 text-sm">
                    <div>
                      <span className="font-medium text-gray-700">Deadline:</span>
                      <span className="text-gray-600">
                        {grant.deadline_info.next_deadline ? grant.deadline_info.next_deadline : 'Ongoing'}
                      </span>
                    </div>
                    <div>
                      <span className="font-medium text-gray-700">Funding:</span>
                      <span className="text-gray-600">
                        ${grant.funding_details.min_amount.toLocaleString()} - ${grant.funding_details.max_amount.toLocaleString()}
                      </span>
                    </div>
                    <div>
                      <span className="font-medium text-gray-700">Match Required:</span>
                      <span className="text-gray-600">
                        {grant.funding_details.requires_matching_funds ? 'Yes' : 'No'}
                      </span>
                    </div>
                    <div>
                      <span className="font-medium text-gray-700">Eligibility:</span>
                      <span className="text-gray-600">{grant.eligibility_score}%</span>
                    </div>
                  </div>
                  
                  {grant.matched_criteria.length > 0 && (
                    <div className="mb-3">
                      <span className="font-medium text-gray-700 mb-1 block">Matched Criteria:</span>
                      <div className="flex flex-wrap gap-2">
                        {grant.matched_criteria.map((criteria, idx) => (
                          <span key={idx} className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded">
                            {criteria}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  {grant.missing_criteria.length > 0 && (
                    <div className="mb-3">
                      <span className="font-medium text-gray-700 mb-1 block">Missing Criteria:</span>
                      <div className="flex flex-wrap gap-2">
                        {grant.missing_criteria.map((criteria, idx) => (
                          <span key={idx} className="px-2 py-1 bg-red-100 text-red-800 text-xs rounded">
                            {criteria}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  <div className="mt-4 pt-4 border-t border-gray-200">
                    <a 
                      href={grant.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:text-blue-800 underline text-sm font-medium"
                    >
                      View Full Grant Details →
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
      
      {matches && matches.length === 0 && (
        <div className="text-center py-8">
          <p className="text-gray-600">
            No grants matched your criteria. Try adjusting your project description or criteria.
          </p>
        </div>
      )}
    </div>
  );
}