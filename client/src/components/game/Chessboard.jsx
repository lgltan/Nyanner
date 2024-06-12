import React, { useState } from 'react';
import './chessboard.css';

const Chessboard = ({ width, height, updateData }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    if (updateData) {
      setData(updateData);
    }
  }, [updateData]);

  const squares = [];
  for (let i = 0; i < height; i++) {
    squares.push(
      <div className={`row ${i % 2 === 0? 'even' : 'odd'}`} key={i}>
        {data[i]?.color || ''}
      </div>
    );
  }

  return (
    <div className="chess-board" style={{ width, height }}>
      {squares}
    </div>
  );
};

export default Chessboard;
