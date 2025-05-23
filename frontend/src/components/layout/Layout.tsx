import { Outlet } from 'react-router-dom';
import Header from './Header';

// Note: Toast functionality is now handled by the centralized toast utility in src/api/toast.ts

const Layout = () => {
  return (
    <div className="min-h-screen flex flex-col bg-neutral-50">
      <Header />

      {/* Main content */}
      <main className="flex-grow container mx-auto px-6 py-8">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-neutral-100 border-t border-neutral-200 py-6">
        <div className="container mx-auto px-6">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-neutral-500 text-sm mb-4 md:mb-0">
              &copy; {new Date().getFullYear()} Equihome Partners. All rights reserved.
            </div>
            <div className="flex space-x-6">
              <a href="#" className="text-neutral-500 hover:text-primary text-sm">Terms of Service</a>
              <a href="#" className="text-neutral-500 hover:text-primary text-sm">Privacy Policy</a>
              <a href="#" className="text-neutral-500 hover:text-primary text-sm">Contact</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
