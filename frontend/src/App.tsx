import { Routes, Route } from 'react-router-dom';
import { FocusStyleManager } from '@blueprintjs/core';
import Layout from './components/layout/Layout';
import Home from './pages/Home';
import Wizard from './pages/Wizard';
import RunsList from './pages/RunsList';
import RunDetail from './pages/RunDetail';
import SimulationRunDetail from './pages/SimulationRunDetail';
import NotFound from './pages/NotFound';

// Only show focus rings when using keyboard navigation
FocusStyleManager.onlyShowFocusOnTabs();

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="wizard" element={<Wizard />} />
        <Route path="runs" element={<RunsList />} />
        <Route path="runs/:simulationId" element={<SimulationRunDetail />} />
        <Route path="runs/:simulationId/results" element={<SimulationRunDetail />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}

export default App;
