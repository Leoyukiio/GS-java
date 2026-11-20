INSERT INTO tb_mb_bairro (nome, cidade, uf, populacao) VALUES ('Pinheiros', 'São Paulo', 'SP', 65000);
INSERT INTO tb_mb_bairro (nome, cidade, uf, populacao) VALUES ('Vila Mariana', 'São Paulo', 'SP', 134000);
INSERT INTO tb_mb_bairro (nome, cidade, uf, populacao) VALUES ('Tatuapé', 'São Paulo', 'SP', 91000);
INSERT INTO tb_mb_bairro (nome, cidade, uf, populacao) VALUES ('Mooca', 'São Paulo', 'SP', 87000);
INSERT INTO tb_mb_indicador_bairro (id_bairro, infraestrutura, seguranca, servicos, lazer) SELECT id_bairro, 8.5, 7.8, 8.4, 7.9 FROM tb_mb_bairro WHERE nome = 'Pinheiros';
INSERT INTO tb_mb_indicador_bairro (id_bairro, infraestrutura, seguranca, servicos, lazer) SELECT id_bairro, 7.5, 7.4, 8.0, 7.5 FROM tb_mb_bairro WHERE nome = 'Vila Mariana';
INSERT INTO tb_mb_indicador_bairro (id_bairro, infraestrutura, seguranca, servicos, lazer) SELECT id_bairro, 7.0, 7.1, 7.6, 7.0 FROM tb_mb_bairro WHERE nome = 'Tatuapé';
INSERT INTO tb_mb_indicador_bairro (id_bairro, infraestrutura, seguranca, servicos, lazer) SELECT id_bairro, 5.9, 6.6, 6.8, 6.3 FROM tb_mb_bairro WHERE nome = 'Mooca';
INSERT INTO tb_mb_usuario (nome, email, perfil, id_bairro) SELECT 'Admin Prefeitura', 'admin@meubairro.com', 'ADMIN', id_bairro FROM tb_mb_bairro WHERE nome = 'Pinheiros';
INSERT INTO tb_mb_usuario (nome, email, perfil, id_bairro) SELECT 'Maria Souza', 'maria@email.com', 'MORADOR', id_bairro FROM tb_mb_bairro WHERE nome = 'Vila Mariana';
INSERT INTO tb_mb_usuario (nome, email, perfil, id_bairro) SELECT 'João Lima', 'joao@email.com', 'MORADOR', id_bairro FROM tb_mb_bairro WHERE nome = 'Mooca';
INSERT INTO tb_mb_reporte (id_usuario, id_bairro, categoria, descricao, latitude, longitude, status) SELECT u.id_usuario, b.id_bairro, 'BURACO', 'Buraco grande na Rua das Flores, perto do número 120.', -23.589, -46.635, 'ABERTO' FROM tb_mb_usuario u, tb_mb_bairro b WHERE u.email = 'maria@email.com' AND b.nome = 'Vila Mariana';
INSERT INTO tb_mb_reporte (id_usuario, id_bairro, categoria, descricao, latitude, longitude, status) SELECT u.id_usuario, b.id_bairro, 'ALAGAMENTO', 'Esquina alaga a cada chuva forte.', -23.559, -46.599, 'ABERTO' FROM tb_mb_usuario u, tb_mb_bairro b WHERE u.email = 'joao@email.com' AND b.nome = 'Mooca';
INSERT INTO tb_mb_voto (id_reporte, id_usuario) SELECT r.id_reporte, u.id_usuario FROM tb_mb_reporte r, tb_mb_usuario u WHERE r.categoria = 'BURACO' AND u.email = 'joao@email.com'
