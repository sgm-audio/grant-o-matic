import { grantApi } from './api';

// Test connection to backend API
export const testConnection = async () => {
  try {
    console.log('Testing connection to backend API...');
    const health = await grantApi.healthCheck();
    console.log('✓ Backend API is healthy:', health);
    return true;
  } catch (error) {
    console.error('✗ Failed to connect to backend API:', error);
    console.log('Make sure the backend is running:');
    console.log('  cd ../api && python main.py');
    return false;
  }
};

// Test grant matching
export const testGrantMatching = async () => {
  try {
    console.log('Testing grant matching...');
    const result = await grantApi.matchGrants({
      project_description: 'I am an emerging electronic music producer based in Toronto working on my debut EP',
      artist_type: 'individual',
      residency: 'Canadian citizen',
      genre: 'electronic',
      project_type: 'Recording',
      budget_amount: 15000.00
    });
    
    console.log('✓ Grant matching test successful:');
    console.log(`  Found ${result.grants.length} grants`);
    if (result.grants.length > 0) {
      const topGrant = result.grants[0];
      console.log(`  Top match: ${topGrant.program_name} (${topGrant.match_score}%, Grade: ${topGrant.match_grade})`);
      if (topGrant.budget_suggestion) {
        console.log(`  Budget suggestion: $${topGrant.budget_suggestion.total_budget.toLocaleString()}`);
      }
    }
    return true;
  } catch (error) {
    console.error('✗ Grant matching test failed:', error);
    return false;
  }
};