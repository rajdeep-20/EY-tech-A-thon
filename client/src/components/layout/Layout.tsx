import React from 'react';
import { Box, AppBar, Toolbar, Typography, Drawer, List, ListItem, ListItemButton, ListItemText, Avatar, CssBaseline } from '@mui/material';
import DashboardIcon from '@mui/icons-material/Dashboard';
import HistoryIcon from '@mui/icons-material/History';
import SettingsIcon from '@mui/icons-material/Settings';

const drawerWidth = 240;
const rightDrawerWidth = 300;

interface LayoutProps {
    children: React.ReactNode;
    rightPanel: React.ReactNode;
}

export default function Layout({ children, rightPanel }: LayoutProps) {
    return (
        <Box sx={{ display: 'flex' }}>
            <CssBaseline />

            {/* Header */}
            <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
                <Toolbar>
                    <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
                        Tata Capital Loan Assistant
                    </Typography>
                    <Avatar sx={{ bgcolor: 'secondary.main' }}>U</Avatar>
                </Toolbar>
            </AppBar>

            {/* Left Sidebar (Navigation) */}
            <Drawer
                variant="permanent"
                sx={{
                    width: drawerWidth,
                    flexShrink: 0,
                    [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
                }}
            >
                <Toolbar />
                <Box sx={{ overflow: 'auto' }}>
                    <List>
                        {['New Loan', 'History', 'Settings'].map((text, index) => (
                            <ListItem key={text} disablePadding>
                                <ListItemButton>
                                    <ListItemText primary={text} />
                                </ListItemButton>
                            </ListItem>
                        ))}
                    </List>
                </Box>
            </Drawer>

            {/* Main Content (Chat) */}
            <Box component="main" sx={{ flexGrow: 1, p: 3, height: '100vh', display: 'flex', flexDirection: 'column' }}>
                <Toolbar />
                {children}
            </Box>

            {/* Right Sidebar (Agent Monitor) */}
            <Drawer
                variant="permanent"
                anchor="right"
                sx={{
                    width: rightDrawerWidth,
                    flexShrink: 0,
                    [`& .MuiDrawer-paper`]: { width: rightDrawerWidth, boxSizing: 'border-box' },
                }}
            >
                <Toolbar />
                {rightPanel}
            </Drawer>
        </Box>
    );
}
