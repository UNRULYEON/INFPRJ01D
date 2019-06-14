import React, { Component } from 'react';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Button from '@material-ui/core/Button';
import Paper from '@material-ui/core/Paper';
import {Line} from 'react-chartjs-2';
import { relative } from 'path';
import Popup from '../Popup'

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
      pred: [],
      dialogIsOpen: false,
      key: 0,
    };
  }

  componentDidMount() {
    fetch('https://cors-anywhere.herokuapp.com/http://142.93.141.46:8000/api/products', {headers: {'Origin': '',}})
      .then(res => {return res.json()})
      .then(data => this.setState({ data }))
      .catch(error => {
        console.log("something bad happened somewhere, rollback!" + error);
      })
  }

  // handleRowclick puts the selected row index to the key state and also calls the handeclick method which changes the dialogIsOpen state
  handleRowClick(index) {
    this.setState({
      key: index,
    })
    this.handleClick()
  }

  handleClick = () => {
    this.setState(state => ({ dialogIsOpen: !state.dialogIsOpen, }));
  }

  render() {
    return (
      <div>
        <Paper>
          <Table>         
            <TableHead>
              <TableRow>
                <TableCell> {this.props.id} </TableCell>
                <TableCell> {this.props.name}</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {
                this.state.data.map((row, index) => (
                  <TableRow onClick={()=>this.handleRowClick(index)} key={index}>
                    {this.props.renderRow(row).map(item =>  <TableCell>{item}</TableCell>)}
                    <Popup/>
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
        {this.state.dialogIsOpen ? 

          console.log("open dialog with key: " + this.state.key) 
          
          : console.log("No Dialog")}
          {/* @dines als je in je component een knop maakt met 'sluiten' ofzo verander dan ook de state van dialogIsOpen, dit doe je door handleClick aan te roepen */}
      </div>
    )
  }
}

export default Tables

