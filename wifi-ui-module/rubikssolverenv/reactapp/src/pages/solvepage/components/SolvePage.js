import React from "react";

import "./SolvePage.css"

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
                        </div>
                      </div>
    }
}

export default SolvePage