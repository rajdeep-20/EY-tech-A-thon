import React, { useState } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, TextField, Button } from '@mui/material';

interface BankDetailsDialogProps {
    open: boolean;
    onClose: () => void;
    onSubmit: (details: any) => void;
}

export default function BankDetailsDialog({ open, onClose, onSubmit }: BankDetailsDialogProps) {
    const [accountNumber, setAccountNumber] = useState('');
    const [ifsc, setIfsc] = useState('');
    const [bankName, setBankName] = useState('');

    const handleSubmit = () => {
        onSubmit({ accountNumber, ifsc, bankName });
        onClose();
    };

    return (
        <Dialog open={open} onClose={onClose}>
            <DialogTitle>Enter Bank Details</DialogTitle>
            <DialogContent>
                <TextField
                    autoFocus
                    margin="dense"
                    label="Account Number"
                    fullWidth
                    variant="outlined"
                    value={accountNumber}
                    onChange={(e) => setAccountNumber(e.target.value)}
                />
                <TextField
                    margin="dense"
                    label="IFSC Code"
                    fullWidth
                    variant="outlined"
                    value={ifsc}
                    onChange={(e) => setIfsc(e.target.value)}
                />
                <TextField
                    margin="dense"
                    label="Bank Name"
                    fullWidth
                    variant="outlined"
                    value={bankName}
                    onChange={(e) => setBankName(e.target.value)}
                />
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>Cancel</Button>
                <Button onClick={handleSubmit} variant="contained">Submit</Button>
            </DialogActions>
        </Dialog>
    );
}
