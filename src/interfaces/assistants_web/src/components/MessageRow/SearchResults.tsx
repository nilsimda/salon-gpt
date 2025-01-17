import { CitationList } from "@/salon-client";
import { cn } from "@/utils";
import { TabGroup, TabList, TabPanels, TabPanel, Tab } from '@headlessui/react';

type SearchResultsProps = {
    searchResults?: CitationList[] | undefined;
}

export const SearchResults: React.FC<SearchResultsProps> = ({ searchResults }) => {
    console.log(searchResults)
    if (!searchResults || searchResults.length === 0) {
        return null;
    }

    return (
        <div className="w-full px-2 py-4">
            <TabGroup>
                <TabList className="flex space-x-1 rounded-xl bg-slate-800 p-1">
                    {searchResults.map((result, idx) => (
                        <Tab
                            key={idx}
                            className={({ selected }) =>
                                cn(
                                    'w-full rounded-lg py-2.5 text-sm font-medium leading-5',
                                    'ring-white/60 ring-offset-2 focus:outline-none focus:ring-2',
                                    selected
                                        ? 'bg-white text-slate-800 shadow'
                                        : 'text-slate-100 hover:bg-slate-700 hover:text-white'
                                )
                            }
                        >
                            Result {idx + 1}
                        </Tab>
                    ))}
                </TabList>
                <TabPanels className="mt-2">
                    {searchResults.map((result, idx) => (
                        <TabPanel
                            key={idx}
                            className="rounded-xl bg-slate-800 p-3 text-slate-100"
                        >
                            <div className="space-y-4">
                                {result.zitate.map((zitat, zIdx) => (
                                    <>
                                        <div key={zIdx} className="border-l-4 pl-4">
                                            <p className="text-sm italic">{zitat.text}</p>
                                        </div>
                                        <div className="mt-4">
                                            <h3 className="text-sm font-medium text-slate-300">Erklärung:</h3>
                                            <p className="mt-1 text-sm">{zitat.erklaerung}</p>
                                        </div>
                                        <div className="mt-2">
                                            <span className="text-xs text-slate-400">
                                                Konfidenz: {(zitat.bewertung * 100).toFixed(1)}%
                                            </span>
                                        </div>
                                    </>
                                ))}
                            </div>
                        </TabPanel>
                    ))}
                </TabPanels>
            </TabGroup>
        </div>
    );
};