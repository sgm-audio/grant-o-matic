import { useQuery } from '@tanstack/react-query';
import { grantApi, type DeadlineItem } from '../services/api';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function Deadlines() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['deadlines', 400],
    queryFn: () => grantApi.getDeadlines(400, false),
  });

  const deadlines: DeadlineItem[] = data?.deadlines ?? [];
  const tracked = data?.tracked_count ?? 0;

  return (
    <div className="space-y-8 px-4 sm:px-0">
      <div className="bg-white rounded-lg shadow-md p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-3">Upcoming deadlines</h1>
        <p className="text-gray-700 max-w-3xl mb-6">
          Deadlines come only from grant records with a verified <code className="text-sm">next_deadline</code>.
          Programs without a parsed date are omitted — check the official agency page linked below.
          Alert channel for this release is downloadable ICS calendar export (no email secrets required).
        </p>
        <div className="flex flex-wrap gap-3">
          <a
            href={`${API_BASE}/deadlines/export.ics?days_ahead=400`}
            className="inline-flex items-center px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
          >
            Download ICS calendar
          </a>
          <a
            href="https://www.factor.ca/artists/deadlines/"
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center px-4 py-2 border border-gray-300 text-gray-800 font-medium rounded-lg hover:bg-gray-50 transition-colors"
          >
            FACTOR deadlines
          </a>
          <a
            href="https://canadacouncil.ca/funding/grants/deadlines"
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center px-4 py-2 border border-gray-300 text-gray-800 font-medium rounded-lg hover:bg-gray-50 transition-colors"
          >
            Canada Council deadlines
          </a>
        </div>
        <p className="text-sm text-gray-500 mt-4">
          Tracked dated deadlines in catalog: {tracked}. Showing next 400 days.
        </p>
      </div>

      {isLoading && (
        <div className="bg-white rounded-lg shadow p-6 text-gray-600">Loading deadlines…</div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-800 rounded-lg p-6">
          Could not load deadlines from the API. Is the backend running on {API_BASE}?
        </div>
      )}

      {!isLoading && !error && deadlines.length === 0 && (
        <div className="bg-amber-50 border border-amber-200 text-amber-900 rounded-lg p-6">
          No upcoming <code className="text-sm">next_deadline</code> values fall in this window.
          Coverage is still sparse for Canada Council programs (dates live on the official deadlines page).
        </div>
      )}

      <div className="space-y-4">
        {deadlines.map((item) => (
          <article key={`${item.id}-${item.deadline_date}`} className="bg-white rounded-lg shadow p-6">
            <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
              <div>
                <h2 className="text-xl font-semibold text-gray-900">{item.program_name}</h2>
                <p className="text-gray-600 mt-1">{item.administering_agency}</p>
                {item.frequency && (
                  <p className="text-sm text-gray-500 mt-2">Frequency: {item.frequency}</p>
                )}
                {item.application_window && (
                  <p className="text-sm text-gray-500 mt-1">Window: {item.application_window}</p>
                )}
              </div>
              <div className="text-left md:text-right shrink-0">
                <p className="text-lg font-semibold text-blue-700">{item.deadline_date}</p>
                {typeof item.days_until === 'number' && (
                  <p className="text-sm text-gray-600 mt-1">
                    {item.days_until === 0
                      ? 'Due today'
                      : item.days_until > 0
                        ? `${item.days_until} days left`
                        : `${Math.abs(item.days_until)} days ago`}
                  </p>
                )}
                {item.url && (
                  <a
                    href={item.url}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-block mt-3 text-blue-600 hover:underline text-sm font-medium"
                  >
                    Official program page
                  </a>
                )}
              </div>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
