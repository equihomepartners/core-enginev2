import React, { useState } from 'react';
import { Button, Card, Icon, Intent, ProgressBar } from '@blueprintjs/core';
import { useNavigate } from 'react-router-dom';
import { useSimulationStore } from '../../store';
import Step1FundBasics from './Step1FundBasics';
import Step2PortfolioStrategy from './Step2PortfolioStrategy';
import Step3RiskVolatility from './Step3RiskVolatility';
import Step4ReviewRun from './Step4ReviewRun';
import { toast } from '../../api/toast';

// Define the steps in the wizard
const STEPS = [
  { id: 1, title: 'Fund Basics', component: Step1FundBasics, icon: 'properties' },
  { id: 2, title: 'Portfolio Strategy', component: Step2PortfolioStrategy, icon: 'chart' },
  { id: 3, title: 'Risk & Volatility', component: Step3RiskVolatility, icon: 'dashboard' },
  { id: 4, title: 'Review & Run', component: Step4ReviewRun, icon: 'play' },
];

const WizardContainer: React.FC = () => {
  const navigate = useNavigate();
  const store = useSimulationStore();
  const currentStep = store?.currentStep || 1;
  const isLoading = store?.isLoading || false;

  // Handle next step
  const handleNext = () => {
    if (currentStep < STEPS.length && store?.setCurrentStep) {
      store.setCurrentStep(currentStep + 1);
    }
  };

  // Handle previous step
  const handlePrevious = () => {
    if (currentStep > 1 && store?.setCurrentStep) {
      store.setCurrentStep(currentStep - 1);
    }
  };

  // Handle cancel
  const handleCancel = () => {
    if (window.confirm('Are you sure you want to cancel? All unsaved changes will be lost.')) {
      navigate('/');
    }
  };

  // Handle run simulation
  const handleRunSimulation = async () => {
    // Generate a simulation ID and navigate to progress page
    const simulationId = `sim-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

    await toast.info('Starting simulation...');

    navigate(`/runs/${simulationId}`);
  };

  // Get current step component
  const CurrentStepComponent = STEPS.find(step => step.id === currentStep)?.component || (() => null);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-display font-semibold text-neutral-900">New Simulation</h1>
          <p className="text-neutral-500 mt-1">Configure your simulation parameters</p>
        </div>
      </div>

      {/* Progress indicator */}
      <div className="bg-white rounded-lg shadow-md border border-neutral-200 p-6">
        <div className="flex items-center justify-between mb-4">
          {STEPS.map((step, index) => (
            <React.Fragment key={step.id}>
              {/* Step indicator */}
              <div className="flex flex-col items-center">
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center ${
                    step.id === currentStep
                      ? 'bg-primary text-white'
                      : step.id < currentStep
                        ? 'bg-primary-light text-white'
                        : 'bg-neutral-200 text-neutral-500'
                  }`}
                >
                  <Icon icon={step.icon} size={16} />
                </div>
                <div className="text-sm font-medium mt-2 text-center">
                  {step.title}
                </div>
              </div>

              {/* Connector line */}
              {index < STEPS.length - 1 && (
                <div className="flex-grow mx-2 h-1 bg-neutral-200">
                  <div
                    className="h-full bg-primary-light"
                    style={{
                      width: `${step.id < currentStep ? '100%' : '0%'}`
                    }}
                  />
                </div>
              )}
            </React.Fragment>
          ))}
        </div>

        {/* Progress bar */}
        <ProgressBar
          value={currentStep / STEPS.length}
          intent={Intent.PRIMARY}
          stripes={false}
          className="mb-2"
        />

        <div className="text-sm text-neutral-500 text-right">
          Step {currentStep} of {STEPS.length}
        </div>
      </div>

      {/* Step content */}
      <div className="bg-white rounded-lg shadow-md border border-neutral-200 p-6">
        <CurrentStepComponent />
      </div>

      {/* Navigation buttons */}
      <div className="flex justify-between items-center">
        <div>
          <Button
            text="Cancel"
            onClick={handleCancel}
            minimal={true}
          />
        </div>

        <div className="flex space-x-4">
          <Button
            text="Previous"
            onClick={handlePrevious}
            disabled={currentStep === 1}
            icon="arrow-left"
          />

          {currentStep < STEPS.length ? (
            <Button
              text="Next"
              intent={Intent.PRIMARY}
              onClick={handleNext}
              rightIcon="arrow-right"
            />
          ) : (
            <Button
              text="Run Simulation"
              intent={Intent.SUCCESS}
              onClick={handleRunSimulation}
              icon="play"
              loading={isLoading}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default WizardContainer;
