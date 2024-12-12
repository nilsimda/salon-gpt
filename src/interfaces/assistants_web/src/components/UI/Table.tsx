import React from 'react';

import { cn } from '@/utils';

interface TableProps<T> extends React.HTMLAttributes<HTMLTableElement> {
  data: T[];
  columns: {
    header: string;
    accessor: keyof T;
    cell?: (value: T[keyof T], row: T) => React.ReactNode;
  }[];
  selectedRows: Set<number>;
  onRowSelect: (rowIndex: number) => void;
}

export function Table<T>({
  data,
  columns,
  selectedRows,
  onRowSelect,
  className,
  ...props
}: TableProps<T>) {
  return (
    <div className="w-full overflow-auto">
      <table className={cn('w-full caption-bottom text-sm', className)} {...props}>
        <thead className="[&_tr]:border-b">
          <tr className="hover:bg-muted/50 data-[state=selected]:bg-muted border-b transition-colors">
            <th className="text-muted-foreground h-12 w-[48px] px-4 text-left align-middle font-medium">
              <span className="sr-only">Select</span>
            </th>
            {columns.map((column, index) => (
              <th
                key={index}
                className="text-muted-foreground h-12 px-4 text-left align-middle font-medium [&:has([role=checkbox])]:pr-0"
              >
                {column.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="[&_tr:last-child]:border-0">
          {data.map((row, rowIndex) => (
            <tr
              key={rowIndex}
              className="hover:bg-muted/50 data-[state=selected]:bg-muted border-b transition-colors"
            >
              <td className="p-4 align-middle [&:has([role=checkbox])]:pr-0">
                <input
                  type="checkbox"
                  checked={selectedRows.has(rowIndex)}
                  onChange={() => onRowSelect(rowIndex)}
                  className="text-primary focus:ring-primary h-4 w-4 rounded border-gray-300"
                />
              </td>
              {columns.map((column, colIndex) => (
                <td key={colIndex} className="p-4 align-middle [&:has([role=checkbox])]:pr-0">
                  {column.cell
                    ? column.cell(row[column.accessor], row)
                    : (row[column.accessor] as React.ReactNode)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
