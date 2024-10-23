import { BrowserRouter as Router } from 'react-router-dom';
import { UsageDashboard } from './components/dashboard/usage-dashboard';

function App() {
  return (
    <Router>
      <UsageDashboard />
    </Router>
  );
}

export default App;