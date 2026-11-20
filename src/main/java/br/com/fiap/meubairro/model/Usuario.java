package br.com.fiap.meubairro.model;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public record Usuario(
        Long id,
        @NotBlank(message = "nome é obrigatório") @Size(max = 100) String nome,
        @NotBlank(message = "email é obrigatório") @Email(message = "email inválido") @Size(max = 150) String email,
        @NotNull(message = "perfil é obrigatório (MORADOR ou ADMIN)") Perfil perfil,
        Long bairroId
) {
}
