package com.yourorg.project.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class LoanOrchestratorService {

    @Autowired
    private PythonExecutionService pythonExecutionService;

    private final Map<String, String> userSessionState = new ConcurrentHashMap<>();
    private final Map<String, String> userData = new ConcurrentHashMap<>(); // Store parsed data temporarily
    private final ObjectMapper objectMapper = new ObjectMapper();

    public String processMessage(String userId, String message) {
        String state = userSessionState.getOrDefault(userId, "GREETING");

        switch (state) {
            case "GREETING":
                userSessionState.put(userId, "COLLECTING_DATA");
                return "Welcome to Tata Capital Loan Assistant. Please tell me your name and the loan amount you are looking for.";

            case "COLLECTING_DATA":
                try {
                    String parsedJson = pythonExecutionService.executeScript("parser.py", message);
                    JsonNode jsonNode = objectMapper.readTree(parsedJson);

                    // Check if we got valid data
                    // parser.py returns "loan_amount" now, not "amount"
                    if (jsonNode.has("name") && jsonNode.has("loan_amount") && !jsonNode.get("name").isNull()) {
                        userData.put(userId, parsedJson); // Store the parsed JSON string
                        userSessionState.put(userId, "VERIFYING");
                        return "Thank you, " + jsonNode.get("name").asText() + ". I have noted your request for "
                                + jsonNode.get("loan_amount").asText()
                                + ". Please upload your documents (ID/Income Proof) to proceed.";
                    } else {
                        return "I couldn't quite catch that. Could you please state your name and loan amount clearly?";
                    }
                } catch (Exception e) {
                    return "Sorry, I had trouble understanding that. Please try again.";
                }

            case "VERIFYING":
                return "Please upload your documents using the attachment button to verify your application.";

            case "SANCTION":
                return "Your loan has already been sanctioned!";

            default:
                return "How can I help you?";
        }
    }

    public String handleFileUpload(String userId, String filePath) {
        String state = userSessionState.getOrDefault(userId, "GREETING");

        if ("VERIFYING".equals(state)) {
            try {
                // Retrieve stored user data
                String storedData = userData.get(userId);
                if (storedData == null) {
                    return "Error: User data not found. Please restart.";
                }

                JsonNode dataNode = objectMapper.readTree(storedData);
                // Add dummy credit history for the mock
                ((com.fasterxml.jackson.databind.node.ObjectNode) dataNode).put("credit_history_months", 24);
                // Add dummy credit score for Keras model
                ((com.fasterxml.jackson.databind.node.ObjectNode) dataNode).put("credit_score", 750);

                // Step 2: Assess Risk (using Keras Deep Learning model)
                String riskJson = pythonExecutionService.executeScript("risk_engine_keras.py", dataNode.toString());

                // Debug: Write raw output to file
                try (java.io.PrintWriter out = new java.io.PrintWriter("server_risk_output.txt")) {
                    out.println(riskJson);
                } catch (Exception e) {
                }

                JsonNode riskNode = objectMapper.readTree(riskJson);

                if ("APPROVED".equals(riskNode.get("decision").asText())) {
                    userSessionState.put(userId, "SANCTION");

                    // Generate Sanction Letter
                    // Sanction agent expects: {"name": ..., "amount": ..., "date": ...}
                    ((com.fasterxml.jackson.databind.node.ObjectNode) dataNode).put("date",
                            java.time.LocalDate.now().toString());

                    // Ensure amount is passed as "amount" for sanction letter, parser gave
                    // "loan_amount"
                    if (dataNode.has("loan_amount")) {
                        ((com.fasterxml.jackson.databind.node.ObjectNode) dataNode).put("amount",
                                dataNode.get("loan_amount").asInt());
                    }

                    String sanctionJson = pythonExecutionService.executeScript("generate_sanction.py",
                            dataNode.toString());
                    JsonNode sanctionNode = objectMapper.readTree(sanctionJson);

                    return "Verification Successful! Your loan is approved. You can download your sanction letter here: "
                            + sanctionNode.get("file_path").asText();
                } else {
                    userSessionState.put(userId, "GREETING"); // Reset
                    return "Verification Complete. Unfortunately, we cannot approve your loan at this time based on the risk assessment.";
                }

            } catch (Exception e) {
                e.printStackTrace();
                return "An error occurred during verification: " + e.getMessage();
            }
        } else {
            return "Please provide your details before uploading documents.";
        }
    }
}
