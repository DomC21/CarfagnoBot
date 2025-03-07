import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { ChatPage } from './pages/ChatPage';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';
import { DashboardPage } from './pages/DashboardPage';
import { QuizPage } from './pages/QuizPage';
import { QuizzesPage } from './pages/QuizzesPage';
import LearningPathPage from './pages/LearningPathPage';
import { User, BookOpen, GraduationCap } from 'lucide-react';
import './App.css';

// Header component with navigation
const Header = () => {
  const { user, logout } = useAuth();
  
  return (
    <header className="bg-blue-600 text-white p-4 flex items-center justify-between">
      <div className="flex items-center gap-2">
        <Link to="/" className="flex items-center gap-2">
          <div className="w-10 h-10 bg-blue-700 rounded flex items-center justify-center text-white font-bold">CE</div>
          <div>
            <h1 className="text-xl font-bold">CarfganoBot</h1>
            <p className="text-xs opacity-80">by Carfgano Enterprises</p>
          </div>
        </Link>
      </div>
      <div className="flex items-center gap-4">
        <span className="font-medium hidden md:inline">Investing Education</span>
        {user ? (
          <div className="flex items-center gap-2">
            <Link to="/dashboard" className="flex items-center gap-1 text-white hover:text-blue-100">
              <User className="h-4 w-4" />
              <span>Dashboard</span>
            </Link>
            <Link to="/quizzes" className="flex items-center gap-1 text-white hover:text-blue-100">
              <BookOpen className="h-4 w-4" />
              <span>Quizzes</span>
            </Link>
            <Link to="/learning-path" className="flex items-center gap-1 text-white hover:text-blue-100">
              <GraduationCap className="h-4 w-4" />
              <span>Learning Path</span>
            </Link>
            <button 
              onClick={logout}
              className="text-white hover:text-blue-100 text-sm"
            >
              Sign Out
            </button>
          </div>
        ) : (
          <div className="flex items-center gap-2">
            <Link to="/login" className="text-white hover:text-blue-100 text-sm">Sign In</Link>
            <Link to="/register" className="bg-white text-blue-600 px-3 py-1 rounded-md text-sm hover:bg-blue-50">
              Register
            </Link>
          </div>
        )}
      </div>
    </header>
  );
};

// Protected route component
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, isLoading } = useAuth();
  
  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }
  
  return <>{children}</>;
};

function App() {
  return (
    <Router>
      <AuthProvider>
        <div className="flex flex-col h-screen bg-gray-50">
          <Header />
          <main className="flex-1 overflow-hidden">
            <Routes>
              <Route path="/" element={<ChatPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route 
                path="/dashboard" 
                element={
                  <ProtectedRoute>
                    <DashboardPage />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/quizzes" 
                element={
                  <ProtectedRoute>
                    <QuizzesPage />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/learning-path" 
                element={
                  <ProtectedRoute>
                    <LearningPathPage />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/quiz/:quizId" 
                element={
                  <ProtectedRoute>
                    <QuizPage />
                  </ProtectedRoute>
                } 
              />
            </Routes>
          </main>
          <footer className="bg-gray-100 p-2 text-center text-xs text-gray-500">
            © {new Date().getFullYear()} Carfgano Enterprises. All rights reserved.
          </footer>
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;
