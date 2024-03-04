import React from "react";

import "./SolvePage.css"
import outputImg from "./output.bmp"

class SolvePage extends React.Component {

    async handleSubmit(e) {
        e.preventDefault();
        try {
            const csrfToken = document.head.querySelector('meta[name="csrf-token"]').content;
            const fetchString = "/" + e.target.id
            const response = await fetch(fetchString, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
            });

            if (response.ok) {
                console.log("success");
            } else {
                console.error('Failed to make connection');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }
    render() { return <div id="SolvePage" className="SolvePage">
                        <div className="ButtonContainer">
                        <form id="sendScramble" className="connForm" action="" onSubmit={this.handleSubmit}>
                            <button id="ScrambleButton">
                              <h2>Scramble</h2>
                            </button>
                          </form>
                          <form id="sendSolve" className="connForm" action="" onSubmit={this.handleSubmit}>
                            <button id="SolveButton">
                              <h2>Solve</h2>
                            </button>
                          </form>
                          <form id="takeNewPicture" className="connForm" action="" onSubmit={this.handleSubmit}>
                            <button id="PicButton">
                              <h2>Get pic</h2>
                            </button>
                          </form>
                          {/* <img src={`${outputImg}?t=${new Date().getTime()}`} alt="bub" /> */}
                        {/* <img src={`http://localhost:8000/${outputImg}`} alt="img would be here if it worked" /> */}
                        </div>
                      </div>
    }
}

export default SolvePage