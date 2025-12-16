package com.yourorg.project.service;

import org.springframework.stereotype.Service;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.file.Paths;
import java.util.stream.Collectors;

@Service
public class PythonAgentService {

    private static final String AGENTS_DIR = "../automation/agents/";

    public String runAgent(String scriptName, String argument) {
        try {
            // Construct the full path to the script
            // Assuming the server is running from the 'server' directory
            String scriptPath = Paths.get(AGENTS_DIR, scriptName).toString();

            ProcessBuilder processBuilder = new ProcessBuilder("python", scriptPath, argument);
            processBuilder.redirectErrorStream(true);

            Process process = processBuilder.start();

            try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
                String output = reader.lines().collect(Collectors.joining("\n"));
                int exitCode = process.waitFor();

                if (exitCode != 0) {
                    throw new RuntimeException("Python script failed with exit code " + exitCode + ": " + output);
                }

                return output;
            }
        } catch (Exception e) {
            throw new RuntimeException("Failed to run python script: " + e.getMessage(), e);
        }
    }

    public String parseInput(String text) {
        return runAgent("parser.py", text);
    }

    public String assessRisk(String jsonInput) {
        return runAgent("risk_engine.py", jsonInput);
    }

    public String generateSanction(String jsonInput) {
        return runAgent("generate_sanction.py", jsonInput);
    }
}
