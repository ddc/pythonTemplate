# -*- encoding: utf-8 -*-
#################################
# MAIN
#################################
STARTING = "Iniciando"
FINISHED = "Finalizado"
NOT_FOUND = "Nao encontrado"
EXITING = "[EXECUCAO ABORTADA]"
TOTAL_SECONDS = "Tempo total de execucao em segundos"
CONFIG_FILE = "Arquivo de configuracoes"
HELP_DEBUG = "[OPCIONAL] Habilitar debug nos logs"
INVALID_PASSWORD = "Password invalido"
PASSW_DECODING = "Decodificando a senha"
PASSW_DECODE_ERROR = "Nao foi possivel decodificar a senha"
PASSW_NOT_ENC_ERROR = f"{PASSW_DECODE_ERROR}:Senha nao esta encriptada"
PASSW_OTHER_KEY_ERROR = f"{PASSW_DECODE_ERROR}:Senha foi encriptada com outra chave privada"
PERMISSION_DENIED = "Permissao negada"
PASSWORD_HIDDEN_MSG = "HIDENPASSWORD"
# CURRENT_PERMISSION = "Permissao atual"
# CHECKING_ARGUMENTS = "Verificando argumentos"
# INVALID_CHAR = "CARACTERE INVALIDO"
# EXIT_QUESTION = "Deseja realmente sair do programa?"
# PID_FOUND = "Programa em execucao!!! Arquivo PID encontrado"
# CHECKING_CONFIGS = "Verificando configuracoes"
#################################
# LOGS
#################################
LOGS_DIR_NOT_FOUND = f"[ERROR]:{EXITING}:NAO FOI POSSIVEL CRIAR DIRETORIO DE LOGS"
LOG_FILE_NOT_WRITABLE = f"[ERROR]:{EXITING}:NAO FOI POSSIVEL REALIZAR ESCRITA NO ARQUIVO DE LOG"
LOG_COMPRESS_ERROR = "[ERROR]:NAO FOI POSSIVEL COMPACTAR O ARQUIVO DE LOG"
LOG_RENAME_ERROR = "[ERROR]:NAO FOI POSSIVEL RENOMEAR O ARQUIVO PARA A DATA DE HOJE"
LOG_REMOVE_ERROR = "[ERROR]:NAO FOI POSSIVEL REMOVER O LOG"
#################################
# FILES
#################################
# FILE_REMOVING = "Removendo o arquivo"
# FILE_REMOVE_SUCCESS = "Arquivo removido com sucesso"
FILE_REMOVE_ERROR = "Nao foi possivel remover o arquivo"
# FILE_UNZIP = "Descompactando o arquivo"
# FILE_UNZIP_ERROR = "Nao foi possivel descompactar o arquivo"
# FILE_CLOSING = "Fechando arquivo"
# FILE_MOVE_ERROR = "Nao foi possivel mover o arquivo"
FILE_COPY_ERROR = "Nao foi possivel copiar o arquivo"
FILE_RENAME_ERROR = "Nao foi possivel renomear o arquivo"
FILE_REPLACE_DENIED = "Permissao negada ao substituir"
# FILE_REMOVING_AFTER_TRANSFER = "Removendo o arquivo apos o envio"
# FILE_RESENDING = "Enviando novamente o arquivo"
# FILE_SAVED_RESEND = "Arquivo salvo para ser enviado posteriormente"
# FILE_SAVED_RESEND_ERROR = "Nao foi possivel salvar o arquivo para ser reenviado"
#################################
# DIRS
#################################
# DIR_CREATING = "Criando diretorio"
# DIR_NOT_FOUND = "Diretorio inexistente"
# DIR_CREATE_ERROR = "Nao foi possivel criar o diretorio"
DIR_CREATE_NO_PERMS = "Permissao negada ao criar diretorio"
DIR_TMP_CREATE_ERROR = "Nao foi possivel criar o diretorio temporario para os arquivos que falharam a transmissao"
DIR_LOCAL_NOT_FOUND = f"{EXITING}:Diretorio local inexistente"
#################################
# DATABASE
#################################
DB_CONN_STARTING = "Iniciando conexao com o banco de dados"
DB_CONN_CHECKING = "Verificando conexao com o bancos de dados"
DB_CONN_CREATE_ERROR = "Cannot Create Database Connection"
DB_CONN_ERROR = "Nao foi possivel estabelecer conexao com o servidor de banco de dados"
DB_CONN_SUCCESS = "Conexao com o banco de dados estabelecida com sucesso"
DB_CONN_STRING = "String de conexao"
# DB_CONN_STRING_ERROR = "Erro na string de conexao do banco de dados"
# DB_CONN_CLOSING = "Encerrando conexao com o banco de dados"
# DB_COLL_STARTING = "Iniciando collection"
# DB_COLL_UNKNOWN = "Collection inexistente"
# DB_TABLE_CHECKING = "Verificando as tabelas do banco de dados"
# DB_TABLE_EMPTY = "Nao foram encontrados dados na database"
# DB_FILE_SQLITE_ERROR = "Arquivo do sqlite nao encontrado"
#################################
# SFTP
#################################
# SFTP_INIT = "INICIANDO TRANSFERENCIA"
# SFTP_AUTH_INIT = "Iniciando autenticacao"
# SFTP_AUTH_PASSW = "Usando autenticacao por senha"
# SFTP_AUTH_PKEY = "Usando autenticacao por chave privada"
# SFTP_CONN_STRING_ERROR = "Erro na string de conexao do SFTP"
# SFTP_CONN_SUCCESS = "Conexao estabelecida com sucesso"
SFTP_CONN_ERROR = "Nao foi possivel estabelecer conexao com o servidor"
# SFTP_TRANSFER_INIT = "Iniciando transferencia"
SFTP_TRANSFER_ERROR = "Nao foi possivel transferir o arquivo"
# SFTP_PASSW_LOGIN_ERROR = "Nao foi possivel autenticar por senha"
# SFTP_PKEY_LOGIN_ERROR = "Nao foi possivel autenticar por chave privada"
# SFTP_PKEY_WRONG_PERMS = "Chave privada com permissoes diferente de '0600'"
# SFTP_PKEY_CHANGED_PERMS = "Permissoes da chave privada trocada para '0600'"
# SFTP_PKEY_CHANGED_ERROR = "Nao foi possivel trocar as permissoes da chave privada para '0600'"
SFTP_PKEY_NOT_FOUND = "Chave privada usada para a autenticacao nao encontrada"
# SFTP_FILES_TO_SEND = "Arquivos a serem enviados"
# SFTP_FILES_MISMATCH = "Arquivo de destino diferente do arquivo de origem"
# SFTP_FILE_REMOVING_AFTER_TRANSFER = "Removendo o arquivo apos o envio"
# SFTP_FILE_RESENDING = "Enviando novamente o arquivo"
# SFTP_FILE_BATCH_CREATE = "Criando arquivo temporario com as informacoes de envio"
# SFTP_FILE_BATCH_REMOVE_ERROR = "Nao foi possivel excluir o arquivo temporario que contem as informacoes de envio"
# SFTP_REMOTE_REMOVE_PART_FILE_ERROR = "Nao foi possivel remover arquivo temporario remoto '_part'"
SFTP_REMOTE_DIR_NOT_FOUND = "Diretorio remoto inexistente"
# SFTP_REMOTE_FILE_FOUND = "Arquivo remoto ja existente"
# SFTP_REMOTE_FILE_RENAME_ERROR = "Nao foi possivel renomear o arquivo remoto"
SFTP_BIN_NOT_FOUND = "Executavel nao encontrado"
# SFTP_SET_UTIME_ERROR = "Nao foi possivel setar o timestamp do arquivo"
# SFTP_RESEND_ERROR = "Nao sera possivel reenviar o arquivo"
SFTP_TRANSFERED = "TRANSFERIDO"
#################################
# PROGRAM
#################################
PROGRAM_DESCRIPTION = ""
