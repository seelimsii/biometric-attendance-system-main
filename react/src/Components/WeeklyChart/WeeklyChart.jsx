import React from 'react'
import './WeeklyChart.css'
import { Bar } from 'react-chartjs-2'
const WeeklyChart = (props) => {
const sourceData=props.data
  return (
    <div className='weekly-chart-card card' >
    <div className='dashboard-headings'>Weekly Hours</div>
      <Bar
      data={{
        labels:sourceData.map((data)=>data.label),
        datasets:[{
            label:'Hours',
            data:sourceData.map((data)=>data.value),
            backgroundColor:["rgba(247, 146, 25, 1)"],
            borderRadius:5
        }]
      }}/>
    </div>
  )
}

export default WeeklyChart
