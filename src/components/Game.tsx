'use client';

import { useEffect, useState } from 'react';
import Grid from './Grid';
import GameOver from './GameOver';
import { initGrid, move, isGameOver } from '../lib/gameLogic';
import styles from '../styles/Game.module.css';

export default function Game() {
  const [grid, setGrid] = useState<number[][]>([]);
  const [score, setScore] = useState(0);
  const [gameOver, setGameOver] = useState(false);

  useEffect(() => {
    resetGame();
  }, []);

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (gameOver) return;

      if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(event.key)) {
        event.preventDefault();
        const { newGrid, newScore, moved } = move(grid, score, event.key);
        if (moved) {
          setGrid(newGrid);
          setScore(newScore);
          if (isGameOver(newGrid)) {
            setGameOver(true);
          }
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [grid, score, gameOver]);

  const resetGame = () => {
    const newGrid = initGrid();
    setGrid(newGrid);
    setScore(0);
    setGameOver(false);
  };

  return (
    <div className={styles.gameContainer}>
      <div className={styles.scoreContainer}>Score: {score}</div>
      <Grid grid={grid} />
      {gameOver && <GameOver onReset={resetGame} />}
    </div>
  );
} 