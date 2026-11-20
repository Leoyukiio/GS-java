package br.com.fiap.meubairro.dao;

import br.com.fiap.meubairro.model.Perfil;
import br.com.fiap.meubairro.model.Usuario;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.jdbc.support.KeyHolder;
import org.springframework.stereotype.Repository;

import java.sql.PreparedStatement;
import java.sql.Types;
import java.util.List;
import java.util.Optional;

@Repository
public class UsuarioDao {

    private static final RowMapper<Usuario> MAPPER = (rs, i) -> {
        long bairro = rs.getLong("id_bairro");
        return new Usuario(rs.getLong("id_usuario"), rs.getString("nome"), rs.getString("email"),
                Perfil.valueOf(rs.getString("perfil")), rs.wasNull() ? null : bairro);
    };

    private final JdbcTemplate jdbc;

    public UsuarioDao(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    public Usuario inserir(Usuario u) {
        KeyHolder kh = new GeneratedKeyHolder();
        jdbc.update(con -> {
            PreparedStatement ps = con.prepareStatement(
                    "INSERT INTO tb_mb_usuario (nome, email, perfil, id_bairro) VALUES (?, ?, ?, ?)",
                    new String[]{"ID_USUARIO"});
            ps.setString(1, u.nome());
            ps.setString(2, u.email().toLowerCase());
            ps.setString(3, u.perfil().name());
            if (u.bairroId() == null) ps.setNull(4, Types.NUMERIC); else ps.setLong(4, u.bairroId());
            return ps;
        }, kh);
        return buscarPorId(kh.getKey().longValue()).orElseThrow();
    }

    public List<Usuario> listar() {
        return jdbc.query("SELECT * FROM tb_mb_usuario ORDER BY nome", MAPPER);
    }

    public Optional<Usuario> buscarPorId(Long id) {
        return jdbc.query("SELECT * FROM tb_mb_usuario WHERE id_usuario = ?", MAPPER, id).stream().findFirst();
    }

    public boolean existeEmail(String email, Long ignorarId) {
        Integer n = jdbc.queryForObject(
                "SELECT COUNT(*) FROM tb_mb_usuario WHERE email = ? AND id_usuario <> ?",
                Integer.class, email.toLowerCase(), ignorarId == null ? -1L : ignorarId);
        return n != null && n > 0;
    }

    public int atualizar(Long id, Usuario u) {
        return jdbc.update("UPDATE tb_mb_usuario SET nome = ?, email = ?, perfil = ?, id_bairro = ? WHERE id_usuario = ?",
                u.nome(), u.email().toLowerCase(), u.perfil().name(), u.bairroId(), id);
    }

    public int remover(Long id) {
        return jdbc.update("DELETE FROM tb_mb_usuario WHERE id_usuario = ?", id);
    }

    public boolean temDependentes(Long id) {
        Integer n = jdbc.queryForObject(
                "SELECT (SELECT COUNT(*) FROM tb_mb_reporte WHERE id_usuario = ?) + (SELECT COUNT(*) FROM tb_mb_voto WHERE id_usuario = ?) FROM dual",
                Integer.class, id, id);
        return n != null && n > 0;
    }
}
