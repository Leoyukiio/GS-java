package br.com.fiap.meubairro.dao;

import br.com.fiap.meubairro.model.Categoria;
import br.com.fiap.meubairro.model.Reporte;
import br.com.fiap.meubairro.model.Status;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.jdbc.support.KeyHolder;
import org.springframework.stereotype.Repository;

import java.sql.PreparedStatement;
import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Repository
public class ReporteDao {

    private static final String SELECT = """
            SELECT r.*, (SELECT COUNT(*) FROM tb_mb_voto v WHERE v.id_reporte = r.id_reporte) AS votos
              FROM tb_mb_reporte r
            """;

    private static final RowMapper<Reporte> MAPPER = (rs, i) -> {
        Timestamp resolvido = rs.getTimestamp("resolvido_em");
        return new Reporte(rs.getLong("id_reporte"), rs.getLong("id_usuario"), rs.getLong("id_bairro"),
                Categoria.valueOf(rs.getString("categoria")), rs.getString("descricao"),
                rs.getDouble("latitude"), rs.getDouble("longitude"), Status.valueOf(rs.getString("status")),
                rs.getTimestamp("criado_em").toLocalDateTime(),
                resolvido == null ? null : resolvido.toLocalDateTime(), rs.getInt("votos"));
    };

    private final JdbcTemplate jdbc;

    public ReporteDao(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    public Reporte inserir(Reporte r) {
        KeyHolder kh = new GeneratedKeyHolder();
        jdbc.update(con -> {
            PreparedStatement ps = con.prepareStatement(
                    "INSERT INTO tb_mb_reporte (id_usuario, id_bairro, categoria, descricao, latitude, longitude, status, criado_em) "
                            + "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", new String[]{"ID_REPORTE"});
            ps.setLong(1, r.usuarioId());
            ps.setLong(2, r.bairroId());
            ps.setString(3, r.categoria().name());
            ps.setString(4, r.descricao());
            ps.setDouble(5, r.latitude());
            ps.setDouble(6, r.longitude());
            ps.setString(7, Status.ABERTO.name());
            ps.setTimestamp(8, Timestamp.valueOf(LocalDateTime.now()));
            return ps;
        }, kh);
        return buscarPorId(kh.getKey().longValue()).orElseThrow();
    }

    public List<Reporte> listar(Long bairroId, Status status, Categoria categoria) {
        StringBuilder sql = new StringBuilder(SELECT).append(" WHERE 1 = 1");
        List<Object> args = new ArrayList<>();
        if (bairroId != null) { sql.append(" AND r.id_bairro = ?"); args.add(bairroId); }
        if (status != null) { sql.append(" AND r.status = ?"); args.add(status.name()); }
        if (categoria != null) { sql.append(" AND r.categoria = ?"); args.add(categoria.name()); }
        sql.append(" ORDER BY r.criado_em DESC");
        return jdbc.query(sql.toString(), MAPPER, args.toArray());
    }

    public Optional<Reporte> buscarPorId(Long id) {
        return jdbc.query(SELECT + " WHERE r.id_reporte = ?", MAPPER, id).stream().findFirst();
    }

    public int atualizarDados(Long id, Reporte r) {
        return jdbc.update(
                "UPDATE tb_mb_reporte SET id_bairro = ?, categoria = ?, descricao = ?, latitude = ?, longitude = ? WHERE id_reporte = ?",
                r.bairroId(), r.categoria().name(), r.descricao(), r.latitude(), r.longitude(), id);
    }

    public int atualizarStatus(Long id, Status status) {
        Timestamp resolvido = status == Status.RESOLVIDO ? Timestamp.valueOf(LocalDateTime.now()) : null;
        return jdbc.update("UPDATE tb_mb_reporte SET status = ?, resolvido_em = ? WHERE id_reporte = ?",
                status.name(), resolvido, id);
    }

    public int remover(Long id) {
        return jdbc.update("DELETE FROM tb_mb_reporte WHERE id_reporte = ?", id);
    }
}
