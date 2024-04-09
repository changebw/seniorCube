import React from "react";
import "./RacePage.css"

class RacePage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      scrambleMoves: "",
      yourTime: "00:00",
      robotTime: "00:00",
    };
  }

  componentDidMount() {
    
  }

  componentWillUnmount() {
    // Clear interval when component unmounts to prevent memory leaks
    clearInterval(this.interval);
  }

  scrambleSetup = () => {
    fetch('/getScramble')
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed with not ok');
        }
        return response.json();
      })
      .then(data => {
        this.setState({
          scrambleMoves: data.scrambleMoves
        })
        let msg = document.getElementById('scramble-string');
        msg.textContent = data.scrambleMoves;
      })
      .catch(error => {
        console.log("Error fetching data",error);
      });
  }

  startFetch = () => {
    console.log("called start fetch");
    fetch('/sendSolve');
    setTimeout(function(){
      fetch('/startTimerConnection');
      this.interval = setInterval(this.fetchData, 900);
    }, 10000);
    let msg = document.getElementById('scramble-string');
    msg.textContent = "Place hands on sensors and release to start timer";
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
        <div id="titletext-container">
          <div>
            <h4 id="scramble-title">Scramble String: </h4>
            <h4 id="scramble-string"> </h4>
          </div>
          <h4 id="scramble-string">Click here to scramble robot's cube!</h4>
          <button id="btn-start-race" onClick={this.scrambleSetup}>Get scramble</button>
        </div>
        <h1>Your Time</h1>
        <h1 id="yourTime">{this.state.yourTime}</h1>
        <h1>Robot's Time</h1>
        <h1>{this.state.robotTime}</h1>
        <button id="btn-start-race" onClick={this.startFetch}>Start</button>
      </div>
    );
  }
}

export default RacePage;