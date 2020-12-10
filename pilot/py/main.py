import etl
import store
import score


def run():
    g = etl.run()
    etl.show_save(g, True)
    m = store.run(g)  # Not working, don't ask me why
    j, p, r = score.run()

    print(r)

    return


if __name__ == "__main__":
    run()
