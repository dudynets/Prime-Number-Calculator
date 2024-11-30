import React, { useEffect, useState } from 'react';
import { Container, Typography } from '@mui/material';
import CreateTask from './CreateTask';
import TaskItem from './TaskItem';
import api from '../../services/api';
import { Task } from '../../types';

const TaskList: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);

  const fetchTasks = async () => {
    try {
      const response = await api.get('/tasks');
      setTasks(response.data);
    } catch (error) {
      console.error('Error fetching tasks:', error);
    }
  };

  const handleNewTask = (task: Task) => {
    setTasks(prev => [task, ...prev]);
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  useEffect(() => {
    const pollActiveTasks = () => {
      tasks.forEach(task => {
        if (task.status === 'waiting' || task.status === 'running') {
          api.get(`/tasks/${task.id}`).then(response => {
            setTasks(prev => prev.map(t => 
              t.id === task.id ? response.data : t
            ));
          });
        }
      });
    };

    const interval = setInterval(pollActiveTasks, 1000);
    return () => clearInterval(interval);
  }, [tasks]);

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" sx={{ mb: 4 }}>
        Find Nth prime number:
      </Typography>
      <CreateTask onTaskCreated={handleNewTask} />
      {tasks.sort((a, b) => b.id - a.id).map(task => (
        <TaskItem 
          key={task.id} 
          task={task} 
          onTaskUpdate={fetchTasks}
        />
      ))}
    </Container>
  );
};

export default TaskList; 