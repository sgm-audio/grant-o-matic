export default function About() {
  return (
    <div className="space-y-8">
      <div className="bg-white rounded-lg shadow-md p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">
          About Grant-O-Matic
        </h1>
        <p className="text-gray-700 leading-relaxed mb-6">
          Grant-O-Matic is an AI-powered system designed specifically for Canadian artists and creators to navigate the complex landscape of grants, funding, and career development opportunities in Canada's unique cultural ecosystem.
        </p>
        
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          Our Mission
        </h2>
        <p className="text-gray-700 leading-relaxed mb-6">
          To empower Canadian creators with the tools and knowledge needed to build sustainable, globally competitive careers while staying rooted in Canada's rich cultural landscape. We believe that artists shouldn't have to leave Canada to succeed—they should be able to leverage Canada's unique advantages to build thriving creative enterprises.
        </p>
        
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          How We Help
        </h2>
        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              🎯 Smart Grant Matching
            </h3>
            <p className="text-gray-700">
              Our AI analyzes your project description and matches it against hundreds of Canadian grant opportunities, saving you hours of research and increasing your chances of success.
            </p>
          </div>
          
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              📅 Deadline Intelligence
            </h3>
            <p className="text-gray-700">
              Never miss an important deadline again. Our system tracks grant deadlines and sends you timely reminders so you can plan your applications effectively.
            </p>
          </div>
          
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              💰 Application Assistance
            </h3>
            <p className="text-gray-700">
              Get help with budget justifications, project descriptions, and other application materials through our AI-powered writing assistant.
            </p>
          </div>
          
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              🇨🇦 Canada-Specific Expertise
            </h3>
            <p className="text-gray-700">
              Unlike generic grant databases, we focus on Canadian funding opportunities that matter to Canadian creators — currently catalogued from the Canada Council for the Arts.
            </p>
          </div>
        </div>
      </div>
      
      <div className="bg-gray-50 rounded-lg p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Who We're For
        </h2>
        <p className="text-gray-700 mb-4">
          Grant-O-Matic is designed for Canadian:
        </p>
        <div className="grid md:grid-cols-3 gap-4 text-gray-600">
          <div>• Musicians and composers</div>
          <div>• Filmmakers and video artists</div>
          <div>• Digital media creators</div>
          <div>• Writers and authors</div>
          <div>• Visual artists</div>
          <div>• Performing artists</div>
          <div>• Game audio designers</div>
          <div>• Multimedia artists</div>
          <div>• Cultural organizations</div>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow-md p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Data Sources
        </h2>
        <p className="text-gray-700 mb-4">
          Our current catalog is loaded from these Canadian funding sources:
        </p>
        <ul className="list-disc list-inside space-y-2 text-gray-700 pl-5">
          <li>
            <a
              href="https://canadacouncil.ca/funding/grants"
              className="text-blue-600 hover:underline"
              target="_blank"
              rel="noreferrer"
            >
              Canada Council for the Arts
            </a>
          </li>
        </ul>
        <p className="text-gray-600 text-sm mt-4">
          Additional agencies will appear here only after their programs are present in the loaded grant data.
        </p>
      </div>
    </div>
  );
}