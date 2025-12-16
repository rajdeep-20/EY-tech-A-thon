package com.yourorg.project.controller;

import com.yourorg.project.service.PythonAgentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/loan")
@CrossOrigin(origins = "http://localhost:5173") // Allow frontend access
public class LoanController {

    @Autowired
    private PythonAgentService pythonAgentService;

    @PostMapping("/parse")
    public ResponseEntity<String> parseInput(@RequestBody String text) {
        try {
            String result = pythonAgentService.parseInput(text);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body("{\"error\": \"" + e.getMessage() + "\"}");
        }
    }

    @PostMapping("/assess")
    public ResponseEntity<String> assessRisk(@RequestBody String jsonInput) {
        try {
            String result = pythonAgentService.assessRisk(jsonInput);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body("{\"error\": \"" + e.getMessage() + "\"}");
        }
    }

    @PostMapping("/sanction")
    public ResponseEntity<String> generateSanction(@RequestBody String jsonInput) {
        try {
            String result = pythonAgentService.generateSanction(jsonInput);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body("{\"error\": \"" + e.getMessage() + "\"}");
        }
    }
}
