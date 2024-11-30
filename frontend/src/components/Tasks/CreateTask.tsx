import React, { useState } from 'react';
import { Box, TextField, Button, Alert } from '@mui/material';
import api from '../../services/api';
import { Task } from '../../types';

interface CreateTaskProps {
  onTaskCreated: (task: Task) => void;
}

const CreateTask: React.FC<CreateTaskProps> = ({ onTaskCreated }) => {
  const [n, setN] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const nValue = parseInt(n);
      const response = await api.post('/tasks', { n: nValue });
      onTaskCreated(response.data);
      setN('');
      setError('');
    } catch (err: any) {
      setError(err.response?.data?.error || 'An error occurred');
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mb: 4 }}>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <Box sx={{ display: 'flex', gap: 2 }}>
        <TextField
          label="N"
          type="number"
          value={n}
          onChange={(e) => setN(e.target.value)}
          inputProps={{ min: 1, max: 1000000 }}
          required
          sx={{ flexGrow: 1 }}
        />
        <Button type="submit" variant="contained">
          Calculate
        </Button>
      </Box>
    </Box>
  );
};

export default CreateTask; 