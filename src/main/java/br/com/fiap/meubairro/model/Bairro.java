package br.com.fiap.meubairro.model;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public record Bairro(
        Long id,
        @NotBlank(message = "nome é obrigatório") @Size(max = 100) String nome,
        @NotBlank(message = "cidade é obrigatória") @Size(max = 100) String cidade,
        @NotBlank(message = "uf é obrigatória") @Size(min = 2, max = 2, message = "uf deve ter 2 letras") String uf,
        @NotNull(message = "populacao é obrigatória") @Min(value = 0, message = "populacao não pode ser negativa") Integer populacao
) {
}
