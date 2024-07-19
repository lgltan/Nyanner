import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import bK from '../game/pieces/bK.png';

const Unauthorized = () => {
    const [unauthImg, setUnauthImg] = useState(bK);
    const navigate = useNavigate()

    return (
        <div className='unauthorized-container'
            style={{width: "50%", margin: " 160px auto", textAlign: "center"}}
        >
            <img src={unauthImg} alt="unauthorized" style={{margin: "auto"}}/>
            <h2 style={{margin: "-10px 0 30px 0"}}>Unauthorized</h2>
            <button className='primary-btn' onClick={() => navigate('/')}>Go Home</button>
        </div>
    );
}

export default Unauthorized;