import { BrowserRouter as Router } from 'react-router-dom';
import { UsageDashboard } from './components/dashboard/usage-dashboard';

function App() {
  return (
    <Router>
      <div style={{ display: 'flex', justifyContent: 'center', width: '100%' }}>
        <UsageDashboard />
      </div>
    </Router>
  );
}

export default App;
