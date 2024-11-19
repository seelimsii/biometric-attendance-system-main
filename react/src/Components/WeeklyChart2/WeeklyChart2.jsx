import React from 'react'
import { Doughnut } from 'react-chartjs-2'
import './WeeklyChart2.css'
const WeeklyChart2 = (prop) => {
    const sourceData = prop.data
  return (
    <div className='card weekly-chart2-card'>
      <div className='dashboard-headings'>Total Weekly Hours</div>
            <Doughnut
                data={{
                    labels: sourceData.map((data) => data.label),
                    datasets: [{
                        label: 'Hours',
                        data: sourceData.map((data) => data.value),
                        backgroundColor: [
                            "rgba(247, 146, 25, 1)",
                            "rgba(0, 114, 188, 1)"

                        ],
                        circumference:180,
                        rotation:-90
                    }]
                }} />
    </div>
  )
}

export default WeeklyChart2
