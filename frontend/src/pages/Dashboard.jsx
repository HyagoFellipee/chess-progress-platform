import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Alert,
  CircularProgress,
} from '@mui/material';
import { Add, History, TrendingUp, Psychology } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext.jsx';
import { analysisAPI } from '../services/api.jsx';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const [analyses, setAnalyses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [newAnalysis, setNewAnalysis] = useState({
    chess_username: '',
    end_date: '',
    game_mode: 'rapid',
  });
  const [createLoading, setCreateLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchAnalyses();
  }, []);

  const fetchAnalyses = async () => {
    try {
      const response = await analysisAPI.getMyAnalyses();
      setAnalyses(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching analyses:', error);
      setError('Failed to load analyses');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateAnalysis = async () => {
    setCreateLoading(true);
    setError('');

    try {
      const response = await analysisAPI.createAnalysis(newAnalysis);
      setAnalyses(prev => [response.data, ...prev]);
      setCreateDialogOpen(false);
      setNewAnalysis({
        chess_username: '',
        end_date: '',
        game_mode: 'rapid',
      });
    } catch (error) {
      console.error('Error creating analysis:', error);
      setError(error.response?.data?.message || 'Failed to create analysis');
    } finally {
      setCreateLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'success';
      case 'processing': return 'warning';
      case 'failed': return 'error';
      default: return 'default';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed': return <TrendingUp />;
      case 'processing': return <CircularProgress size={16} />;
      case 'failed': return <Psychology />;
      default: return <History />;
    }
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            Welcome back, {user?.username}!
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Track your chess evolution and compare with your opponents
          </Typography>
        </Box>
        <Button onClick={logout} variant="outlined">
          Logout
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={4}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Typography variant="h3" color="primary">
              {user?.total_analyses || 0}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Total Analyses
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Typography variant="h3" color="success.main">
              {analyses.filter(a => a.status === 'completed').length}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Completed
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Typography variant="h3" color="warning.main">
              {analyses.filter(a => a.status === 'processing').length}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Processing
            </Typography>
          </Paper>
        </Grid>
      </Grid>

      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h5" component="h2">
          Your Analyses
        </Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => setCreateDialogOpen(true)}
        >
          New Analysis
        </Button>
      </Box>

      {analyses.length === 0 ? (
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <Psychology sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
          <Typography variant="h6" gutterBottom>
            No analyses yet
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Create your first analysis to start tracking your chess evolution!
          </Typography>
          <Button
            variant="contained"
            startIcon={<Add />}
            onClick={() => setCreateDialogOpen(true)}
          >
            Create First Analysis
          </Button>
        </Paper>
      ) : (
        <Grid container spacing={3}>
          {analyses.map((analysis) => (
            <Grid item xs={12} md={6} lg={4} key={analysis.id}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                    <Typography variant="h6" component="h3">
                      {analysis.chess_username}
                    </Typography>
                    <Chip
                      icon={getStatusIcon(analysis.status)}
                      label={analysis.status}
                      color={getStatusColor(analysis.status)}
                      size="small"
                    />
                  </Box>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Mode: {analysis.game_mode.charAt(0).toUpperCase() + analysis.game_mode.slice(1)}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Until: {new Date(analysis.end_date).toLocaleDateString()}
                  </Typography>
                  {analysis.status === 'completed' && (
                    <Box sx={{ mt: 2 }}>
                      <Typography variant="body2">
                        Position: <strong>{analysis.user_position_in_ranking}</strong> of {analysis.total_opponents}
                      </Typography>
                      <Typography variant="body2">
                        Percentile: <strong>{analysis.percentile?.toFixed(1)}%</strong>
                      </Typography>
                    </Box>
                  )}
                </CardContent>
                <CardActions>
                  <Button size="small" disabled={analysis.status !== 'completed'}>
                    View Details
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      <Dialog 
        open={createDialogOpen} 
        onClose={() => setCreateDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Create New Analysis</DialogTitle>
        <DialogContent>
          <TextField
            margin="normal"
            required
            fullWidth
            label="Chess.com Username"
            value={newAnalysis.chess_username}
            onChange={(e) => setNewAnalysis(prev => ({ ...prev, chess_username: e.target.value }))}
            helperText="Your username on Chess.com"
          />
          <TextField
            margin="normal"
            required
            fullWidth
            label="End Date"
            type="date"
            value={newAnalysis.end_date}
            onChange={(e) => setNewAnalysis(prev => ({ ...prev, end_date: e.target.value }))}
            InputLabelProps={{ shrink: true }}
            helperText="Analyze opponents until this date"
          />
          <TextField
            margin="normal"
            required
            fullWidth
            select
            label="Game Mode"
            value={newAnalysis.game_mode}
            onChange={(e) => setNewAnalysis(prev => ({ ...prev, game_mode: e.target.value }))}
          >
            <MenuItem value="rapid">Rapid</MenuItem>
            <MenuItem value="blitz">Blitz</MenuItem>
            <MenuItem value="bullet">Bullet</MenuItem>
            <MenuItem value="daily">Daily</MenuItem>
          </TextField>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateDialogOpen(false)}>Cancel</Button>
          <Button 
            onClick={handleCreateAnalysis}
            variant="contained"
            disabled={createLoading || !newAnalysis.chess_username || !newAnalysis.end_date}
          >
            {createLoading ? <CircularProgress size={24} /> : 'Create Analysis - $5.00'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default Dashboard;
