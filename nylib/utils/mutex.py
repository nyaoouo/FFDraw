import os
import pathlib



if os.name == "nt":
    import msvcrt


    def portable_lock(fp):
        fp.seek(0)
        msvcrt.locking(fp.fileno(), msvcrt.LK_LOCK, 1)


    def is_lock(fp):
        fp.seek(0)
        try:
            msvcrt.locking(fp.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError:
            return True
        else:
            msvcrt.locking(fp.fileno(), msvcrt.LK_UNLCK, 1)
            return False


    def portable_unlock(fp):
        fp.seek(0)
        msvcrt.locking(fp.fileno(), msvcrt.LK_UNLCK, 1)
else:
    import fcntl


    def portable_lock(fp):
        fcntl.flock(fp.fileno(), fcntl.LOCK_EX)


    def is_lock(fp):
        try:
            fcntl.flock(fp.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            return True
        else:
            fcntl.flock(fp.fileno(), fcntl.LOCK_UN)
            return False


    def portable_unlock(fp):
        fcntl.flock(fp.fileno(), fcntl.LOCK_UN)


class Mutex:
    fp = None

    def __init__(self, name):
        self.name = pathlib.Path(name).absolute()

    def is_lock(self):
        if not self.name.exists(): return False
        with open(self.name, 'wb') as tmp:
            return is_lock(tmp)

    def acquire(self):
        self.fp = open(self.name, 'wb')
        portable_lock(self.fp)

    def release(self):
        portable_unlock(self.fp)
        self.fp.close()
        self.name.unlink()

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, _type, value, tb):
        self.release()
