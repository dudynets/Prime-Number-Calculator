import React from 'react';
import { Card, CardContent, Typography, LinearProgress, Button } from '@mui/material';
import { Task } from '../../types';
import api from '../../services/api';

interface TaskItemProps {
  task: Task;
  onTaskUpdate: () => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onTaskUpdate }) => {
  const handleCancel = async () => {
    try {
      await api.post(`/tasks/${task.id}/cancel`);
      onTaskUpdate();
    } catch (error) {
      console.error('Error canceling task:', error);
    }
  };

  const handleDelete = async () => {
    try {
      await api.delete(`/tasks/${task.id}`);
      onTaskUpdate();
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  const getTimeDuration = () => {
    if (!task.completed_at) return null;
    const start = new Date(task.created_at);
    const end = new Date(task.completed_at);
    const diff = (end.getTime() - start.getTime()) / 1000; // in seconds
    return `${diff.toFixed(2)} seconds`;
  };

  return (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Typography variant="h6">N: {task.n}</Typography>
        <Typography color="textSecondary">Status: {task.status}</Typography>
        
        {(task.status === 'waiting' || task.status === 'running') && (
          <>
            <LinearProgress variant="determinate" value={task.progress || 0} sx={{ my: 2 }} />
            <Typography>Progress: {task.progress || 0}%</Typography>
            <Button variant="contained" color="error" onClick={handleCancel} sx={{ mt: 1 }}>
              Cancel
            </Button>
          </>
        )}

        {task.status === 'done' && (
          <>
            <Typography>Result: {task.result}</Typography>
            <Typography>Time: {getTimeDuration()}</Typography>
            <Button variant="outlined" color="error" onClick={handleDelete} sx={{ mt: 1 }}>
              Delete
            </Button>
          </>
        )}

        {task.status === 'cancelled' && (
          <>
            <Button variant="outlined" color="error" onClick={handleDelete} sx={{ mt: 1 }}>
              Delete
            </Button>
          </>
        )}

        {task.status === 'error' && (
          <>
            <Typography color="error">Error: {task.error}</Typography>
            <Button variant="outlined" color="error" onClick={handleDelete} sx={{ mt: 1 }}>
              Delete
            </Button>
          </>
        )}
      </CardContent>
    </Card>
  );
};

export default TaskItem; 