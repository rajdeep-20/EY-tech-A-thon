import { useState, useEffect, useRef } from 'react'
import Layout from './components/layout/Layout'
import AgentPanel from './components/AgentPanel'
import ChatArea from './components/ChatArea'
import BankDetailsDialog from './components/BankDetailsDialog'

interface Message {
    id: number;
    text: string;
    sender: 'user' | 'agent';
}

function App() {
    const [stage, setStage] = useState('SALES');
    const [messages, setMessages] = useState<Message[]>([
        { id: 1, text: "Hello! I am your Loan Assistant. How can I help you today?", sender: 'agent' }
    ]);
    const [isBankDialogOpen, setIsBankDialogOpen] = useState(false);
    const userId = useRef(`user_${Date.now()}`).current;

    const addMessage = (text: string, sender: 'user' | 'agent') => {
        setMessages(prev => [...prev, { id: Date.now(), text, sender }]);
    };

    const determineStage = (message: string) => {
        const lowerMsg = message.toLowerCase();
        if (lowerMsg.includes("upload") || lowerMsg.includes("documents")) {
            setStage('VERIFICATION');
        } else if (lowerMsg.includes("approved") || lowerMsg.includes("sanctioned")) {
            setStage('SANCTION');
        } else if (lowerMsg.includes("unfortunately") || lowerMsg.includes("cannot approve")) {
            setStage('COMPLETED'); // Or FAILED
        } else if (lowerMsg.includes("welcome") || lowerMsg.includes("help")) {
            setStage('SALES');
        }
    };

    const handleSendMessage = async (text: string) => {
        addMessage(text, 'user');

        try {
            const response = await fetch('http://localhost:8081/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ userId, message: text })
            });
            const data = await response.json();
            const agentResponse = data.response;

            addMessage(agentResponse, 'agent');
            determineStage(agentResponse);

        } catch (error) {
            addMessage("Sorry, I'm having trouble connecting to the server.", 'agent');
        }
    };

    const handleFileUpload = async (file: File) => {
        addMessage(`Uploaded: ${file.name}`, 'user');

        const formData = new FormData();
        formData.append('file', file);
        formData.append('userId', userId);

        try {
            const response = await fetch('http://localhost:8081/api/upload', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            const agentResponse = data.response;

            addMessage(agentResponse, 'agent');
            determineStage(agentResponse);

            // If verification successful, we might want to close the loop or ask for bank details if needed
            // But orchestrator handles it. 

        } catch (error) {
            addMessage("Error uploading file.", 'agent');
        }
    };

    const handleBankDetailsSubmit = (details: any) => {
        // For now, just log it and maybe send a message. 
        // The backend orchestrator currently triggers risk check on file upload.
        addMessage(`Bank Details Provided: Account ${details.accountNumber}`, 'user');
        setIsBankDialogOpen(false);
        // We could send this to the chat to be parsed if we wanted to enhance the backend later
    };

    return (
        <Layout rightPanel={<AgentPanel currentStage={stage} />}>
            <ChatArea
                messages={messages}
                onSendMessage={handleSendMessage}
                onFileUpload={handleFileUpload}
            />
            <BankDetailsDialog
                open={isBankDialogOpen}
                onClose={() => setIsBankDialogOpen(false)}
                onSubmit={handleBankDetailsSubmit}
            />
        </Layout>
    )
}

export default App
