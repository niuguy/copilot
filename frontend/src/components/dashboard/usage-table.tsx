import { UsageItem, SortDirection } from '@/types';
import { ChevronUp, ChevronDown, ArrowUpDown } from 'lucide-react';
import { formatTimestamp } from '@/utils/date';

interface UsageTableProps {
  data: UsageItem[];
  reportSort: SortDirection;
  creditSort: SortDirection;
  onSort: (column: 'report' | 'credit') => void;
}

export const UsageTable: React.FC<UsageTableProps> = ({
  data,
  reportSort,
  creditSort,
  onSort,
}) => {
  const getSortIcon = (sortState: SortDirection) => {
    switch (sortState) {
      case 'asc':
        return <ChevronUp className="w-4 h-4 inline ml-1" />;
      case 'desc':
        return <ChevronDown className="w-4 h-4 inline ml-1" />;
      default:
        return <ArrowUpDown className="w-4 h-4 inline ml-1" />;
    }
  };

  return (
    <div className="overflow-x-auto">
      <table className="w-full table-fixed bg-white border">
        <thead className="sticky top-0 bg-gray-50">
          <tr>
            <th className="w-1/4 px-6 py-3 text-left text-sm font-semibold text-gray-900">Message ID</th>
            <th className="w-1/4 px-6 py-3 text-left text-sm font-semibold text-gray-900">Timestamp</th>
            <th 
              className="w-1/4 px-6 py-3 text-left text-sm font-semibold text-gray-900 cursor-pointer"
              onClick={() => onSort('report')}
            >
              Report Name {getSortIcon(reportSort)}
            </th>
            <th 
              className="w-1/4 px-6 py-3 text-left text-sm font-semibold text-gray-900 cursor-pointer"
              onClick={() => onSort('credit')}
            >
              Credits Used {getSortIcon(creditSort)}
            </th>
          </tr>
        </thead>
        <tbody>
          {data.map((item) => (
            <tr key={item.id} className="border-t hover:bg-gray-50">
              <td className="px-6 py-4 text-sm text-gray-900 truncate">{item.id}</td>
              <td className="px-6 py-4 text-sm text-gray-900 truncate">{formatTimestamp(item.timestamp)}</td>
              <td className="px-6 py-4 text-sm text-gray-900 truncate">{item.report_name || ''}</td>
              <td className="px-6 py-4 text-sm text-gray-900 truncate">{item.credits.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
