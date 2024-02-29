import React from "react";
import './Header.css';

class Header extends React.Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handlePageUpdate(cmd,title,response) {
        console.log("Response: ",response);
        if (response.ok) {
            if (cmd === "makeConnection"){
                title.textContent = "Successfully connected!";
            }
            if (cmd === "closeConnection"){
                title.textContent = "Successfully disconnected!";
            }
        } else {
            title.textContent = "There was an error.";
        }
    }

    async handleSubmit(e) {
        e.preventDefault();
        console.log("clicked form submit");
        try {
            const csrfToken = document.head.querySelector('meta[name="csrf-token"]').content;
            const fetchString = "/" + e.target.id;
            const response = await fetch(fetchString, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
            });

            let title = document.getElementById("title");

            let cmd = fetchString.substring(1,fetchString.length+1)

            this.handlePageUpdate(cmd,title,response);

        } catch (error) {
            console.error('Error:', error);
        }
    }

    render() {
        return  <header className="Header">
                    <h2>Rubik's Cube Solver Control Center</h2>
                    <div className="ConnectionsContainer">
                        <div className="formsContainer">
                            <form id="makeConnection" className="connForm" action="" onSubmit={this.handleSubmit}>
                                <h4 id="title">No device detected</h4>
                                <button
                                onClick={this.handleClick}>
                                    Connect
                                </button>
                            </form>
                            <form id="closeConnection" className="connForm" action="" onSubmit={this.handleSubmit}>
                                <h4>Close</h4>
                                <button className="grayed">Close Connection</button>
                            </form>
                        </div>
                    </div>
                </header>;
    }

    handleClick() {
        console.log("clicked btn");
    }
}

export default Header;