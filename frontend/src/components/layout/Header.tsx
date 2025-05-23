import { Link, NavLink, useNavigate } from 'react-router-dom';
import { Button, Icon } from '@blueprintjs/core';
import Logo from './Logo';

const Header = () => {
  const navigate = useNavigate();
  return (
    <header className="header-bar">
      <div className="container mx-auto flex justify-between items-center h-full">
        <div className="flex items-center">
          <Link to="/" className="flex items-center group">
            <Logo className="h-9 w-9 mr-3 transition-transform group-hover:scale-105" />
            <div className="flex flex-col">
              <span className="text-xl font-display font-semibold tracking-tight">Equihome</span>
              <span className="text-xs text-neutral-200 -mt-1">Simulation Engine</span>
            </div>
          </Link>

          <div className="h-8 mx-6 border-l border-primary-light opacity-30"></div>

          <nav className="hidden md:block">
            <ul className="flex space-x-2">
              <li>
                <NavLink
                  to="/"
                  className={({ isActive }) =>
                    isActive ? 'nav-link-active' : 'nav-link'
                  }
                  end
                >
                  <Icon icon="dashboard" className="mr-1.5" size={14} />
                  Dashboard
                </NavLink>
              </li>
              <li>
                <NavLink
                  to="/runs"
                  className={({ isActive }) =>
                    isActive ? 'nav-link-active' : 'nav-link'
                  }
                >
                  <Icon icon="history" className="mr-1.5" size={14} />
                  Simulations
                </NavLink>
              </li>
              <li>
                <NavLink
                  to="/docs"
                  className={({ isActive }) =>
                    isActive ? 'nav-link-active' : 'nav-link'
                  }
                >
                  <Icon icon="manual" className="mr-1.5" size={14} />
                  Documentation
                </NavLink>
              </li>
            </ul>
          </nav>
        </div>

        <div className="flex items-center space-x-4">
          <Button
            minimal={true}
            icon="help"
            className="text-white hover:bg-primary-light"
            onClick={() => navigate('/docs')}
          />
          <Button
            intent="primary"
            icon="play"
            text="Run New Simulation"
            className="shadow-sm"
            onClick={() => navigate('/wizard')}
          />
        </div>
      </div>
    </header>
  );
};

export default Header;
