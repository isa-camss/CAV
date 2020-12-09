import etl
import store as st


def run():
    g = etl.run()
    etl.show_save(g, True)
    # m = st.run(g)

    return


if __name__ == "__main__":
    run()
