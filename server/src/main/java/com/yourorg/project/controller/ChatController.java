package com.yourorg.project.controller;

import com.yourorg.project.service.LoanOrchestratorService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Map;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "http://localhost:5173")
public class ChatController {

    @Autowired
    private LoanOrchestratorService loanOrchestratorService;

    private static final String UPLOAD_DIR = "../automation/data/";

    @PostMapping("/chat")
    public ResponseEntity<Map<String, String>> chat(@RequestBody Map<String, String> payload) {
        String userId = payload.get("userId");
        String message = payload.get("message");

        String response = loanOrchestratorService.processMessage(userId, message);

        return ResponseEntity.ok(Map.of("response", response));
    }

    @PostMapping("/upload")
    public ResponseEntity<Map<String, String>> uploadFile(
            @RequestParam("file") MultipartFile file,
            @RequestParam("userId") String userId) {

        try {
            // Ensure directory exists
            Path uploadPath = Paths.get(UPLOAD_DIR);
            if (!Files.exists(uploadPath)) {
                Files.createDirectories(uploadPath);
            }

            // Save file
            String fileName = file.getOriginalFilename();
            Path filePath = uploadPath.resolve(fileName);
            Files.copy(file.getInputStream(), filePath, java.nio.file.StandardCopyOption.REPLACE_EXISTING);

            // Trigger Orchestrator
            String response = loanOrchestratorService.handleFileUpload(userId, filePath.toString());

            return ResponseEntity.ok(Map.of("response", response));

        } catch (IOException e) {
            return ResponseEntity.internalServerError().body(Map.of("error", "File upload failed: " + e.getMessage()));
        }
    }
}
