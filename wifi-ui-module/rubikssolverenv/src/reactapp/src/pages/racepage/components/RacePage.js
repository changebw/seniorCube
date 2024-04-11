import React from "react";
import "./RacePage.css"

let hour = 0;
let minute = 0;
let second = 0;
let count = 0;
let timer = false;

class RacePage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      scrambleMoves: "",
      yourTime: "00:00",
      robotTime: "00:00",
    };
    this.stopWatch = this.stopWatch.bind(this);
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
    setTimeout(() => {
      fetch('/startTimerConnection');
      this.interval = setInterval(this.fetchData, 900);
      timer = true;
      this.stopWatch();
    }, 2000);
    let msg = document.getElementById('scramble-string');
    msg.textContent = "Place hands on sensors and release to start timer";
  }

  stopWatch = () => { 
    if (timer) { 
        count++; 
  
        if (count === 100) { 
            second++; 
            count = 0; 
        } 
  
        if (second === 60) { 
            minute++; 
            second = 0; 
        } 
  
        if (minute === 60) { 
            hour++; 
            minute = 0; 
            second = 0; 
        } 
  
        let hrString = hour; 
        let minString = minute; 
        let secString = second; 
        let countString = count; 
  
        if (hour < 10) { 
            hrString = "0" + hrString; 
        } 
  
        if (minute < 10) { 
            minString = "0" + minString; 
        } 
  
        if (second < 10) { 
            secString = "0" + secString; 
        } 
  
        if (count < 10) { 
            countString = "0" + countString; 
        } 
  
        // document.getElementById('hr').innerHTML = hrString; 
        // document.getElementById('min').innerHTML = minString; 
        // document.getElementById('sec').innerHTML = secString; 
        // document.getElementById('count').innerHTML = countString;
        console.log(hour + " " + minute + " " + second); 
        setTimeout(this.stopWatch, 10); 
    } 
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