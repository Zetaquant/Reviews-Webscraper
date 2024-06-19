from src.utils import get_html, parse_reviews, get_all_reviews, get_all_reviews_selenium
import pandas as pd


def main():
    driver_path = '/home/simon/Desktop/Quant/Amazon Webscraper/chrome-linux64'
    url = (
        "https://www.amazon.com/XVX-Mechanical-Swappable-Pre-lubed-Stabilizer/product-reviews/B0C9ZJHQHM/ref=cm_cr_getr_d_paging_btm_prev_1?ie=UTF8&reviewerType=all_reviews&pageNumber=1")  # Example product URL
    # html = get_html(url)
    # reviews = parse_reviews(html)
    # for review in reviews:
    #     print(review)

    all_reviews = get_all_reviews_selenium(url, driver_path)
    df = pd.DataFrame(all_reviews)
    df.to_csv('../data/keyboard.csv', index=False)


def print_csv():
    df = pd.read_csv('../data/keyboard.csv')
    print(df)


def save_reviews_to_text(csv_file, output_file):
    reviews_df = pd.read_csv(csv_file)
    with open(output_file, 'w', encoding='utf-8') as file:
        for index, review in reviews_df.iterrows():
            file.write(f"Title: {review['title']}\n")
            file.write(f"Rating: {review['rating']}\n")
            file.write(f"Image Url: {review['image_url']}\n")
            file.write(f"Review: {review['body']}\n")
            file.write("\n" + "-" * 80 + "\n\n")


if __name__ == "__main__":
    save_reviews_to_text("../data/keyboard.csv", "../data/keyboard.txt")
    # main()
