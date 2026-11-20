CREATE TABLE tb_mb_bairro (
    id_bairro  NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome       VARCHAR2(100) NOT NULL,
    cidade     VARCHAR2(100) NOT NULL,
    uf         CHAR(2)       NOT NULL,
    populacao  NUMBER(10)    DEFAULT 0 NOT NULL CHECK (populacao >= 0),
    CONSTRAINT uk_mb_bairro_nome_cidade UNIQUE (nome, cidade)
);
CREATE TABLE tb_mb_usuario (
    id_usuario NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome       VARCHAR2(100) NOT NULL,
    email      VARCHAR2(150) NOT NULL,
    perfil     VARCHAR2(10)  NOT NULL CHECK (perfil IN ('MORADOR','ADMIN')),
    id_bairro  NUMBER,
    CONSTRAINT uk_mb_usuario_email UNIQUE (email),
    CONSTRAINT fk_mb_usuario_bairro FOREIGN KEY (id_bairro) REFERENCES tb_mb_bairro (id_bairro)
);
CREATE TABLE tb_mb_reporte (
    id_reporte  NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_usuario  NUMBER         NOT NULL,
    id_bairro   NUMBER         NOT NULL,
    categoria   VARCHAR2(15)   NOT NULL CHECK (categoria IN ('BURACO','ILUMINACAO','LIXO','ALAGAMENTO','OUTRO')),
    descricao   VARCHAR2(500)  NOT NULL,
    latitude    NUMBER(9,6)    NOT NULL,
    longitude   NUMBER(9,6)    NOT NULL,
    status      VARCHAR2(15)   DEFAULT 'ABERTO' NOT NULL CHECK (status IN ('ABERTO','EM_ANDAMENTO','RESOLVIDO')),
    criado_em   TIMESTAMP      DEFAULT SYSTIMESTAMP NOT NULL,
    resolvido_em TIMESTAMP,
    CONSTRAINT fk_mb_reporte_usuario FOREIGN KEY (id_usuario) REFERENCES tb_mb_usuario (id_usuario),
    CONSTRAINT fk_mb_reporte_bairro  FOREIGN KEY (id_bairro)  REFERENCES tb_mb_bairro (id_bairro)
);
CREATE TABLE tb_mb_voto (
    id_voto    NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_reporte NUMBER    NOT NULL,
    id_usuario NUMBER    NOT NULL,
    criado_em  TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    CONSTRAINT uk_mb_voto UNIQUE (id_reporte, id_usuario),
    CONSTRAINT fk_mb_voto_reporte FOREIGN KEY (id_reporte) REFERENCES tb_mb_reporte (id_reporte),
    CONSTRAINT fk_mb_voto_usuario FOREIGN KEY (id_usuario) REFERENCES tb_mb_usuario (id_usuario)
);
CREATE TABLE tb_mb_indicador_bairro (
    id_indicador   NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_bairro      NUMBER NOT NULL,
    infraestrutura NUMBER(3,1) NOT NULL CHECK (infraestrutura BETWEEN 0 AND 10),
    seguranca      NUMBER(3,1) NOT NULL CHECK (seguranca BETWEEN 0 AND 10),
    servicos       NUMBER(3,1) NOT NULL CHECK (servicos BETWEEN 0 AND 10),
    lazer          NUMBER(3,1) NOT NULL CHECK (lazer BETWEEN 0 AND 10),
    CONSTRAINT uk_mb_indicador_bairro UNIQUE (id_bairro),
    CONSTRAINT fk_mb_indicador_bairro FOREIGN KEY (id_bairro) REFERENCES tb_mb_bairro (id_bairro)
);
CREATE INDEX idx_mb_reporte_bairro ON tb_mb_reporte (id_bairro);
CREATE INDEX idx_mb_reporte_status ON tb_mb_reporte (status);
CREATE INDEX idx_mb_voto_reporte ON tb_mb_voto (id_reporte)
