import React, { useState, useRef, useEffect } from 'react';
import { Box, TextField, IconButton, Paper, Typography, Avatar } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import AttachFileIcon from '@mui/icons-material/AttachFile';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import PersonIcon from '@mui/icons-material/Person';

interface Message {
    id: number;
    text: string;
    sender: 'user' | 'agent';
}

interface ChatAreaProps {
    onSendMessage: (text: string) => void;
    onFileUpload?: (file: File) => void;
    messages: Message[];
}

export default function ChatArea({ onSendMessage, onFileUpload, messages }: ChatAreaProps) {
    const [input, setInput] = useState('');
    const messagesEndRef = useRef<null | HTMLDivElement>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = () => {
        if (!input.trim()) return;
        onSendMessage(input);
        setInput('');
    };

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files[0]) {
            if (onFileUpload) {
                onFileUpload(event.target.files[0]);
            }
        }
    };

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%', overflow: 'hidden' }}>
            {/* Message List */}
            <Box sx={{ flexGrow: 1, overflowY: 'auto', p: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
                {messages.map((msg) => (
                    <Box
                        key={msg.id}
                        sx={{
                            display: 'flex',
                            justifyContent: msg.sender === 'user' ? 'flex-end' : 'flex-start',
                            alignItems: 'flex-start',
                            gap: 1
                        }}
                    >
                        {msg.sender === 'agent' && <Avatar sx={{ bgcolor: 'primary.main' }}><SmartToyIcon /></Avatar>}
                        <Paper
                            elevation={1}
                            sx={{
                                p: 2,
                                maxWidth: '70%',
                                bgcolor: msg.sender === 'user' ? 'primary.main' : 'grey.100',
                                color: msg.sender === 'user' ? 'white' : 'text.primary',
                                borderRadius: 2
                            }}
                        >
                            <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>{msg.text}</Typography>
                        </Paper>
                        {msg.sender === 'user' && <Avatar sx={{ bgcolor: 'secondary.main' }}><PersonIcon /></Avatar>}
                    </Box>
                ))}
                <div ref={messagesEndRef} />
            </Box>

            {/* Input Area */}
            <Box sx={{ p: 2, bgcolor: 'background.paper', borderTop: 1, borderColor: 'divider' }}>
                <Box sx={{ display: 'flex', gap: 1 }}>
                    <input
                        type="file"
                        hidden
                        ref={fileInputRef}
                        onChange={handleFileChange}
                    />
                    <IconButton color="primary" onClick={() => fileInputRef.current?.click()}>
                        <AttachFileIcon />
                    </IconButton>
                    <TextField
                        fullWidth
                        placeholder="Type your message..."
                        variant="outlined"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                    />
                    <IconButton color="primary" onClick={handleSend} size="large">
                        <SendIcon />
                    </IconButton>
                </Box>
            </Box>
        </Box>
    );
}
