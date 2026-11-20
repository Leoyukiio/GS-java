# Meu Bairro — API REST (CitizenTech · Global Solution 2026.2)

API em **Java 21 + Spring Boot 3** com banco **Oracle (FIAP)**. Moradores reportam problemas urbanos, vizinhos confirmam com voto, e os indicadores de cada bairro geram uma nota e um ranking.

## Arquitetura (padrão de aula)

```
controller  →  bo (regras de negócio)  →  dao (JDBC/SQL)  →  Oracle
     ↑              ↑
   model        exception (@RestControllerAdvice)
```

| Pacote | Conteúdo |
|---|---|
| `model` | `Bairro`, `Usuario`, `Reporte`, `Voto`, `IndicadorBairro`, `BairroResumo` + enums `Perfil`, `Categoria`, `Status` |
| `dao` | `BairroDao`, `UsuarioDao`, `ReporteDao`, `VotoDao`, `IndicadorBairroDao` (JdbcTemplate, SQL explícito) |
| `bo` | `BairroBO`, `UsuarioBO`, `ReporteBO`, `VotoBO` |
| `controller` | `BairroController`, `UsuarioController`, `ReporteController`, `HomeController` |
| `exception` | `RecursoNaoEncontradoException` (404), `RegraNegocioException` (422), `ConflitoException` (409), `GlobalExceptionHandler`, `ApiError` |

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | `/bairros` | Lista bairros |
| GET | `/bairros/{id}` | Detalhe com indicadores, nota e posição |
| POST | `/bairros` | Cria bairro |
| PUT | `/bairros/{id}` | Atualiza bairro |
| DELETE | `/bairros/{id}` | Remove (se não houver reportes/usuários) |
| GET / PUT | `/bairros/{id}/indicadores` | Consulta / define indicadores (0 a 10) |
| GET | `/ranking` | Ranking pela nota |
| GET | `/usuarios`, `/usuarios/{id}` | Consulta |
| POST | `/usuarios` | Cria usuário (e-mail único) |
| PUT | `/usuarios/{id}` | Atualiza |
| DELETE | `/usuarios/{id}` | Remove (se não tiver reportes/votos) |
| GET | `/reportes?bairroId=&status=&categoria=` | Lista com filtros |
| GET | `/reportes/{id}` | Detalhe |
| POST | `/reportes` | Cria (nasce `ABERTO`) |
| PUT | `/reportes/{id}` | Edita (não permitido se `RESOLVIDO`) |
| PUT | `/reportes/{id}/status` | Avança status (`{"status":"EM_ANDAMENTO","adminId":1}`), só ADMIN |
| DELETE | `/reportes/{id}` | Remove com seus votos |
| GET | `/reportes/{id}/votos` | Lista votos |
| POST | `/reportes/{id}/votos` | Confirma `{"usuarioId":2}` |
| DELETE | `/reportes/{id}/votos/{usuarioId}` | Remove voto |

Swagger: `/swagger-ui.html`

**Regras de negócio:** nota = 0,35·infra + 0,25·segurança + 0,20·serviços + 0,20·lazer; status só avança (ABERTO → EM_ANDAMENTO → RESOLVIDO); autor não vota no próprio reporte; um voto por usuário; reporte resolvido não aceita edição nem voto.

**Erros** seguem o formato `{timestamp, status, erro, mensagem, caminho, detalhes[]}`.

## Como executar

**Ferramentas:** IntelliJ IDEA (ou VS Code), Git, Postman/Insomnia.
**Versões:** Java JDK 21, Maven 3.9+, Oracle (servidor da FIAP).

1. Clone o repositório e entre na pasta.
2. Defina as variáveis de ambiente (sem commitar senha):
   ```
   DB_URL=jdbc:oracle:thin:@oracle.fiap.com.br:1521:ORCL
   DB_USER=RMxxxxx
   DB_PASSWORD=sua_senha
   ```
3. `mvn spring-boot:run` (ou rode `MeuBairroApplication` no IntelliJ).
4. Na primeira execução a aplicação **cria as tabelas** (`schema.sql`) e carrega dados de exemplo (`data.sql`) se o banco estiver vazio. Para desligar: `DB_INIT=false`.
5. Acesse `http://localhost:8080/swagger-ui.html`.

Via Docker: `docker build -t meu-bairro-api . && docker run -p 8080:8080 -e DB_URL=... -e DB_USER=... -e DB_PASSWORD=... meu-bairro-api`

## Deploy no Render

1. Suba o código para o GitHub.
2. No Render: **New → Web Service** → conecte o repositório → *Runtime:* **Docker**.
3. Em *Environment*, cadastre `DB_URL`, `DB_USER`, `DB_PASSWORD` (o Render fornece `PORT` sozinho).
4. Deploy. A URL pública fica em `https://<nome>.onrender.com` (abra `/swagger-ui.html`).

> O Oracle da FIAP precisa estar acessível pela internet a partir do Render.

### Alternativa: Oracle Cloud Free (Autonomous Database, sem wallet)

Se o Oracle da FIAP não estiver acessível pelo Render, use um Autonomous Database (Always Free) com TLS simples:

1. No Oracle Cloud: **Autonomous Database > Create** (Transaction Processing, *Always Free*). Defina a senha do usuário `ADMIN`.
2. Em *Network*: **Access type = Secure access from everywhere** e, em *Mutual TLS (mTLS) authentication*, **desmarque "Require mutual TLS"** (permite conectar sem wallet).
3. Em **Database connection**, escolha *TLS authentication = TLS* e copie a *connection string* do serviço `_low`.
4. Monte as variáveis (o `host` e o `service_name` vêm da string copiada):
   ```
   DB_URL=jdbc:oracle:thin:@(description=(retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1521)(host=<HOST>))(connect_data=(service_name=<SERVICE_NAME>))(security=(ssl_server_dn_match=yes)))
   DB_USER=ADMIN
   DB_PASSWORD=<senha do ADMIN>
   ```
5. Use essas variáveis localmente e no Render. Nenhuma mudança de código é necessária; as tabelas são criadas na primeira execução.

## Links
- GitHub: https://github.com/Leoyukiio/GS-java
- Deploy: **não realizado** — a conta do Oracle da FIAP estava bloqueada (`ORA-28000`) até o fechamento da entrega. A API foi validada localmente contra um Oracle (todos os endpoints testados) e o procedimento de deploy acima, com o `Dockerfile`, está pronto para ser executado quando o banco estiver disponível.
