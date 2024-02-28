import './App.css';

import {Route, Routes} from 'react-router-dom';


import Header from './components/Header';
import Navbar from './components/Navbar';
import RacePage from './pages/racepage/components/RacePage';
import SolvePage from './pages/solvepage/components/SolvePage';
import LearnPage from './pages/learnpage/components/LearnPage';
import AboutPage from './pages/aboutpage/components/AboutPage';

function App() {
  return <div id="main" className="main">
          <div>
            <Header />
            <Navbar />
          </div>
          <div>
            <Routes>
              <Route path="/" element={<SolvePage/>}/>
              <Route path="/race" element={<RacePage/>}/>
              <Route path="/learn" element={<LearnPage/>}/>
              <Route path="/about" element={<AboutPage/>}/>
            </Routes>
          </div>
        </div>;
}

export default App;