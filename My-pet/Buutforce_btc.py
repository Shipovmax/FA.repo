import os
import sys
import time
import json
import hashlib
import binascii
import threading
from multiprocessing import Process, Value, Array, Lock
from datetime import datetime
import ecdsa
import requests

# ГЛОБАЛЬНЫЕ СЧЕТЧИКИ (SHARED MEMORY)
def init_counters():
    global shared_checked, shared_found, global_lock
    shared_checked = Value('L', 0)  # Long (64-bit)
    shared_found = Value('L', 0)
    global_lock = Lock()

BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

class Bitcoin:
    @staticmethod
    def prikey():
        """Генерация приватного ключа (32 байта = 256 бит)"""
        return binascii.hexlify(os.urandom(32)).decode()
    
    @staticmethod
    def pubkey(prikey_hex):
        """SECP256K1: приватный → публичный ключ"""
        try:
            prikey_bytes = binascii.unhexlify(prikey_hex)
            signing_key = ecdsa.SigningKey.from_string(
                prikey_bytes, 
                curve=ecdsa.SECP256k1
            )
            pubkey_bytes = signing_key.verifying_key.to_string()
            return '04' + binascii.hexlify(pubkey_bytes).decode()
        except:
            return None
    
    @staticmethod
    def hash160(pubkey_hex):
        """SHA256(pubkey) → RIPEMD160"""
        try:
            pubkey_bytes = binascii.unhexlify(pubkey_hex)
            sha = hashlib.sha256(pubkey_bytes).digest()
            h160 = hashlib.new('ripemd160', sha)
            return h160.hexdigest()
        except:
            return None
    
    @staticmethod
    def address(hash160_hex):
        """RIPEMD160 → Base58Check адрес"""
        try:
            versioned = '00' + hash160_hex
            versioned_bytes = binascii.unhexlify(versioned)
            
            # Контрольная сумма
            checksum = hashlib.sha256(
                hashlib.sha256(versioned_bytes).digest()
            ).digest()[:4]
            
            full = versioned_bytes + checksum
            
            # Base58 кодирование
            num = int(binascii.hexlify(full), 16)
            encoded = ''
            
            while num > 0:
                num, remainder = divmod(num, 58)
                encoded = BASE58_ALPHABET[remainder] + encoded
            
            # Ведущие '1' для нулей
            for byte in full:
                if byte == 0:
                    encoded = '1' + encoded
                else:
                    break
            
            return encoded if encoded else '1'
        except:
            return None

def worker(worker_id, shared_checked, shared_found, global_lock, check_balance=False):
    """РАБОЧИЙ ПРОЦЕСС - ГЕНЕРИРУЕТ И ПРОВЕРЯЕТ АДРЕСА"""
    
    local_checked = 0
    local_found = 0
    last_report = time.time()
    start_time = time.time()
    
    print(f"✅ Worker #{worker_id} запущен", flush=True)
    
    while True:
        try:
            # ГЕНЕРИРУЕМ КОШЕЛЕК
            priv = Bitcoin.prikey()
            pub = Bitcoin.pubkey(priv)
            
            if pub is None:
                continue
            
            h160 = Bitcoin.hash160(pub)
            if h160 is None:
                continue
            
            addr = Bitcoin.address(h160)
            if addr is None:
                continue
            
            local_checked += 1
            
            # ОБНОВЛЯЕМ ГЛОБАЛЬНЫЙ СЧЕТЧИК (с блокировкой)
            with global_lock:
                shared_checked.value += 1
            
            # ПРОВЕРЯЕМ БАЛАНС (если включено)
            balance = 0
            if check_balance:
                try:
                    resp = requests.get(
                        f"https://blockchain.info/q/addressbalance/{addr}",
                        timeout=2
                    )
                    if resp.status_code == 200:
                        balance = int(resp.text) / 100000000
                except:
                    pass
            
            # ЕСЛИ НАЙДЕН КОШЕЛЕК С БАЛАНСОМ
            if balance > 0:
                local_found += 1
                with global_lock:
                    shared_found.value += 1
                
                print(f"\n🎉🎉🎉 НАЙДЕН КОШЕЛЕК! 🎉🎉🎉", flush=True)
                print(f"Worker #{worker_id} | Balance: {balance:.8f} BTC", flush=True)
                print(f"Address: {addr}", flush=True)
                print(f"Private Key: {priv}", flush=True)
                
                # СОХРАНЯЕМ
                filename = f"FOUND_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(filename, 'w') as f:
                    json.dump({
                        'address': addr,
                        'private_key': priv,
                        'balance': balance,
                        'timestamp': datetime.now().isoformat()
                    }, f)
                print(f"Сохранено в {filename}\n", flush=True)
            
            # РЕАЛЬТАЙМ ОТЧЕТНОСТЬ (каждые 2 секунды)
            if time.time() - last_report > 2:
                elapsed = time.time() - start_time
                speed = local_checked / elapsed if elapsed > 0 else 0
                
                print(f"📊 Worker #{worker_id} | "
                      f"Local: {local_checked:,} | "
                      f"Speed: {speed:,.0f}/s | "
                      f"Found: {local_found}", 
                      flush=True)
                last_report = time.time()
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            pass

