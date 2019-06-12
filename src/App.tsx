import React from 'react';
import './App.css';

// Components
import Header from './components/header';
import Navbar from './components/navbar';
import Table from './components/table';

// let id = 0;
// function createData(id: number, item: number, stock: number) {
//   id += 1;
//   return { id, item, stock };
// }

// const rows = [
//   createData(1, 2, 20),
//   createData(2, 6, 62),
//   createData(3, 1, 31),
// ];

// const rowData = (row: { title: any; principalmaker: any; amountofpaintings: number; }) => [row.id, row.item, row.stock]

const data = [{
  id: 0,
  item: 26,
  stock: 50
},]

const rowData = (row: { id: number; name: string; stock: number; }) => [row.id, row.name, row.stock]

const App: React.FC = () => {
  return (
    <div className="App">
      <Header />
      <Table id="id" name="name" stock="stock" renderRow={rowData} data={data} />
      <Navbar />
    </div>
  );
}

export default App;
