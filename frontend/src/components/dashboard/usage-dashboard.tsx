import { useState, useEffect } from 'react';
import { UsageItem, ChartDataItem } from '@/types';
import { apiService } from '@/services/api';
import { UsageChart } from './usage-chart';
import { UsageTable } from './usage-table';

export function UsageDashboard() {
  const [data, setData] = useState<UsageItem[]>([]);
  const [chartData, setChartData] = useState<ChartDataItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const response = await apiService.getUsageData();
      setData(response.usage);
      setChartData(response.chart_data);
      setIsLoading(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch data');
      setIsLoading(false);
    }
  };

  if (isLoading) return <div className="p-4 text-center">Loading...</div>;
  if (error) return <div className="p-4 text-red-500 text-center">{error}</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 ">
      <div className="flex flex-col items-center"> <h1>Usage Dashboard</h1></div>
     
      <div className="flex flex-col items-center">
        <div className="w-full mb-8">
          <div className="h-64">
            <UsageChart data={chartData} />
          </div>
        </div>
        <div className="w-full mt-8">
            <UsageTable data={data} />
        </div>
      </div>
    </div>
  );
}
