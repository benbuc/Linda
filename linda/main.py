from dotenv import load_dotenv

from linda.linda import Linda

load_dotenv()


def main():
    linda = Linda()
    linda.checkAll()
