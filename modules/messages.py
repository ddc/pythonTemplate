# -*- encoding: utf-8 -*-
#################################
# MAIN
#################################
STARTING = "Starting"
FINISHED = "Finished"
NOT_FOUND = "Not found"
EXITING = "[EXITING]"
TOTAL_SECONDS = "Total run time in seconds"
CONFIG_FILE = "Configuration file"
HELP_DEBUG = "[OPTIONAL] Enable debug in logs"
INVALID_PASSWORD = "Invalid Password"
PASSW_DECODING = "Decoding the password"
PASSW_DECODE_ERROR = "Unable to decode the password"
PASSW_NOT_ENC_ERROR = f"{PASSW_DECODE_ERROR}:Password is not encrypted"
PASSW_OTHER_KEY_ERROR = f"{PASSW_DECODE_ERROR}:Password was encrypted with another private key"
PERMISSION_DENIED = "Permission denied"
PASSWORD_HIDDEN_MSG = "HIDENPASSWORD"
PERMISSION_CURRENT = "Current Permission"
# CHECKING_ARGUMENTS = "Checking arguments"
# CHECKING_CONFIGS = "Checking settings"
# INVALID_CHAR = "INVALID CHARACTER"
# PID_FOUND = "PID file found. Program still running!!!"
# EXIT_QUESTION = "Do you really want to exit the program?"
#################################
# LOGS
#################################
LOGS_DIR_NOT_FOUND = f"[ERROR]:{EXITING}:UNABLE TO CREATE LOGS DIRECTORY"
LOG_FILE_NOT_WRITABLE = f"[ERROR]:{EXITING}:UNABLE TO OPEN THE LOG FILE FOR WRITING"
LOG_COMPRESS_ERROR = "[ERROR]:UNABLE TO COMPRESS THE LOG FILE"
LOG_RENAME_ERROR = "[ERROR]:UNABLE TO RENAME THE LOG FILE TO TODAY'S DATE"
LOG_REMOVE_ERROR = "[ERROR]:UNABLE TO REMOVE THE LOG FILE"
#################################
# FILES
#################################
# FILE_REMOVING = "Removing the file"
# FILE_REMOVE_SUCCESS = "File successfully removed"
FILE_REMOVE_ERROR = "Unable to remove the file"
# FILE_UNZIP = "Unzipping the file"
# FILE_UNZIP_ERROR = "Unable to unzip the file"
# FILE_CLOSING = "Closing the file"
# FILE_MOVE_ERROR = "Unable to move the file"
FILE_COPY_ERROR = "Unable to copy the file"
FILE_RENAME_ERROR = "Unable to rename the file"
FILE_REPLACE_DENIED = "Permission denied when replacing the file"
# FILE_REMOVING_AFTER_TRANSFER = "Removing the file after uploading"
# FILE_RESENDING = "Resending the file"
# FILE_SAVED_RESEND = "File saved to be sent later"
# FILE_SAVED_RESEND_ERROR = "Unable to save file to resend later"
#################################
# DIRS
#################################
# DIR_CREATING = "Creating directory"
# DIR_NOT_FOUND = "Directory not found"
# DIR_CREATE_ERROR = "Unable to create directory"
DIR_CREATE_NO_PERMS = "Permission denied when creating directory"
DIR_TMP_CREATE_ERROR = "Unable to create temporary directory for files that failed the upload"
DIR_LOCAL_NOT_FOUND = f"{EXITING}:Local directory not found"
#################################
# DATABASE
#################################
DB_CONN_STARTING = "Starting database connection"
DB_CONN_CHECKING = "Checking database connection"
DB_CONN_CREATE_ERROR = "Unable to create database connection"
DB_CONN_ERROR = "Unable to establish connection to database server"
DB_CONN_SUCCESS = "Database connection successfully established"
DB_CONN_STRING = "Connection string"
# DB_CONN_STRING_ERROR = "Database connection string error"
# DB_CONN_CLOSING = "Closing database connection"
# DB_COLL_STARTING = "Starting collection"
# DB_COLL_NOT_FOUND = "Collection not found"
# DB_TABLE_CHECKING = "Checking database tables"
# DB_TABLE_EMPTY = "No data found in database"
# DB_FILE_SQLITE_ERROR = "SQLite file not found"
#################################
# SFTP
#################################
# SFTP_STARTING = "STARTING TRANSFERS"
# SFTP_AUTH_INIT = "Starting authentication"
# SFTP_AUTH_PASSW = "Using password authentication"
# SFTP_AUTH_PKEY = "Using private key authentication"
# SFTP_CONN_STRING_ERROR = "SFTP connection string error"
# SFTP_CONN_SUCCESS = "SFTP connection successfully established"
SFTP_CONN_ERROR = "Unable to establish connection to SFTP server"
SFTP_TRANSFER_ERROR = "Unable to transfer file"
# SFTP_PASSW_LOGIN_ERROR = "Unable to authenticate using password"
# SFTP_PKEY_LOGIN_ERROR = "Unable to authenticate using private key"
SFTP_PKEY_WRONG_PERMS = "Private key with permissions other than '0600'"
SFTP_PKEY_CHANGED_PERMS = "Private key permissions changed to '0600'"
SFTP_PKEY_CHANGED_ERROR = "Unable to change private key permissions to '0600'"
SFTP_PKEY_NOT_FOUND = "Private key used for authentication not found"
# SFTP_FILES_TO_SEND = "Files to be sent"
# SFTP_FILES_MISMATCH = "Destination file different from source file"
# SFTP_FILE_REMOVING_AFTER_TRANSFER = "Removing the file after uploading"
# SFTP_FILE_RESENDING = "Uploading the file again"
# SFTP_FILE_BATCH_CREATE = "Creating a temporary file with SFTP batch information"
# SFTP_FILE_BATCH_REMOVE_ERROR = "Unable to delete temporary file containing SFTP batch information"
# SFTP_REMOTE_REMOVE_PART_FILE_ERROR = "Unable to remove remote temporary file '_part'"
SFTP_REMOTE_DIR_NOT_FOUND = "Remote directory not found"
# SFTP_REMOTE_FILE_FOUND = "Remote file found"
# SFTP_REMOTE_FILE_RENAME_ERROR = "Unable to rename remote file"
SFTP_BIN_NOT_FOUND = "SFTP not found"
# SFTP_SET_UTIME_ERROR = "Unable to set file timestamp"
# SFTP_RESEND_ERROR = "Unbale to resend the file"
SFTP_TRANSFERED = "TRANSFERED"
#################################
# PROGRAM
#################################
PROGRAM_DESCRIPTION = ""
