import React from "react";
import "./RacePage.css"

class RacePage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
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
        <h1>Your Time</h1>
        <h1 id="yourTime">{this.state.yourTime}</h1>
        <h1>Robot's Time</h1>
        <h1>{this.state.robotTime}</h1>
      </div>
    );
  }
}

export default RacePage;