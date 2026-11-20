package br.com.fiap.meubairro.model;

import jakarta.validation.constraints.DecimalMax;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import java.time.LocalDateTime;

public record Reporte(
        Long id,
        @NotNull(message = "usuarioId é obrigatório") Long usuarioId,
        @NotNull(message = "bairroId é obrigatório") Long bairroId,
        @NotNull(message = "categoria é obrigatória") Categoria categoria,
        @NotBlank(message = "descricao é obrigatória")
        @Size(min = 10, max = 500, message = "descricao deve ter entre 10 e 500 caracteres") String descricao,
        @NotNull(message = "latitude é obrigatória") @DecimalMin("-90") @DecimalMax("90") Double latitude,
        @NotNull(message = "longitude é obrigatória") @DecimalMin("-180") @DecimalMax("180") Double longitude,
        Status status,
        LocalDateTime criadoEm,
        LocalDateTime resolvidoEm,
        Integer votos
) {
}
