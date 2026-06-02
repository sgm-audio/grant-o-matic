import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div className="space-y-8">
      <div className="text-center py-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Grant-O-Matic
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          AI-powered grant matching system designed specifically for Canadian artists and creators
        </p>
        <Link to="/match" className="inline-block mt-6 px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors shadow-lg">
          Start Finding Grants
        </Link>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow hover:shadow-md transition-shadow">
          <div className="p-6">
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0">
                <div className="h-10 w-10 bg-blue-100 rounded-lg flex items-center justify-center text-blue-600">
                  🤖
                </div>
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">AI Grant Matching</h3>
                <p className="text-gray-600">
                  Get personalized grant recommendations based on your project description, location, and artistic discipline
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow hover:shadow-md transition-shadow">
          <div className="p-6">
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0">
                <div className="h-10 w-10 bg-green-100 rounded-lg flex items-center justify-center text-green-600">
                  📅
                </div>
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Deadline Tracking</h3>
                <p className="text-gray-600">
                  Never miss a grant deadline with automated alerts and calendar integration
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow hover:shadow-md transition-shadow">
          <div className="p-6">
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0">
                <div className="h-10 w-10 bg-purple-100 rounded-lg flex items-center justify-center text-purple-600">
                  📝
                </div>
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Application Assistant</h3>
                <p className="text-gray-600">
                  Generate budget justifications and improve your grant applications with AI-powered assistance
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-gray-50 rounded-lg p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">How It Works</h2>
        <ol className="list-decimal list-inside space-y-4 text-gray-700">
          <li>
            Describe your project: Tell us about your artistic project, location, and goals
          </li>
          <li>
            Get matched: Our AI scans hundreds of Canadian grants to find the best fits
          </li>
          <li>
            Apply with confidence: Receive personalized guidance and application materials
          </li>
          <li>
            Track & renew: Monitor deadlines and reapply with improved strategies
          </li>
        </ol>
      </div>
    </div>
  );
}