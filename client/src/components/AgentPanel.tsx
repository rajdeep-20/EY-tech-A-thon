import React from 'react';
import { Box, Typography, Paper, Chip, CircularProgress } from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';

interface AgentPanelProps {
    currentStage: string;
}

const agents = [
    { id: 'SALES', name: 'Sales Agent', role: 'Intent & Data Collection' },
    { id: 'VERIFICATION', name: 'Verification Agent', role: 'KYC & Documents' },
    { id: 'RISK', name: 'Risk Engine', role: 'Credit Assessment' },
    { id: 'SANCTION', name: 'Sanction Agent', role: 'Generate Letter' },
];

export default function AgentPanel({ currentStage }: AgentPanelProps) {
    const getStatus = (agentId: string) => {
        const stages = agents.map(a => a.id);
        const currentIndex = stages.indexOf(currentStage);
        const agentIndex = stages.indexOf(agentId);

        if (currentStage === 'FAILED' && agentIndex === currentIndex) return 'FAILED';
        if (agentIndex < currentIndex) return 'COMPLETED';
        if (agentIndex === currentIndex) return 'ACTIVE';
        return 'IDLE';
    };

    return (
        <Box sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
                Agent Orchestration
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                {agents.map((agent) => {
                    const status = getStatus(agent.id);
                    const isActive = status === 'ACTIVE';
                    const isCompleted = status === 'COMPLETED';
                    const isFailed = status === 'FAILED';

                    return (
                        <Paper
                            key={agent.id}
                            elevation={isActive ? 3 : 1}
                            sx={{
                                p: 2,
                                border: isActive ? '2px solid #1976d2' : isFailed ? '2px solid #d32f2f' : '1px solid #e0e0e0',
                                opacity: status === 'IDLE' ? 0.6 : 1,
                                display: 'flex',
                                flexDirection: 'column',
                                gap: 1,
                                transition: 'all 0.3s ease'
                            }}
                        >
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <Typography variant="subtitle1" fontWeight="bold">
                                    {agent.name}
                                </Typography>
                                {isCompleted && <CheckCircleIcon color="success" />}
                                {isFailed && <ErrorIcon color="error" />}
                                {isActive && <CircularProgress size={20} />}
                            </Box>
                            <Typography variant="body2" color="text.secondary">
                                {agent.role}
                            </Typography>
                            {isActive && (
                                <Chip label="Processing..." color="primary" size="small" variant="outlined" />
                            )}
                        </Paper>
                    );
                })}
            </Box>
        </Box>
    );
}
