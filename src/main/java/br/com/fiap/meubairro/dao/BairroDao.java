package br.com.fiap.meubairro.dao;

import br.com.fiap.meubairro.model.Bairro;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.jdbc.support.KeyHolder;
import org.springframework.stereotype.Repository;

import java.sql.PreparedStatement;
import java.util.List;
import java.util.Optional;

@Repository
public class BairroDao {

    private static final RowMapper<Bairro> MAPPER = (rs, i) -> new Bairro(
            rs.getLong("id_bairro"), rs.getString("nome"), rs.getString("cidade"),
            rs.getString("uf"), rs.getInt("populacao"));

    private final JdbcTemplate jdbc;

    public BairroDao(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    public Bairro inserir(Bairro b) {
        KeyHolder kh = new GeneratedKeyHolder();
        jdbc.update(con -> {
            PreparedStatement ps = con.prepareStatement(
                    "INSERT INTO tb_mb_bairro (nome, cidade, uf, populacao) VALUES (?, ?, ?, ?)",
                    new String[]{"ID_BAIRRO"});
            ps.setString(1, b.nome());
            ps.setString(2, b.cidade());
            ps.setString(3, b.uf().toUpperCase());
            ps.setInt(4, b.populacao());
            return ps;
        }, kh);
        return buscarPorId(kh.getKey().longValue()).orElseThrow();
    }

    public List<Bairro> listar() {
        return jdbc.query("SELECT * FROM tb_mb_bairro ORDER BY nome", MAPPER);
    }

    public Optional<Bairro> buscarPorId(Long id) {
        return jdbc.query("SELECT * FROM tb_mb_bairro WHERE id_bairro = ?", MAPPER, id).stream().findFirst();
    }

    public boolean existeNomeNaCidade(String nome, String cidade, Long ignorarId) {
        Integer n = jdbc.queryForObject(
                "SELECT COUNT(*) FROM tb_mb_bairro WHERE UPPER(nome) = UPPER(?) AND UPPER(cidade) = UPPER(?) AND id_bairro <> ?",
                Integer.class, nome, cidade, ignorarId == null ? -1L : ignorarId);
        return n != null && n > 0;
    }

    public int atualizar(Long id, Bairro b) {
        return jdbc.update("UPDATE tb_mb_bairro SET nome = ?, cidade = ?, uf = ?, populacao = ? WHERE id_bairro = ?",
                b.nome(), b.cidade(), b.uf().toUpperCase(), b.populacao(), id);
    }

    public int remover(Long id) {
        return jdbc.update("DELETE FROM tb_mb_bairro WHERE id_bairro = ?", id);
    }

    public boolean temDependentes(Long id) {
        Integer n = jdbc.queryForObject(
                "SELECT (SELECT COUNT(*) FROM tb_mb_reporte WHERE id_bairro = ?) + (SELECT COUNT(*) FROM tb_mb_usuario WHERE id_bairro = ?) FROM dual",
                Integer.class, id, id);
        return n != null && n > 0;
    }
}
