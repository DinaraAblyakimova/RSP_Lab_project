import threading
import time
import sys

counter = 0
lock = threading.Lock()
rlock = threading.RLock()


def increment(mode):
    global counter
    for _ in range(100_000):
        if mode == "nosync":
            val = counter
            time.sleep(0.000001)  
            val += 1
            counter = val
        elif mode == "sync":
            with lock:
                counter += 1
        elif mode == "rlock":
            with rlock:
                counter += 1


def decrement(mode):
    global counter
    for _ in range(100_000):
        if mode == "nosync":
            val = counter
            time.sleep(0.000001)   
            val -= 1
            counter = val
        elif mode == "sync":
            with lock:
                counter -= 1
        elif mode == "rlock":
            with rlock:
                counter -= 1


def run_mode(mode, n_inc, n_dec):
    global counter
    counter = 0
    threads = []
    start = time.time()

    for _ in range(n_inc):
        t = threading.Thread(target=increment, args=(mode,))
        threads.append(t)
        t.start()

    for _ in range(n_dec):
        t = threading.Thread(target=decrement, args=(mode,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end = time.time()
    print(f"\nРежим: {mode}")
    print(f"Итоговый счетчик = {counter}")
    print(f"Время выполнения: {end - start:.4f} сек")


if __name__ == "__main__":
    if len(sys.argv) == 4:
        mode = sys.argv[1].lower()
        n_inc = int(sys.argv[2])
        n_dec = int(sys.argv[3])
        run_mode(mode, n_inc, n_dec)
    else:
        print("Авто-тест всех режимов (по 5 потоков инкремента и 5 потоков декремента)")
        for m in ["nosync", "sync", "rlock"]:
            run_mode(m, 5, 5)
