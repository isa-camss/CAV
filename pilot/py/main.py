import etl
import store as st


def run():
    g = etl.run()
    etl.show_save(g, True)
    # m = st.run(g)  # Not working, don't ask me why
    

    return


if __name__ == "__main__":
    run()
