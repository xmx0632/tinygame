export function initGrid(): number[][] {
  const grid = Array(4).fill(0).map(() => Array(4).fill(0));
  addNewTile(grid);
  addNewTile(grid);
  return grid;
}

export function addNewTile(grid: number[][]): void {
  const emptyCells = [];
  for (let i = 0; i < 4; i++) {
    for (let j = 0; j < 4; j++) {
      if (grid[i][j] === 0) {
        emptyCells.push({ x: i, y: j });
      }
    }
  }
  if (emptyCells.length > 0) {
    const { x, y } = emptyCells[Math.floor(Math.random() * emptyCells.length)];
    grid[x][y] = Math.random() < 0.9 ? 2 : 4;
  }
}

export function move(grid: number[][], score: number, direction: string): {
  newGrid: number[][];
  newScore: number;
  moved: boolean;
} {
  const newGrid = grid.map(row => [...row]);
  let newScore = score;
  let moved = false;

  const moveAndMerge = (line: number[]): number[] => {
    // 移除0
    let newLine = line.filter(cell => cell !== 0);
    
    // 合并相同的数字
    for (let i = 0; i < newLine.length - 1; i++) {
      if (newLine[i] === newLine[i + 1]) {
        newLine[i] *= 2;
        newScore += newLine[i];
        newLine.splice(i + 1, 1);
      }
    }
    
    // 补充0
    while (newLine.length < 4) {
      newLine.push(0);
    }
    
    return newLine;
  };

  // 根据方向处理移动
  if (direction === 'ArrowLeft') {
    for (let i = 0; i < 4; i++) {
      const oldRow = [...newGrid[i]];
      newGrid[i] = moveAndMerge(newGrid[i]);
      if (!moved && newGrid[i].some((val, idx) => val !== oldRow[idx])) {
        moved = true;
      }
    }
  } else if (direction === 'ArrowRight') {
    for (let i = 0; i < 4; i++) {
      const oldRow = [...newGrid[i]];
      newGrid[i] = moveAndMerge([...newGrid[i]].reverse()).reverse();
      if (!moved && newGrid[i].some((val, idx) => val !== oldRow[idx])) {
        moved = true;
      }
    }
  } else if (direction === 'ArrowUp') {
    for (let j = 0; j < 4; j++) {
      const column = newGrid.map(row => row[j]);
      const oldColumn = [...column];
      const newColumn = moveAndMerge(column);
      for (let i = 0; i < 4; i++) {
        if (!moved && newColumn[i] !== oldColumn[i]) {
          moved = true;
        }
        newGrid[i][j] = newColumn[i];
      }
    }
  } else if (direction === 'ArrowDown') {
    for (let j = 0; j < 4; j++) {
      const column = newGrid.map(row => row[j]).reverse();
      const oldColumn = [...column];
      const newColumn = moveAndMerge(column).reverse();
      for (let i = 0; i < 4; i++) {
        if (!moved && newColumn[i] !== oldColumn[i]) {
          moved = true;
        }
        newGrid[i][j] = newColumn[i];
      }
    }
  }

  if (moved) {
    addNewTile(newGrid);
  }

  return { newGrid, newScore, moved };
}

export function isGameOver(grid: number[][]): boolean {
  // 检查是否有空格
  for (let i = 0; i < 4; i++) {
    for (let j = 0; j < 4; j++) {
      if (grid[i][j] === 0) return false;
    }
  }

  // 检查是否可以合并
  for (let i = 0; i < 4; i++) {
    for (let j = 0; j < 4; j++) {
      if (j < 3 && grid[i][j] === grid[i][j + 1]) return false;
      if (i < 3 && grid[i][j] === grid[i + 1][j]) return false;
    }
  }
  return true;
} 