import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import GrantMatcher from './pages/GrantMatcher';
import About from './pages/About';
import Deadlines from './pages/Deadlines';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
        <nav className="bg-white/80 backdrop-blur-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex-shrink-0">
                <Link to="/" className="text-xl font-bold text-gray-800">
                  Grant-O-Matic
                </Link>
              </div>
              <div className="hidden md:flex md:space-x-6">
                <Link to="/" className="text-gray-600 hover:text-gray-900 transition-colors">
                  Home
                </Link>
                <Link to="/match" className="text-gray-600 hover:text-gray-900 transition-colors">
                  Grant Matcher
                </Link>
                <Link to="/deadlines" className="text-gray-600 hover:text-gray-900 transition-colors">
                  Deadlines
                </Link>
                <Link to="/about" className="text-gray-600 hover:text-gray-900 transition-colors">
                  About
                </Link>
              </div>
            </div>
          </div>
        </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8 pb-8">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/match" element={<GrantMatcher />} />
          <Route path="/deadlines" element={<Deadlines />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </main>

      <footer className="bg-gray-50 border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-sm text-gray-500">
            Grant-O-Matic © {new Date().getFullYear()} - Helping Canadian artists find funding
          </p>
        </div>
      </footer>
      </div>
    </Router>
  );
}

export default App;
