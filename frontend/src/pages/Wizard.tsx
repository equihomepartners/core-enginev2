import React, { useEffect, useRef } from 'react';
import WizardContainer from '../components/wizard/WizardContainer';
import { useSimulationStore } from '../store';

const Wizard: React.FC = () => {
  const store = useSimulationStore();
  const initializedRef = useRef(false);

  // Reset to step 1 when the wizard is loaded - only once
  useEffect(() => {
    if (store && store.setCurrentStep && !initializedRef.current) {
      initializedRef.current = true;
      store.setCurrentStep(1);
    }
  }, []);

  return (
    <div className="max-w-6xl mx-auto">
      <WizardContainer />
    </div>
  );
};

export default Wizard;
