import os
from in_place import InPlace

if __name__ == '__main__':
    if not os.path.isfile('.env'):
        with open('.env', 'w') as env_file:
            env_file.close()
    with InPlace('.env') as env_file:
        written = False
        random_key = os.urandom(32).hex()
        for line in env_file:
            if line.startswith('SECRET_KEY'):
                env_file.write(f'SECRET_KEY={random_key}\n')
                written = True
            else:
                env_file.write(line)
        if not written:
            env_file.write(f'SECRET_KEY={random_key}\n')
        pass
