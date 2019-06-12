import React, { Component } from 'react';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

// Placeholder
let id = 0;
function createData(item, stock) {
  id += 1;
  return { id, item, stock };
}

// const randomData = [
//   createData(2, 20),
//   createData(6, 62),
//   createData(1, 31),
// ];

class Tables extends Component {
  constructor(props) {
    super(props)
    this.state = {
      data: [],
    };
  }

  componentDidMount() {
    fetch('https://cors-anywhere.herokuapp.com/http://142.93.141.46:8000/api/products', {headers: {'Origin': '',}})
      .then(res => {return res.json()})
      .then(data => this.setState({ data }))
      .catch(error => {
        console.log("something bad happened somewhere, rollback!" + error);
      });
  }

  render() {
    return (
      <div>
        <Paper>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell> {this.props.id} </TableCell>
                <TableCell> {this.props.name} </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {
                this.state.data.map((row, index) => (
                  <TableRow key={index}>
                    {this.props.renderRow(row).map(item => <TableCell>{item}</TableCell>)}
                  </TableRow>
                ))
              }
            </TableBody>
          </Table>


          {/* Placeholder table */}
          {/* <Table>
            <TableHead>
              <TableRow>
                <TableCell align="right">ID</TableCell>
                <TableCell align="right">Item</TableCell>
                <TableCell align="right">Stock</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {randomData.map(row => (
                <TableRow>
                  <TableCell align="right">{row.id}</TableCell>
                  <TableCell align="right">{row.item}</TableCell>
                  <TableCell align="right">{row.stock}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table> */}
        </Paper>
      </div>
    )
  }
}

export default Tables

