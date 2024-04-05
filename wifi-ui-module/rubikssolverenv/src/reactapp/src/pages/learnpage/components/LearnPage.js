import React from "react";
import "./LearnPage.css"

class LearnPage extends React.Component{
    constructor(props) {
      super(props);
      this.state = {
        moves: "",
        curr_move: "",
      };
    }

    // startLearnModeConnection Takes pictures with cam1, cam2, and starts continuous connection with motors ESP.
    startLearnConn = () => {
      console.log("called start learn mode");
      fetch('/startLearnModeConnection')
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed with not ok');
          }
          return response.json();
        })
        .then(data => {
          this.setState({
            moves: data.moves,
            curr_move: data.curr_move,
          });
        })
        .catch(error => {
          console.error('Error fetching data', error);
        });
    }

    getMove = () => {
      console.log("called getMove");
      fetch('/sendMove')
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed with not ok');
          }
          return response.json();
        })
        .then(data => {
          this.setState({
            moves: data.moves,
            curr_move: data.curr_move,
          });
        })
        .catch(error => {
          console.error('Error fetching data', error);
        });
    }

    render() { 
      return <div id="LearnPage" className="LearnPage">
          <div className="instruction-container">
            <h1 className="instruction">Move String:</h1>
            <h2 id="move-string">{this.state.moves}</h2>
          </div>
          <div>
            <h1>Current move:</h1>
            <h1>{this.state.curr_move}</h1>
          </div>
          <div className="btnHolder">
            <button 
              id="btn-start-learn"
              onClick={this.startLearnConn}
            >Start</button>
            <button 
              id="btn-next-move"
              onClick={this.getMove}
            >Next</button>
          </div>
        </div>
    };

}

export default LearnPage;