package br.com.fiap.meubairro.model;

import jakarta.validation.constraints.NotNull;

import java.time.LocalDateTime;

public record Voto(
        Long id,
        Long reporteId,
        @NotNull(message = "usuarioId é obrigatório") Long usuarioId,
        LocalDateTime criadoEm
) {
}
