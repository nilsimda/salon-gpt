import React from 'react'
import { cn } from "@/utils"

interface TableProps<T> extends React.HTMLAttributes<HTMLTableElement> {
    data: T[]
    columns: {
        header: string
        accessor: keyof T
        cell?: (value: T[keyof T], row: T) => React.ReactNode
    }[]
    selectedRows: Set<number>
    onRowSelect: (rowIndex: number) => void
}

export function Table<T>({ data, columns, selectedRows, onRowSelect, className, ...props }: TableProps<T>) {
    return (
        <div className="w-full overflow-auto">
            <table className={cn("w-full caption-bottom text-sm", className)} {...props}>
                <thead className="[&_tr]:border-b">
                    <tr className="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted">
                        <th className="h-12 w-[48px] px-4 text-left align-middle font-medium text-muted-foreground">
                            <span className="sr-only">Select</span>
                        </th>
                        {columns.map((column, index) => (
                            <th
                                key={index}
                                className="h-12 px-4 text-left align-middle font-medium text-muted-foreground [&:has([role=checkbox])]:pr-0"
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
                            className="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted"
                        >
                            <td className="p-4 align-middle [&:has([role=checkbox])]:pr-0">
                                <input
                                    type="checkbox"
                                    checked={selectedRows.has(rowIndex)}
                                    onChange={() => onRowSelect(rowIndex)}
                                    className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
                                />
                            </td>
                            {columns.map((column, colIndex) => (
                                <td key={colIndex} className="p-4 align-middle [&:has([role=checkbox])]:pr-0">
                                    {column.cell ? column.cell(row[column.accessor], row) : row[column.accessor] as React.ReactNode}
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}