import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { UsageItem, ChartData, SortState } from '@/types';
import { fetchUsageData } from '@/services/api';
import { UsageChart } from './usage-chart';
import { UsageTable } from './usage-table';

export function UsageDashboard() {
  const [data, setData] = useState<UsageItem[]>([]);
  const [chartData, setChartData] = useState<ChartData[]>([]);
  const [searchParams, setSearchParams] = useSearchParams();
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const sortState: SortState = {
    reportSort: (searchParams.get('reportSort') as SortState['reportSort']) || 'none',
    creditSort: (searchParams.get('creditSort') as SortState['creditSort']) || 'none',
  };

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const response = await fetchUsageData();
      setData(response.usage);
      
      // Process chart data
      const dateGroups = response.usage.reduce<Record<string, number>>((acc, item) => {
        const date = new Date(item.timestamp).toLocaleDateString('en-GB');
        acc[date] = (acc[date] || 0) + item.credits;
        return acc;
      }, {});
      
      const chartData = Object.entries(dateGroups).map(([date, credits]) => ({
        date,
        credits: Number(credits.toFixed(2))
      })).sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
      
      setChartData(chartData);
      setIsLoading(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch data');
      setIsLoading(false);
    }
  };

  const handleSort = (column: 'report' | 'credit') => {
    const nextSort = {
      none: 'asc',
      asc: 'desc',
      desc: 'none'
    } as const;

    const newSortState = {
      ...sortState,
      [column === 'report' ? 'reportSort' : 'creditSort']: 
        nextSort[sortState[column === 'report' ? 'reportSort' : 'creditSort']]
    };

    setSearchParams(newSortState);
  };

  const getSortedData = () => {
    let sortedData = [...data];

    if (sortState.reportSort !== 'none') {
      sortedData.sort((a, b) => {
        const aName = a.report_name || '';
        const bName = b.report_name || '';
        return sortState.reportSort === 'asc' 
          ? aName.localeCompare(bName)
          : bName.localeCompare(aName);
      });
    }

    if (sortState.creditSort !== 'none') {
      sortedData.sort((a, b) => {
        return sortState.creditSort === 'asc'
          ? a.credits - b.credits
          : b.credits - a.credits;
      });
    }

    return sortedData;
  };

  if (isLoading) return <div className="p-4">Loading...</div>;
  if (error) return <div className="p-4 text-red-500">{error}</div>;

  return (
    <div className="p-4 max-w-6xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Usage Dashboard</h1>
      <UsageChart data={chartData} />
      <UsageTable 
        data={getSortedData()} 
        sortState={sortState}
        onSort={handleSort}
      />
    </div>
  );
}