def stats_monitor(shared_checked, shared_found, global_lock, num_workers):
    """ПОТОК СТАТИСТИКИ - ВЫВОДИТ ГЛОБАЛЬНЫЙ ПРОГРЕСС"""
    
    start_time = time.time()
    last_checked = 0
    
    print("\n" + "="*70)
    print("🔥 BITCOIN SCANNER LAUNCHED 🔥")
    print("="*70 + "\n")
    
    while True:
        try:
            time.sleep(5)
            
            with global_lock:
                total = shared_checked.value
                found = shared_found.value
            
            elapsed = time.time() - start_time
            speed = total / elapsed if elapsed > 0 else 0
            new_checked = total - last_checked
            
            print(f"""
╔════════════════════════════════════════════════════════════╗
║              📊 ГЛОБАЛЬНАЯ СТАТИСТИКА                     ║
╠════════════════════════════════════════════════════════════╣
║ Всего проверено:    {total:,} адресов
║ Скорость:           {speed:,.0f} адресов/сек
║ За последние 5сек:  {new_checked:,} адресов
║ Найдено:            {found} кошельков с балансом
║ Прошло времени:     {elapsed/60:.1f} минут
║ Активных воркеров:  {num_workers}
╚════════════════════════════════════════════════════════════╝
""", flush=True)
            
            last_checked = total
        
        except KeyboardInterrupt:
            break
        except:
            pass

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Bitcoin Scanner')
    parser.add_argument('-p', '--processes', type=int, default=8, 
                       help='Количество процессов (default: 8)')
    parser.add_argument('-b', '--balance', action='store_true',
                       help='Проверять баланс через API (медленнее!)')
    args = parser.parse_args()
    
    # ИНИЦИАЛИЗАЦИЯ СЧЕТЧИКОВ
    shared_checked = Value('L', 0)
    shared_found = Value('L', 0)
    global_lock = Lock()
    
    processes = []
    
    # ЗАПУСК ВОРКЕРОВ
    for i in range(args.processes):
        p = Process(
            target=worker,
            args=(i, shared_checked, shared_found, global_lock, args.balance),
            daemon=True
        )
        p.start()
        processes.append(p)
    
    # ЗАПУСК МОНИТОРА СТАТИСТИКИ
    monitor = threading.Thread(
        target=stats_monitor,
        args=(shared_checked, shared_found, global_lock, args.processes),
        daemon=True
    )
    monitor.start()
    
    try:
        # ОСНОВНОЙ ЦИКЛ
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n⏹ ОСТАНОВКА СКАНИРОВАНИЯ...")
        
        # ФИНАЛЬНАЯ СТАТИСТИКА
        elapsed = time.time() - monitor.ident if hasattr(monitor, 'ident') else 0
        with global_lock:
            total = shared_checked.value
            found = shared_found.value
        
        print(f"""
╔════════════════════════════════════════════════════════════╗
║                   ✅ ИТОГОВЫЙ ОТЧЕТ                        ║
╠════════════════════════════════════════════════════════════╣
║ Всего проверено:    {total:,}
║ Найдено:            {found}
║ Воркеров:           {args.processes}
╚════════════════════════════════════════════════════════════╝
""")
        
        # ОСТАНАВЛИВАЕМ ПРОЦЕССЫ
        for p in processes:
            p.terminate()
            p.join(timeout=1)
        
        sys.exit(0)