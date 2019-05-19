import React from 'react';
import './Navbar.css';

const Navbar: React.FC = () => {
  return (
    <div className="Navbar--container">
      <a href="/" className="Navbar--item Navbar--item-active">Dashboard</a>
    </div>
  );
}

export default Navbar;
