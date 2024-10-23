import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { ChartData } from '@/types';

interface UsageChartProps {
  data: ChartData[];
}

export function UsageChart({ data }: UsageChartProps) {
  return (
    <div className="h-64 mb-8">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="credits" fill="#4f46e5" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}