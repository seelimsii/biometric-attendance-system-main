import React from 'react'
import { Doughnut } from 'react-chartjs-2'
import './TodaysHoursChart.css'
const TodaysHoursChart = (prop) => {
    const sourceData = prop.data
    return (
        <div className='card today-chart-card'>
            <div className='dashboard-headings'>Todays Hours</div>
            <Doughnut
                data={{
                    labels: sourceData.map((data) => data.label),
                    datasets: [{
                        label: 'Hours',
                        data: sourceData.map((data) => data.value),
                        backgroundColor: [
                            "rgba(247, 146, 25, 1)",
                            "rgba(0, 114, 188, 1)"

                        ]
                    }]
                }} />
        </div>
    )
}

export default TodaysHoursChart
