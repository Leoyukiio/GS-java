package br.com.fiap.meubairro.dao;

import br.com.fiap.meubairro.model.IndicadorBairro;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public class IndicadorBairroDao {

    private static final RowMapper<IndicadorBairro> MAPPER = (rs, i) -> new IndicadorBairro(
            rs.getLong("id_indicador"), rs.getLong("id_bairro"), rs.getBigDecimal("infraestrutura"),
            rs.getBigDecimal("seguranca"), rs.getBigDecimal("servicos"), rs.getBigDecimal("lazer"));

    private final JdbcTemplate jdbc;

    public IndicadorBairroDao(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    public Optional<IndicadorBairro> buscarPorBairro(Long bairroId) {
        return jdbc.query("SELECT * FROM tb_mb_indicador_bairro WHERE id_bairro = ?", MAPPER, bairroId)
                .stream().findFirst();
    }

    public List<IndicadorBairro> listar() {
        return jdbc.query("SELECT * FROM tb_mb_indicador_bairro", MAPPER);
    }

    public void salvar(Long bairroId, IndicadorBairro in) {
        int n = jdbc.update(
                "UPDATE tb_mb_indicador_bairro SET infraestrutura = ?, seguranca = ?, servicos = ?, lazer = ? WHERE id_bairro = ?",
                in.infraestrutura(), in.seguranca(), in.servicos(), in.lazer(), bairroId);
        if (n == 0) {
            jdbc.update(
                    "INSERT INTO tb_mb_indicador_bairro (id_bairro, infraestrutura, seguranca, servicos, lazer) VALUES (?, ?, ?, ?, ?)",
                    bairroId, in.infraestrutura(), in.seguranca(), in.servicos(), in.lazer());
        }
    }

    public int removerPorBairro(Long bairroId) {
        return jdbc.update("DELETE FROM tb_mb_indicador_bairro WHERE id_bairro = ?", bairroId);
    }
}
