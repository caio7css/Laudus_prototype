CREATE TABLE IF NOT EXISTS medicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL DEFAULT '',
    crm TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    especializacao TEXT NOT NULL,
    acesso_exames_imagem BOOLEAN NOT NULL
);

INSERT INTO medicos (nome, crm, senha, especializacao, acesso_exames_imagem) VALUES
('Ana Beatriz Ramos',     '123456', 'senha123', 'Cardiologia', 1),
('Carlos Eduardo Lima',   '234567', 'senha234', 'Dermatologia', 0),
('Milena Veiga',          '345678', 'senha345', 'Radiologia', 1),
('Rafael Costa Melo',     '456789', 'senha456', 'Oftalmologia', 0),
('Juliana Farias',        '567890', 'senha567', 'Neurologia', 1),
('Pedro Henrique Alves',  '678901', 'senha678', 'Gastroenterologia', 0),
('Fernanda Duarte',       '789012', 'senha789', 'Ortopedia', 1),
('Marcos Vinícius Souza', '890123', 'senha890', 'Pediatria', 0),
('Larissa Nogueira',      '901234', 'senha901', 'Pneumologia', 0),
('Bruno Cavalcanti',      '012345', 'senha012', 'Urologia', 0);
