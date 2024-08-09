from backend.utility import read_data
from frontend.home import main


if __name__ == "__main__":

    data_location = f"data/processed_INDEX_BTCUSD_1W.csv"
    print(data_location)

    processed_data = read_data(data_location)
    print(processed_data)

    main(processed_data)
