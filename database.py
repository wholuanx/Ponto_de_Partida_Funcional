import sqlite3
import os
import hashlib
from datetime import datetime

def init_database():
    """Inicializa o banco de dados SQLite3"""
    conn = sqlite3.connect('turismo.db')
    cursor = conn.cursor()
    
    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            endereco TEXT,
            telefone TEXT,
            cpf TEXT UNIQUE,
            passaporte TEXT,
            foto_perfil TEXT,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela de pontos turísticos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pontos_turisticos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            descricao TEXT NOT NULL,
            endereco TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            imagem TEXT,
            categoria TEXT,
            horario_funcionamento TEXT,
            preco_entrada TEXT,
            telefone_contato TEXT,
            site_oficial TEXT,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela de avaliações
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            ponto_turistico_id INTEGER NOT NULL,
            nota INTEGER NOT NULL CHECK (nota >= 1 AND nota <= 5),
            comentario TEXT,
            data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
            FOREIGN KEY (ponto_turistico_id) REFERENCES pontos_turisticos (id),
            UNIQUE(usuario_id, ponto_turistico_id)
        )
    ''')
    
    # Tabela de registros de visitas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitas_pontos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            ponto_turistico_id INTEGER NOT NULL,
            data_visita TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            origem_sudeste INTEGER NOT NULL CHECK (origem_sudeste IN (0, 1)),
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
            FOREIGN KEY (ponto_turistico_id) REFERENCES pontos_turisticos (id)
        )
    ''')

    # Inserir dados iniciais de pontos turísticos do Rio de Janeiro
    pontos_turisticos = [
        {
            'nome': 'Cristo Redentor',
            'descricao': 'O Cristo Redentor é uma estátua art déco que retrata Jesus Cristo, localizada no topo do morro do Corcovado, a 709 metros acima do nível do mar, no Parque Nacional da Tijuca, com vista para a maior parte da cidade do Rio de Janeiro.',
            'endereco': 'Parque Nacional da Tijuca - Alto da Boa Vista, Rio de Janeiro - RJ',
            'latitude': -22.9519,
            'longitude': -43.2105,
            'imagem': 'cristo_redentor.jpg',
            'categoria': 'Religioso/Histórico',
            'horario_funcionamento': '8h às 19h',
            'preco_entrada': 'R$ 65,00',
            'telefone_contato': '(21) 2558-1329',
            'site_oficial': 'https://www.corcovado.com.br'
        },
        {
            'nome': 'Pão de Açúcar',
            'descricao': 'O Pão de Açúcar é um morro localizado no bairro da Urca, na cidade do Rio de Janeiro. É um dos principais cartões-postais da cidade. O morro é um dos mais famosos do Brasil.',
            'endereco': 'Av. Pasteur, 520 - Urca, Rio de Janeiro - RJ',
            'latitude': -22.9486,
            'longitude': -43.1634,
            'imagem': 'pao_acucar.jpg',
            'categoria': 'Natureza/Panorâmico',
            'horario_funcionamento': '8h às 21h',
            'preco_entrada': 'R$ 95,00',
            'telefone_contato': '(21) 2546-8400',
            'site_oficial': 'https://www.bondinho.com.br'
        },
        {
            'nome': 'Praia de Copacabana',
            'descricao': 'Copacabana é um bairro situado na Zona Sul do município do Rio de Janeiro. É um dos bairros mais famosos e prestigiados do Brasil e um dos mais conhecidos do mundo.',
            'endereco': 'Copacabana, Rio de Janeiro - RJ',
            'latitude': -22.9711,
            'longitude': -43.1822,
            'imagem': 'copacabana.jpg',
            'categoria': 'Praia/Recreação',
            'horario_funcionamento': '24h',
            'preco_entrada': 'Gratuito',
            'telefone_contato': '',
            'site_oficial': ''
        },
        {
            'nome': 'Jardim Botânico',
            'descricao': 'O Jardim Botânico do Rio de Janeiro é um instituto de pesquisas e jardim botânico localizado no bairro do Jardim Botânico, na Zona Sul da cidade do Rio de Janeiro.',
            'endereco': 'R. Jardim Botânico, 1008 - Jardim Botânico, Rio de Janeiro - RJ',
            'latitude': -22.9701,
            'longitude': -43.2247,
            'imagem': 'jardim_botanico.jpg',
            'categoria': 'Natureza/Educativo',
            'horario_funcionamento': '8h às 17h',
            'preco_entrada': 'R$ 15,00',
            'telefone_contato': '(21) 3874-1808',
            'site_oficial': 'https://www.jbrj.gov.br'
        },
        {
            'nome': 'Lapa',
            'descricao': 'A Lapa é um bairro boêmio do Rio de Janeiro, famoso por seus bares, restaurantes e casas noturnas. É conhecida pelos Arcos da Lapa e pela vida noturna vibrante.',
            'endereco': 'Lapa, Rio de Janeiro - RJ',
            'latitude': -22.9110,
            'longitude': -43.1844,
            'imagem': 'lapa.jpg',
            'categoria': 'Cultura/Entretenimento',
            'horario_funcionamento': 'Varia conforme estabelecimento',
            'preco_entrada': 'Varia',
            'telefone_contato': '',
            'site_oficial': ''
        }
    ]
    
    # Inserir pontos turísticos se não existirem
    for ponto in pontos_turisticos:
        cursor.execute('''
            INSERT OR IGNORE INTO pontos_turisticos 
            (nome, descricao, endereco, latitude, longitude, imagem, categoria, 
             horario_funcionamento, preco_entrada, telefone_contato, site_oficial)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            ponto['nome'], ponto['descricao'], ponto['endereco'], 
            ponto['latitude'], ponto['longitude'], ponto['imagem'], 
            ponto['categoria'], ponto['horario_funcionamento'], 
            ponto['preco_entrada'], ponto['telefone_contato'], ponto['site_oficial']
        ))
    
    admin_nome = 'admin'
    admin_email = 'admin@turismo.com'
    admin_senha_hash = hashlib.sha256('0000'.encode()).hexdigest()
    admin_endereco = 'Endereço Admin'
    admin_telefone = '00000000000'
    admin_cpf = '00000000000'

    cursor.execute('SELECT id FROM usuarios WHERE nome = ?', (admin_nome,))
    admin_row = cursor.fetchone()

    if admin_row:
        cursor.execute('''
            UPDATE usuarios
            SET email = ?, senha = ?, endereco = ?, telefone = ?, cpf = ?
            WHERE id = ?
        ''', (admin_email, admin_senha_hash, admin_endereco, admin_telefone, admin_cpf, admin_row[0]))
    else:
        cursor.execute('SELECT id FROM usuarios WHERE nome = ?', ('adm',))
        legacy_admin = cursor.fetchone()

        if legacy_admin:
            cursor.execute('''
                UPDATE usuarios
                SET nome = ?, email = ?, senha = ?, endereco = ?, telefone = ?, cpf = ?
                WHERE id = ?
            ''', (admin_nome, admin_email, admin_senha_hash, admin_endereco, admin_telefone, admin_cpf, legacy_admin[0]))
        else:
            cursor.execute('''
                INSERT INTO usuarios (nome, email, senha, endereco, telefone, cpf)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (admin_nome, admin_email, admin_senha_hash, admin_endereco, admin_telefone, admin_cpf))
    
    conn.commit()
    conn.close()

def get_connection():
    """Retorna uma conexão com o banco de dados"""
    return sqlite3.connect('turismo.db')

if __name__ == '__main__':
    init_database()
    print("Banco de dados inicializado com sucesso!")
