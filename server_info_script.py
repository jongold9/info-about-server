import os
import platform
import socket
import subprocess

# Открываем файл для записи
with open('server_info.txt', 'w') as file:
    # Получаем информацию о системе и записываем в файл
    file.write("=== Информация о сервере ===\n")
    file.write(f"Операционная система: {platform.system()} {platform.release()}\n")
    file.write(f"Архитектура процессора: {platform.machine()}\n")

    # Получаем информацию о сетевых интерфейсах и записываем в файл
    file.write("\n=== Информация о сети ===\n")
    hostname = socket.gethostname()
    file.write(f"Имя хоста: {hostname}\n")
    ip_address = socket.gethostbyname(hostname)
    file.write(f"IP-адрес: {ip_address}\n")

    # Получаем информацию о сетевой конфигурации и записываем в файл
    network_info = subprocess.getoutput('ip a')
    file.write("Сетевая конфигурация:\n")
    file.write(network_info)

    # Получаем информацию о процессоре и оперативной памяти и записываем в файл
    file.write("\n=== Информация о процессоре и памяти ===\n")
    cpu_info = subprocess.getoutput('lscpu')
    file.write("Информация о процессоре:\n")
    file.write(cpu_info)
    mem_info = subprocess.getoutput('free -m')
    file.write("Информация о памяти:\n")
    file.write(mem_info)

    # Получаем информацию о дисковом пространстве и записываем в файл
    file.write("\n=== Информация о дисках ===\n")
    disk_info = subprocess.getoutput('df -h')
    file.write("Информация о дисках:\n")
    file.write(disk_info)

    # Получаем информацию о Docker и записываем в файл
    file.write("\n=== Информация о Docker ===\n")
    docker_info = subprocess.getoutput('docker info')
    file.write("Информация о Docker:\n")
    file.write(docker_info)

    # Получаем информацию о пользователях и группах и записываем в файл
    file.write("\n=== Информация о пользователях и группах ===\n")
    users_info = subprocess.getoutput('cat /etc/passwd')
    file.write("Информация о пользователях и группах:\n")
    file.write(users_info)

    # Получаем информацию о версии ядра и записываем в файл
    file.write("\n=== Информация о версии ядра ===\n")
    kernel_info = subprocess.getoutput('uname -r')
    file.write(f"Версия ядра: {kernel_info}\n")

    # Получаем информацию о службах и записываем в файл
    file.write("\n=== Информация о службах ===\n")
    services_info = subprocess.getoutput('systemctl list-units --type=service')
    file.write("Информация о запущенных службах:\n")
    file.write(services_info)

    # Получаем информацию о текущих соединениях и записываем в файл
    file.write("\n=== Информация о текущих соединениях ===\n")
    connections_info = subprocess.getoutput('netstat -tunapl')
    file.write("Информация о текущих соединениях:\n")
    file.write(connections_info)

    # Получаем информацию о загруженности процессора и записываем в файл
    file.write("\n=== Информация о загруженности процессора ===\n")
    cpu_load_info = subprocess.getoutput('uptime')
    file.write("Информация о загруженности процессора:\n")
    file.write(cpu_load_info)

    # Попытка определения используемой базы данных
    file.write("\n=== Информация о базах данных ===\n")

    # Проверка установленных баз данных
    databases_info = ""
    if os.path.exists('/etc/init.d/mysql'):
        databases_info += "MySQL/MariaDB установлен\n"
    if os.path.exists('/etc/init.d/postgresql'):
        databases_info += "PostgreSQL установлен\n"

    if databases_info:
        file.write(databases_info)

        # Дополнительная информация о базах данных (замените <user> и <password> на ваши учетные данные)
        if 'MySQL/MariaDB' in databases_info:
            mysql_db_info = subprocess.getoutput('mysql -u <user> -p<password> -e "SHOW DATABASES;"')
            file.write("\nИнформация о базах данных MySQL/MariaDB:\n")
            file.write(mysql_db_info)
        if 'PostgreSQL' in databases_info:
            postgres_db_info = subprocess.getoutput('psql -U <user> -l')
            file.write("\nИнформация о базах данных PostgreSQL:\n")
            file.write(postgres_db_info)
    else:
        file.write("Не установлены известные базы данных\n")

    # Получаем информацию о открытых портах и записываем в файл
    file.write("\n=== Открытые порты ===\n")
    open_ports = []
    for port in range(1, 1025):  # Проверяем первые 1024 порта
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip_address, port))
        if result == 0:
            open_ports.append(port)
        sock.close()

    if open_ports:
        file.write("Открытые порты:\n")
        for port in open_ports:
            file.write(f"Порт {port} открыт\n")
    else:
        file.write("Открытых портов не обнаружено\n")

# Выводим сообщение об успешном завершении
print("Информация о сервере сохранена в файл 'server_info.txt'.")
