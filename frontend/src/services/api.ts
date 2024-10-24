import { UsageResponse } from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const apiService = {
  async getUsageData(): Promise<UsageResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/usage`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    } catch (error) {
      throw new Error(`Failed to fetch usage data: ${error}`);
    }
  }
};