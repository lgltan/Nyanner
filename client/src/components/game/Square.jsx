const Square = ({ index, piece, onDragStart, onDragEnd, onDrop }) => {
    const handleMouseUp = () => {
      onDragEnd();
    };
  
    const handleMouseMove = (e) => {
      e.preventDefault(); // Prevent text selection
      onDragEnd();
    };
  
    return (
      <div
        className={`square ${piece ? 'occupied' : ''}`}
        onMouseDown={onDragStart}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onDragOver={onDrop}
        draggable={!!piece}
      >
        {piece ? piece : ''}
      </div>
    );
  };
  