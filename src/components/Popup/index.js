import React, { Component } from 'react';
import Button from '@material-ui/core/Button';
import Popupreact from "reactjs-popup";
import {Line} from 'react-chartjs-2';
import { relative } from 'path';
import Tables from '../table';



class Popup extends Component {
    constructor(props) {
      super(props)
      this.state = {
        data: [],
        key: 1,
      };
    }

    
    componentDidMount() {
        fetch(`https://cors-anywhere.herokuapp.com/http://142.93.141.46:8000/api/sales/predict/${this.state.key}`, {headers: {'Origin': '',}})
          .then(res => {return res.json()})
          .then(res => {
            console.log(res)
            return res  
          })
          .then(res => this.setState({
            data: {
              labels: ['t-4', 't-3', 't-2', 't-1', 't', 't+1'],
              datasets: [
                {
                  label: 'Prediction',
                  fill: false,
                  lineTension: 0.1,
                  backgroundColor: 'rgba(75,192,192,0.4)',
                  borderColor: 'rgba(75,192,192,1)',
                  borderCapStyle: 'butt',
                  borderDash: [],
                  borderDashOffset: 0.0,
                  borderJoinStyle: 'miter',
                  pointBorderColor: 'rgba(75,192,192,1)',
                  pointBackgroundColor: '#fff',
                  pointBorderWidth: 1,
                  pointHoverRadius: 5,
                  pointHoverBackgroundColor: 'rgba(75,192,192,1)',
                  pointHoverBorderColor: 'rgba(220,220,220,1)',
                  pointHoverBorderWidth: 2,
                  pointRadius: 1,
                  pointHitRadius: 10,
                  data:[24,18,18,21,19]
                }
              ]
            }
          }))
          .catch(error => {
            console.log("something bad happened somewhere, rollback!" + error);
          })
      }
      

    render(){
        return(
            <Popupreact  closeOnDocumentClick modal={true} trigger={<Button variant="contained" color="primary">Prediction</Button>}>
            <div>
            <h2></h2>
              <Line data={this.state.data} />

            </div>
            </Popupreact>
        )
    }
}
export default Popup