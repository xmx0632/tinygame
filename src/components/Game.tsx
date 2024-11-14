'use client';

import { useEffect, useState, TouchEvent } from 'react';
import Grid from './Grid';
import GameOver from './GameOver';
import { initGrid, move, isGameOver } from '../lib/gameLogic';
import styles from '../styles/Game.module.css';

export default function Game() {
  const [grid, setGrid] = useState<number[][]>([]);
  const [score, setScore] = useState(0);
  const [gameOver, setGameOver] = useState(false);
  const [touchStart, setTouchStart] = useState<{ x: number; y: number } | null>(null);

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

  const handleTouchStart = (e: TouchEvent) => {
    const touch = e.touches[0];
    setTouchStart({
      x: touch.clientX,
      y: touch.clientY
    });
  };

  const handleTouchEnd = (e: TouchEvent) => {
    if (!touchStart || gameOver) return;

    const touch = e.changedTouches[0];
    const deltaX = touch.clientX - touchStart.x;
    const deltaY = touch.clientY - touchStart.y;
    const minSwipeDistance = 30; // 最小滑动距离

    // 确定主要的滑动方向
    if (Math.abs(deltaX) > Math.abs(deltaY)) {
      // 水平滑动
      if (Math.abs(deltaX) > minSwipeDistance) {
        const direction = deltaX > 0 ? 'ArrowRight' : 'ArrowLeft';
        const { newGrid, newScore, moved } = move(grid, score, direction);
        if (moved) {
          setGrid(newGrid);
          setScore(newScore);
          if (isGameOver(newGrid)) {
            setGameOver(true);
          }
        }
      }
    } else {
      // 垂直滑动
      if (Math.abs(deltaY) > minSwipeDistance) {
        const direction = deltaY > 0 ? 'ArrowDown' : 'ArrowUp';
        const { newGrid, newScore, moved } = move(grid, score, direction);
        if (moved) {
          setGrid(newGrid);
          setScore(newScore);
          if (isGameOver(newGrid)) {
            setGameOver(true);
          }
        }
      }
    }

    setTouchStart(null);
  };

  const handleTouchMove = (e: TouchEvent) => {
    // 防止页面滚动
    e.preventDefault();
  };

  const resetGame = () => {
    const newGrid = initGrid();
    setGrid(newGrid);
    setScore(0);
    setGameOver(false);
  };

  return (
    <div 
      className={styles.gameContainer}
      onTouchStart={handleTouchStart}
      onTouchEnd={handleTouchEnd}
      onTouchMove={handleTouchMove}
    >
      <div className={styles.scoreContainer}>Score: {score}</div>
      <Grid grid={grid} />
      {gameOver && <GameOver onReset={resetGame} />}
    </div>
  );
} 