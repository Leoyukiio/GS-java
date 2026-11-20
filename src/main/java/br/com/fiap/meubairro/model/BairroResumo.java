package br.com.fiap.meubairro.model;

import java.math.BigDecimal;

public record BairroResumo(
        Bairro bairro,
        IndicadorBairro indicadores,
        BigDecimal nota,
        Integer posicao
) {
}
