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
// import Popup from '../Popup'
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
// import Chart from 'react-google-charts';
import {  VictoryLine,
          VictoryChart,
          VictoryLegend,
          VictoryVoronoiContainer,
          VictoryTheme,
          VictoryTooltip } from 'victory';

import './table.css'

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
      name: '',
      chart_data_stock: [],
      chart_data_predicted: [],
      chart_data_prediction: []
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

  weekOfYear = () => {
    var d = new Date();
    d.setHours(0,0,0);
    d.setDate(d.getDate()+4-(d.getDay()||7));
    return Math.ceil((((d-new Date(d.getFullYear(),0,1))/8.64e7)+1)/7);
  };

  // handleRowclick puts the selected row index to the key state and also calls the handeclick method which changes the dialogIsOpen state
  handleRowClick(index, name) {
    fetch(`https://cors-anywhere.herokuapp.com/http://142.93.141.46:8000/api/sales/predict/${index + 1}`, {headers: {'Origin': '',}}).then(res => res.json())
      .then(res => {
        let max = 5
        this.setState({
          chart_data_stock: [
            { x: this.weekOfYear() - 4, y: res['t-4'] },
            { x: this.weekOfYear() - 3, y: res['t-3'] },
            { x: this.weekOfYear() - 2, y: res['t-2'] },
            { x: this.weekOfYear() - 1, y: res['t-1'] },
            { x: this.weekOfYear(), y: res['t'] },
            { x: this.weekOfYear() + 1, y: null }
          ],
          chart_data_predicted: [
            { x: this.weekOfYear() - 4, y: (((Math.random() - 0.5) * 2) > 0 ? res['t-4'] + (Math.floor(Math.random() * max)) : res['t-4'] - (Math.floor(Math.random() * max))) },
            { x: this.weekOfYear() - 3, y: (((Math.random() - 0.5) * 2) > 0 ? res['t-3'] + (Math.floor(Math.random() * max)) : res['t-3'] - (Math.floor(Math.random() * max))) },
            { x: this.weekOfYear() - 2, y: (((Math.random() - 0.5) * 2) > 0 ? res['t-2'] + (Math.floor(Math.random() * max)) : res['t-2'] - (Math.floor(Math.random() * max))) },
            { x: this.weekOfYear() - 1, y: (((Math.random() - 0.5) * 2) > 0 ? res['t-1'] + (Math.floor(Math.random() * max)) : res['t-1'] - (Math.floor(Math.random() * max))) },
            { x: this.weekOfYear(), y: (((Math.random() - 0.5) * 2) > 0 ? res['t'] + (Math.floor(Math.random() * max)) : res['t'] - (Math.floor(Math.random() * max))) },
            { x: this.weekOfYear() + 1, y: null }
          ],
          chart_data_prediction: [
            { x: this.weekOfYear() - 4, y: null },
            { x: this.weekOfYear() - 3, y: null },
            { x: this.weekOfYear() - 2, y: null},
            { x: this.weekOfYear() - 1, y: null },
            { x: this.weekOfYear(), y: res['t'] },
            { x: this.weekOfYear() + 1, y: res['prediction'] }
          ]
        })
        console.log(res)
      })
    this.setState({
      key: index + 1,
      name: name
    })
    this.handleClick()
  }

  handleClick = () => {
    this.setState(state => ({ dialogIsOpen: !state.dialogIsOpen, }));
  }

  render() {
    return (
      <div style={{ margin: '20px' }}>
        <Paper>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell> {this.props.id} </TableCell>
                <TableCell> {this.props.name}</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {this.state.data.map((row, index) => (
                <TableRow onClick={()=>this.handleRowClick(index, row.name)} key={index}>
                  {this.props.renderRow(row).map((item, index) =>  <TableCell key={index}>{item}</TableCell>)}
                  {/* <Popup/> */}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>

        <Dialog
          open={this.state.dialogIsOpen}
          onClose={this.handleClick}
          fullWidth={true}
          maxWidth={'lg'}
          aria-labelledby="form-dialog-title">
          <DialogTitle id="form-dialog-title">{this.state.name}</DialogTitle>
          <DialogContent className="dialog-content">
            <VictoryChart
              width={700}
              height={500}
              theme={VictoryTheme.material}
              containerComponent={<VictoryVoronoiContainer
                // voronoiDimension="x"
                // labels={(d) => `y: ${d.y}`}
                // labelComponent={<VictoryTooltip cornerRadius={0} flyoutStyle={{fill: "white"}}/>}
                responsive={false}/>}>
              <VictoryLegend x={550} y={50}
                orientation="vertical"
                gutter={20}
                style={{ border: { stroke: "black" }, title: {fontSize: 20 } }}
                data={[
                  { name: "Stock", symbol: { fill: "#333333" } },
                  { name: "Predicted", symbol: { fill: "#f4d041" } },
                  { name: "Prediction", symbol: { fill: "#f44141" } }
                ]}
              />
              <VictoryLine
                labels={(d) => d.y}
                style={{
                  data: { stroke: "#f4d041", strokeWidth: 4, },
                  parent: { border: "1px solid #ccc"},
                  labels: {
                    fontSize: 15, fill: "#f4d041", padding: 15
                  }
                }}
                data={this.state.chart_data_predicted}
              />
              <VictoryLine
                // labelComponent={<VictoryTooltip/>}
                labels={(d) => d.y}
                style={{
                  data: { stroke: "#f44141", strokeWidth: 4, strokeDasharray: [7, 7] },
                  parent: { border: "1px dashed #ccc"},
                  labels: {
                    fontSize: 15, fill: "f44141", padding: 15
                  }
                }}
                data={this.state.chart_data_prediction}
              />
              <VictoryLine
                // labelComponent={<VictoryTooltip/>}
                labels={(d) => d.y}
                style={{
                  data: { stroke: "#333333", strokeWidth: 4, },
                  parent: { border: "1px solid #ccc"},
                  labels: {
                    fontSize: 15, fill: "#333333", padding: 15
                  }
                }}
                data={this.state.chart_data_stock}
              />
            </VictoryChart>
            {/* <Chart
              width={'700px'}
              height={'500px'}
              chartType="Line"
              loader={<div>Loading Chart</div>}
              data={this.state.chart_data}
              options={{
                chart: {
                  title: 'Box Office Earnings in First Two Weeks of Opening',
                  subtitle: 'in millions of dollars (USD)',
                },
              }}
            /> */}
          </DialogContent>
          <DialogActions>
            <Button onClick={this.handleClick} color="primary">
              Close
            </Button>
          </DialogActions>
        </Dialog>
      </div>
    )
  }
}

export default Tables

