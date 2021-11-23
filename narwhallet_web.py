from narwhallet.core.kws.server import Server


if __name__ == '__main__':
    try:
        Server()
    except Exception:
        print('Oh no! Server couldn\'t start!')
