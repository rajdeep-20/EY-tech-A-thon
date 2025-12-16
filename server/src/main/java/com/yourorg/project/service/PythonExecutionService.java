package com.yourorg.project.service;

import org.springframework.stereotype.Service;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.stream.Collectors;

@Service
public class PythonExecutionService {

    // Pointing to the existing agents directory
    private static final String AGENTS_DIR = "../automation/agents/";

    public String executeScript(String scriptName, String jsonInput) {
        try {
            String scriptPath = Paths.get(AGENTS_DIR, scriptName).toString();

            // Create temp file for input
            java.nio.file.Path tempInput = java.nio.file.Files.createTempFile("agent_input_", ".json");
            java.nio.file.Files.writeString(tempInput, jsonInput);

            // Pass temp file path as argument
            ProcessBuilder processBuilder = new ProcessBuilder("python", scriptPath,
                    tempInput.toAbsolutePath().toString());
            processBuilder.redirectErrorStream(true);

            Process process = processBuilder.start();

            try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
                String output = reader.lines().collect(Collectors.joining("\n"));
                int exitCode = process.waitFor();

                // Cleanup temp file
                try {
                    java.nio.file.Files.deleteIfExists(tempInput);
                } catch (Exception e) {
                }

                if (exitCode != 0) {
                    System.err.println("Script execution failed: " + output);
                    throw new RuntimeException("Python script execution failed with exit code " + exitCode);
                }

                return output;
            }
        } catch (Exception e) {
            throw new RuntimeException("Failed to execute python script: " + e.getMessage(), e);
        }
    }
}
