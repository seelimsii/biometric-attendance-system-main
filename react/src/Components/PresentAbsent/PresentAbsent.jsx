import React from 'react'
import "./PresentAbsent.css"
const PresentAbsent = () => {
    return (
        <div className='card pa-card'>
            <div className='dashboard-headings'>This Month</div>
            <div className="pa-card-div">
                <div className="pa-div">
                    <div className="pa-text present">
                        Present
                    </div>
                    <div className="pa-number present">
                        18
                    </div>
                </div>
                <div className="vertical-line"></div>
                <div className="pa-div">
                    <div className="pa-text absent">
                        Absent
                    </div>
                    <div className="pa-number absent">
                        2
                    </div>
                </div>
            </div>
        </div>
    )
}

export default PresentAbsent
