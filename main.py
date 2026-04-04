from edgar import set_identity

from finpipe.fundamentals.financials import show


def main() -> None:
    set_identity("yourmail@gmail.com")
    show("NVDA", "income", headlines=True)


if __name__ == "__main__":
    main()
