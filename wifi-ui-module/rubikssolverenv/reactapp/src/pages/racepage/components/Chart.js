import React from 'react';
import { useEffect, useState } from 'react';
import {
  Line,
  LineChart,
  XAxis,
  YAxis,
} from 'recharts';

let counter = 0;

const generateDummyData = () => {
  let obj = {
    name: counter+1,
    value: counter+1
  };
  let obj2 = {
    name: counter+2,
    value: counter+2
  };
  counter++;
  return [obj,obj2];
  // return Array.from({ length: 10 }, (_, index) => ({
  //   name: counter+1,
  //   value: index+1 // Generating random values for demonstration
  // }));
};

const MyChart = ({plotTitle}) => {
  
  let [data, setData] = useState([]);
  let [generating, setGenerating] = useState(false);

  useEffect(() => {
    
    let interval;
    if (generating){
      interval = setInterval(() => {
        setData(generateDummyData());
      }, 1000);
    }
    
    return () => {
      clearInterval(interval);
    }
    
  }, [generating]);

  const stopGenerate = () => {
    console.log("called");
    console.log(generating);
    setGenerating(false);
  };

  const startGenerate = () => {
    console.log("called start");
    console.log(generating);
    setGenerating(true);
  };

  return ( 
      <div className='plotContainer'>
        <h4>{plotTitle}</h4>
        <LineChart width={500} height={300} data={data}>
          <XAxis dataKey="name" />
          <YAxis />
          <Line dataKey="value" />
        </LineChart>
        {/* temp buttons for debugging*/}
        <button
          id='startGraph'
          className='graphButton'
          onClick={startGenerate}>
          Start
        </button>
        <button
          id="stopGraph"
          className='graphButton' 
          onClick={stopGenerate}>
          Stop
        </button>
      </div>
  );
}

export default MyChart;