package br.com.fiap.meubairro.config;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.core.io.ClassPathResource;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.nio.charset.StandardCharsets;

@Component
public class DatabaseInitializer implements ApplicationRunner {

    private static final Logger log = LoggerFactory.getLogger(DatabaseInitializer.class);

    private final JdbcTemplate jdbc;
    private final boolean habilitado;

    public DatabaseInitializer(JdbcTemplate jdbc, @Value("${app.db.init:true}") boolean habilitado) {
        this.jdbc = jdbc;
        this.habilitado = habilitado;
    }

    @Override
    public void run(ApplicationArguments args) throws IOException {
        if (!habilitado) return;

        Integer existe = jdbc.queryForObject(
                "SELECT COUNT(*) FROM user_tables WHERE table_name = 'TB_MB_BAIRRO'", Integer.class);
        if (existe == null || existe == 0) {
            log.info("Criando tabelas do Meu Bairro...");
            executar("schema.sql");
        }
        Integer bairros = jdbc.queryForObject("SELECT COUNT(*) FROM tb_mb_bairro", Integer.class);
        if (bairros != null && bairros == 0) {
            log.info("Carregando dados de exemplo...");
            executar("data.sql");
        }
    }

    private void executar(String arquivo) throws IOException {
        String sql = new String(new ClassPathResource(arquivo).getInputStream().readAllBytes(), StandardCharsets.UTF_8);
        for (String comando : sql.split(";\\s*\\n")) {
            String c = comando.trim();
            if (!c.isEmpty()) jdbc.execute(c.endsWith(";") ? c.substring(0, c.length() - 1) : c);
        }
    }
}
