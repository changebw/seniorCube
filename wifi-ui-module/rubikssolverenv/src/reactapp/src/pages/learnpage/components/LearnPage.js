import React from "react";
import "./LearnPage.css"

class LearnPage extends React.Component{
    constructor(props) {
      super(props);
      this.state = {
        solveMoves: "",
        currSolveMove: "",
        scrambleMoves: "",
        currScrambleMove: "",
      };
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
          let msg = document.getElementById('msg-to-user');
          msg.textContent = data.scrambleMoves;
        })
        .catch(error => {
          console.log("Error fetching data",error);
        });
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
            solveMoves: data.solveMoves,
            currSolveMove: data.currSolveMove,
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
            solveMoves: data.solveMoves,
            currSolveMove: data.currSolveMove,
          });
        })
        .catch(error => {
          console.error('Error fetching data', error);
        });
    }

    render() { 
      return <div id="LearnPage" className="LearnPage">
          <div className="instruction-container">
            <h1 className="instruction">Scramble String:</h1>
            <h2 id="move-string">{this.state.scrambleMoves}</h2>
          </div>
          <div className="instruction-container">
            <h1 className="instruction">Solve String:</h1>
            <h2 id="move-string">{this.state.solveMoves}</h2>
          </div>
          <div>
            <h1>Current solve move:</h1>
            <h1>{this.state.currSolveMove}</h1>
          </div>
          <div className="btnHolder">
            <button 
              id="btn-get-scramble"
              onClick={this.scrambleSetup}
            >Get scramble</button>
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