import React from "react";
import ReactApexChart from "react-apexcharts";

// class MyChart extends React.Component {
//   constructor(props) {
//     super(props);

//     this.state = {
//       options: {
//         chart: {
//           id: "realtime",
//           type: 'line',
//           animations: {
//             enabled: true,
//             easing: 'linear',
//             dynamicAnimation: {
//                 speed: 1000
//             }
//           }
//         },
//         toolbar: {
//             show: false
//         },
//         zoom: {
//             enabled: false
//         },
//         dataLabels: {
//             enabled: false
//         },
//         stroke: {
//             curve: 'smooth'
//         },
//         title: {
//             text: 'Dynamic updating chart',
//             align: 'left'
//         },
//         xaxis: {
//           categories: [0,1,2]
//         }
//       },
//       series: [
//         {
//           name: "series-1",
//           data: [1,2,3]
//         }
//       ]
//     };
//   }

//   // getNewSeries = ({min, max}) => {
//   //   const newDataPoint = Math.random() * (max - min) + min;
//   //   const newData = [...this.state.series[0].data, newDataPoint].slice(-8);
//   //   return newData.map(() => Math.random() * (max - min) + min);
//   // };

//   getNewCategories = () => {
//     const axiss = this.state.options.xaxis.categories;
//     const newCats = axiss.map(value => Number(value) + 1);
//     console.log(axiss);
//     return newCats;
//   };

//   componentDidMount() {
//     window.setInterval(() => {
//       const { min, max } = {
//         min: 10,
//         max: 90
//       };

//       // const newData = this.getNewSeries({ min, max });
//       const newCats = this.getNewCategories();
//       const newData = newCats.map(() => Math.random() * (max - min) + min);

//       this.setState(prevState => ({
//         series: [{
//           data: newData
//         }],
//         options: {
//           ...prevState.options,
//           xaxis: {
//             ...prevState.options.xaxis,
//             categories: newCats
//           }
//         }
//       }));
//     }, 2000);
//   }

//   render() {
//     return (
//       <div className="app">
//         <div className="row">
//           <div className="mixed-chart">
//             <Chart
//               options={this.state.options}
//               series={this.state.series}
//               type="line"
//               width="500"
//             />
//           </div>
//         </div>
//       </div>
//     );
//   }
// }

const XAXISRANGE = 10;

class MyChart extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
    
      series: [{
        data: []
      }],
      options: {
        chart: {
          id: 'realtime',
          height: 350,
          type: 'line',
          animations: {
            enabled: true,
            easing: 'linear',
            dynamicAnimation: {
              speed: 1000
            }
          },
          toolbar: {
            show: false
          },
          zoom: {
            enabled: false
          }
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: 'smooth'
        },
        title: {
          text: 'Dynamic Updating Chart',
          align: 'left'
        },
        markers: {
          size: 0
        },
        xaxis: {
          type: 'datetime',
          range: XAXISRANGE,
        },
        yaxis: {
          max: 100
        },
        legend: {
          show: false
        },
      },
    
    
    };
  }

  getNewSeries(lastDate, range) {
    const newDataPoint = {
      x: lastDate + 1000, // Assuming data point every second
      y: Math.floor(Math.random() * (range.max - range.min + 1)) + range.min,
    };
  
    return [newDataPoint];
  }


  componentDidMount() {
    const updateInterval = 1000; // milliseconds
    let lastDate = Date.now() - (XAXISRANGE * 1000);
  
    window.setInterval(() => {
      const newData = this.getNewSeries(lastDate, {
        min: 10,
        max: 90
      });
  
      lastDate = newData[newData.length - 1].x;
  
      this.setState({
        series: [{
          data: newData
        }]
      });
    }, updateInterval);
  }  


  render() {
    return (
      <div>
        <div id="chart">
          <ReactApexChart options={this.state.options} series={this.state.series} type="line" height={350} />
        </div>
        <div id="html-dist"></div>
      </div>
    );
  }
}

export default MyChart