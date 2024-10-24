export interface UsageItem {
    id: number;
    timestamp: string;
    report_name?: string;
    credits: number;
  }
  
  export interface UsageResponse {
    usage: UsageItem[];
    total_credits: number;
  }
  
  // src/types/dashboard.ts
  export type SortDirection = 'none' | 'asc' | 'desc';
  
  export interface SortState {
    reportSort: SortDirection;
    creditSort: SortDirection;
  }
  
  export interface ChartData {
    date: string;
    credits: number;
  }