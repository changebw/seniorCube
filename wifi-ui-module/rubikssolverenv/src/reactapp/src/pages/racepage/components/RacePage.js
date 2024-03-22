import React from "react";
import "./RacePage.css"
// import MyChart from "./Chart";

class RacePage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      // receiving: false,
      yourTime: "0:00",
      robotTime: "0:00",
    };
  }

  componentDidMount() {
    this.startFetch();
  }

  componentWillUnmount() {
    // Clear interval when component unmounts to prevent memory leaks
    clearInterval(this.interval);
  }

  startFetch = () => {
    console.log("called start fetch");
    fetch('/startTimerConnection');
    this.interval = setInterval(this.fetchData, 900);
    // .then(response => {
    //   if (!response.ok) {
    //     throw new Error("Failed to start time fetching");
    //   }
    //   this.interval = setInterval(this.fetchData, 900);
    //   return response.json();
    // })
  }

  fetchData = () => {
    fetch('/getTime')
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed with not ok');
        }
        console.log("getting next time..");
        return response.json();
      })
      .then(data => {
        this.setState({
          // receiving: true,
          yourTime: data.yourTime,
          robotTime: data.robotTime,
        });
      })
      .catch(error => {
        console.error('Error fetching data', error);
      });
  };

  render() {
    return (
      <div id="RacePage" className="RacePage">
        {/* <button>Start</button> */}
        <h4>Your Time</h4>
        <h2 id="yourTime">{this.state.yourTime}</h2>
        <h4>Robot's Time</h4>
        <h2>{this.state.robotTime}</h2>
      </div>
    );
  }
}



// class RacePage extends React.Component{

//     interval = setInterval(this.fetchData, 5000);
//     fetchData() {
//       fetch('/getTime')
//       .then(response => {
//         if (!response.ok) {
//           throw new Error('Failed with not ok')
//         }
//         return response.json();
//       })
//       .then(data => {
//         console.log("Received Data is:", data);
//       })
//       .catch(error => {
//         console.error('Error fetching data', error);
//       })
//     }

//     render () { return <div id="RacePage" className="RacePage">
//                         <h4>
//                           Your Time
//                         </h4>
//                         <h2 id="yourTime">0:00</h2>
//                         <h4>
//                           Robot's Time
//                         </h4>
//                         <h2>0:00</h2>
//                        </div>

//     }
//     // render() { return <div id="RacePage" className="RacePage">
//     //                     <div className="plotsContainer">
//     //                       <MyChart
//     //                         plotTitle={"Your Time"}
//     //                       />
//     //                       <MyChart
//     //                         plotTitle={"Robot's Time"}
//     //                       />
//     //                     </div>
//     //                     <h2>Place hands on sensor</h2>
//     //                   </div>
//     // };

// }

export default RacePage;