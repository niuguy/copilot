import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { ChartData } from '@/types';

interface UsageChartProps {
  data: ChartData[];
}

export function UsageChart({ data }: UsageChartProps) {
  return (
    <div className="h-64 mb-8">
      {/* <h2 className="text-lg font-semibold mb-2">Usage Chart</h2> */}
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
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
