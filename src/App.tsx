import React from 'react';
import './App.css';

// Components
import Header from './components/header';
import Navbar from './components/navbar';

const App: React.FC = () => {
  return (
    <div className="App">
      <Header />
      <Navbar />
    </div>
  );
}

export default App;
