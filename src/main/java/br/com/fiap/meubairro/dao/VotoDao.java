package br.com.fiap.meubairro.dao;

import br.com.fiap.meubairro.model.Voto;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.jdbc.support.KeyHolder;
import org.springframework.stereotype.Repository;

import java.sql.PreparedStatement;
import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public class VotoDao {

    private static final RowMapper<Voto> MAPPER = (rs, i) -> new Voto(rs.getLong("id_voto"),
            rs.getLong("id_reporte"), rs.getLong("id_usuario"), rs.getTimestamp("criado_em").toLocalDateTime());

    private final JdbcTemplate jdbc;

    public VotoDao(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    public Voto inserir(Long reporteId, Long usuarioId) {
        KeyHolder kh = new GeneratedKeyHolder();
        jdbc.update(con -> {
            PreparedStatement ps = con.prepareStatement(
                    "INSERT INTO tb_mb_voto (id_reporte, id_usuario, criado_em) VALUES (?, ?, ?)",
                    new String[]{"ID_VOTO"});
            ps.setLong(1, reporteId);
            ps.setLong(2, usuarioId);
            ps.setTimestamp(3, Timestamp.valueOf(LocalDateTime.now()));
            return ps;
        }, kh);
        return buscarPorId(kh.getKey().longValue()).orElseThrow();
    }

    public Optional<Voto> buscarPorId(Long id) {
        return jdbc.query("SELECT * FROM tb_mb_voto WHERE id_voto = ?", MAPPER, id).stream().findFirst();
    }

    public List<Voto> listarPorReporte(Long reporteId) {
        return jdbc.query("SELECT * FROM tb_mb_voto WHERE id_reporte = ? ORDER BY criado_em", MAPPER, reporteId);
    }

    public boolean existe(Long reporteId, Long usuarioId) {
        Integer n = jdbc.queryForObject(
                "SELECT COUNT(*) FROM tb_mb_voto WHERE id_reporte = ? AND id_usuario = ?",
                Integer.class, reporteId, usuarioId);
        return n != null && n > 0;
    }

    public int remover(Long reporteId, Long usuarioId) {
        return jdbc.update("DELETE FROM tb_mb_voto WHERE id_reporte = ? AND id_usuario = ?", reporteId, usuarioId);
    }

    public int removerPorReporte(Long reporteId) {
        return jdbc.update("DELETE FROM tb_mb_voto WHERE id_reporte = ?", reporteId);
    }
}
