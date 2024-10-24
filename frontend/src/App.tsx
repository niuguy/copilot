import { BrowserRouter as Router } from 'react-router-dom';
import { UsageDashboard } from './components/dashboard/usage-dashboard';

function App() {
  return (
    <Router>
      <div style={{ width: '100%', height: '100vh' }}>
        <UsageDashboard />
      </div>
    </Router>
  );
}

export default App;
