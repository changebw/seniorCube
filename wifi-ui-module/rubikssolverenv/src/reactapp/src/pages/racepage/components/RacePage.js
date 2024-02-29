import React from "react";
import "./RacePage.css"
import MyChart from "./Chart";

class RacePage extends React.Component{
    render() { return <div id="RacePage" className="RacePage">
                        <div className="plotsContainer">
                          <MyChart
                            plotTitle={"Your Time"}
                          />
                          <MyChart
                            plotTitle={"Robot's Time"}
                          />
                        </div>
                        <h2>Place hands on sensor</h2>
                      </div>
    };

}

export default RacePage;