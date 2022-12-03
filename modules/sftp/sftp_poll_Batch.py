# -*- encoding: utf-8 -*-
from datetime import datetime
import logging
import logging.handlers
import os
import subprocess
import paramiko
from modules import utils, messages, constants


class SFTP:
    def __init__(self, **kwargs):
        self.debug = kwargs.get("debug")
        self.host = kwargs.get("host")
        self.port = int(kwargs.get("port"), 22)
        self.user = kwargs.get("user")
        self.password = kwargs.get("password")
        self.remote_dir = kwargs.get("remote_dir")
        self.backup_dir = kwargs.get("backup_dir")
        self.linux_sftp_bin = kwargs.get("linux_sftp_bin", "/usr/bin/sftp")
        self.pkey_file = os.path.expanduser(kwargs.get("pkey_file"))
        self.set_remote_time = kwargs.get("set_remote_time", True)
        self.full_host = f"{self.user}@{self.host}:{self.port}"
        self.batchfile_path = kwargs.get("batchfile_path",
                                         f"{constants.TMP_DIR}/"
                                         f"sftpBatchFile.txt")

    def _get_paramiko_connection(self, file_src):
        if self.debug:
            logging.getLogger("paramiko.transport").setLevel(logging.DEBUG)
        else:
            logging.getLogger("paramiko.transport").setLevel(logging.ERROR)

        try:
            _wsize = pow(2, 24)
            _maxpsize = pow(2, 24)
            transport = paramiko.Transport(self.host, self.port)

            if self.pkey_file is not None and os.path.isfile(self.pkey_file):
                paramiko_key = paramiko.RSAKey.from_private_key_file(
                    self.pkey_file
                )
                transport.connect(username=self.user, pkey=paramiko_key)
            else:
                passw = self.password
                if passw is None or len(passw) == 0:
                    error_msg = f"{messages.SFTP_CONN_ERROR}: " \
                                f"{messages.INVALID_PASSWORD}: {file_src}"
                    return {
                        "sftp": None,
                        "transport": None,
                        "error_msg": error_msg}
                else:
                    transport.connect(username=self.user, password=passw)

            transport.banner_timeout = 600
            transport.handshake_timeout = 600
            transport.auth_timeout = 600
            sftp = paramiko.SFTPClient.from_transport(
                transport,
                window_size=_wsize,
                max_packet_size=_maxpsize
            )

            file_mtime = datetime.fromtimestamp(os.stat(file_src).st_mtime)
            remote_dir = utils.format_path_dates(self.remote_dir, file_mtime)

            try:
                sftp.stat(remote_dir)
            except IOError as e:
                sftp.close() if sftp is not None else None
                transport.close() if transport is not None else None
                error_msg = f"[{messages.SFTP_REMOTE_DIR_NOT_FOUND}]:" \
                            f"{utils.get_exception(e)}: " \
                            f"{file_src} -> {remote_dir}"
                return {"sftp": None,
                        "transport": None,
                        "error_msg": error_msg}
        except Exception as e:
            error_msg = f"[{messages.SFTP_CONN_ERROR}]:" \
                        f"{utils.get_exception(e)}"
            return {"sftp": None, "transport": None, "error_msg": error_msg}
        return {"sftp": sftp, "transport": transport, "error_msg": None}

    def start_send_paramiko_pool(self, file_src, file_dst):
        conn = self._get_paramiko_connection(file_src)
        if conn.get("error_msg") is not None:
            return {
                "result": False,
                "level": "ERROR",
                "msg": conn.get("error_msg"),
                "filename": os.path.basename(file_src)}

        sftp = conn.get("sftp")
        transport = conn.get("transport")
        temp_file_dst = f"{file_dst}_part"
        log_header_msg = f"[PARAMIKO]:[{self.full_host}]"

        if sftp is not None and transport is not None:
            local_stat = os.stat(file_src)
            times = (local_stat.st_atime, local_stat.st_mtime)

            try:
                sftp.remove(file_dst)
            except IOError as e:
                if hasattr(e, "errno") and e.errno == 13:
                    sftp.close() if sftp is not None else None
                    transport.close() if transport is not None else None
                    msg = f"{log_header_msg}:{messages.FILE_REPLACE_DENIED}:" \
                          f"{utils.get_exception(e)}: " \
                          f"{os.path.basename(file_dst)}"
                    return {
                        "result": False,
                        "level": "ERROR",
                        "msg": msg,
                        "filename": os.path.basename(file_dst)}

            try:
                sftp.put(file_src, temp_file_dst)
                if sftp.stat(temp_file_dst).st_size == local_stat.st_size:
                    sftp.rename(temp_file_dst, file_dst)
                    sftp.utime(file_dst, times)
                    sftp.close() if sftp is not None else None
                    transport.close() if transport is not None else None
                else:
                    sftp.remove(temp_file_dst)
                    sftp.close() if sftp is not None else None
                    transport.close() if transport is not None else None
                    msg = f"{log_header_msg}:{messages.SFTP_TRANSFER_ERROR}:" \
                          f"{file_src}"
                    return {
                        "result": False,
                        "level": "ERROR",
                        "msg": msg,
                        "filename": os.path.basename(file_src)}
            except Exception as e:
                sftp.close()
                transport.close() if transport is not None else None
                msg = f"{log_header_msg}:{messages.SFTP_TRANSFER_ERROR}:" \
                      f"{utils.get_exception(e)}: {file_src}"
                return {
                    "result": False,
                    "level": "ERROR",
                    "msg": msg,
                    "filename": os.path.basename(file_src)}

            if self.backup_dir is not None and len(self.backup_dir) > 0 \
                    and os.path.isdir(self.backup_dir):
                utils.start_backup(file_src,
                                   f"{self.backup_dir}/"
                                   f"{os.path.basename(file_dst)}")

            try:
                if os.path.isfile(file_src):
                    os.remove(file_src)
            except Exception as e:
                msg = f"{log_header_msg}:{messages.FILE_REMOVE_ERROR}:" \
                      f"{utils.get_exception(e)}: " \
                      f"{os.path.basename(file_src)}"
                return {
                    "result": False,
                    "level": "ERROR",
                    "msg": msg,
                    "filename": os.path.basename(file_src)}

            msg = f"[PARAMIKO]:[{messages.SFTP_TRANSFERED}]:" \
                  f"[{self.full_host}]:" \
                  f"[{local_stat.st_size} bytes]: " \
                  f"{file_src} -> {file_dst}"
            return {
                "result": True,
                "level": "INFO",
                "msg": msg,
                "filename": os.path.basename(file_dst)}
        else:
            msg = f"{log_header_msg}:{conn.get('error_msg')}"
            return {
                "result": False,
                "level": "ERROR",
                "msg": msg,
                "filename": os.path.basename(file_src)}


    def start_send_sftp_pool(self, file_src, file_dst):
        """
            /usr/bin/sftp -p -b /tmp/sftp_batch.txt -P 2201 -i ~/.ssh/id_rsa user@host
            -p conservar timestamp
            -b usar arquivo com os comandos
            -P porta
            -i path da chave privada
        """

        temp_file_dst = f"{file_dst}_part"
        user_host = f"{self.user}@{self.host}"
        local_stat = os.stat(file_src)
        size_bytes = f"{local_stat.st_size} bytes"
        log_header_msg = f"[SFTP]:[{self.full_host}]"
        warn_msg = ""

        if not os.path.exists(self.linux_sftp_bin):
            msg = f"{log_header_msg}:{messages.SFTP_BIN_NOT_FOUND}: " \
                  f"{self.linux_sftp_bin}"
            return {
                "result": False,
                "level": "ERROR",
                "msg": msg,
                "filename": None}

        if not os.path.exists(self.pkey_file):
            msg = f"{log_header_msg}:{messages.SFTP_PKEY_NOT_FOUND}: " \
                  f"{self.pkey_file}"
            return {
                "result": False,
                "level": "ERROR",
                "msg": msg,
                "filename": None}

        if os.name != "nt":
            pkey_permissions = oct(os.stat(self.pkey_file).st_mode)[-4:]
            if pkey_permissions != "0600":
                warn_msg += f"[{messages.SFTP_PKEY_WRONG_PERMS}]: " \
                            f"[{messages.PERMISSION_CURRENT}: " \
                            f"{pkey_permissions}]:" \
                            f"[{self.pkey_file}]: {self.pkey_file}"
                try:
                    os.chmod(self.pkey_file, 0o600)
                    warn_msg += f"[{messages.SFTP_PKEY_CHANGED_PERMS}]: " \
                                f"[{self.pkey_file}]: {file_src}"
                except OSError as e:
                    msg = f"[{messages.SFTP_PKEY_CHANGED_ERROR}]: " \
                          f"[{messages.PERMISSION_CURRENT}: " \
                          f"{pkey_permissions}]:" \
                          f"[{self.pkey_file}]:" \
                          f"{utils.get_exception(e)}: " \
                          f"{file_src}"
                    return {
                        "result": False,
                        "level": "ERROR",
                        "msg": msg,
                        "filename": os.path.basename(file_src)}

        try:
            with open(self.batchfile_path, "w") as tmp_file:
                tmp_file.write(f"cd {os.path.dirname(self.remote_dir)}\n")
                tmp_file.write(f"put {file_src} {temp_file_dst}\n")
                tmp_file.write(f"rename {temp_file_dst} {file_dst}")
            cmd = f"{self.linux_sftp_bin} -p -b {self.batchfile_path} " \
                  f"-P {int(self.port)} -i {self.pkey_file} {user_host}"

            process = subprocess.Popen(cmd,
                                       shell=True,
                                       executable="bash",
                                       universal_newlines=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode or stderr is not None and len(stderr) > 0:
                msg = f"{log_header_msg}:" \
                      f"[STDERR]:[RETURNCODE:{str(process.returncode)}]:" \
                      f"{stderr} {file_src}"
                msg += f"\n{cmd}\n" if self.debug else ""
                return {
                    "result": False,
                    "level": "ERROR",
                    "msg": msg,
                    "filename": os.path.basename(file_src)}

            if self.backup_dir is not None \
                    and len(self.backup_dir) > 0 \
                    and os.path.isdir(self.backup_dir):
                utils.start_backup(file_src,
                                   f"{self.backup_dir}/"
                                   f"{os.path.basename(file_dst)}")

            try:
                if os.path.isfile(file_src):
                    os.remove(file_src)
            except Exception as e:
                warn_msg += f"{log_header_msg}:{messages.FILE_REMOVE_ERROR}:" \
                            f"{utils.get_exception(e)}: {file_src}"

            msg = f"[SFTP]:[{messages.SFTP_TRANSFERED}]:[{self.full_host}]:"
            if len(warn_msg) > 0:
                msg += f"[{warn_msg}]"
            msg += f"[{size_bytes}]: " \
                   f"{file_src} -> {file_dst}"

            if self.debug and stdout is not None and len(stdout) > 0:
                msg += f"\n\n{cmd}:\n[STDOUT]: {stdout}"
            return {
                "result": True,
                "level": "INFO",
                "msg": msg,
                "filename": os.path.basename(file_dst)}
        except Exception as e:
            msg = f"{log_header_msg}:" \
                  f"[{size_bytes}]: " \
                  f"{utils.get_exception(e)}: " \
                  f"{file_src}"
            return {
                "result": False,
                "level": "ERROR",
                "msg": msg,
                "filename": os.path.basename(file_src)}
