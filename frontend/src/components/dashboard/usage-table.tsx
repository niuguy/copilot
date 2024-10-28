import React from 'react';
import { UsageItem } from '@/types';
import { formatTimestamp } from '@/utils/date';
import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  getSortedRowModel,
  SortingState,
  useReactTable,
} from "@tanstack/react-table"
import { useEffect, useState, useMemo } from "react"
import { useSearchParams } from 'react-router-dom'

interface UsageTableProps {
  data: UsageItem[];
}

export const UsageTable: React.FC<UsageTableProps> = ({ data }) => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [sorting, setSorting] = useState<SortingState>([])

  useEffect(() => {
    const reportSort = searchParams.get('reportSort');
    const creditSort = searchParams.get('creditSort');
    const newSorting: SortingState = [];

    if (reportSort) {
      newSorting.push({ id: 'report_name', desc: reportSort === 'desc' });
    }
    if (creditSort) {
      newSorting.push({ id: 'credits', desc: creditSort === 'desc' });
    }

    setSorting(newSorting);
  }, [searchParams]);

  const updateSorting = (newSorting: SortingState) => {
    // Update the internal state
    setSorting(newSorting)

    // Update the search params
    const params = new URLSearchParams(searchParams);
    
    ['reportSort', 'creditSort'].forEach(param => params.delete(param));
    
    newSorting.forEach((sort) => {
      if (sort.id === 'report_name') {
        params.set('reportSort', sort.desc ? 'desc' : 'asc');
      } else if (sort.id === 'credits') {
        params.set('creditSort', sort.desc ? 'desc' : 'asc');
      }
    });

    setSearchParams(params);
  };

  const columns = useMemo<ColumnDef<UsageItem>[]>(
    () => [
      {
        accessorKey: "id",
        header: "Message ID",
        cell: ({ row }) => <div className="truncate">{row.getValue("id")}</div>,
        enableSorting: false,
      },
      {
        accessorKey: "timestamp",
        header: "Timestamp",
        cell: ({ row }) => <div>{formatTimestamp(row.getValue("timestamp"))}</div>,
        enableSorting: false,
      },
      {
        accessorKey: "report_name",
        header: "Report Name",
        cell: ({ row }) => <div className="truncate">{row.getValue("report_name") || ''}</div>,
        enableSorting: true,
      },
      {
        accessorKey: "credits",
        header: "Credits Used",
        cell: ({ row }) => <div>{(row.getValue("credits") as number).toFixed(2)}</div>,
        enableSorting: true,
      },
    ],
    []
  )

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    // onSortingChange: setSorting,
    onSortingChange: (updater) => {
      const newSorting = typeof updater === 'function' ? updater(sorting) : updater;
      updateSorting(newSorting);
    },
    getSortedRowModel: getSortedRowModel(),
    state: {
      sorting,
    },
    enableMultiSort: true,
    maxMultiSortColCount: 2,
    enableSortingRemoval: true, // Enable the ability to remove sorting
    isMultiSortEvent: () => true,
    
  })

  return (
    <div className="relative w-full">
      <div className="w-full max-w-4xl">
      <table className="table-auto border-collapse w-full border-2 border-gray-500">
        <thead className="bg-gray-50">
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <th
                  key={header.id}
                  className="border-2 border-gray-500 px-3 py-3 text-left font-semibold"
                  onClick={header.column.getToggleSortingHandler()}
                  style={{ 
                    cursor: header.column.getCanSort() ? 'pointer' : 'default',
                    minWidth: '150px',
                    maxWidth: '250px'
                  }}
                  title={
                    header.column.getCanSort()
                      ? header.column.getNextSortingOrder() === 'asc'
                        ? 'Sort ascending'
                        : header.column.getNextSortingOrder() === 'desc'
                          ? 'Sort descending'
                          : 'Clear sort'
                      : undefined
                  }
                >
                  {flexRender(
                    header.column.columnDef.header,
                    header.getContext()
                  )}
                  <span>
                    {{
                      asc: ' 🔼',
                      desc: ' 🔽',
                    }[header.column.getIsSorted() as string] ?? ''}
                  </span>
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row) => (
            <tr key={row.id}>
              {row.getVisibleCells().map((cell) => (
                <td 
                  key={cell.id} 
                  className="border-2 border-gray-500 px-3 py-2 whitespace-nowrap overflow-hidden text-ellipsis"
                >
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
        </table>
      </div>
    </div>
  )
}
