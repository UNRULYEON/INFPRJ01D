import React from 'react';
import './App.css';

// Components
import Header from './components/header';
import Navbar from './components/navbar';
import Table from './components/table';

const App: React.FC = () => {
  return (
    <div className="App">
      <Header />
      <Table />
      <Navbar />
    </div>
  );
}

export default App;
