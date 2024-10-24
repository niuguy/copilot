import { format } from 'date-fns';

export const formatTimestamp = (timestamp: string): string => {
  return format(new Date(timestamp), 'dd-MM-yyyy HH:mm');
};

// src/utils/sort.ts
import { UsageItem, SortDirection } from '@/types';

export const getSortedData = (
  data: UsageItem[],
  reportSort: SortDirection,
  creditSort: SortDirection
): UsageItem[] => {
  let sortedData = [...data];

  if (reportSort !== 'none') {
    sortedData.sort((a, b) => {
      const aName = a.report_name || '';
      const bName = b.report_name || '';
      return reportSort === 'asc'
        ? aName.localeCompare(bName)
        : bName.localeCompare(aName);
    });
  }

  if (creditSort !== 'none') {
    sortedData.sort((a, b) => {
      return creditSort === 'asc'
        ? a.credits - b.credits
        : b.credits - a.credits;
    });
  }

  return sortedData;
};