package br.com.fiap.meubairro.model;

import jakarta.validation.constraints.DecimalMax;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotNull;

import java.math.BigDecimal;

public record IndicadorBairro(
        Long id,
        Long bairroId,
        @NotNull @DecimalMin("0") @DecimalMax("10") BigDecimal infraestrutura,
        @NotNull @DecimalMin("0") @DecimalMax("10") BigDecimal seguranca,
        @NotNull @DecimalMin("0") @DecimalMax("10") BigDecimal servicos,
        @NotNull @DecimalMin("0") @DecimalMax("10") BigDecimal lazer
) {
}
