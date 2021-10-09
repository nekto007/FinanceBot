from auth import authorization


def getcookie(update, context):
    print(authorization.get_auth())


if __name__ == '__main__':
    getcookie('1', '2')
