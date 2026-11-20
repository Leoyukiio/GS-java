package br.com.fiap.meubairro.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
public class HomeController {
    @GetMapping("/")
    public Map<String, String> home() {
        return Map.of("api", "Meu Bairro - CitizenTech", "status", "ok", "docs", "/swagger-ui.html");
    }
}
