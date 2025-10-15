// frontend/src/components/index.js
// Export individual components
export { default as Layout } from './Layout/Layout';
export { default as Header } from './Layout/Header';
export { default as Sidebar } from './Layout/Sidebar';

// Charts
export { default as SeverityChart } from './charts/SeverityChart';
export { default as ScanHistoryChart } from './charts/ScanHistoryChart';

// Scans
export { default as ScanCard } from './scans/ScanCard';
export { default as ScanForm } from './scans/ScanForm';
export { default as ScanStatus } from './scans/ScanStatus';

// Findings
export { default as FindingCard } from './findings/FindingCard';
export { default as FindingList } from './findings/FindingList';
export { default as SeverityChip } from './findings/SeverityChip';

// AI
export { default as AIAnalysisCard } from './ai/AIAnalysisCard';
export { default as RemediationSteps } from './ai/RemediationSteps';

// Common
export { default as LoadingSpinner } from './common/LoadingSpinner';
export { default as ErrorAlert } from './common/ErrorAlert';
export { default as ConfirmDialog } from './common/ConfirmDialog';